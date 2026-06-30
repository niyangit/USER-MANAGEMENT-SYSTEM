from cachetools import TTLCache

failed_logins = TTLCache(
    maxsize=10000,
    ttl=60
)