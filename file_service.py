import csv
import os
from tkinter import messagebox


class FileService:
    def __init__(self):
        self.file_name = 'to_do_file.csv'
        self.file_headers = ['id', 'title', 'description', 'status', 'start_time', 'end_time']

    def write_in_file(self, task_list):
        try:
            my_file = open(self.file_name, 'w')
            writer = csv.DictWriter(my_file, fieldnames=self.file_headers)
            writer.writeheader()
            writer.writerows(task_list)
            my_file.close()
        except Exception as e:
            messagebox.showwarning(title='Error', message="Error: " + str(e))

    def read_from_file(self):
        try:
            if not os.path.isfile(self.file_name):
                open(self.file_name, 'x')

            my_file = open(self.file_name, 'r')
            reader = csv.DictReader(my_file)
            csv_list = list()

            for task in reader:
                csv_list.append(task)

            my_file.close()

            return csv_list

        except (FileNotFoundError, Exception) as e:
            messagebox.showwarning(title='Error', message=str(e))
            return []
