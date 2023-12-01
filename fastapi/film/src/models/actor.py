import orjson
from utils.mixin import PersonMixin
from utils.orjson import orjson_dumps


class Actor(PersonMixin):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
