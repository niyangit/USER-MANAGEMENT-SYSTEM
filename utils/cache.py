from cachetools import TTLCache

user_cache = TTLCache(
    maxsize=1000,
    ttl=300
)

users_cache = TTLCache(
    maxsize=10,
    ttl=60
)