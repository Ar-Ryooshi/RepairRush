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

    def engager(self, joueur, progression_jour=1.0):
        """
        Engage le technicien et soustrait le salaire ajusté.
        progression_jour est un float entre 0 et 1 indiquant la progression de la journée.
        """
        cout_restant = self.salaire * progression_jour
        if joueur.argent >= cout_restant:
            joueur.argent -= int(cout_restant) #empêche que le .0 soit ajouté
            joueur.techniciens_possedes.append(self)
            print(f"{self.nom} engagé pour {cout_restant:.2f}.")
            return True
        print(f"Pas assez d'argent pour engager {self.nom}.")
        return False

    def licencier(self, joueur):
        if self in joueur.techniciens_possedes:
            joueur.techniciens_possedes.remove(self)
            joueur.trigger_ui_update()
            print(f"{self.nom} licencié.")
            return True
        print(f"{self.nom} n'est pas engagé, donc ne peut pas être licencié.")
        return False

# Liste des techniciens disponibles
technicians = [
    Technician("Rémy Tourneur", "Mécanique", "Débutant", 100, 0.75, 'images/Tech7.png'),
    Technician("Jack Soudey", "Mécanique", "Moyen", 200, 1, 'images/Tech7.png'),
    Technician("Claude Piston", "Mécanique", "Expert", 300, 1.5, 'images/Tech7.png'),
    Technician("Hubert Volt", "Électrique", "Débutant", 150, 0.75, 'images/Tech7.png'),
    Technician("Fred Fraiseuse", "Électrique", "Moyen", 250, 1, 'images/Tech7.png'),
    Technician("Léon Laser", "Électrique", "Expert", 350, 1.5, 'images/Tech7.png'),
    Technician("Alex Byte", "Informatique", "Débutant", 120, 0.75, 'images/Tech7.png'),
    Technician("Lucas Pixel", "Informatique", "Moyen", 220, 1, 'images/Tech7.png'),
    Technician("Dave Data", "Informatique", "Expert", 320, 1.5, 'images/Tech7.png')
]

# Dictionnaire pour garder une référence aux boutons d'engagement
engagement_buttons = {}

# Classe Joueur pour les tests


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
        assign_button = ctk.CTkButton(tech_frame, text="Attribuer", font=("Arial", 10))
        assign_button.pack(pady=5)

        def licencier_technicien(tech=technician):
            if tech.licencier(joueur):
                argent_label.configure(text=f"{joueur.argent}")
                update_engaged_frame(engaged_frame, joueur, argent_label, engagement_buttons)
                # Réactiver le bouton d'engagement
                engagement_buttons[tech].configure(state="normal")

        fire_button = ctk.CTkButton(tech_frame, text="Licencier", font=("Arial", 10), command=licencier_technicien)
        fire_button.pack(pady=5)
        

# Fonction pour engager un technicien
def engager_technicien(technicien, joueur, engaged_frame, argent_label, engagement_buttons, button, progress_bar):
    progression = progress_bar.get()  # Entre 0.0 et 1.0
    salaire_proportionnel = int(technicien.salaire * progression)  # Arrondi au plus proche entier
    if joueur.argent >= salaire_proportionnel:
        joueur.argent -= salaire_proportionnel  # Déduire le salaire arrondi
        if technicien.engager(joueur):  # Engage le technicien
            joueur.trigger_ui_update()
            update_engaged_frame(engaged_frame, joueur, argent_label, engagement_buttons)
            button.configure(state="disabled")
    else:
        print(f"Pas assez d'argent pour engager {technicien.nom}.")



