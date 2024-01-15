import ttkbootstrap as tb
from K import *
from views.helper import View

class HomeView(View):
    def __init__(self, app):
        super().__init__(app)

        self.create_widgets()

    def create_widgets(self):
        bg1 = tb.Frame(self.frame)
        bg1.pack(expand=True, fill=BOTH)
        bg2 = tb.Frame(self.frame, bootstyle=DARK)
        bg2.pack(expand=True, fill=BOTH, side=BOTTOM)
        tb.Label(bg1, text="Grand Task Compendium", bootstyle="primary", font=(FONT_FAMILY, 30)).pack(side=TOP, pady=60)
        tb.Label(bg1, text="A reliable storage for your tasks", bootstyle="secondary", font=(FONT_FAMILY, 15)).pack(side=TOP)
        tb.Label(bg2, text="Easy to use and 100% secure", bootstyle="inverse dark", font=(FONT_FAMILY, 15)).pack(side=BOTTOM, pady=40)
        tb.Button(bg1, text="Register", command=self.app.show_registration_view, bootstyle=SUCCESS).pack(side=BOTTOM, ipadx=30, ipady=5, pady=40)
        tb.Button(bg2, text="Login", command=self.app.show_login_view, bootstyle=INFO).pack(side=BOTTOM, ipadx=39,ipady=5)
