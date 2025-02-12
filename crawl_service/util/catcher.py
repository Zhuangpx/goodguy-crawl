import logging


def catcher(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logging.exception(e)
            raise RuntimeError('internal error')

    wrapper.__name__ = f.__name__
    return wrapper
