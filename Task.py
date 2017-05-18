import os
import pickle
import subprocess

import docker

from TaskState import TaskState

docker_client = docker.from_env()


class Task:
    def __init__(self, task_id):
        self.id = task_id
        self.workspace_path = None
        self.state = TaskState.COMPILING

    def save(self):
        file = open('tasks/' + self.id + '/task.obj', 'wb')
        this = self
        pickle.dump(this, file)

    def get_status(self):
        return self.state

    def change_state(self, state):
        self.state = state
        self.save()

    def save_input_files(self, input_files):
        path = 'tasks/' + self.id + '/input_files/'
        if not os.path.exists(path):
            os.makedirs(path)
        filename = input_files.name
        with open(os.path.join(path, filename), 'wb') as file:
            file.write(input_files.body)
            file.close()

        self.workspace_path = path
        self.save()

    def compile(self, bash_command):
        process = subprocess.Popen(bash_command.split(),
                                   stdout=subprocess.PIPE, cwd=self.workspace_path)
        output, error = process.communicate()

        # TODO : docker
        docker_output = docker_client.containers.run("alpine", "ls -l")
        print(docker_output)

        self.change_state(TaskState.SUCCESS)
        return output

    @staticmethod
    def get_task(task_id):
        file = open('tasks/' + task_id + '/task.obj', 'rb')
        return pickle.load(file)
