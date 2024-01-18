"Additional exceptions raised by the Redis client"

from redis.exceptions import (
    AuthorizationError,
    AuthenticationError,
    AuthenticationWrongNumberOfArgsError,
    BusyLoadingError,
    ChildDeadlockedError,
    ConnectionError,
    DataError,
    InvalidResponse,
    PubSubError,
    ReadOnlyError,
    RedisError,
    ResponseError,
    TimeoutError,
    WatchError,
    NoScriptError,
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from aiokeydb.types.jobs import Job

class JobError(Exception):
    def __init__(self, job: 'Job'):
        super().__init__(
            f"Job {job.id} {job.status}\n\nThe above job failed with the following error:\n\n{job.error}"
        )
        self.job = job