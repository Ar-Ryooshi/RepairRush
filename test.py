from PIL import Image, ImageTk
import customtkinter as ctk
from modules.Machines2 import machines_possedees, InterfaceGraphique
from modules.Technician import technicians
from modules.Joueur import Joueur, creer_labels_profil
import pickle
import os
import tkinter.messagebox as messagebox

# Configuration de la fenêtre principale
root = ctk.CTk()
root.geometry("1024x576")
root.title("Repair Rush")

# Dossier et fichier de sauvegarde
SAVE_DIR = "save"
SAVE_FILE = os.path.join(SAVE_DIR, "sauvegarde.pkl")

# Variables globales
player_data = {"nom": "", "entreprise": "", "photo": ""}
images_cache = {}  # Pour éviter le garbage collection des images

# Vérifier la présence d'une sauvegarde
def verifier_sauvegarde():
    return os.path.exists(SAVE_FILE)

# Sauvegarder les données actuelles
def sauvegarder_donnees():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    data = {
        "player_data": player_data,
        "machines": machines_possedees,
        "technicians": technicians,
    }
    with open(SAVE_FILE, "wb") as f:
        pickle.dump(data, f)
    messagebox.showinfo("Sauvegarde", "Données sauvegardées avec succès.")

# Charger les données et lancer l'interface
def charger_partie():
    if verifier_sauvegarde():
        with open(SAVE_FILE, "rb") as f:
            data = pickle.load(f)
        global player_data, machines_possedees, technicians
        player_data.update(data["player_data"])
        machines_possedees.clear()
        machines_possedees.extend(data["machines"])
        technicians.clear()
        technicians.extend(data["technicians"])
        creer_interface_jeu()

# Fenêtre de dialogue (Notifications)

# Interface principale du jeu
def creer_interface_jeu():
    for widget in root.winfo_children():
        widget.destroy()

    frame = ctk.CTkFrame(root)
    frame.pack(fill="both", expand=True)

    joueur_instance = Joueur(player_data["nom"], player_data["entreprise"], player_data["photo"])
    creer_labels_profil(frame, joueur_instance, selected_currency="€")

    # Scrollable Frame pour machines

    # Machines Frame
    machines_frame = ctk.CTkFrame(frame, width=1380, height=300)
    machines_frame.place(x=10, y=800)
    InterfaceGraphique(machines_frame, machines_possedees)

    # Boutons d'action
    ctk.CTkButton(frame, text="Sauvegarder", command=sauvegarder_donnees).pack(side="bottom", pady=10)
    ctk.CTkButton(frame, text="Quitter", command=root.quit).pack(side="bottom", pady=10)

# Afficher l'écran d'accueil
def creer_ecran_accueil():
    for widget in root.winfo_children():
        widget.destroy()

    # Fond d'écran
    try:
        bg_image = Image.open("images/Backg.jpg").resize((1024, 576))
        bg_image_tk = ImageTk.PhotoImage(bg_image)
        background_label = ctk.CTkLabel(root, image=bg_image_tk, text="")
        background_label.image = bg_image_tk
        background_label.place(relwidth=1, relheight=1)
    except FileNotFoundError:
        print("Erreur : L'image de fond n'a pas été trouvée.")

    # Titre et boutons
    title_label = ctk.CTkLabel(root, text="Repair Rush", font=("Arial", 50, "bold"))
    title_label.pack(pady=100)
    play_button = ctk.CTkButton(root, text="Jouer", command=creer_ecran_choix_partie, font=("Arial", 20), width=300)
    play_button.pack(pady=20)
    quit_button = ctk.CTkButton(root, text="Quitter", command=root.quit, font=("Arial", 20), width=300)
    quit_button.pack(pady=20)

# Écran de choix entre nouvelle partie et chargement
def creer_ecran_choix_partie():
    for widget in root.winfo_children():
        widget.destroy()

    ctk.CTkLabel(root, text="Choisissez une option :", font=("Arial", 20)).pack(pady=20)
    new_game_button = ctk.CTkButton(root, text="Nouvelle Partie", command=demander_nom, font=("Arial", 20), width=300)
    new_game_button.pack(pady=10)
    load_game_button = ctk.CTkButton(
        root, text="Charger Partie", command=charger_partie, font=("Arial", 20), width=300,
        state="normal" if verifier_sauvegarde() else "disabled"
    )
    load_game_button.pack(pady=10)
    back_button = ctk.CTkButton(root, text="Retour", command=creer_ecran_accueil, font=("Arial", 20), width=300)
    back_button.pack(pady=10)

# Demander le nom du joueur
def demander_nom():
    for widget in root.winfo_children():
        widget.destroy()

    ctk.CTkLabel(root, text="Entrez votre nom :", font=("Arial", 20)).pack(pady=20)
    nom_entry = ctk.CTkEntry(root)
    nom_entry.pack(pady=10)

    ctk.CTkLabel(root, text="Nom de l'entreprise :", font=("Arial", 20)).pack(pady=20)
    entreprise_entry = ctk.CTkEntry(root)
    entreprise_entry.pack(pady=10)

    error_label = ctk.CTkLabel(root, text="", font=("Arial", 12), text_color="red")
    error_label.pack(pady=5)

    def valider_nom():
        nom = nom_entry.get().strip()
        entreprise = entreprise_entry.get().strip()
        if len(nom) < 3 or len(entreprise) < 3:
            error_label.configure(text="Nom et entreprise doivent avoir au moins 3 caractères.")
        else:
            player_data["nom"] = nom
            player_data["entreprise"] = entreprise
            choisir_photo_profil()

    ctk.CTkButton(root, text="Suivant", command=valider_nom, font=("Arial", 20)).pack(pady=20)

# Choisir la photo de profil
def choisir_photo_profil():
    for widget in root.winfo_children():
        widget.destroy()

    ctk.CTkLabel(root, text="Choisissez une photo de profil :", font=("Arial", 20)).pack(pady=10)
    images = [f"images/Profil{i}.png" for i in range(1, 7)]
    frame = ctk.CTkFrame(root)
    frame.pack(pady=20)

    for img_path in images:
        try:
            img = Image.open(img_path).resize((100, 100))
            img_tk = ImageTk.PhotoImage(img)
            images_cache[img_path] = img_tk
            btn = ctk.CTkButton(frame, image=img_tk, text="", command=lambda path=img_path: pre_lancer_jeu(path))
            btn.pack(side="left", padx=10)
        except FileNotFoundError:
            print(f"Erreur : L'image {img_path} est introuvable.")

# Préparer avant de lancer le jeu
def pre_lancer_jeu(photo_path):
    player_data["photo"] = photo_path
    creer_interface_jeu()

# Lancer l'écran d'accueil
creer_ecran_accueil()

# Boucle principale de l'application
root.mainloop()
