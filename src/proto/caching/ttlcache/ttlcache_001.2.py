from cachetools import TTLCache, cachedmethod
import time

class DataProcessor:
    def __init__(self):
        # Create a TTL cache with max 100 items, TTL of 5 seconds
        self.cache = TTLCache(maxsize=100, ttl=5)

    @cachedmethod(lambda self: self.cache)
    def process_data(self, value):
        print(f"Processing {value}...")  # Simulate expensive operation
        time.sleep(1)
        return value * 2

# Usage
processor = DataProcessor()

print(processor.process_data(10))  # "Processing 10..." + returns 20
print(processor.process_data(10))  # Returns 20 directly from cache (no print)
time.sleep(6)
print(processor.process_data(10))  # "Processing 10..." again (cache expired)   


