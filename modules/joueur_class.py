from modules.Machines import machines_disponibles, machines_possedees
import customtkinter as ctk
from PIL import Image, ImageTk

class Joueur:
    def __init__(self, nom, entreprise, argent=100000):
        self.nom = nom
        self.entreprise = entreprise
        self._argent = argent
        self._jour_actuel = 1
        self.machines_possedees = machines_possedees  # Initialiser avec les machines de départ
        self.techniciens_possedes = []
        self._ui_update_callback = None  # Pour définir une méthode de mise à jour UI

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
        return sum(machine.revenu_par_periode for machine in self.machines_possedees)

    @property
    def couts_fixes(self):
        return sum(technicien.salaire for technicien in self.techniciens_possedes)

    @property
    def solde_net(self):
        return self.revenu - self.couts_fixes

    def set_ui_update_callback(self, callback):
        """Permet de définir une méthode externe à appeler lors des mises à jour."""
        self._ui_update_callback = callback

    def trigger_ui_update(self):
        """Appelle la méthode de mise à jour si définie."""
        if self._ui_update_callback:
            self._ui_update_callback()

    def incrementer_jour(self):
        self.jour_actuel += 1

    def ajouter_revenu(self):
        self.argent += self.revenu

    def acheter_machine(self, machine):
        if self.argent >= machine.cout_achat:
            self.argent -= machine.cout_achat
            self.machines_possedees.append(machine)
            machines_disponibles.remove(machine)
            self.trigger_ui_update()
            return True
        return False

def creer_labels_profil(root, joueur):
    # Profil du joueur (cadre principal)
    profile_frame = ctk.CTkFrame(root, width=600, height=325, corner_radius=10, fg_color="#FFA500")
    profile_frame.place(x=10, y=10)

    # Ajout de l'image du joueur
    image_path = "Images/qatari_boss.png"  # Assurez-vous que l'image est dans le dossier 'Images'
    image = Image.open(image_path)
    photo_de_profil = ctk.CTkImage(light_image=image, size=(80, 80))

    profile_image_label = ctk.CTkLabel(profile_frame, text="", image=photo_de_profil)
    profile_image_label.place(x=20, y=20)

    # Labels pour le profil
    labels = {
        "argent": ctk.CTkLabel(profile_frame, text=f"{joueur.argent} €", font=("Arial", 12), text_color="black"),
        "jour_actuel": ctk.CTkLabel(profile_frame, text=f"{joueur.jour_actuel}", font=("Arial", 12), text_color="black"),
        "revenu": ctk.CTkLabel(profile_frame, text=f"{joueur.revenu} €", font=("Arial", 12), text_color="black"),
        "couts_fixes": ctk.CTkLabel(profile_frame, text=f"{joueur.couts_fixes} €", font=("Arial", 12), text_color="black"),
        "solde_net": ctk.CTkLabel(profile_frame, text=f"{joueur.solde_net} €", font=("Arial", 12), text_color="black"),
    }

    # Positionnement
    labels_positions = [
        ("Argent:", 120, 100, "argent"),
        ("Jour actuel:", 120, 130, "jour_actuel"),
        ("Revenu par période:", 120, 160, "revenu"),
        ("Coûts fixes:", 120, 190, "couts_fixes"),
        ("Solde net:", 120, 220, "solde_net"),
    ]

    for text, x, y, key in labels_positions:
        ctk.CTkLabel(profile_frame, text=text, font=("Arial", 12), text_color="black").place(x=x, y=y)
        labels[key].place(x=250, y=y)

    # Méthode pour mettre à jour dynamiquement les labels
    def update_ui():
        labels["argent"].configure(text=f"{joueur.argent} €")
        labels["jour_actuel"].configure(text=f"{joueur.jour_actuel}")
        labels["revenu"].configure(text=f"{joueur.revenu} €")
        labels["couts_fixes"].configure(text=f"{joueur.couts_fixes} €")
        labels["solde_net"].configure(text=f"{joueur.solde_net} €")

    joueur.set_ui_update_callback(update_ui)

    return labels
