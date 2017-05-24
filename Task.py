import os
import pickle
import subprocess
import time
from zipfile import ZipFile

from TaskState import TaskState


class Task:
    TASKS_FOLDER = 'tasks/'
    SAVED_OBJECT_NAME = 'task.obj'
    OUTPUT_ZIP_NAME = 'output.zip'
    OUTPUT_LOG_NAME = 'output.log'

    def __init__(self, task_id, output_files):
        self.id = task_id
        self.output_files = output_files
        self.workspace_path = None
        self.state = TaskState.COMPILING

        self.output_log = None

    def __get_workspace_path(self):
        return Task.TASKS_FOLDER + self.id + '/workspace/'

    def __get_save_path(self):
        return Task.TASKS_FOLDER + self.id + '/' + Task.SAVED_OBJECT_NAME

    def get_output_zip_path(self):
        return Task.TASKS_FOLDER + self.id + '/' + Task.OUTPUT_ZIP_NAME

    def save(self):
        file = open(self.__get_save_path(), 'wb')
        this = self
        pickle.dump(this, file)

    def get_state(self):
        return self.state

    def change_state(self, state):
        self.state = state
        self.save()

    def save_input_files(self, input_files):
        workspace_path = self.__get_workspace_path()
        if not os.path.exists(workspace_path):
            os.makedirs(workspace_path)
        filename = input_files.name
        with open(os.path.join(workspace_path, filename), 'wb') as file:
            file.write(input_files.body)
            file.close()

        self.workspace_path = workspace_path
        self.save()

    def compile(self, bash_command):
        output_file = Task.TASKS_FOLDER + self.id + '/' + Task.OUTPUT_LOG_NAME
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

        with ZipFile(self.get_output_zip_path(), 'w') as zip_file:
            zip_file.write(self.__get_workspace_path() + self.output_files, self.output_files)

        self.change_state(TaskState.SUCCESS)

    @staticmethod
    def get_task(task_id):
        try:
            file = open(Task.TASKS_FOLDER + task_id + '/' + Task.SAVED_OBJECT_NAME, 'rb')
            return pickle.load(file)
        except FileNotFoundError:
            return None
