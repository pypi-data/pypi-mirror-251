# decorator-http

To simplify handling HTTP requests in Python, you can utilize the `decorator-http` package, which allows you to employ decorators for various HTTP methods. Begin by installing the package using the following pip command:

```bash
pip install decorator-http
```

Now, let's explore how to use this package with different HTTP methods:

## GET

```python
from decorator_http import get

@get('https://some-website.com', headers={'Content-Type': 'application/json'})
def get_example(data=None, response=None, error=None):
    if error:
        print('Failed to request details:', error)
        return

    print('Response data:', data)
    print('Response status:', response.status_code)

get_example()
```

### Handling Errors
You can handle errors by checking the `error` parameter within the decorator function. If an error occurs, it will be passed to the function, allowing you to handle it accordingly.

```python
@get('https://wrong-website.com', headers={'Content-Type': 'application/json'})
def get_example(data=None, response=None, error=None):
    if error:
        print('Failed to request details:', error)
        return

    print('Response data:', data)
    print('Response status:', response.status_code)

get_example()
```

## POST

```python
from decorator_http import post, put, delete

@post('https://some-website.com', body={"hello": "world"}, headers={'Content-Type': 'application/json'})
def post_example(data=None, response=None, error=None):
    if error:
        print('Error:', error)
        return

    print('Response data:', data)
    print('Response status:', response.status_code)

post_example()
```

## Example for PUT and DELETE

For PUT and DELETE requests, you can use the respective decorators in a similar manner. Here's an example for DELETE:

```python
@delete('https://some-website.com', headers={'Content-Type': 'application/json'})
def delete_example(data=None, response=None, error=None):
    if error:
        print('Error:', error)
        return

    print('Response data:', data)
    print('Response status:', response.status_code)

delete_example()
```

Similarly, you can use `@put` for PUT requests following a comparable structure.