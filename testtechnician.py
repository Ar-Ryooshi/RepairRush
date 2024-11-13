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

# Classe Joueur pour les tests
class Joueur:
    def __init__(self, nom, entreprise, argent=1000):
        self.nom = nom
        self.entreprise = entreprise
        self.argent = argent
        self.techniciens_possedes = []

# Interface graphique pour tester l'engagement et le licenciement des techniciens
if __name__ == "__main__":
    # Création du joueur pour tester l'interface
    joueur = Joueur(nom="Mr Boss", entreprise="Boss International", argent=10000)

    # Initialiser CustomTkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.geometry("1200x700")
    root.title("Techniciens Disponibles")

    # Affichage de l'argent du joueur
    argent_label = ctk.CTkLabel(root, text=f"Argent : {joueur.argent} €", font=("Arial", 14))
    argent_label.place(x=10, y=10)

    # Créer le ScrollableFrame pour les techniciens (semblable à l'interface rouge des machines)
    technicians_scrollable_frame = ctk.CTkScrollableFrame(root, width=1160, height=300, fg_color="#FF7F7F")
    technicians_scrollable_frame.place(x=10, y=50)

    # Frame des techniciens engagés (limité à 6)
    engaged_frame = ctk.CTkFrame(root, width=1160, height=200, fg_color="#333333")
    engaged_frame.place(x=10, y=400)

    # Dictionnaire pour stocker les boutons d'engagement des techniciens
    engagement_buttons = {}

    # Ajouter chaque technicien dans la ScrollableFrame
    def update_engaged_frame():
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
                    argent_label.configure(text=f"Argent : {joueur.argent} €")
                    update_engaged_frame()
                    # Réactiver le bouton d'engagement
                    engagement_buttons[tech].configure(state="normal")

            fire_button = ctk.CTkButton(tech_frame, text="Licencier", font=("Arial", 10), command=licencier_technicien)
            fire_button.pack(pady=5)

    # Ajouter chaque technicien dans la ScrollableFrame
    for idx, technician in enumerate(technicians):
        # Créer une sous-frame pour chaque technicien
        tech_frame = ctk.CTkFrame(technicians_scrollable_frame, width=180, height=250, fg_color="#333333", corner_radius=10)
        tech_frame.grid(row=idx, column=0, padx=10, pady=10)

        # Image du technicien
        image = Image.open(technician.image_path).resize((60, 60))
        tech_image = ImageTk.PhotoImage(image)
        image_label = ctk.CTkLabel(tech_frame, text="", image=tech_image)
        image_label.image = tech_image  # Garde une référence pour éviter que l'image ne soit supprimée
        image_label.pack(pady=5)

        # Nom du technicien
        name_label = ctk.CTkLabel(tech_frame, text=technician.nom, font=("Arial", 10))
        name_label.pack()

        # Spécialité et niveau
        specialite_label = ctk.CTkLabel(tech_frame, text=f"Spécialité: {technician.specialite}", font=("Arial", 10))
        specialite_label.pack()
        niveau_label = ctk.CTkLabel(tech_frame, text=f"Niveau: {technician.niveau}", font=("Arial", 10))
        niveau_label.pack()

        # Créer le bouton d'engagement
        action_button = ctk.CTkButton(tech_frame, text=f"Engager ({technician.salaire} €)")
        action_button.pack(pady=5)

        # Ajouter le bouton au dictionnaire pour pouvoir le réactiver plus tard
        engagement_buttons[technician] = action_button

        # Fonction pour engager le technicien
        def engager_technicien(tech=technician, button=action_button):
            if len(joueur.techniciens_possedes) < 6 and tech not in joueur.techniciens_possedes:  # Maximum de 6 techniciens et empêcher double engagement
                if tech.engager(joueur):
                    argent_label.configure(text=f"Argent : {joueur.argent} €")
                    update_engaged_frame()  # Mettre à jour la frame des techniciens engagés
                    button.configure(state="disabled")  # Désactiver le bouton après engagement
            else:
                print("Nombre maximum de techniciens atteint ou technicien déjà engagé!")

        # Assigner la fonction d'engagement au bouton
        action_button.configure(command=lambda t=technician, b=action_button: engager_technicien(t, b))

    # Lancer l'interface graphique
    root.mainloop()
