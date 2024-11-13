import customtkinter as ctk
import tkinter as tk  # Importer tkinter pour utiliser tk.StringVar
from tkinter import messagebox
from PIL import Image, ImageTk

# Initialiser CustomTkinter avec un thème clair ou sombre
ctk.set_appearance_mode("light")  # Options: "light" ou "dark"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

class Technician:
    def __init__(self, name, role, experience, salary, image):
        self.name = name
        self.role = role
        self.experience = experience
        self.salary = salary
        self.image = image

class TechnicienApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Techniciens") 
        self.root.geometry("600x400")
        self.root.config(bg="#E6F2FF")

        # Charger les images pour chaque rôle et niveau d'expérience
        self.images = {
            "Mécanicien": [ImageTk.PhotoImage(Image.open(f"technician_{i}.png").resize((100, 100), Image.LANCZOS)) for i in range(1, 4)],
            "Informaticien": [ImageTk.PhotoImage(Image.open(f"informaticien_{i}.png").resize((100, 100), Image.LANCZOS)) for i in range(1, 4)],
            "Électricien": [ImageTk.PhotoImage(Image.open(f"electricien_{i}.png").resize((100, 100), Image.LANCZOS)) for i in range(1, 4)]
        }

        # Définir des techniciens par rôle
        self.technician_options = {
            "Mécanicien": [
                Technician("Jean", "Mécanicien", "peux expérimenté", 2000, self.images["Mécanicien"][0]),
                Technician("Pierre", "Mécanicien", "Moyennement Expérimenté", 3000, self.images["Mécanicien"][1]),
                Technician("Jacques", "Mécanicien", "Plus expérimenté", 4000, self.images["Mécanicien"][2]),
            ],
            "Informaticien": [
                Technician("Alice", "Informaticien", "peux expérimenté", 2200, self.images["Informaticien"][0]),
                Technician("Bob", "Informaticien", "Moyennement Expérimenté", 3200, self.images["Informaticien"][1]),
                Technician("Clara", "Informaticien", "Plus expérimenté", 4200, self.images["Informaticien"][2]),
            ],
            "Électricien": [
                Technician("Luc", "Électricien", "Peux expérimenté", 2100, self.images["Électricien"][0]),
                Technician("Marc", "Électricien", "Moyennement Expérimenté", 3100, self.images["Électricien"][1]),
                Technician("Paul", "Électricien", "Plus expérimenté", 4100, self.images["Électricien"][2]),
            ]
        }

        # Dropdown pour le rôle du technicien
        ctk.CTkLabel(self.root, text="Sélectionnez la catégorie du Technicien:", bg_color="#E6F2FF", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
        
        # Utilisation de tk.StringVar pour le menu déroulant avec traceur
        self.role_var = tk.StringVar(value="Mécanicien")  # Initialiser avec le rôle "Mécanicien"
        self.role_var.trace("w", self.display_technicians)  # Ajout d'un traceur pour la mise à jour

        role_dropdown = ctk.CTkComboBox(self.root, variable=self.role_var, values=list(self.technician_options.keys()), font=("Arial", 12))
        role_dropdown.grid(row=0, column=1, padx=10, pady=10)

        # Cadre pour afficher les techniciens
        self.frame_technicians = ctk.CTkFrame(self.root, fg_color="#E6F2FF", corner_radius=10)
        self.frame_technicians.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Initial display of technicians
        self.display_technicians()

    def display_technicians(self, *args):
        # Effacer les cadres de techniciens actuels
        for widget in self.frame_technicians.winfo_children():
            widget.destroy()

        # Obtenir le rôle sélectionné et afficher les techniciens correspondants
        role = self.role_var.get()
        technicians = self.technician_options.get(role, [])

        for index, technician in enumerate(technicians):
            technician_frame = ctk.CTkFrame(self.frame_technicians, fg_color="#B3D1FF", corner_radius=10)
            technician_frame.grid(row=0, column=index, padx=10, pady=10, sticky="n")

            # Afficher l'icône
            label_image = tk.Label(technician_frame, image=technician.image, bg="#B3D1FF")
            label_image.image = technician.image  # Pour éviter que l'image soit supprimée par le garbage collector
            label_image.pack(pady=5)  # L'image est ajoutée en premier

            # Afficher le nom et le rôle
            label_name = ctk.CTkLabel(technician_frame, text=f"{technician.name} ({technician.role})", font=("Arial", 12), bg_color="#B3D1FF")
            label_name.pack()

            # Afficher le niveau d'expérience et le salaire
            label_experience = ctk.CTkLabel(technician_frame, text=f"Expérience: {technician.experience}", font=("Arial", 10), bg_color="#B3D1FF")
            label_experience.pack()

            label_salary = ctk.CTkLabel(technician_frame, text=f"Salaire: {technician.salary} €", font=("Arial", 10), bg_color="#B3D1FF")
            label_salary.pack()

            # Bouton pour sélectionner ce technicien
            btn_select = ctk.CTkButton(technician_frame, text="Choisir", command=lambda t=technician: self.select_technician(t), font=("Arial", 10), corner_radius=8)
            btn_select.pack(pady=5)

    def select_technician(self, technician):
        # Afficher les informations du technicien sélectionné
        messagebox.showinfo("Sélection Technicien", f"Technicien sélectionné :\nNom: {technician.name}\nRôle: {technician.role}\nExpérience: {technician.experience}\nSalaire: {technician.salary} €")

# Lancer l'application
root = ctk.CTk()
app = TechnicienApp(root)
root.mainloop()
