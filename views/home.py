import ttkbootstrap as tb
from K import *
from views.helper import View

class HomeView(View):
    def __init__(self, app):
        super().__init__(app)

        self.create_widgets()

    def create_widgets(self):
        tb.Label(self.frame, text="Grand Compendium of Tasks", bootstyle="primary", font=(FONT_FAMILY, 30)).pack(side=TOP, pady=60)
        tb.Label(self.frame, text="A reliable storage for your tasks", bootstyle="secondary", font=(FONT_FAMILY, 15)).pack(side=TOP)
        tb.Label(self.frame, text="easy to use and 100% secure", bootstyle="secondary", font=(FONT_FAMILY, 15)).pack(side=TOP)
        tb.Button(self.frame, text="Register", command=self.app.show_registration_view, bootstyle=SUCCESS).pack(side=BOTTOM, ipadx=30, ipady=5, pady=40)
        tb.Button(self.frame, text="Login", command=self.app.show_login_view, bootstyle=INFO).pack(side=BOTTOM, ipadx=39,ipady=5)
