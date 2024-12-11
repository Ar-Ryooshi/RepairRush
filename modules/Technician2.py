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
        self.machine_image_label = None

    def assign_to_machine(self, machine, assign_button, joueur, tech_frame):
        if self.assigned_machine is not None:
            print(f"{self.nom} est déjà assigné à une machine.")
            return False
        if self.specialite != machine.type_machine:
            print(f"{self.nom} ne peut pas être assigné à la machine {machine.nom} ({machine.niveau_machine}) car les types ne correspondent pas.")
            return False
        self.assigned_machine = machine
        machine.technicien = self
        print(f"{self.nom} a été assigné à la machine {machine.nom} ({machine.niveau_machine}).")
        assign_button.configure(text="Désaffecter", command=lambda: self.unassign_from_machine(assign_button, joueur))
        
        # Charger l'image de la machine
        machine_image = Image.open(machine.image_path).resize((20, 20))
        machine_image = ImageTk.PhotoImage(machine_image)

        # Créer ou mettre à jour l'image de la machine
        if self.machine_image_label is None:
            self.machine_image_label = ctk.CTkLabel(tech_frame, image=machine_image, text="")
            self.machine_image_label.image = machine_image  # Garder une référence
            self.machine_image_label.place(relx=1.0, rely=1.0, anchor="se")  # En bas à droite
        else:
            self.machine_image_label.configure(image=machine_image)
            self.machine_image_label.image = machine_image

        return True
    
    def unassign_from_machine(self, assign_button=None, joueur=None):
        if self.assigned_machine is None:
            print(f"{self.nom} n'est pas assigné à une machine.")
            return False
        if self.assigned_machine.en_reparation_flag:
            print(f"{self.nom} ne peut pas être désassigné car la machine {self.assigned_machine.nom} ({self.assigned_machine.niveau_machine}) est en réparation.")
            return False
        print(f"{self.nom} a été désassigné de la machine {self.assigned_machine.nom} ({self.assigned_machine.niveau_machine}).")
        self.assigned_machine.technicien = None
        self.assigned_machine = None
        if assign_button:
            assign_button.configure(text="Attribuer", command=lambda: open_assign_window(self, joueur, assign_button))
        
        # Supprimer l'image de la machine
        if self.machine_image_label is not None:
            self.machine_image_label.place_forget()
            self.machine_image_label = None

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
            if self.assigned_machine is not None:
                if self.assigned_machine.en_reparation_flag:
                    print(f"{self.nom} ne peut pas être licencié car la machine {self.assigned_machine.nom} ({self.assigned_machine.niveau_machine}) est en réparation.")
                    return False
                self.unassign_from_machine(None, None)  # Désassigner de la machine
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

        # Afficher l'image de la machine assignée (si disponible)
        if technician.assigned_machine:
            machine_image = Image.open(technician.assigned_machine.image_path).resize((20, 20))
            machine_image = ImageTk.PhotoImage(machine_image)
            machine_label = ctk.CTkLabel(tech_frame, image=machine_image, text="")
            machine_label.image = machine_image  # Garder une référence à l'image
            machine_label.place(relx=1.0, rely=1.0, anchor="se")  # Position en bas à droite

        # Bouton d'assignation/désassignation
        assign_button = ctk.CTkButton(tech_frame, font=("Arial", 10))

        if technician.assigned_machine is None:
            # Le technicien n'est pas assigné
            assign_button.configure(
                text="Attribuer",
                command=lambda tech=technician, btn=assign_button: open_assign_window(tech, joueur, btn)
            )
        else:
            # Le technicien est déjà assigné
            assign_button.configure(
                text="Désaffecter",
                command=lambda tech=technician, btn=assign_button: tech.unassign_from_machine(btn, joueur)
            )

        assign_button.pack(pady=5)

        # Bouton pour licencier le technicien
        def licencier_technicien(tech=technician):
            if tech.licencier(joueur):
                argent_label.configure(text=f"Argent : {joueur.argent} €")
                update_engaged_frame(engaged_frame, joueur, argent_label, engagement_buttons)
                # Réactiver le bouton d'engagement
                if tech in engagement_buttons:
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
def open_assign_window(technician, joueur, assign_button):
    from modules.Machines2 import machines_possedees  # Import local pour éviter les importations circulaires
    assign_window = ctk.CTkToplevel()
    assign_window.title("Attribuer un technicien à une machine")
    assign_window.geometry("400x300")

    ctk.CTkLabel(assign_window, text=f"Attribuer {technician.nom} à une machine", font=("Arial", 14)).pack(pady=10)

    for machine in machines_possedees:
        machine_button = ctk.CTkButton(assign_window, text=f"{machine.nom} ({machine.niveau_machine})", command=lambda m=machine: assign_technician_to_machine(technician, m, assign_window, assign_button, joueur, tech_frame=None))
        machine_button.pack(pady=5)

    def assign_technician_to_machine(technician, machine, window, assign_button, joueur, tech_frame):
        if machine.technicien is not None:
            print(f"Impossible d'assigner {technician.nom} à la machine {machine.nom} ({machine.niveau_machine}). La machine est déjà occupée.")
            return
        
        if technician.assign_to_machine(machine, assign_button, joueur, tech_frame):
            print(f"{technician.nom} a été assigné à la machine {machine.nom} ({machine.niveau_machine}).")
            assign_button.configure(
                text="Désaffecter",
                command=lambda tech=technician, btn=assign_button: tech.unassign_from_machine(btn, joueur)
            )
            window.destroy()
        else:
            print(f"Impossible d'assigner {technician.nom} à la machine {machine.nom} ({machine.niveau_machine}).")

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

    root.mainloop()