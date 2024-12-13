"""
Module Joueur pour gérer les informations et les actions du joueur dans RepairRush.

Ce fichier inclut la classe Joueur, responsable de la gestion des données du joueur,
ainsi que des fonctions pour créer et mettre à jour l'interface du profil utilisateur.
"""

from modules.Machines import machines_disponibles, machines_possedees
import customtkinter as ctk
from PIL import Image
from modules.NotificationsManager import get_global_notifications_manager

class Joueur:
    """
    Classe représentant le joueur et ses interactions.

    Attributs :
        nom (str) : Nom du joueur.
        entreprise (str) : Nom de l'entreprise du joueur.
        photo (str) : Chemin vers l'image de profil du joueur.
        argent (int) : Montant d'argent disponible.
        jour_actuel (int) : Numéro du jour actuel.
        machines_possedees (list) : Liste des machines possédées.
        techniciens_possedes (list) : Liste des techniciens engagés.
        _ui_update_callback (function) : Fonction de mise à jour de l'interface.
        compteur_appels (int) : Compteur pour gérer l'incrémentation des jours.

    Méthodes :
        set_ui_update_callback(callback) : Définit une méthode externe pour mettre à jour l'UI.
        trigger_ui_update() : Appelle la méthode de mise à jour si définie.
        incrementer_jour() : Incrémente le jour après plusieurs appels.
        ajouter_revenu() : Ajoute les revenus des machines à l'argent du joueur.
        acheter_machine(machine) : Achète une machine et met à jour les ressources.
        payer_salaires() : Déduit les salaires des techniciens de l'argent disponible.
    """

    def __init__(self, nom, entreprise, photo, argent=7500):
        """
        Initialise un joueur avec des valeurs par défaut.

        Args :
            nom (str) : Nom du joueur.
            entreprise (str) : Nom de l'entreprise du joueur.
            photo (str) : Chemin vers l'image de profil.
            argent (int) : Montant d'argent initial (par défaut : 7500).
        """
        self.nom = nom
        self.entreprise = entreprise
        self.photo = photo
        self._argent = argent
        self._jour_actuel = 1
        self.machines_possedees = machines_possedees
        self.techniciens_possedes = []
        self._ui_update_callback = None
        self.compteur_appels = 0

    # --- Propriétés pour gérer les données du joueur ---
    @property
    def argent(self):
        return self._argent

    @argent.setter
    def argent(self, value):
        self._argent = value
        self.trigger_ui_update()

    @property
    def jour_actuel(self):
        return self._jour_actuel

    @jour_actuel.setter
    def jour_actuel(self, value):
        self._jour_actuel = value
        self.trigger_ui_update()

    @property
    def revenu(self):
        """Calcule les revenus totaux des machines possédées."""
        return sum(machine.revenu_par_periode for machine in self.machines_possedees)

    @property
    def couts_fixes(self):
        """Calcule les coûts fixes totaux des techniciens engagés."""
        return sum(technicien.salaire for technicien in self.techniciens_possedes)

    @property
    def solde_net(self):
        """Retourne le solde net : revenu - coûts fixes."""
        return self.revenu - self.couts_fixes

    # --- Méthodes ---
    def set_ui_update_callback(self, callback):
        """Définit une méthode externe pour mettre à jour l'interface."""
        self._ui_update_callback = callback

    def trigger_ui_update(self):
        """Appelle la méthode de mise à jour si définie."""
        if self._ui_update_callback:
            self._ui_update_callback()

    def incrementer_jour(self):
        """
        Incrémente le jour actuel après un certain nombre d'appels.
        Utilisé pour synchroniser l'avancement dans le temps.
        """
        self.compteur_appels += 1
        if self.compteur_appels >= 4:
            self.jour_actuel += 1
            self.compteur_appels = 0
            self.trigger_ui_update()

    def ajouter_revenu(self):
        """Ajoute les revenus des machines possédées à l'argent du joueur."""
        self.argent += self.revenu

    def acheter_machine(self, machine):
        """
        Achète une machine si le joueur a suffisamment d'argent.

        Args :
            machine : La machine à acheter.

        Returns :
            bool : True si l'achat a réussi, False sinon.
        """
        if self.argent >= machine.cout_achat:
            self.argent -= machine.cout_achat
            self.machines_possedees.append(machine)
            if machine in machines_disponibles:
                machines_disponibles.remove(machine)
            self.trigger_ui_update()
            return True
        return False

    def payer_salaires(self):
        """Déduit les salaires des techniciens de l'argent du joueur."""
        manager = get_global_notifications_manager()
        total_salaires = self.couts_fixes
        if self.argent >= total_salaires:
            self.argent -= total_salaires
            if manager:
                manager.ajouter_notification(f"Salaires payés : {total_salaires} €.")
        else:
            if manager:
                manager.ajouter_notification("Pas assez d'argent pour payer tous les salaires !")


