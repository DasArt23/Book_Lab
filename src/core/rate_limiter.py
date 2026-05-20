import asyncio
import time
from config import AppConfig


class RateLimiter:
    def __init__(self):
        self.config = AppConfig()
        self._semaphore = asyncio.Semaphore(self.config.max_concurrent_requests)
        self._last_request_time = 0
        self._lock = asyncio.Lock()
        self._rate_limited_until = 0

    async def acquire(self) -> bool:
        if time.time() < self._rate_limited_until:
            await asyncio.sleep(self._rate_limited_until - time.time())

        await self._semaphore.acquire()

        async with self._lock:
            now = time.time()
            elapsed = now - self._last_request_time
            if elapsed < self.config.request_delay:
                await asyncio.sleep(self.config.request_delay - elapsed)
            self._last_request_time = time.time()

        return True

    def release(self):
        self._semaphore.release()

    def mark_rate_limited(self):
        self._rate_limited_until = time.time() + self.config.rate_limit_cooldown

    async def __aenter__(self):
        await self.acquire()
        return self

    async def __aexit__(self, *args):
        self.release()
