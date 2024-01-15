import ttkbootstrap as tb
from K import *
from views.helper import View
import requests as req
from json import dumps

class RegistrationView(View):
    def __init__(self, app):
        super().__init__(app)
        self.role = "Admin"
        self.name_var = tb.StringVar()
        self.nick_var = tb.StringVar()
        self.email_var = tb.StringVar()
        self.password_var1 = tb.StringVar()
        self.password_var2 = tb.StringVar()
        self.create_widgets()

    def create_widgets(self):
        tb.Label(self.frame, text="Name: ").pack()
        tb.Entry(self.frame, textvariable=self.name_var).pack()
        tb.Label(self.frame, text="Username: ").pack()
        tb.Entry(self.frame, textvariable=self.nick_var).pack()
        tb.Label(self.frame, text="Email: ").pack()
        tb.Entry(self.frame, textvariable=self.email_var).pack()
        tb.Label(self.frame, text="Password: ").pack()
        tb.Entry(self.frame, textvariable=self.password_var1, show="*").pack()
        tb.Label(self.frame, text="Password Confirmation: ").pack()
        tb.Entry(self.frame, textvariable=self.password_var2, show="*").pack()
        tb.Button(self.frame, text="Submit", bootstyle=SUCCESS,command=self.register).pack()
        tb.Button(self.frame, text="Back",command=self.app.show_home_view, bootstyle=DANGER).pack()

    def register(self):
        if self.password_var1.get() == self.password_var2.get():
            id_loop = True
            id = 0
            while id_loop:
                try:
                    auth = req.post(f"{self.app.url}users", data=dumps({"alt_name": self.nick_var.get(),
                                                                        "id": id,
                                                                      "email": self.email_var.get(),
                                                                      "name": self.name_var.get(),
                                                                      "password": self.password_var1.get(),
                                                                      "role": "Admin"})).json()
                    id_loop = False
                except:
                    id += 1
            if auth is None:
                self.create_toast("Account Created", "Welcome to Food Online")
                auth = req.post(f"{self.app.url}token", data={"username": self.email_var.get(),
                                                                  "password": self.password_var1.get()}).json()
                self.app.token = {"access_token": auth["access_token"], "token_type": "bearer"}
                self.app.authenticated = TRUE
                self.app.email = self.email_var.get()
                self.password_var1.set("")
                self.app.show_tasks_view()
            else:
                self.create_toast("401 Error", "Bad Credentials")
        else:
            self.create_toast("401 Error", "Passwords Dont Match")