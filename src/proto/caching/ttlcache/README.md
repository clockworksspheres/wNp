# TTLCache related:

from search.brave.com:

## python cachetools.ttlcache example

Quick Answer

The `cachetools.TTLCache` class in Python provides a cache with a time-to-live (TTL) expiration for its entries. It is initialized with a `maxsize` parameter to define the maximum number of items the cache can hold and a `ttl` parameter to specify the time in seconds after which entries expire. For example, `cache = TTLCache(maxsize=128, ttl=5)` creates a cache that holds up to 128 items, each expiring after 5 seconds.

An example of using `TTLCache` involves setting a value and retrieving it after a delay to demonstrate expiration. The following code snippet shows this:

```
from cachetools import TTLCache
from sched import scheduler

cache = TTLCache(maxsize=128, ttl=5)
cache["abc"] = 42

def display_cached_value(cache_key):
    try:
        cached_value = cache[cache_key]
        print(f"{cache_key}={cached_value}")
    except KeyError:
        print(f"{cache_key}=Not in cache")

runner = scheduler()
runner.enter(2, 1, display_cached_value, argument=("abc",))
runner.enter(6, 1, display_cached_value, argument=("abc",))
runner.run()
```

This code sets a value "abc" with the value 42, then attempts to retrieve it after 2 seconds (still within the TTL) and again after 6 seconds (after expiration), demonstrating that the value is no longer available after the TTL has passed.

`TTLCache` is commonly used in applications requiring temporary storage of data, such as caching API responses, database queries, or session tokens. For instance, in a web application, a cache with a TTL of 55 minutes might be used to store authentication tokens to ensure they are refreshed frequently. Similarly, a cache with a 6-hour TTL can be used to store frequently accessed data in a large-scale system. The cache can also be integrated with custom timers to spread expiration events across multiple instances, improving performance under load.

In another use case, `TTLCache` is used to cache metadata for articles in a feed system, with a TTL of 5 minutes to ensure freshness. The cache is also used in a command-line bot to store OAuth tokens for Stack Exchange, with a TTL of 10 minutes to limit token validity. These examples illustrate the flexibility of `TTLCache` in managing short-lived data efficiently across various application domains.

[

](https://gist.github.com/chaddotson/7a7e758af9ea3de01ae8b3b3abde311f)

[

](https://www.programcreek.com/python/example/104146/cachetools.TTLCache)

[

](https://python.hotexamples.com/examples/cachetools/TTLCache/-/python-ttlcache-class-examples.html)

[

](https://snyk.io/advisor/python/cachetools/functions/cachetools.TTLCache)

[

](https://www.javatpoint.com/python-cachetools-module)

## as a decorator

Finished

`cachetools.TTLCache` can be used as a **decorator** via the `@cached` decorator to automatically cache the results of function calls based on their arguments, with entries expiring after a specified time-to-live (TTL).

You apply it by passing a `TTLCache` instance to the `@cached` decorator:

```
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
```

This pattern is ideal for caching API responses, database queries, or any I/O-bound function where results can be reused briefly.

[

](https://pypi.org/project/cachetools/)

[

](https://github.com/tkem/cachetools)

[

](https://rawheel.medium.com/caching-method-responses-with-cachetools-in-python-b7cfd9e86ad6)

[

](https://cachetools.readthedocs.io/en/v4.2.4/)

[

](https://www.programcreek.com/python/example/104146/cachetools.TTLCache)

[cachetools TTLCache decorator example Python](https://search.brave.com/search?q=cachetools%20TTLCache%20decorator%20example%20Python)

-----


# **Used Method - Second of the two below**

## python @cached class method decorator ttl cachetools classmethod

Quick Answer
To implement a time-to-live (TTL) cache for a class method using the cachetools library in Python, you can use the @cachetools.cachedmethod decorator. This decorator allows you to cache the results of class methods with a specified TTL, ensuring that cached values expire after a defined period.

The @cachetools.cachedmethod decorator takes a function that returns a cache object, typically a TTLCache, and applies caching to the decorated method. For example, you can define a class with a class method that uses a TTLCache with a maximum size and a TTL in seconds:

import cachetools

class ExampleClass:
    EXP = 2

    @classmethod
    @cachetools.cachedmethod(lambda cls: cachetools.TTLCache(maxsize=128, ttl=600))
    def example_classmethod(cls, i):
        return i * cls.EXP

In this example, example_classmethod will cache its results for 600 seconds (10 minutes), and the cache can hold up to 128 entries. The cache is tied to the class instance via the lambda cls: ... function, which provides the cache object for each class method call. This approach ensures that the cached results are valid for the specified TTL and are automatically removed after expiration.

It is important to note that when using cachetools for multiple methods within a class, it is recommended to use separate cache instances to avoid key conflicts that could lead to incorrect results. Additionally, the TTLCache class from cachetools supports both maximum size and TTL settings, making it suitable for managing cached data with time-based expiration.


## example on how to use the class

Finished
Here’s an example of how to use @cachetools.cachedmethod with a class method:

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

This demonstrates caching per instance, where results are reused within the TTL window. The lambda self: self.cache provides the cache object for each method call.


-----




