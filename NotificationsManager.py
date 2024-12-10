from customtkinter import CTkTextbox, CTkFrame

class NotificationsManager:
    def __init__(self, root, x, y, width, height):
        self.frame = CTkFrame(root, width=width, height=height, fg_color="#222222")
        self.frame.place(x=x, y=y)
        self.textbox = CTkTextbox(self.frame, width=width-20, height=height-20, state="disabled")
        self.textbox.pack(padx=10, pady=10)

    def ajouter_notification(self, message):
        """Ajoute une notification."""
        self.textbox.configure(state="normal")
        self.textbox.insert("end", f"{message}\n")
        self.textbox.configure(state="disabled")
        self.textbox.yview_moveto(1)  # Scroll automatique vers le bas

# Instance globale pour tout le projet
_notifications_manager = None

def set_global_notifications_manager(manager):
    global _notifications_manager
    _notifications_manager = manager

def get_global_notifications_manager():
    return _notifications_manager

