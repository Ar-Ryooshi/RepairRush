import customtkinter as ctk
from Interface import InterfacePrincipale

class MenuPrincipal:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Repair Rush - Menu Principal")
        self.root.geometry("800x600")
        self.create_ui()

    def create_ui(self):
        # Ajouter le titre
        title_label = ctk.CTkLabel(self.root, text="Repair Rush", font=("Arial", 24))
        title_label.pack(pady=50)

        # Ajouter les boutons
        start_button = ctk.CTkButton(self.root, text="Jouer", command=self.start_game)
        start_button.pack(pady=10)

        quit_button = ctk.CTkButton(self.root, text="Quitter", command=self.root.quit)
        quit_button.pack(pady=10)

    def start_game(self):
        # Détruire le menu principal et lancer l'interface principale
        self.root.destroy()
        InterfacePrincipale().run()

    def run(self):
        self.root.mainloop()
