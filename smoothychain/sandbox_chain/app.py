from flask import Flask, request
from sandbox import Sandbox

app = Flask(__name__)


s = Sandbox()


@app.route("/", methods=["POST"])
def execute():
    code = request.form.get("code")
    loc = {}
    s.execute(code, locals=loc)
    return loc["msg"]


if __name__ == "__main__":
    app.run(port=8082)
