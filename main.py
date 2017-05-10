from sanic import Sanic
from sanic.response import json

app = Sanic()


@app.route("/")
async def root(request):
    return json({"wip": "wip"})


@app.route("/compile",  methods=['POST'])
async def compile(request):
    # TODO : Get input files parse output file
    # TODO: Get the build process and execute it
    return json({"wip": "wip"})


@app.route("/install",  methods=['POST'])
async def install(request):
    return json({"wip": "wip"})


@app.route("/uninstall",  methods=['DELETE'])
async def uninstall(request):
    return json({"wip": "wip"})


@app.route("/list",  methods=['GET'])
async def list(request):
    # List installed compilers
    return json({"wip": "wip"})


@app.route("/status",  methods=['GET'])
async def status(request):
    return json({"wip": "wip"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7894)
