import asyncio
import httpx
from config import AppConfig


class FetchError(Exception):
    def __init__(self, url: str, message: str, is_rate_limit: bool = False):
        self.url = url
        self.message = message
        self.is_rate_limit = is_rate_limit
        super().__init__(f"{url}: {message}")


class ErrorHandler:
    def __init__(self, rate_limiter=None):
        self.config = AppConfig()
        self.rate_limiter = rate_limiter

    async def fetch_with_retry(self, client: httpx.AsyncClient, url: str, rate_limiter=None) -> str:
        last_error = None

        for attempt in range(self.config.retry_count):
            try:
                if rate_limiter:
                    await rate_limiter.acquire()

                response = await client.get(url)

                if response.status_code == 429:
                    if rate_limiter:
                        rate_limiter.mark_rate_limited()
                    raise FetchError(url, "Rate limit", is_rate_limit=True)

                if response.status_code == 503:
                    raise FetchError(url, f"HTTP {response.status_code}")

                if response.status_code >= 500:
                    raise FetchError(url, f"HTTP {response.status_code}")

                if response.status_code >= 400:
                    raise FetchError(url, f"HTTP {response.status_code}")

                response.raise_for_status()
                return response.text

            except httpx.TimeoutException as e:
                last_error = FetchError(url, f"Timeout: {e}")

            except httpx.ConnectError as e:
                last_error = FetchError(url, f"Connection error: {e}")

            except FetchError as e:
                last_error = e
                if e.is_rate_limit:
                    return None

            except Exception as e:
                last_error = FetchError(url, str(e))

            if attempt < self.config.retry_count - 1:
                delay = self.config.retry_backoff_factor ** attempt
                await asyncio.sleep(delay)

        raise last_error
