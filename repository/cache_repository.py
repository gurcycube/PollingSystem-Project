from service.redis_client import redis_client

class CacheRepository:
    def __init__(self, ttl: int = 3600):

        self.ttl = ttl

    def set(self, key: str, value: str):
        redis_client.setex(key, self.ttl, value)
        return {"message": f"Key '{key}' set in cache with TTL {self.ttl} seconds"}

    def get(self, key: str):
        value = redis_client.get(key)
        if value is None:
            return {"message": f"Key '{key}' not found in cache"}
        return value

    def delete(self, key: str):
        result = redis_client.delete(key)
        if result == 1:
            return {"message": f"Key '{key}' deleted from cache"}
        else:
            return {"message": f"Key '{key}' not found in cache"}

    def exists(self, key: str):
        return redis_client.exists(key) == 1
