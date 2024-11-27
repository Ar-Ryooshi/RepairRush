import customtkinter as ctk
from PIL import Image, ImageTk

# Classe Technician
class Technician:
    def __init__(self, nom, specialite, niveau, salaire, facteur_reparation, image_path):
        self.nom = nom
        self.specialite = specialite
        self.niveau = niveau
        self.salaire = salaire
        self.facteur_reparation = facteur_reparation
        self.image_path = image_path
        self.assigned_machine = None

    def assign_to_machine(self, machine):
        if self.assigned_machine is not None:
            print(f"{self.nom} est déjà assigné à une machine.")
            return False
        self.assigned_machine = machine
        machine.technicien = self
        print(f"{self.nom} a été assigné à la machine {machine.nom}.")
        return True

    def engager(self, joueur):
        if joueur.argent >= self.salaire:
            joueur.argent -= self.salaire
            joueur.techniciens_possedes.append(self)
            print(f"{self.nom} engagé.")
            return True
        print(f"Pas assez d'argent pour engager {self.nom}.")
        return False

    def licencier(self, joueur):
        if self in joueur.techniciens_possedes:
            joueur.techniciens_possedes.remove(self)
            print(f"{self.nom} licencié.")
            return True
        print(f"{self.nom} n'est pas engagé, donc ne peut pas être licencié.")
        return False

# Liste des techniciens disponibles
technicians = [
    Technician("Rémy Tourneur", "Mécanique", "Débutant", 100, 1.25, 'images/Tech7.png'),
    Technician("Jack Soudey", "Mécanique", "Moyen", 200, 1, 'images/Tech7.png'),
    Technician("Claude Piston", "Mécanique", "Expert", 300, 0.75, 'images/Tech7.png'),
    Technician("Hubert Volt", "Électrique", "Débutant", 150, 1.25, 'images/Tech7.png'),
    Technician("Fred Fraiseuse", "Électrique", "Moyen", 250, 1, 'images/Tech7.png'),
    Technician("Léon Laser", "Électrique", "Expert", 350, 0.75, 'images/Tech7.png'),
    Technician("Alex Byte", "Informatique", "Débutant", 120, 1.25, 'images/Tech7.png'),
    Technician("Lucas Pixel", "Informatique", "Moyen", 220, 1, 'images/Tech7.png'),
    Technician("Dave Data", "Informatique", "Expert", 320, 0.75, 'images/Tech7.png')
]

# Dictionnaire pour garder une référence aux boutons d'engagement
engagement_buttons = {}

# Classe Joueur pour les tests
class Joueur:
    def __init__(self, argent):
        self.argent = argent
        self.techniciens_possedes = []

# Fonction pour mettre à jour la frame des techniciens engagés
def update_engaged_frame(engaged_frame, joueur, argent_label, engagement_buttons):
    # Supprimer les widgets précédents
    for widget in engaged_frame.winfo_children():
        widget.destroy()

    # Afficher les techniciens engagés
    for idx, technician in enumerate(joueur.techniciens_possedes):
        # Créer une sous-frame pour chaque technicien engagé
        tech_frame = ctk.CTkFrame(engaged_frame, width=180, height=150, fg_color="#444444", corner_radius=10)
        tech_frame.grid(row=0, column=idx, padx=10, pady=10)

        # Image du technicien
        image = Image.open(technician.image_path).resize((60, 60))
        tech_image = ImageTk.PhotoImage(image)
        image_label = ctk.CTkLabel(tech_frame, text="", image=tech_image)
        image_label.image = tech_image  # Garde une référence pour éviter que l'image ne soit supprimée
        image_label.pack(pady=5)

        # Nom du technicien
        name_label = ctk.CTkLabel(tech_frame, text=technician.nom, font=("Arial", 10))
        name_label.pack()

        # Boutons Attribuer et Licencier
        assign_button = ctk.CTkButton(tech_frame, text="Attribuer", font=("Arial", 10), command=lambda tech=technician: open_assign_window(tech, joueur))
        assign_button.pack(pady=5)

        def licencier_technicien(tech=technician):
            if tech.licencier(joueur):
                argent_label.configure(text=f"Argent : {joueur.argent} €")
                update_engaged_frame(engaged_frame, joueur, argent_label, engagement_buttons)
                # Réactiver le bouton d'engagement
                engagement_buttons[tech].configure(state="normal")

        fire_button = ctk.CTkButton(tech_frame, text="Licencier", font=("Arial", 10), command=licencier_technicien)
        fire_button.pack(pady=5)

