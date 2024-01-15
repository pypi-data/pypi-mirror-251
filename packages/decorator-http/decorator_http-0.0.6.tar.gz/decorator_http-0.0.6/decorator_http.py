import requests


def get(url: str, headers=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                response = requests.get(url, headers=headers)
                return func(response.content, response, None)
            except Exception as error:
                return func(None, None, error)
        return wrapper
    return decorator


def delete(url: str, headers=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                response = requests.delete(url, headers=headers)
                return func(response.content, response, None)
            except Exception as error:
                return func(None, None, error)
        return wrapper
    return decorator


def put(url: str, body=None, headers=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                response = requests.put(url, json=body, headers=headers)
                return func(response.content, response, None)
            except Exception as error:
                return func(None, None, error)
        return wrapper
    return decorator


def patch(url: str, body=None, headers=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                response = requests.patch(url, json=body, headers=headers)
                return func(response.content, response, None)
            except Exception as error:
                return func(None, None, error)
        return wrapper
    return decorator
