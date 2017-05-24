import os
import pickle
import subprocess
import time
from zipfile import ZipFile

from TaskState import TaskState


class Task:
    def __init__(self, task_id, output_files):
        self.id = task_id
        self.output_files = output_files
        self.workspace_path = None
        self.state = TaskState.COMPILING

        self.output_log = None

    def save(self):
        file = open('tasks/' + self.id + '/task.obj', 'wb')
        this = self
        pickle.dump(this, file)

    def get_state(self):
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
        output_file = 'tasks/' + self.id + '/output.log'
        print('Running command : ' + bash_command)

        with open(output_file, 'wb') as writer, open(output_file, 'rb', 1) as reader:
            process = subprocess.Popen(bash_command,
                                       stdout=writer,
                                       cwd=self.workspace_path,
                                       shell=True)
            while process.poll() is None:
                print(reader.read())
                time.sleep(0.5)
            print(reader.read())

        with open(output_file, 'rb', 1) as reader:
            self.output_log = reader.read()

        with ZipFile('tasks/' + self.id + '/output.zip', 'w') as zip_file:
            zip_file.write('tasks/' + self.id + '/input_files/' + self.output_files, self.output_files)

        self.change_state(TaskState.SUCCESS)

    def get_output_zip(self):
        if self.state != TaskState.SUCCESS:
            return None
        return 'tasks/' + self.id + '/output.zip'

    @staticmethod
    def get_task(task_id):
        try:
            file = open('tasks/' + task_id + '/task.obj', 'rb')
            return pickle.load(file)
        except FileNotFoundError:
            return None