# Fonction pour engager un technicien
def engager_technicien(technicien, joueur, argent_value, engaged_frame, engagement_buttons, button):
    # Logique pour engager un technicien et mettre à jour l'interface
    if len(joueur.techniciens_possedes) < 6 and technicien not in joueur.techniciens_possedes:  # Maximum de 6 techniciens et empêcher double engagement
        if technicien.engager(joueur):
            argent_value.configure(text=f"Argent : {joueur.argent} €")
            update_engaged_frame(engaged_frame, joueur, argent_value, engagement_buttons)  # Mettre à jour la frame des techniciens engagés
            button.configure(state="disabled")  # Désactiver le bouton après engagement
    else:
        print("Nombre maximum de techniciens atteint ou technicien déjà engagé!")

# Fonction pour ouvrir une fenêtre d'assignation
def open_assign_window(technician, joueur):
    from Machines import machines_possedees  # Import local pour éviter les importations circulaires
    assign_window = ctk.CTkToplevel()
    assign_window.title("Attribuer un technicien à une machine")
    assign_window.geometry("400x300")

    ctk.CTkLabel(assign_window, text=f"Attribuer {technician.nom} à une machine", font=("Arial", 14)).pack(pady=10)

    for machine in machines_possedees:
        machine_button = ctk.CTkButton(assign_window, text=f"{machine.nom} ({machine.niveau_machine})", command=lambda m=machine: assign_technician_to_machine(technician, m, assign_window))
        machine_button.pack(pady=5)

def assign_technician_to_machine(technician, machine, window):
    if machine.assign_technician(technician):
        print(f"{technician.nom} a été assigné à la machine {machine.nom}.")
        window.destroy()
    else:
        print(f"Impossible d'assigner {technician.nom} à la machine {machine.nom}.")

# Exemple d'utilisation dans un autre fichier
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1380x800")

    joueur = Joueur(argent=1000)

    # Création d'un cadre pour les techniciens dans l'interface principale
    techniciens_frame = ctk.CTkFrame(root, width=1380, height=300)
    techniciens_frame.place(x=0, y=0)

    argent_label = ctk.CTkLabel(root, text=f"Argent : {joueur.argent} €", font=("Arial", 14))
    argent_label.place(x=10, y=310)

    engagement_buttons = {}

    for idx, technician in enumerate(technicians):
        tech_frame = ctk.CTkFrame(techniciens_frame, width=180, height=150, fg_color="#444444", corner_radius=10)
        tech_frame.grid(row=0, column=idx, padx=10, pady=10)

        # Image du technicien
        image = Image.open(technician.image_path).resize((60, 60))
        tech_image = ImageTk.PhotoImage(image)
        image_label = ctk.CTkLabel(tech_frame, text="", image=tech_image)
        image_label.image = tech_image  # Garde une référence pour éviter que l'image ne soit supprimée
        image_label.pack(pady=5)

        # Nom du technicien
        name_label = ctk.CTkLabel(tech_frame, text=technician.nom, font=("Arial", 10))
        name_label.pack()

        # Bouton d'action (Engager)
        action_button = ctk.CTkButton(tech_frame, text="Engager")
        action_button.pack(pady=5)

        # Ajouter le bouton au dictionnaire pour pouvoir le réactiver plus tard
        engagement_buttons[technician] = action_button

        # Fonction pour engager le technicien
        def engager_technicien(tech=technician, button=action_button):
            if len(joueur.techniciens_possedes) < 6 and tech not in joueur.techniciens_possedes:  # Maximum de 6 techniciens et empêcher double engagement
                if tech.engager(joueur):
                    argent_label.configure(text=f"Argent : {joueur.argent} €")
                    update_engaged_frame(techniciens_frame, joueur, argent_label, engagement_buttons)  # Mettre à jour la frame des techniciens engagés
                    button.configure(state="disabled")  # Désactiver le bouton après engagement
            else:
                print("Nombre maximum de techniciens atteint ou technicien déjà engagé!")

        # Assigner la fonction d'engagement au bouton
        action_button.configure(command=lambda t=technician, b=action_button: engager_technicien(t, b))

    # Lancer l'interface graphique
    root.mainloop()
