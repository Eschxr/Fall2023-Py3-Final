import ttkbootstrap as tb
from ttkbootstrap import utility
from K import *
from views.helper import View
import requests as req
from json import dumps


class TasksView(View):
    def __init__(self, app):
        super().__init__(app)
        self.tree_columns = ("title", "id", "complete", "priority", "description")
        self.create_widgets()

    def create_widgets(self):
        # Add code to display a list of tasks here
        tb.Label(self.frame, text="Welcome to Your List", bootstyle="info", font=(FONT_FAMILY, 25)).pack(side=TOP, pady=60)

        self.tasks_tree = tb.Treeview(self.frame, bootstyle=SUCCESS, columns=self.tree_columns, show=HEADINGS)
        self.tasks_tree.pack(expand=TRUE, fill=X, padx=PL, pady=PL)
        self.tasks_tree.heading('title', text="Title")
        self.tasks_tree.heading('id', text="ID")
        self.tasks_tree.heading('complete', text="Completion")
        self.tasks_tree.heading('priority', text="Priority")
        self.tasks_tree.heading('description', text="Description")

        tb.Button(self.frame, text="Get Tasks List", command=self.get_tasks, bootstyle=DARK).pack(side=LEFT, padx=10, pady=10)
        tb.Button(self.frame, text="Task Details", command=self.app.show_task_view, bootstyle=DARK).pack(side=LEFT, padx=10, pady=10)
        tb.Button(self.frame, text="Create Task", command=self.app.show_create_task_view, bootstyle="outline success").pack(side=RIGHT, padx=10, pady=10)
        tb.Button(self.frame, text="Update Task", command=self.app.show_update_task_view, bootstyle="outline info").pack(side=RIGHT, padx=10, pady=10)
        

    def get_tasks(self):
        self.tasks_tree.delete(*self.tasks_tree.get_children())
        headers={'Content-Type': "application/json", "Authorization": f"Bearer {self.app.token['access_token']}"}
        tasks = req.get(f"{self.app.url}tasks", headers=headers)
        tasklist = []
        for task in tasks.json():
            tasklist.append((task["title"], str(task["id"]), str(task["complete"]), str(task["priority"]), task["description"]))
        for obtask in tasklist:
            self.tasks_tree.insert('', END, values=obtask)


class TaskView(View):
    def __init__(self, app):
        super().__init__(app)
        self.requested_task_id = tb.StringVar()
        self.displayed_task = tb.StringVar()
        self.create_widgets()

    def create_widgets(self):
        tb.Label(self.frame, text="Task Manager", font=(FONT_FAMILY, 25), bootstyle=PRIMARY).pack(padx=PM, pady=PM)
        tb.Label(self.frame, textvariable=self.displayed_task, font=(FONT_FAMILY, 15), bootstyle=INFO).pack(padx=PM, pady=PM)
        tb.Entry(self.frame, textvariable=self.requested_task_id, width=40).pack(padx=PM, pady=PM)
        tb.Button(self.frame, text="Search Task by ID", command=self.get_task, bootstyle=SUCCESS).pack(padx=PS, pady=PS)
        tb.Button(self.frame, text="Delete Current Task", command=self.delete_task, bootstyle="outline warning").pack(padx=PS, pady=PS)
        tb.Button(self.frame, text="Back to List", command=self.app.show_tasks_view, bootstyle=INFO).pack(padx=PS, pady=PS)

    def get_task(self):
        headers={'Content-Type': "application/json", "Authorization": f"Bearer {self.app.token['access_token']}"}
        tasks = req.get(f"{self.app.url}tasks", headers=headers)
        try:
            for task in tasks.json():
                if str(task["id"]) == str(self.requested_task_id.get()):
                    self.displayed_task.set(f"Task Title: {task['title']} \nTask ID: {task['id']} \nTask Completion: {task['complete']} \nTask Priority: {task['priority']} \nTask Description: {task['description']}") 
                    break
            self.create_toast("Success", "Your task has been displayed")
        except:
            self.create_toast("Error", "No task found with given task ID")

    def delete_task(self):
        headers={'Content-Type': "application/json", "Authorization": f"Bearer {self.app.token['access_token']}"}
        if self.requested_task_id.get() != None:
            try:
                req.delete(f"{self.app.url}tasks/{int(self.requested_task_id.get())}", headers=headers)
                self.create_toast("Success", "Your task has been deleted")
            except:
                self.create_toast("Error", "A problem has occured, please check your task ID or try again later")
        else:
            self.create_toast("Error", "Invalid Task ID")

