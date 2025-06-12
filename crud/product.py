from __future__ import annotations

import json
import os
from typing import Any, Dict

import requests

from cache.redis_client import redis_client

BASE = "https://dummyjson.com/products"
VERIFY_SSL = os.getenv("PRODUCTS_VERIFY_SSL", "true").lower() == "true"
TTL = 300  # segundos

def _build_query(params: Dict[str, Any]) -> Dict[str, Any]:
    mapping = {
        "skip": "skip",
        "limit": "limit",
        "search": "q",
        "category": "category",
        "sort": "sort",
    }
    return {mapping[k]: v for k, v in params.items() if v is not None}


def _cache_key(params: Dict[str, Any]) -> str:
    return "products:" + "|".join(f"{k}={v}" for k, v in sorted(params.items()))


# ─── API pública ──────────────────────────────────────────────
def fetch_products(
    *,
    skip: int = 0,
    limit: int = 10,
    search: str | None = None,
    category: str | None = None,
    sort: str | None = None,
) -> dict:

    params = dict(skip=skip, limit=limit, search=search,
                  category=category, sort=sort)
    key = _cache_key(params)

    if (cached := redis_client.get(key)):
        return json.loads(cached)

    resp = requests.get(
        BASE,
        params=_build_query(params),
        timeout=10,
        verify=VERIFY_SSL,     
    )
    resp.raise_for_status()
    data = resp.json()
    redis_client.setex(key, TTL, json.dumps(data))
    return data


def fetch_product(product_id: int) -> dict | None:
    key = f"product:{product_id}"
    if (cached := redis_client.get(key)):
        return json.loads(cached)

    resp = requests.get(
        f"{BASE}/{product_id}",
        timeout=10,
        verify=VERIFY_SSL,  
    )
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    data = resp.json()
    redis_client.setex(key, TTL, json.dumps(data))
    return data
