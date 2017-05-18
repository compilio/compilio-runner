import os

import docker

docker_client = docker.from_env()


class Task:
    def __init__(self, task_id):
        self.id = task_id
        self.workspace_path = None

    def get_status(self):
        pass

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
        process = os.subprocess.Popen(bash_command.split(),
                                      stdout=os.subprocess.PIPE, cwd=self.workspace_path)
        output, error = process.communicate()

        # TODO : docker
        docker_output = docker_client.containers.run("alpine", "ls -l")
        print(docker_output)

        return output
