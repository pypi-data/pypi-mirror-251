from functools import wraps
def TimeFunc(func):
    wraps(func)
    def Wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print(end_time - start_time)
    return Wrapper