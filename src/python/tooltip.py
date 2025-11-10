import customtkinter as ctk
import tkinter as tk

class ToolTip:
    def __init__(self, widget, text, bg="#1c1c1c", fg="white", waittime=400, padx=10, pady=6):
        self.widget = widget
        self.text = text
        self.waittime = waittime
        self.bg = bg
        self.fg = fg
        self.padx = padx
        self.pady = pady
        self.tip_window = None
        self.id = None

        self.widget.bind("<Enter>", self.schedule)
        self.widget.bind("<Leave>", self.hide)
        self.widget.bind("<ButtonPress>", self.hide)

    def schedule(self, event=None):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.show)

    def unschedule(self):
        _id = self.id
        self.id = None
        if _id:
            self.widget.after_cancel(_id)

    def show(self, event=None):
        if self.tip_window:
            return
        x = self.widget.winfo_rootx() + 20 #+40 test
        y = self.widget.winfo_rooty() + 20#+25 test

        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            tw,
            text=self.text,
            justify='left',
            background=self.bg,
            foreground=self.fg,
            relief='solid',
            borderwidth=1,
            padx=self.padx,
            pady=self.pady,
            font=("Segoe UI", 10)
        )
        label.pack(ipadx=1)

    def hide(self, event=None):
        self.unschedule()
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None
