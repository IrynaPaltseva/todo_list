import datetime
from tkinter import *
import tkinter as t
from tkinter import ttk, messagebox
import datetime as dt
from tkcalendar import DateEntry

from helpers.file_service import FileService


def main():
    file_service = FileService()
    status = ["Didn't even started", "In progress", "Yay,Done!"]
    date = dt.datetime.today()
    date_format = "%A, %B %d, %Y"
    font_style = ("Times", 10, "bold")

    window = t.Tk()
    window.config(background='#bdc9c0')
    window.title("The Best To Do List Ever!")
    window.geometry("1500x850")

    title_entry = None
    description_entry = None
    time_entry = None
    edit_status_combobox = None

    task_list = []
    task_last_id = 0
    initial_form_data = {
        "title": "",
        "description": "",
        "status": status[0],
        "end_time": datetime.datetime.today().strftime(date_format),
        "start_time": "",
        'index': -1
    }
    form_data = {
        "title": "",
        "description": "",
        "status": status[0],
        "end_time": datetime.datetime.today().strftime(date_format),
        "start_time": "",
        'index': -1
    }
    frame = t.Frame(window, background='#94B39A')
    frame.grid(row=2, column=0, pady=(5, 0), sticky='nw')
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    canvas = Canvas(frame, bg="#94B39A", height=700, highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="news")

    vsb = Scrollbar(frame, orient="vertical", command=canvas.yview)
    vsb.grid(row=0, column=1, sticky='nes')
    canvas.configure(yscrollcommand=vsb.set)
    canvas.config(width=1500-vsb.winfo_width())

    # test end

    frame_all_tasks = t.LabelFrame(canvas, background='#94B39A', font=font_style, padx=20, pady=10, width=1500)
    frame_all_tasks.grid(row=0, column=0, sticky='news')
    # frame_all_tasks.grid(row=1, column=1, sticky='news')
    # test
    canvas.create_window((0, 0), window=frame_all_tasks, anchor='nw')

    # test end

    # label1 = t.Label(frame, background='#94B39A', text="ALL YOUR TASKS IN ONE PLACE:", font=("Times", 13), padx=5, pady=5)
    # label1.grid(row=0, column=0)

    frame_beginning = t.LabelFrame(frame_all_tasks, text='To Do', font=("Times", 10, "bold"), background='#94B39A', width=500, padx=5, pady=5)
    # frame_beginning.config(width=450)
    frame_beginning.grid(row=2, column=0, sticky='nw') # , ipadx=0, ipady=0

    frame_in_progress = t.LabelFrame(frame_all_tasks, text='In Progress', font=("Times", 10, "bold"), background='#94B39A', width=500, padx=5, pady=5)
    frame_in_progress.grid(row=2, column=1, sticky='nw')

    frame_done = t.LabelFrame(frame_all_tasks, text='Done!', font=("Times", 10, "bold"), background='#94B39A', width=500, padx=5, pady=5)
    frame_done.grid(row=2, column=2, sticky='nw')

    def openNewWindow(is_update=False):
        global new_window
        new_window = Toplevel(window, background='#EEA579', padx=20, pady=10)
        new_window.title("Needs to be done ASAP")
        new_window.geometry("470x350")
        new_window.focus()

        frame_Info = t.LabelFrame(new_window, text="New task", background='#EEA579', font=("Times", 10, 'bold'), padx=20, pady=10)
        frame_Info.grid()

        title_label = t.Label(frame_Info, text='Title: ', background='#EEA579',  font=("Times", 13), padx=5, pady=5)
        title_label.grid(row=0, column=0, sticky='w')
        nonlocal title_entry
        title_entry = t.Entry(frame_Info, width=40, font=("Times", 10, "bold"))
        title_entry.insert(END, form_data['title'])
        title_entry.grid(row=0, column=1, sticky='w')

        description_label = t.Label(frame_Info, text='Description: ', background='#EEA579', font=("Times", 13), padx=5, pady=5)
        description_label.grid(row=1, column=0, sticky='w')

        nonlocal description_entry
        description_entry = t.Text(frame_Info, width=35, height=3)
        description_entry.insert(END, form_data['description'])
        description_entry.grid(row=1, column=1, ipady=60, sticky='w')

        if is_update:
            description_label = t.Label(frame_Info, text='Status: ', background='#EEA579', font=("Times", 13), padx=5, pady=5)
            description_label.grid(row=2, column=0, sticky='w')
            nonlocal edit_status_combobox
            edit_status_combobox = ttk.Combobox(frame_Info, values=status, state='readonly')
            edit_status_combobox.current(status.index(form_data['status']))
            edit_status_combobox.grid(row=2, column=1)

        time_label = t.Label(frame_Info, background='#EEA579', text='Due date: ', font=("Times", 13), padx=5, pady=5)
        time_label.grid(row=3, column=0, sticky='w')
        nonlocal time_entry
        today = date.today()
        end_date = get_date_obj(form_data['end_time'])
        year = end_date.year
        month = end_date.month
        day = end_date.day
        time_entry = DateEntry(frame_Info, selectmode='day', year=year, month=month,
                       day=day, width=44, background='darkblue',
                       foreground='white', borderwidth=2, mindate=today)
        time_entry.grid(row=3, column=1, sticky='w')

        # button
        button_text = "Update task" if is_update else "Create task"
        button_command = update_single_task if is_update else create_task
        button_new = t.Button(frame_Info, background='#c96115', text=button_text, font=("Times", 13, "bold"), borderwidth=0, command=button_command)
        button_new.grid(row=5, columnspan=2)

    def is_form_valid():
        title = title_entry.get()
        description = description_entry.get("1.0", 'end-1c')

        if not title or not description:
            return False

        return True

    def add_task_to_list():
        nonlocal task_last_id
        task_last_id += 1

        new_task_dict = {
            'id': task_last_id,
            'title': title_entry.get(),
            'description': description_entry.get("1.0", 'end-1c'),
            'status': status[0],
            'end_time': time_entry.get_date().strftime(date_format),
            'start_time':  dt.datetime.today().strftime(date_format)
        }
        task_list.append(new_task_dict)

    def clear_new_task_form_data():
        nonlocal form_data
        form_data = initial_form_data

    def show_single_task(task):
        task_id = task['id']
        title = task['title']
        description = task['description']
        end_date = task['end_time']
        start_date = task['start_time']
        task_status = task['status']

        nonlocal task_last_id
        if int(task_id) > task_last_id:
            task_last_id = int(task_id)

        parent = get_task_parent(task_status)

        single_task_frame = t.LabelFrame(
            parent,
            font=("Times", 10, "bold"),
            padx=5, pady=5, background='#94B39A'
        )

        single_task_frame.grid(padx=(5, 0), sticky='w') # 400

        create_label(parent=single_task_frame, text='Task Title: ', row=0, column=0, sticky='w')

        title2_entry = t.Label(single_task_frame, text=title, font=("Times", 13, 'bold'), background='#94B39A')
        title2_entry.grid(row=0, column=1, sticky='w')

        create_label(parent=single_task_frame, text='Task Description: ', row=1, column=0, sticky='w')

        description_label = t.Label(single_task_frame, background='#94B39A', text=description, width=30, wraplength=280,
                                    justify=LEFT, font=("Times", 13), padx=5, pady=5)
        description_label.grid(row=1, column=1, sticky='news')

        create_label(parent=single_task_frame, text='Task was set on: ', row=2, column=0, sticky='w')
        create_label(parent=single_task_frame, text=start_date, row=2, column=1, sticky='w')

        create_label(parent=single_task_frame, text='Due date: ', row=3, column=0, sticky='w')

        create_label(parent=single_task_frame, text=end_date, row=3, column=1, sticky='w')

        create_label(parent=single_task_frame, text='Status: ', row=4, column=0, sticky='w')

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground="gray", background="gray")

        status_combobox = ttk.Combobox(single_task_frame, values=status, state='readonly')
        status_combobox.bind("<<ComboboxSelected>>", lambda event: change_status(event, task_id))
        status_combobox.current(status.index(task_status))
        status_combobox.grid(row=4, column=1, sticky='w')

        # buttons
        button_edit = t.Button(single_task_frame, text='Edit', font=("Times", 12), background='#1A5653', command=lambda: edit_task(task_id))
        button_edit.grid(row=5, column=1)
        button_delete = t.Button(single_task_frame, background='#1A5653', text='Del', font=("Times", 12),
                                 command=lambda: delete_task(task_id))
        button_delete.grid(row=5, column=1, sticky='e')

        canvas.create_window((0, 0), window=frame_all_tasks, anchor='nw')
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def get_task_parent(task_status):
        parent = frame_beginning

        if task_status == status[1]:
            parent = frame_in_progress
        elif task_status == status[2]:
            parent = frame_done

        return parent

    def get_date_obj(selected_date):
        if isinstance(selected_date, str):
            return datetime.datetime.strptime(selected_date, date_format)
        else:
            return selected_date

    def show_all_tasks():
        for task in task_list:
            show_single_task(task)

    def create_label(parent, text, row, column, sticky):
        new_label = t.Label(parent, background='#94B39A', text=text, font=("Times", 13), padx=5, pady=5)
        new_label.grid(row=row, column=column, sticky=sticky)

    def clear_screen():
        clear_frame(frame_done)
        clear_frame(frame_in_progress)
        clear_frame(frame_beginning)

    def clear_frame(selected_frame):
        if selected_frame != None:
            for child in selected_frame.winfo_children():
                child.destroy()

    def create_task():
        if is_form_valid():
            add_task_to_list()
            update_tasks()
            clear_new_task_form_data()
            new_window.destroy()
            file_service.write_in_file(task_list)
        else:
            t.messagebox.showwarning(title='Error', message="Please enter the title and description")
            new_window.focus()

    def update_tasks():
        clear_screen()
        show_all_tasks()
        canvas.create_window((0, 0), window=frame_all_tasks, anchor='nw')
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def update_single_task():
        get_form_data()
        update_task_dictionary()
        update_tasks()
        new_window.destroy()
        clear_new_task_form_data()
        file_service.write_in_file(task_list)

    def get_form_data():
        nonlocal form_data
        updated_form_data = {
            'id': form_data['id'],
            'title': title_entry.get(),
            'description': description_entry.get("1.0", 'end-1c'),
            'status': edit_status_combobox.get(),
            'end_time': time_entry.get_date().strftime(date_format),
            'start_time': form_data['start_time'],
            'index': form_data['index']
        }
        form_data = updated_form_data

    def update_task_dictionary():
        updated_task = {
            "id": form_data['id'],
            "title": form_data['title'],
            "description": form_data['description'],
            "end_time": form_data['end_time'],
            "start_time": form_data["start_time"],
            "status": form_data['status']
        }
        task_list[form_data['index']] = updated_task

    def change_status(event, task_id):
        selected_box = event.widget
        value = selected_box.get()

        for i in range(len(task_list)):
            if task_list[i]['id'] == task_id:
                task_list[i]['status'] = value
                break

        update_tasks()

    def delete_task(task_id):
        for i in range(len(task_list)):
            if task_list[i]['id'] == task_id:
                del task_list[i]
                break
        update_tasks()
        file_service.write_in_file(task_list)

    def edit_task(task_id):
        for i in range(len(task_list)):
            if task_list[i]['id'] == task_id:
                nonlocal form_data
                form_data = task_list[i]
                form_data['index'] = i
                break
        openNewWindow(True)

    def open_from_file():
        nonlocal task_list
        task_list = file_service.read_from_file()
        show_all_tasks()

    # button
    buttonAddTask = t.Button(frame, text='+ Add task', background='#1A5653', font=("Times", 12), command=openNewWindow)
    buttonAddTask.grid(row=1, column=0, padx=10, pady=10, sticky='es')

    open_from_file()
    if len(task_list) > 0:
        frame.grid_propagate(False)

    frame.config(width=window.winfo_width(), height=800)
    canvas.config(scrollregion=canvas.bbox("all"))


    window.mainloop()


main()

