import asyncio
from importlib.util import cache_from_source
import json
import math
import time
from datetime import datetime, timedelta
from typing import Optional, Any
from uuid import uuid4

from redis.asyncio import Redis as CacheRedis
from redis.asyncio.client import PubSub

from app.my_config import get_settings

settings = get_settings()

my_cache_redis: CacheRedis = CacheRedis.from_url(url=f"{settings.REDIS_URL}", db=0, decode_responses=True, auto_close_connection_pool=True)


async def redis_ready() -> bool:
    try:
        await my_cache_redis.ping()
        return True
    except Exception as e:
        print(f"🌋 Failed in redis_om_ready: {e}")
        return False



class CacheManager:
    def __init__(self, cache_redis: CacheRedis):
        self.cache_redis = cache_redis
        
    async def incr(self):
        await self.cache_redis.incr(name="total_visits")
        
    async def total_visits(self):
        return await self.cache_redis.get(name="total_visits")

cache_manager = CacheManager(cache_redis=my_cache_redis)