import datetime
from aiokeydb.v1.exceptions import (
    ModuleError,
)
from aiokeydb.v1.utils import str_if_bytes


def timestamp_to_datetime(response):
    "Converts a unix timestamp to a Python datetime object"
    if not response:
        return None
    try:
        response = int(response)
    except ValueError:
        return None
    return datetime.datetime.fromtimestamp(response)


def string_keys_to_dict(key_string, callback):
    return dict.fromkeys(key_string.split(), callback)



class CaseInsensitiveDict(dict):
    "Case insensitive dict implementation. Assumes string keys only."

    def __init__(self, data):
        for k, v in data.items():
            self[k.upper()] = v

    def __contains__(self, k):
        return super().__contains__(k.upper())

    def __delitem__(self, k):
        super().__delitem__(k.upper())

    def __getitem__(self, k):
        return super().__getitem__(k.upper())

    def get(self, k, default=None):
        return super().get(k.upper(), default)

    def __setitem__(self, k, v):
        super().__setitem__(k.upper(), v)

    def update(self, data):
        data = CaseInsensitiveDict(data)
        super().update(data)


def parse_debug_object(response):
    "Parse the results of Redis's DEBUG OBJECT command into a Python dict"
    # The 'type' of the object is the first item in the response, but isn't
    # prefixed with a name
    response = str_if_bytes(response)
    response = "type:" + response
    response = dict(kv.split(":") for kv in response.split())

    # parse some expected int values from the string response
    # note: this cmd isn't spec'd so these may not appear in all redis versions
    int_fields = ("refcount", "serializedlength", "lru", "lru_seconds_idle")
    for field in int_fields:
        if field in response:
            response[field] = int(response[field])

    return response


def parse_object(response, infotype):
    """Parse the results of an OBJECT command"""
    if infotype in ("idletime", "refcount"):
        return int_or_none(response)
    return response


def parse_info(response):
    """Parse the result of Redis's INFO command into a Python dict"""
    info = {}
    response = str_if_bytes(response)

    def get_value(value):
        if "," not in value or "=" not in value:
            try:
                if "." in value:
                    return float(value)
                else:
                    return int(value)
            except ValueError:
                return value
        else:
            sub_dict = {}
            for item in value.split(","):
                k, v = item.rsplit("=", 1)
                sub_dict[k] = get_value(v)
            return sub_dict

    for line in response.splitlines():
        if line and not line.startswith("#"):
            if line.find(":") != -1:
                # Split, the info fields keys and values.
                # Note that the value may contain ':'. but the 'host:'
                # pseudo-command is the only case where the key contains ':'
                key, value = line.split(":", 1)
                if key == "cmdstat_host":
                    key, value = line.rsplit(":", 1)

                if key == "module":
                    # Hardcode a list for key 'modules' since there could be
                    # multiple lines that started with 'module'
                    info.setdefault("modules", []).append(get_value(value))
                else:
                    info[key] = get_value(value)
            else:
                # if the line isn't splittable, append it to the "__raw__" key
                info.setdefault("__raw__", []).append(line)

    return info


def parse_memory_stats(response, **kwargs):
    """Parse the results of MEMORY STATS"""
    stats = pairs_to_dict(response, decode_keys=True, decode_string_values=True)
    for key, value in stats.items():
        if key.startswith("db."):
            stats[key] = pairs_to_dict(
                value, decode_keys=True, decode_string_values=True
            )
    return stats


SENTINEL_STATE_TYPES = {
    "can-failover-its-master": int,
    "config-epoch": int,
    "down-after-milliseconds": int,
    "failover-timeout": int,
    "info-refresh": int,
    "last-hello-message": int,
    "last-ok-ping-reply": int,
    "last-ping-reply": int,
    "last-ping-sent": int,
    "master-link-down-time": int,
    "master-port": int,
    "num-other-sentinels": int,
    "num-slaves": int,
    "o-down-time": int,
    "pending-commands": int,
    "parallel-syncs": int,
    "port": int,
    "quorum": int,
    "role-reported-time": int,
    "s-down-time": int,
    "slave-priority": int,
    "slave-repl-offset": int,
    "voted-leader-epoch": int,
}


def parse_sentinel_state(item):
    result = pairs_to_dict_typed(item, SENTINEL_STATE_TYPES)
    flags = set(result["flags"].split(","))
    for name, flag in (
        ("is_master", "master"),
        ("is_slave", "slave"),
        ("is_sdown", "s_down"),
        ("is_odown", "o_down"),
        ("is_sentinel", "sentinel"),
        ("is_disconnected", "disconnected"),
        ("is_master_down", "master_down"),
    ):
        result[name] = flag in flags
    return result


