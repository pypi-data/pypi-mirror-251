from functools import wraps


def repeat(number_of_times):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(number_of_times):
                func(*args, **kwargs)

        return wrapper

    return decorate


if __name__ == "__main__":

    @repeat(5)
    def tst():
        print("Hello")

    tst()
