
from datetime import timedelta

from cache.redis_client import redis_client


def save_refresh(token: str, ttl_minutes: int) -> None:
    redis_client.setex(f"refresh:{token}", timedelta(minutes=ttl_minutes), "1")


def delete_refresh(token: str) -> None:
    redis_client.delete(f"refresh:{token}")


def is_refresh_valid(token: str) -> bool:
    return redis_client.exists(f"refresh:{token}") == 1
