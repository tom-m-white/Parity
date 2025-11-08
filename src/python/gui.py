import customtkinter as ctk

class ParityApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.title("Parity")
        self.geometry("600x400")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Frame for layout
        self.frame = ctk.CTkFrame(self, corner_radius=15)
        self.frame.pack(expand=True, fill="both", padx=40, pady=40)

        # Title
        self.title_label = ctk.CTkLabel(
            self.frame,
            text="Parity",
            font=("Segoe UI", 28, "bold"),
            text_color="white"
        )
        self.title_label.pack(pady=(20, 10))

        # Subtitle
        self.subtitle = ctk.CTkLabel(
            self.frame,
            text="The state or condition of being equal, especially regarding status or pay",
            font=("Segoe UI", 14),
            text_color="gray80"
        )
        self.subtitle.pack(pady=(0, 25))

        # Search input
        self.query = ctk.StringVar()
        self.entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="Type your search here...",
            textvariable=self.query,
            width=300,
            height=40,
            corner_radius=10,
            font=("Segoe UI", 13)
        )
        self.entry.pack(pady=(0, 20))
        self.entry.bind("<Return>", self.search)

        # Search button
        self.search_button = ctk.CTkButton(
            self.frame,
            text="Search",
            width=150,
            height=40,
            corner_radius=10,
            command=self.search,
        )
        self.search_button.pack()

    def search(self, event=None):
        query_text = self.query.get().strip()
        if query_text:
            print(f"User searched: {query_text}")
            self.query.set("")


if __name__ == "__main__":
    app = ParityApp()
    app.mainloop()
