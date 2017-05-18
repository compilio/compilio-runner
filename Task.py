import os
import subprocess

import docker

from TaskState import TaskState

docker_client = docker.from_env()


class Task:
    def __init__(self, task_id):
        self.id = task_id
        self.workspace_path = None
        self.state = TaskState.COMPILING

    def get_status(self):
        return self.state

    def change_state(self, state):
        self.state = state

    def save_input_files(self, input_files):
        path = 'tasks/' + self.id + '/input_files/'
        if not os.path.exists(path):
            os.makedirs(path)
        filename = input_files.name
        with open(os.path.join(path, filename), 'wb') as file:
            file.write(input_files.body)
            file.close()

        self.workspace_path = path

    def compile(self, bash_command):
        process = subprocess.Popen(bash_command.split(),
                                   stdout=subprocess.PIPE, cwd=self.workspace_path)
        output, error = process.communicate()

        # TODO : docker
        docker_output = docker_client.containers.run("alpine", "ls -l")
        print(docker_output)

        self.change_state(TaskState.SUCCESS)
        return output
