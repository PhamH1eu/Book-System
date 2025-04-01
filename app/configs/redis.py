import redis
from .Environment import get_environment_variables

env = get_environment_variables()

def create_redis():
    return redis.ConnectionPool(
        host=env.REDIS_HOSTNAME,
        port=env.REDIS_PORT,
        decode_responses=True,
        username=env.REDIS_USERNAME,
        password=env.REDIS_PASSWORD,
    )

def get_redis():
    return redis.Redis(connection_pool=create_redis())