class CreateTaskView(View):
    def __init__(self, app):
        super().__init__(app)
        self.task_name_var = tb.StringVar()
        self.task_description_var = tb.StringVar()
        self.create_widgets()

    def create_widgets(self):
        tb.Label(self.frame, text="Task Name:", font=(FONT_FAMILY, 25), bootstyle=PRIMARY).pack(padx=PM, pady=PM)
        tb.Entry(self.frame, textvariable=self.task_name_var, width=40).pack(padx=PM, pady=PM)
        tb.Label(self.frame, text="Description:", font=(FONT_FAMILY, 25), bootstyle=PRIMARY).pack(padx=PM, pady=PM)
        tb.Entry(self.frame, textvariable=self.task_description_var, width=40).pack(padx=PM, pady=PM)

        tb.Button(self.frame, text="Create Task", command=self.create_task, bootstyle=SUCCESS).pack(padx=PS, pady=PS)
        tb.Button(self.frame, text="Back", command=self.app.show_tasks_view, bootstyle="outline dark").pack(padx=PS, pady=PS)

    def create_task(self):
        task_name = self.task_name_var.get()
        task_description = self.task_description_var.get()
        headers={'Content-Type': "application/json", "Authorization": f"Bearer {self.app.token['access_token']}"}
        data = {
            "complete": False,
            "description": task_description,
            "priority": 1,
            "title": task_name
        }
        response = req.post(f"{self.app.url}tasks", data=dumps(data), headers=headers)
        
        if response.status_code == 201:
            self.create_toast("Task Created", f"Task '{task_name}' created successfully")
        else:
            self.create_toast("Error", f"Request failed with status code {response.status_code}")

        # After creating the task, show the task page
        self.app.show_tasks_view()


class UpdateTaskView(View):
    def __init__(self, app):
        super().__init__(app)
        self.taskid = tb.StringVar()
        self.updated_name_var = tb.StringVar()
        self.updated_description_var = tb.StringVar()
        self.updated_completion_var = tb.BooleanVar()
        self.create_widgets()

    def create_widgets(self):
        tb.Label(self.frame, text="Task ID:", font=(FONT_FAMILY, 15), bootstyle=PRIMARY).pack(padx=PM, pady=PS)
        tb.Entry(self.frame, textvariable=self.taskid, width=40).pack(padx=PM, pady=PM)
        tb.Label(self.frame, text="Updated Task Name:", font=(FONT_FAMILY, 15), bootstyle=PRIMARY).pack(padx=PM, pady=PS)
        tb.Entry(self.frame, textvariable=self.updated_name_var, width=40).pack(padx=PM, pady=PM)
        tb.Label(self.frame, text="Updated Description:", font=(FONT_FAMILY, 15), bootstyle=PRIMARY).pack(padx=PM, pady=PS)
        tb.Entry(self.frame, textvariable=self.updated_description_var, width=40).pack(padx=PM, pady=PM)
        tb.Label(self.frame, text="Updated Completion Status:", font=(FONT_FAMILY, 15), bootstyle=PRIMARY).pack(padx=PM, pady=PS)
        tb.Entry(self.frame, textvariable=self.updated_completion_var, width=40).pack(padx=PM, pady=PM)

        tb.Button(self.frame, text="Update Task", command=self.update_task, bootstyle=SUCCESS).pack(padx=PS, pady=PXS)
        tb.Button(self.frame, text="Back", command=self.app.show_tasks_view, bootstyle="outline dark").pack(padx=PS, pady=PXS)

    def update_task(self):
        taskid = int(self.taskid.get())
        updated_task_name = self.updated_name_var.get()
        updated_task_description = self.updated_description_var.get()
        updated_completion_status = bool(self.updated_completion_var.get())
        headers={'Content-Type': "application/json", "Authorization": f"Bearer {self.app.token['access_token']}"}
        data = {
            "complete": updated_completion_status,
            "description": updated_task_description,
            "priority": 1,
            "title": updated_task_name
        }
        response = req.put(f"{self.app.url}tasks/{taskid}", data=dumps(data), headers=headers)
        
        if response.status_code == 204:
            self.create_toast("Task Updated", f"Task '{updated_task_name}' created successfully")
        else:
            self.create_toast("Error", f"Request failed with status code {response.status_code}")

        # After creating the task, show the task page
        self.app.show_tasks_view()
