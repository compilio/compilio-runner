import os
import subprocess

from sanic import Sanic
from sanic.response import json

app = Sanic()


@app.route("/")
async def root(request):
    return json({"wip": "wip"})


@app.route("/compile", methods=['POST'])
async def compile(request):
    # TODO : param : task_id, build process commands (bash script)
    # TODO : Record a new task
    # TODO : Spawn a new worker ?
    # TODO : Get the build process and execute it
    # TODO : Need to know output file to send to Compilio
    # TODO : Send result to Compilio

    def save_files(req):
        path = 'tasks/' + req.form['task_id'][0] + '/input_files/'
        if not os.path.exists(path):
            os.makedirs(path)
        filename = req.files.get('0').name
        with open(os.path.join(path, filename), 'wb') as file:
            file.write(req.files.get('0').body)
            file.close()
        return path

    bash_command = request.form['bash'][0]

    workspace_path = save_files(request)

    process = subprocess.Popen(bash_command.split(),
                               stdout=subprocess.PIPE, cwd=workspace_path)
    output, error = process.communicate()

    return json({"output": output})


@app.route("/install", methods=['POST'])
async def install(request):
    # TODO : Add a new authorized compiler entry
    return json({"wip": "wip"})


@app.route("/uninstall", methods=['DELETE'])
async def uninstall(request):
    # TODO : Remove a new authorized compiler entry
    return json({"wip": "wip"})


@app.route("/list", methods=['GET'])
async def list(request):
    # TODO : List installed compilers
    return json({"wip": "wip"})


@app.route("/status", methods=['GET'])
async def status(request):
    # TODO : Get a task status
    # TODO : param : task_id
    return json({"wip": "wip"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7894)