def parse_sentinel_master(response):
    return parse_sentinel_state(map(str_if_bytes, response))


def parse_sentinel_masters(response):
    result = {}
    for item in response:
        state = parse_sentinel_state(map(str_if_bytes, item))
        result[state["name"]] = state
    return result


def parse_sentinel_slaves_and_sentinels(response):
    return [parse_sentinel_state(map(str_if_bytes, item)) for item in response]


def parse_sentinel_get_master(response):
    return response and (response[0], int(response[1])) or None


def pairs_to_dict(response, decode_keys=False, decode_string_values=False):
    """Create a dict given a list of key/value pairs"""
    if response is None:
        return {}
    if decode_keys or decode_string_values:
        # the iter form is faster, but I don't know how to make that work
        # with a str_if_bytes() map
        keys = response[::2]
        if decode_keys:
            keys = map(str_if_bytes, keys)
        values = response[1::2]
        if decode_string_values:
            values = map(str_if_bytes, values)
        return dict(zip(keys, values))
    else:
        it = iter(response)
        return dict(zip(it, it))


def pairs_to_dict_typed(response, type_info):
    it = iter(response)
    result = {}
    for key, value in zip(it, it):
        if key in type_info:
            try:
                value = type_info[key](value)
            except Exception:
                # if for some reason the value can't be coerced, just use
                # the string value
                pass
        result[key] = value
    return result


def zset_score_pairs(response, **options):
    """
    If ``withscores`` is specified in the options, return the response as
    a list of (value, score) pairs
    """
    if not response or not options.get("withscores"):
        return response
    score_cast_func = options.get("score_cast_func", float)
    it = iter(response)
    return list(zip(it, map(score_cast_func, it)))


def sort_return_tuples(response, **options):
    """
    If ``groups`` is specified, return the response as a list of
    n-element tuples with n being the value found in options['groups']
    """
    if not response or not options.get("groups"):
        return response
    n = options["groups"]
    return list(zip(*[response[i::n] for i in range(n)]))


def int_or_none(response):
    if response is None:
        return None
    return int(response)


def parse_stream_list(response):
    if response is None:
        return None
    data = []
    for r in response:
        if r is not None:
            data.append((r[0], pairs_to_dict(r[1])))
        else:
            data.append((None, None))
    return data


def pairs_to_dict_with_str_keys(response):
    return pairs_to_dict(response, decode_keys=True)


def parse_list_of_dicts(response):
    return list(map(pairs_to_dict_with_str_keys, response))


def parse_xclaim(response, **options):
    if options.get("parse_justid", False):
        return response
    return parse_stream_list(response)


def parse_xautoclaim(response, **options):
    if options.get("parse_justid", False):
        return response[1]
    response[1] = parse_stream_list(response[1])
    return response


def parse_xinfo_stream(response, **options):
    data = pairs_to_dict(response, decode_keys=True)
    if not options.get("full", False):
        first = data["first-entry"]
        if first is not None:
            data["first-entry"] = (first[0], pairs_to_dict(first[1]))
        last = data["last-entry"]
        if last is not None:
            data["last-entry"] = (last[0], pairs_to_dict(last[1]))
    else:
        data["entries"] = {_id: pairs_to_dict(entry) for _id, entry in data["entries"]}
        data["groups"] = [
            pairs_to_dict(group, decode_keys=True) for group in data["groups"]
        ]
    return data


def parse_xread(response):
    if response is None:
        return []
    return [[r[0], parse_stream_list(r[1])] for r in response]


def parse_xpending(response, **options):
    if options.get("parse_detail", False):
        return parse_xpending_range(response)
    consumers = [{"name": n, "pending": int(p)} for n, p in response[3] or []]
    return {
        "pending": response[0],
        "min": response[1],
        "max": response[2],
        "consumers": consumers,
    }


def parse_xpending_range(response):
    k = ("message_id", "consumer", "time_since_delivered", "times_delivered")
    return [dict(zip(k, r)) for r in response]


def float_or_none(response):
    if response is None:
        return None
    return float(response)


def bool_ok(response):
    return str_if_bytes(response) == "OK"


def parse_zadd(response, **options):
    if response is None:
        return None
    if options.get("as_score"):
        return float(response)
    return int(response)


def parse_client_list(response, **options):
    clients = []
    for c in str_if_bytes(response).splitlines():
        # Values might contain '='
        clients.append(dict(pair.split("=", 1) for pair in c.split(" ")))
    return clients


