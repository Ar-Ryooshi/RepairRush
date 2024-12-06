import customtkinter as ctk
from PIL import Image, ImageTk
from Technician import Technician, technicians
from Machines import Machine, machines_possedees

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

def open_assign_window(technician, joueur):
    assign_window = ctk.CTkToplevel()
    assign_window.title("Attribuer un technicien à une machine")
    assign_window.geometry("400x300")

    ctk.CTkLabel(assign_window, text=f"Attribuer {technician.nom} à une machine", font=("Arial", 14)).pack(pady=10)

    for machine in machines_possedees:
        machine_button = ctk.CTkButton(assign_window, text=machine.nom, command=lambda m=machine: assign_technician_to_machine(technician, m, assign_window))
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