# --- Interface utilisateur du profil joueur ---
def creer_labels_profil(root, joueur, selected_currency, image_path="images/Profil2.png"):
    """
    Crée les labels du profil utilisateur dans l'interface.

    Args :
        root : Fenêtre ou cadre parent.
        joueur (Joueur) : Instance du joueur.
        selected_currency (str) : Symbole de la monnaie à afficher.
        image_path (str) : Chemin vers l'image par défaut (optionnel).

    Returns :
        dict : Dictionnaire des labels créés.
    """
    profile_frame = ctk.CTkFrame(root, width=600, height=330, corner_radius=10, fg_color="#FFA500")
    profile_frame.place(x=10, y=10)
    image_path = joueur.photo
    image = Image.open(image_path)
    photo_de_profil = ctk.CTkImage(light_image=image, size=(80, 80))
    profile_image_label = ctk.CTkLabel(profile_frame, text="", image=photo_de_profil)
    profile_image_label.place(x=20, y=20)

    # Création des labels
    labels = {
        "nom": ctk.CTkLabel(profile_frame, text=f"{joueur.nom}", font=("Arial", 16, "bold"), text_color="black"),
        "entreprise": ctk.CTkLabel(profile_frame, text=f"{joueur.entreprise}", font=("Arial", 12), text_color="black"),
        "argent": ctk.CTkLabel(profile_frame, text=f"{int(joueur.argent)} {selected_currency}", font=("Arial", 12), text_color="black"),
        "jour_actuel": ctk.CTkLabel(profile_frame, text=f"{joueur.jour_actuel}", font=("Arial", 12), text_color="black"),
        "revenu": ctk.CTkLabel(profile_frame, text=f"{int(joueur.revenu)} {selected_currency}", font=("Arial", 12), text_color="black"),
        "couts_fixes": ctk.CTkLabel(profile_frame, text=f"{int(joueur.couts_fixes)} {selected_currency}", font=("Arial", 12), text_color="black"),
        "solde_net": ctk.CTkLabel(profile_frame, text=f"{int(joueur.solde_net)} {selected_currency}", font=("Arial", 12), text_color="black"),
    }

    # Positions des labels
    labels_positions = [
        ("Nom :", 120, 30, "nom"),
        ("Entreprise :", 120, 60, "entreprise"),
        ("Argent :", 120, 100, "argent"),
        ("Jour actuel :", 120, 130, "jour_actuel"),
        ("Revenu par période :", 120, 160, "revenu"),
        ("Coûts fixes :", 120, 190, "couts_fixes"),
        ("Solde net :", 120, 220, "solde_net"),
    ]

    # Placement des labels
    for text, x, y, key in labels_positions:
        ctk.CTkLabel(profile_frame, text=text, font=("Arial", 12), text_color="black").place(x=x, y=y)
        labels[key].place(x=250, y=y)

    # Mise à jour automatique de l'interface
    def update_ui():
        labels["nom"].configure(text=f"{joueur.nom}")
        labels["entreprise"].configure(text=f"{joueur.entreprise}")
        labels["argent"].configure(text=f"{int(joueur.argent)} {selected_currency}")
        labels["revenu"].configure(text=f"{joueur.revenu} {selected_currency}")
        labels["jour_actuel"].configure(text=f"{joueur.jour_actuel}")
        labels["couts_fixes"].configure(text=f"{joueur.couts_fixes} {selected_currency}")
        labels["solde_net"].configure(text=f"{joueur.solde_net} {selected_currency}")

    joueur.set_ui_update_callback(update_ui)

    return labels
