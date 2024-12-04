from PIL import Image, ImageTk
import customtkinter as ctk
import os

# Configuration de la fenêtre principale
root = ctk.CTk()
root.geometry("1024x576")
root.title("Repair Rush")

# Variables globales
current_step = 0
tutorial_steps = [
    {"text": "Bienvenue dans Repair Rush !", "color": "yellow"},
    {"text": "Votre but est de gérer des machines et techniciens pour maximiser vos profits.", "color": "orange"},
    {"text": "Planifiez, entretenez et réparez vos machines avant qu'elles ne tombent en panne !", "color": "red"}
]
player_data = {"nom": "", "entreprise": "", "photo": ""}

# Vérifier sauvegarde
def verifier_sauvegarde():
    return os.path.exists("save/sauvegarde.pkl")

# Nouvelle partie
def nouvelle_partie():
    afficher_tutoriel()

# Charger partie
def charger_partie():
    if verifier_sauvegarde():
        os.system("start python Interface.py --charger")
        root.destroy()

# Quitter jeu
def quitter_jeu():
    root.destroy()

# Afficher tutoriel
def afficher_tutoriel():
    global current_step
    for widget in root.winfo_children():
        widget.destroy()

    if current_step < len(tutorial_steps):
        step = tutorial_steps[current_step]
        text_label = ctk.CTkLabel(root, text=step["text"], font=("Arial", 20, "bold"), fg_color=step["color"], corner_radius=10)
        text_label.pack(pady=50)
        next_button = ctk.CTkButton(root, text="→ Suivant", command=lambda: avancer_tutoriel(), width=150)
        next_button.pack(pady=20)
    else:
        demander_nom()

# Avancer tutoriel
def avancer_tutoriel():
    global current_step
    current_step += 1
    afficher_tutoriel()

# Demander nom
def demander_nom():
    for widget in root.winfo_children():
        widget.destroy()
    label = ctk.CTkLabel(root, text="Entrez votre nom :", font=("Arial", 20))
    label.pack(pady=20)
    entry = ctk.CTkEntry(root)
    entry.pack(pady=10)
    error_label = ctk.CTkLabel(root, text="", font=("Arial", 12), text_color="red")
    error_label.pack(pady=5)
    next_button = ctk.CTkButton(root, text="Suivant", command=lambda: valider_nom(entry, error_label), width=150)
    next_button.pack(pady=20)

def valider_nom(entry, error_label):
    nom_joueur = entry.get().strip()
    if len(nom_joueur) < 3:
        error_label.configure(text="Le nom doit contenir au moins 3 caractères !")
    else:
        player_data["nom"] = nom_joueur
        demander_entreprise()

# Demander entreprise
def demander_entreprise():
    for widget in root.winfo_children():
        widget.destroy()
    label = ctk.CTkLabel(root, text="Entrez le nom de votre entreprise :", font=("Arial", 20))
    label.pack(pady=20)
    entry = ctk.CTkEntry(root)
    entry.pack(pady=10)
    error_label = ctk.CTkLabel(root, text="", font=("Arial", 12), text_color="red")
    error_label.pack(pady=5)
    next_button = ctk.CTkButton(root, text="Suivant", command=lambda: valider_entreprise(entry, error_label), width=150)
    next_button.pack(pady=20)

def valider_entreprise(entry, error_label):
    nom_entreprise = entry.get().strip()
    if len(nom_entreprise) < 3:
        error_label.configure(text="Le nom doit contenir au moins 3 caractères !")
    else:
        player_data["entreprise"] = nom_entreprise
        choisir_photo_profil()

# Choisir photo profil
def choisir_photo_profil():
    for widget in root.winfo_children():
        widget.destroy()
    label = ctk.CTkLabel(root, text="Choisissez une photo de profil :", font=("Arial", 20))
    label.pack(pady=10)
    images = ["images/profil1.png", "images/profil2.png", "images/profil3.png", "images/profil4.png", "images/profil5.png", "images/profil6.png"]
    for img_path in images:
        img = ImageTk.PhotoImage(Image.open(img_path).resize((100, 100)))
        button = ctk.CTkButton(root, image=img, text="", command=lambda path=img_path: lancer_partie(path))
        button.image = img
        button.pack(side="left", padx=10)

# Lancer partie
def lancer_partie(photo_path):
    player_data["photo"] = photo_path
    os.system("start python Interface.py")
    root.destroy()

# Afficher écran options
def afficher_ecran_options():
    for widget in root.winfo_children():
        widget.destroy()
    bg_label = ctk.CTkLabel(root, image=bg_image_tk, text="")
    bg_label.place(relwidth=1, relheight=1)
    options_label = ctk.CTkLabel(root, text="Repair Rush", font=("Arial", 50, "bold"), fg_color="transparent")
    options_label.pack(pady=100)
    new_game_button = ctk.CTkButton(root, text="Nouvelle Partie", command=nouvelle_partie, font=("Arial", 20), width=300)
    new_game_button.pack(pady=20)
    load_game_button = ctk.CTkButton(
        root, text="Charger Partie", command=charger_partie, font=("Arial", 20), width=300,
        state="normal" if verifier_sauvegarde() else "disabled"
    )
    load_game_button.pack(pady=20)
    quit_button = ctk.CTkButton(root, text="Quitter", command=quitter_jeu, font=("Arial", 20), width=300)
    quit_button.pack(pady=20)

# Charger image de fond
background_image = Image.open("images/Backg.jpg").resize((1024, 576))
bg_image_tk = ImageTk.PhotoImage(background_image)
background_label = ctk.CTkLabel(root, image=bg_image_tk, text="")
background_label.place(relwidth=1, relheight=1)
title_label = ctk.CTkLabel(root, text="Repair Rush", font=("Arial", 50, "bold"))
title_label.pack(pady=100)
play_button = ctk.CTkButton(root, text="Jouer", command=afficher_ecran_options, font=("Arial", 20), width=300)
play_button.pack(pady=20)
quit_button = ctk.CTkButton(root, text="Quitter", command=quitter_jeu, font=("Arial", 20), width=300)
quit_button.pack(pady=20)
background_label.lower()

root.mainloop()
