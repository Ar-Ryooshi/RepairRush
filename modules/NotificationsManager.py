"""
Gestionnaire de notifications pour l'application RepairRush.

Ce module fournit une classe pour gérer les notifications dans une interface utilisateur, qui notifie le joueur des événements importants,
ainsi que des fonctions pour définir et obtenir une instance globale du gestionnaire de notifications.
"""

from customtkinter import CTkTextbox, CTkFrame

class NotificationsManager:
    """
    Classe NotificationsManager pour gérer les notifications.

    Attributs:
        frame (CTkFrame): Le cadre contenant la zone de texte des notifications.
        textbox (CTkTextbox): La zone de texte où les notifications sont affichées.

    Méthodes:
        __init__(root, x, y, width, height): Initialise le gestionnaire de notifications.
        ajouter_notification(message): Ajoute une notification à la zone de texte.
    """

    def __init__(self, root, x, y, width, height):
        """
        Initialise le gestionnaire de notifications.

        Args:
            root: La fenêtre ou le cadre parent.
            x (int): La position x du cadre.
            y (int): La position y du cadre.
            width (int): La largeur du cadre.
            height (int): La hauteur du cadre.
        """
        self.frame = CTkFrame(root, width=width, height=height, fg_color="#222222")
        self.frame.place(x=x, y=y)
        self.textbox = CTkTextbox(self.frame, width=width-20, height=height-20, state="disabled")
        self.textbox.pack(padx=10, pady=10)

    def ajouter_notification(self, message):
        """
        Ajoute une notification à la zone de texte.

        Args:
            message (str): Le message de notification à ajouter.
        """
        self.textbox.configure(state="normal")
        self.textbox.insert("end", f"{message}\n")
        self.textbox.configure(state="disabled")
        self.textbox.yview_moveto(1)  # Scroll automatique vers le bas

# Instance globale pour tout le projet
_notifications_manager = None

def set_global_notifications_manager(manager):
    """
    Définit l'instance globale du gestionnaire de notifications.

    Args:
        manager (NotificationsManager): L'instance du gestionnaire de notifications à définir.
    """
    global _notifications_manager
    _notifications_manager = manager

def get_global_notifications_manager():
    """
    Obtient l'instance globale du gestionnaire de notifications.

    Returns:
        NotificationsManager: L'instance globale du gestionnaire de notifications.
    """
    return _notifications_manager