def parse_config_get(response, **options):
    response = [str_if_bytes(i) if i is not None else None for i in response]
    return response and pairs_to_dict(response) or {}


def parse_scan(response, **options):
    cursor, r = response
    return int(cursor), r


def parse_hscan(response, **options):
    cursor, r = response
    return int(cursor), r and pairs_to_dict(r) or {}


def parse_zscan(response, **options):
    score_cast_func = options.get("score_cast_func", float)
    cursor, r = response
    it = iter(r)
    return int(cursor), list(zip(it, map(score_cast_func, it)))


def parse_zmscore(response, **options):
    # zmscore: list of scores (double precision floating point number) or nil
    return [float(score) if score is not None else None for score in response]


def parse_slowlog_get(response, **options):
    space = " " if options.get("decode_responses", False) else b" "

    def parse_item(item):
        result = {"id": item[0], "start_time": int(item[1]), "duration": int(item[2])}
        # Redis Enterprise injects another entry at index [3], which has
        # the complexity info (i.e. the value N in case the command has
        # an O(N) complexity) instead of the command.
        if isinstance(item[3], list):
            result["command"] = space.join(item[3])
        else:
            result["complexity"] = item[3]
            result["command"] = space.join(item[4])
        return result

    return [parse_item(item) for item in response]


def parse_stralgo(response, **options):
    """
    Parse the response from `STRALGO` command.
    Without modifiers the returned value is string.
    When LEN is given the command returns the length of the result
    (i.e integer).
    When IDX is given the command returns a dictionary with the LCS
    length and all the ranges in both the strings, start and end
    offset for each string, where there are matches.
    When WITHMATCHLEN is given, each array representing a match will
    also have the length of the match at the beginning of the array.
    """
    if options.get("len", False):
        return int(response)
    if options.get("idx", False):
        if options.get("withmatchlen", False):
            matches = [
                [(int(match[-1]))] + list(map(tuple, match[:-1]))
                for match in response[1]
            ]
        else:
            matches = [list(map(tuple, match)) for match in response[1]]
        return {
            str_if_bytes(response[0]): matches,
            str_if_bytes(response[2]): int(response[3]),
        }
    return str_if_bytes(response)


def parse_cluster_info(response, **options):
    response = str_if_bytes(response)
    return dict(line.split(":") for line in response.splitlines() if line)


def _parse_node_line(line):
    line_items = line.split(" ")
    node_id, addr, flags, master_id, ping, pong, epoch, connected = line.split(" ")[:8]
    addr = addr.split("@")[0]
    node_dict = {
        "node_id": node_id,
        "flags": flags,
        "master_id": master_id,
        "last_ping_sent": ping,
        "last_pong_rcvd": pong,
        "epoch": epoch,
        "slots": [],
        "migrations": [],
        "connected": True if connected == "connected" else False,
    }
    if len(line_items) >= 9:
        slots, migrations = _parse_slots(line_items[8:])
        node_dict["slots"], node_dict["migrations"] = slots, migrations
    return addr, node_dict


def _parse_slots(slot_ranges):
    slots, migrations = [], []
    for s_range in slot_ranges:
        if "->-" in s_range:
            slot_id, dst_node_id = s_range[1:-1].split("->-", 1)
            migrations.append(
                {"slot": slot_id, "node_id": dst_node_id, "state": "migrating"}
            )
        elif "-<-" in s_range:
            slot_id, src_node_id = s_range[1:-1].split("-<-", 1)
            migrations.append(
                {"slot": slot_id, "node_id": src_node_id, "state": "importing"}
            )
        else:
            s_range = [sl for sl in s_range.split("-")]
            slots.append(s_range)

    return slots, migrations


def parse_cluster_nodes(response, **options):
    """
    @see: https://redis.io/commands/cluster-nodes  # string / bytes
    @see: https://redis.io/commands/cluster-replicas # list of string / bytes
    """
    if isinstance(response, (str, bytes)):
        response = response.splitlines()
    return dict(_parse_node_line(str_if_bytes(node)) for node in response)


