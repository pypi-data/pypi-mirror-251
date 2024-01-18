# Flask Auth Middleware

Flask Auth Middlewawre is a middleware for securing flask application. It provides a convenient way to secure your Flask routes and endpoints using jwt tokens.

## Features

- Seamless integration with Flask applications.
- Easily protect routes and endpoints with JWT authentication.
- Lightweight and designed for simplicity.


## Requirements

Python 3

* [Flask](https://flask.palletsprojects.com/en/3.0.x/) obvisouly 😁😁😁😊😊
* [PyJWT](https://pyjwt.readthedocs.io/en/stable/)

## Installation

<div class="termy">

```console
$ pip install flask_auth_middleware
```

</div>

## Example

### Create it

* Create a file `app.py` with:
```Python
from flask import Flask
from flask_auth_middleware import JWTAuthMiddleware

app = Flask(__name__)

app.wsgi_app = JWTAuthMiddleware(app, "your_secret_key")


@app.get("/")
def hello():
    return "Hello, World!"

@app.get("/namaste")
def hello():
    return "Namaste, World!"
```

Here all the routes of flask application will be protected by JWTAuthMiddleware.

## If you want to secure selective routes. Then here you go:
```python
from flask import Flask, jsonify, request

from flask_auth_middleware import login_required

app = Flask(__name__)


secret_key = "your_secret_key"


@app.route("/public")
def public_data():
    return jsonify({"message": "This is public data"})


@app.route("/protected")
@login_required(secret_key=secret_key, algorithms=["HS256"])
def protected_route(decoded_payload):
    # your logic with decoded payload
    return jsonify(
        {"message": "This is public data.", "decoded_payload": decoded_payload}
    )


if __name__ == "__main__":
    app.run(debug=True)

```

<div class="termy">

### Run it

* Run the server with:
```console
$ flask run
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

</div>

## Contributing 
Feel free to contribute to this project.

## License

This project is licensed under the terms of the MIT license.