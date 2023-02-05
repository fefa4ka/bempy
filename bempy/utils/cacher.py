from functools import wraps

def cached(func):
    func.cache = {}
    @wraps(func)
    def wrapper(*args):
        try:
            return func.cache[args]
        except KeyError:
            func.cache[args] = result = func(*args)
            return result
    return wrapper
