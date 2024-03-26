import flask

app = flask.Flask(__name__)


@app.route('/test')
def index():
    """
    Basic route to test the server
    """
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True, port=12345, host='0.0.0.0')
