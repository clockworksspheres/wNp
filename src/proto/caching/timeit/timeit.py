import time

def timeit():
    """ 
    a utility decoration to time running time
    """ 
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            args = [str(arg) for arg in args]

            print(f"[{(end - start):8f}]: f({args} -> {result}")
            return result
        return wrapper
    return decorator

