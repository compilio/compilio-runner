import yaml
from sanic import Sanic, response
from sanic.response import json

from Task import Task

app = Sanic()
INSTALLED_COMPILERS_YML = 'installed_compilers.yml'
with open(INSTALLED_COMPILERS_YML, 'r') as yml_file:
    installed_compilers = yaml.load(yml_file)


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

    new_task = Task(request.form['task_id'][0],
                    request.form['output_files'][0])
    new_task.save_input_files(request.files.get('0'))
    new_task.compile(request.form['bash'][0])
    return json({"output": "success"})


@app.route("/install", methods=['POST'])
async def install(request):
    compiler_name = request.form['compiler_name'][0]
    if compiler_name in installed_compilers:
        return json({"already added": "wip"})

    installed_compilers.append(compiler_name)

    yaml.dump(installed_compilers, open(INSTALLED_COMPILERS_YML, 'w'))
    return json({"wip": "wip"})


@app.route("/uninstall", methods=['DELETE'])
async def uninstall(request):
    compiler_name = request.form['compiler_name'][0]
    if compiler_name not in installed_compilers:
        return json({"already added": "wip"})

    installed_compilers.remove(compiler_name)

    yaml.dump(installed_compilers, open(INSTALLED_COMPILERS_YML, 'w'))
    return json({"wip": "wip"})


@app.route("/installed_compilers", methods=['GET'])
async def get_installed_compilers(request):
    return json({"installed_compilers": installed_compilers})


@app.route("/task", methods=['GET'])
async def get_state(request):
    if 'id' not in request.args:
        return json({"state": "id required"})

    task = Task.get_task(request.args['id'][0])

    if task is None:
        return json({"state": "not found"})

    return json({"id": task.id,
                 "state": task.get_state().name,
                 "output_log": task.output_log})


@app.route("/get_output_files", methods=['GET'])
async def get_output_files(request):
    if 'id' not in request.args:
        return json({"error": "id required"})

    task = Task.get_task(request.args['id'][0])

    if task is None:
        return json({"error": "Task not found"})

    return await response.file(task.get_output_files())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7894)
