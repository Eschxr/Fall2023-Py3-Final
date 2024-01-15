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
        bg1 = tb.Frame(self.frame)
        bg1.pack(expand=True, fill=BOTH)
        bg2 = tb.Frame(self.frame, bootstyle=DARK)
        bg2.pack(expand=True, fill=BOTH, side=BOTTOM)
        tb.Label(bg1, text="First Name: ", bootstyle="secondary", font=(FONT_FAMILY, 15)).pack(padx=8, pady=8)
        tb.Entry(bg1, textvariable=self.name_var, width=40).pack(padx=8, pady=8)
        tb.Label(bg1, text="Username: ", bootstyle="secondary", font=(FONT_FAMILY, 15)).pack(padx=8, pady=8)
        tb.Entry(bg1, textvariable=self.nick_var, width=40).pack(padx=8, pady=8)
        tb.Label(bg1, text="Email: ", bootstyle="secondary", font=(FONT_FAMILY, 15)).pack(padx=8, pady=8)
        tb.Entry(bg1, textvariable=self.email_var, width=40).pack(padx=8, pady=8)
        tb.Label(bg1, text="Password: ", bootstyle="secondary", font=(FONT_FAMILY, 15)).pack(padx=8, pady=8)
        tb.Entry(bg1, textvariable=self.password_var1, show="*", width=40).pack(padx=8, pady=8)
        tb.Label(bg1, text="Password Confirmation: ", bootstyle="secondary", font=(FONT_FAMILY, 15)).pack(padx=8, pady=8)
        tb.Entry(bg1, textvariable=self.password_var2, show="*", width=40).pack(padx=8, pady=8)
        tb.Label(bg2, text="Welcome to the Registration Menu!", bootstyle="inverse dark", font=(FONT_FAMILY, 25)).pack(padx=8, pady=15)
        tb.Button(bg2, text="Submit", bootstyle=SUCCESS,command=self.register).pack(side=RIGHT, padx=15, pady=5)
        tb.Button(bg2, text="Back",command=self.app.show_home_view, bootstyle=DANGER).pack(side=RIGHT, padx=3, pady=5)

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
                self.create_toast("Success", "Account Registration Successful")
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