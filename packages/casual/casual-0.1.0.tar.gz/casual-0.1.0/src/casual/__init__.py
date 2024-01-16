from quart import Quart, render_template


app = Quart(__name__)


@app.route("/", methods=["GET", "POST"])
async def echo():
    return await render_template("index.html.j2")


def run() -> None:
    app.run(port=5001, debug=True)