def parse_geosearch_generic(response, **options):
    """
    Parse the response of 'GEOSEARCH', GEORADIUS' and 'GEORADIUSBYMEMBER'
    commands according to 'withdist', 'withhash' and 'withcoord' labels.
    """
    if options["store"] or options["store_dist"]:
        # `store` and `store_dist` cant be combined
        # with other command arguments.
        # relevant to 'GEORADIUS' and 'GEORADIUSBYMEMBER'
        return response

    if type(response) != list:
        response_list = [response]
    else:
        response_list = response

    if not options["withdist"] and not options["withcoord"] and not options["withhash"]:
        # just a bunch of places
        return response_list

    cast = {
        "withdist": float,
        "withcoord": lambda ll: (float(ll[0]), float(ll[1])),
        "withhash": int,
    }

    # zip all output results with each casting function to get
    # the properly native Python value.
    f = [lambda x: x]
    f += [cast[o] for o in ["withdist", "withhash", "withcoord"] if options[o]]
    return [list(map(lambda fv: fv[0](fv[1]), zip(f, r))) for r in response_list]


def parse_command(response, **options):
    commands = {}
    for command in response:
        cmd_dict = {}
        cmd_name = str_if_bytes(command[0])
        cmd_dict["name"] = cmd_name
        cmd_dict["arity"] = int(command[1])
        cmd_dict["flags"] = [str_if_bytes(flag) for flag in command[2]]
        cmd_dict["first_key_pos"] = command[3]
        cmd_dict["last_key_pos"] = command[4]
        cmd_dict["step_count"] = command[5]
        if len(command) > 7:
            cmd_dict["tips"] = command[7]
            cmd_dict["key_specifications"] = command[8]
            cmd_dict["subcommands"] = command[9]
        commands[cmd_name] = cmd_dict
    return commands


def parse_pubsub_numsub(response, **options):
    return list(zip(response[0::2], response[1::2]))


def parse_client_kill(response, **options):
    if isinstance(response, int):
        return response
    return str_if_bytes(response) == "OK"


def parse_acl_getuser(response, **options):
    if response is None:
        return None
    data = pairs_to_dict(response, decode_keys=True)

    # convert everything but user-defined data in 'keys' to native strings
    data["flags"] = list(map(str_if_bytes, data["flags"]))
    data["passwords"] = list(map(str_if_bytes, data["passwords"]))
    data["commands"] = str_if_bytes(data["commands"])
    if isinstance(data["keys"], str) or isinstance(data["keys"], bytes):
        data["keys"] = list(str_if_bytes(data["keys"]).split(" "))
    if data["keys"] == [""]:
        data["keys"] = []
    if "channels" in data:
        if isinstance(data["channels"], str) or isinstance(data["channels"], bytes):
            data["channels"] = list(str_if_bytes(data["channels"]).split(" "))
        if data["channels"] == [""]:
            data["channels"] = []
    if "selectors" in data:
        data["selectors"] = [
            list(map(str_if_bytes, selector)) for selector in data["selectors"]
        ]

    # split 'commands' into separate 'categories' and 'commands' lists
    commands, categories = [], []
    for command in data["commands"].split(" "):
        if "@" in command:
            categories.append(command)
        else:
            commands.append(command)

    data["commands"] = commands
    data["categories"] = categories
    data["enabled"] = "on" in data["flags"]
    return data


def parse_acl_log(response, **options):
    if response is None:
        return None
    if isinstance(response, list):
        data = []
        for log in response:
            log_data = pairs_to_dict(log, True, True)
            client_info = log_data.get("client-info", "")
            log_data["client-info"] = parse_client_info(client_info)

            # float() is lossy comparing to the "double" in C
            log_data["age-seconds"] = float(log_data["age-seconds"])
            data.append(log_data)
    else:
        data = bool_ok(response)
    return data


def parse_client_info(value):
    """
    Parsing client-info in ACL Log in following format.
    "key1=value1 key2=value2 key3=value3"
    """
    client_info = {}
    infos = str_if_bytes(value).split(" ")
    for info in infos:
        key, value = info.split("=")
        client_info[key] = value

    # Those fields are defined as int in networking.c
    for int_key in {
        "id",
        "age",
        "idle",
        "db",
        "sub",
        "psub",
        "multi",
        "qbuf",
        "qbuf-free",
        "obl",
        "argv-mem",
        "oll",
        "omem",
        "tot-mem",
    }:
        client_info[int_key] = int(client_info[int_key])
    return client_info


def parse_module_result(response):
    if isinstance(response, ModuleError):
        raise response
    return True


def parse_set_result(response, **options):
    """
    Handle SET result since GET argument is available since Redis 6.2.
    Parsing SET result into:
    - BOOL
    - String when GET argument is used
    """
    if options.get("get"):
        # Redis will return a getCommand result.
        # See `setGenericCommand` in t_string.c
        return response
    return response and str_if_bytes(response) == "OK"
