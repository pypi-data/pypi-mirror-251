# flask-orjson

A Flask JSON provider using the fast [orjson][] library. Using this provider
will significantly speed up reading JSON data in requests and generating JSON
responses.

[orjson]: https://github.com/ijl/orjson

## Example

```python
from flask import Flask
from flask_orjson import OrjsonProvider

app = Flask(__name__)
app.json = OrjsonProvider(app)
```
