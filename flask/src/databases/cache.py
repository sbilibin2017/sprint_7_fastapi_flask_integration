from config import config
import redis

cache = redis.Redis(
    host=config.docker.redis_host,
    port=config.redis.port,
    db=config.redis.db,
)
