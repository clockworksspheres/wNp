from cachetools import cached, TTLCache
import time

# Create a TTLCache with max 100 items, each living for 10 seconds
@cached(cache=TTLCache(maxsize=100, ttl=10))
def slow_function(x):
    time.sleep(2)  # Simulate expensive computation
    return x * x

# First call computes the result
print(slow_function(5))  # Takes ~2 seconds → 25

# Second call within 10 seconds returns cached result instantly
print(slow_function(5))  # Returns immediately → 25

time.sleep(11)

# Call after TTL expiry recomputes the result
print(slow_function(5))  # Takes ~2 seconds again → 25


