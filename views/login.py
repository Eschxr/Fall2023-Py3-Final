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
        bg0 = tb.Frame(self.frame, bootstyle=LIGHT)
        bg0.pack(expand=TRUE, fill=BOTH)
        bg1 = tb.Frame(bg0, bootstyle=DARK)
        bg1.pack(expand=TRUE, fill=BOTH)
        bg2 = tb.Frame(bg0, bootstyle=DARK)
        bg2.pack(expand=TRUE, fill=BOTH)
        bg3 = tb.Frame(bg0, bootstyle=SECONDARY)
        bg3.pack(expand=TRUE, side=BOTTOM, anchor=SE, padx=10, pady=10)
        tb.Label(bg1, text="Please Enter Your Credentials", font=(FONT_FAMILY, 30), bootstyle="inverse dark").pack(padx=10, ipady=25)
        tb.Label(bg1, text="Email:", font=(FONT_FAMILY, 20), bootstyle="inverse dark").pack(side=LEFT, anchor=S, padx=10, pady=25)
        tb.Entry(bg1, textvariable=self.email_var, width=85).pack(side=LEFT, anchor=SE, padx=10, pady=25)
        tb.Label(bg2, text="Password:", font=(FONT_FAMILY, 20), bootstyle="inverse dark").pack(side=LEFT, anchor=N, padx=10, pady=25)
        tb.Entry(bg2, textvariable=self.password_var, show="*", width=80).pack(side=LEFT, anchor=NE, padx=10, pady=25)
        tb.Button(bg3, text="Login", command=self.login, bootstyle=SUCCESS).pack(side=RIGHT, padx=5, pady=10)
        tb.Button(bg3, text="Back", command=self.app.show_home_view, bootstyle=DANGER).pack(side=RIGHT, padx=10, pady=10)

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
