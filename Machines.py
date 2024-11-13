import customtkinter as ctk
from PIL import Image, ImageTk

# Classe Machine
class Machine:
    def __init__(self, nom, niveau_machine, type_machine, cout_achat, temps_entretien, revenu_par_periode, deplet_rate, image_path):
        self.nom = nom
        self.niveau_machine = niveau_machine
        self.type_machine = type_machine
        self.cout_achat = cout_achat
        self.temps_entretien = temps_entretien
        self.revenu_par_periode = revenu_par_periode
        self.deplet_rate = deplet_rate
        self.image_path = image_path
        self.etat = 100
        self.frame = None
        self.image = None  # Garder une référence de l'image

    def create_interface(self, root):
        """Crée l'interface visuelle pour chaque machine."""
        self.frame = ctk.CTkFrame(root, width=200, height=300, corner_radius=10)
        self.frame.pack(pady=10, padx=10, side="left")

        ctk.CTkLabel(self.frame, text=f"{self.nom} ({self.niveau_machine})", font=("Arial", 12)).pack(pady=5)

        # Conteneur pour l'image et la barre d'état
        image_et_barre_frame = ctk.CTkFrame(self.frame, width=150, height=150)
        image_et_barre_frame.pack()

        # Charger l'image et garder la référence
        self.image = ImageTk.PhotoImage(Image.open(self.image_path).resize((150, 150)))
        ctk.CTkLabel(image_et_barre_frame, image=self.image, text="").grid(row=0, column=0, padx=5)

        # Canvas pour la barre d'état verticale
        self.canvas = ctk.CTkCanvas(image_et_barre_frame, width=31, height=150, bg="black")
        self.canvas.grid(row=0, column=1, padx=5)

        # Bouton de réparation
        ctk.CTkButton(self.frame, text="Réparer", command=self.reparer).pack(pady=10)

        # Initialisation de la barre d'état
        self.update_barre()

    def degrader_etat(self):
        """Dégrade l'état de la machine."""
        if self.etat > 0:
            self.etat = max(0, self.etat - self.deplet_rate)
            self.update_barre()

    def degrader_etat_progressivement(self):
        """Appelle la fonction de dégradation de manière répétée."""
        if self.etat > 0:
            self.degrader_etat()
            self.frame.after(1000, self.degrader_etat_progressivement)

    def update_barre(self):
        """Met à jour la barre d'état verticale."""
        self.canvas.delete("barre")
        height = int(self.canvas.winfo_height() * (self.etat / 100))
        y_position = self.canvas.winfo_height() - height
        color = self.get_color_for_etat()
        if self.etat > 0:
            self.canvas.create_rectangle(1, y_position, 33, self.canvas.winfo_height(), fill=color, tags="barre")

    def get_color_for_etat(self):
        """Retourne la couleur appropriée en fonction de l'état actuel."""
        return "green" if self.etat >= 60 else "yellow" if 20 <= self.etat < 60 else "red"
    

    def reparer(self):
        """Répare la machine (remet l'état à 100%)."""
        self.etat = 100
        self.update_barre()
    def reparer type_machine

# Classe InterfaceGraphique
class InterfaceGraphique:
    def __init__(self, frame, machines_possedees):
        self.frame = frame
        self.frame.configure(corner_radius=0)
        self.machines = machines_possedees
        self.create_machines_interface()
        # Assure que la dégradation est démarrée après la création de l'interface
        self.start_degradation()

    def create_machines_interface(self):
        """Crée l'interface des machines."""
        for machine in self.machines:
            machine.create_interface(self.frame)
            machine.update_barre()  # S'assure que chaque barre est mise à jour à 100 %

    def update_interface(self, machines_possedees):
        """Met à jour l'interface en recréant les widgets des machines possédées."""
        # Supprime les widgets existants
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # Met à jour la liste des machines et recrée l'interface
        self.machines = machines_possedees
        self.create_machines_interface()
        
        # Assure que la dégradation est démarrée après la mise à jour de l'interface
        self.start_degradation()

    def start_degradation(self):
        """Lance la dégradation progressive des machines."""
        for machine in self.machines:
            machine.degrader_etat_progressivement()
            
def acheter_machine(machine, joueur, argent_value, scrollable_frame, interface_machines):
    """Permet d'acheter une machine si le joueur a suffisamment d'argent."""
    if machine in machines_disponibles and joueur.argent >= machine.cout_achat:
        joueur.argent -= machine.cout_achat

        # Ajouter la machine à la liste des machines possédées et la retirer des disponibles
        machines_possedees.append(machine)
        machines_disponibles.remove(machine)

        # Mise à jour de l'affichage de l'argent du joueur
        argent_value.configure(text=f"Argent : {joueur.argent} €")

        # Mise à jour de l'interface des machines possédées et disponibles
        interface_machines.update_interface(machines_possedees)

        print(f"Machine {machine.nom} achetée.")
    else:
        print("Pas assez d'argent pour acheter cette machine.")
# Liste des machines disponibles à l'achat
machines_disponibles = [
    Machine("Tour", "Maître", "Méchanique", 25000, 6, 3500, 0.165, "images/TourNiveau2.png"),
    Machine("CNC", "Artisan", "Électrique", 30000, 7, 4000, 0.135, "images/CNCNiveau1.png"),
    Machine("CNC", "Virtuose", "Électrique", 35000, 9, 4500, 0.12, "images/CNCNiveau2.png"),
    Machine("Bras Robot", "Rookie", "Informatique", 15000, 4, 2000, 0.1, "images/RobotNiveau1.png"),
    Machine("Bras Robot", "Légendaire", "Informatique", 23000, 5, 2500, 0.084, "images/RobotNiv2.png")
]

# Liste des machines possédées par le joueur au départ (une seule machine niveau 1)
machines_possedees = [
    Machine("Tour", "Apprentis", "Méchanique", 20000, 5, 3000, 0.21, "images/TourNiveau1.png")
]

# Exemple d'utilisation dans un autre fichier
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1380x800")

    # Création d'un cadre pour les machines dans l'interface principale
    machines_frame = ctk.CTkFrame(root, width=1380, height=300)
    machines_frame.place(x=0, y=250)

    # Initialiser l'interface des machines dans le cadre
    interface = InterfaceGraphique(machines_frame, machines_possedees)

    root.mainloop()
