import ttkbootstrap as tb
from K import *
from views import login, registration, tasks, home


class TaskApp(tb.Window):
    def __init__(self):
        super().__init__(themename="cerculean")
        self.title("Task Manager")
        self.geometry("1280x720")

        # User variables
        self.authenticated = False
        self.email = tb.StringVar()
        self.token: dict = {}
        self.url = 'http://192.168.3.247:8000/'

        # Views variables
        self.current_view = None
        self.header_frame = None
        self.views = {
            "home": home.HomeView(self),
            "registration": registration.RegistrationView(self),
            "login": login.LoginView(self),
            "view_tasks": tasks.TasksView(self),
            "view_task": tasks.TaskView(self),
            "create_task": tasks.CreateTaskView(self),
            "update_task": tasks.UpdateTaskView(self)
        }

        # Init Welcome Screen
        self.create_header()
        self.show_home_view()

    def create_header(self):
        self.header_frame = tb.Frame(self, bootstyle=PRIMARY)

        logout_button = tb.Button(self.header_frame, text="Logout", command=self.logout, bootstyle=DANGER)
        logout_button.pack(side=RIGHT, padx=PM, pady=PS)

    def show_header(self):
        self.header_frame.pack(fill=X)

    def hide_header(self):
        self.header_frame.pack_forget()

    def logout(self):
        self.authenticated = False
        self.show_home_view()

    def show_home_view(self):
        self.set_current_view("home")

    def show_registration_view(self):
        self.set_current_view("registration")

    def show_login_view(self):
        self.set_current_view("login")

    def show_task_view(self):
        self.set_current_view("view_task")

    def show_tasks_view(self):
        self.set_current_view("view_tasks")

    def show_create_task_view(self):
        self.set_current_view("create_task")
    
    def show_update_task_view(self):
        self.set_current_view("update_task")

    def set_current_view(self, key):
        self.destroy_current_view()
        self.current_view = key
        if self.authenticated:
            self.show_header()
        else:
            self.hide_header()
        self.views.get(key).pack_view()

    def destroy_current_view(self):
        if self.current_view:
            self.views.get(self.current_view).unpack_view()


if __name__ == "__main__":
    app = TaskApp()
    app.place_window_center()
    app.mainloop()
