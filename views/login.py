import ttkbootstrap as tb
import requests as req
from K import *
from views.helper import View


class LoginView(View):
    def __init__(self, app):
        super().__init__(app)
        self.email_var = tb.StringVar()
        self.password_var = tb.StringVar()
        self.create_widgets()

    def create_widgets(self):
        tb.Label(self.frame, text="Email:").pack()
        tb.Entry(self.frame, textvariable=self.email_var).pack()
        tb.Label(self.frame, text="Password:").pack()
        tb.Entry(self.frame, textvariable=self.password_var, show="*").pack()
        tb.Button(self.frame, text="Login", command=self.login, bootstyle=SUCCESS).pack()
        tb.Button(self.frame, text="Back", command=self.app.show_home_view, bootstyle=DANGER).pack()

    def login(self):
        email = self.email_var.get()
        password = self.password_var.get()

        auth = req.post(f"{self.app.url}token", data={"username": email,
                                                                  "password": password}).json()

        try:
            self.app.token = {"access_token": auth["access_token"], "token_type": "bearer"}
            self.app.authenticated = TRUE
            self.app.email = email
            self.password_var.set("")
            self.app.show_tasks_view()
        except:
            self.create_toast("401 Error", "Bad Credentials")
