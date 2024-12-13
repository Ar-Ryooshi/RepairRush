"""
Fichier principal pour Repair Rush.
Ce script gère l'initialisation de l'application, l'affichage de l'interface utilisateur et les interactions globales.
"""

# --- Importations des bibliothèques et modules nécessaires ---
import os
import json
import customtkinter as ctk
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk
<<<<<<< HEAD
from customtkinter import CTkImage
=======

from sound_manager import SoundManager
sound_manager = SoundManager()
>>>>>>> 543241cc8413c0f64dff1384314af4cc515ac71c

# Importation des modules spécifiques au jeu
from modules.Machines import machines_disponibles, machines_possedees, InterfaceGraphique, acheter_machine
from modules.Technician import technicians, engagement_buttons, update_engaged_frame, engager_technicien
from modules.Joueur import Joueur, creer_labels_profil
from modules.sound_manager import SoundManager

# --- Configuration initiale de l'application ---
# Initialisation du gestionnaire de son
sound_manager = SoundManager()

# Configuration globale de l'apparence
ctk.set_appearance_mode("dark")  # Mode sombre par défaut
ctk.set_default_color_theme("blue")  # Thème couleur par défaut

# Définition des variables globales
player_data = {}  # Stockage des données du joueur
selected_currency = "€" # Devise sélectionnée par défaut
SAVE_FILE = "save/Save.json" # Fichier de sauvegarde

# --- Initialisation de la fenêtre principale ---
root = ctk.CTk()
root.title("Repair Rush")
root.after(100, lambda: root.state('zoomed'))  # Agrandit la fenêtre après 100 ms

# --- Création des cadres pour gérer différentes sections de l'interface ---
frames = {}
for frame_name in ["menu_principal", "parametres", "accueil", "choix_partie", "nom_joueur", "photo_profil"]:
    frame = ctk.CTkFrame(root)
    frame.place(relwidth=1, relheight=1)  # Chaque frame occupe tout l'espace
    frames[frame_name] = frame

def creer_ecran_accueil():

    """
    Crée et affiche l'écran d'accueil du jeu.

    Cette fonction initialise l'écran d'accueil avec un fond d'écran, un titre,
    et des boutons pour commencer une partie ou quitter le jeu.

    Exceptions:
        FileNotFoundError: Si l'image de fond n'est pas trouvée, un message
        d'erreur est affiché dans la console.
    """
    frame = frames["accueil"]  # Récupère le cadre associé à l'accueil
    frame.lift()  # Amène ce cadre au premier plan
    for widget in frame.winfo_children():
        widget.destroy()  # Supprime tous les widgets existants pour éviter les doublons

    # Ajout d'un fond d'écran
    try:
        bg_image = CTkImage(
            light_image=Image.open("images/Backg.jpg"),  # Charge l'image de fond
            size=(root.winfo_screenwidth(), root.winfo_screenheight())  # Adapte la taille au plein écran
        )
        background_label = ctk.CTkLabel(frame, image=bg_image, text="")  # Crée un label avec l'image
        background_label.place(relwidth=1, relheight=1)  # Étire l'image pour couvrir tout le cadre
    except FileNotFoundError:
        print("Erreur : L'image de fond n'a pas été trouvée.")  # Log l'erreur si le fichier est introuvable

    # Titre du jeu
    title_label = ctk.CTkLabel(
        frame, 
        text="Repair Rush", 
        font=("Arial", 50, "bold")  # Style du titre
    )
    title_label.pack(pady=100)  # Ajoute un espace vertical autour du titre

    # Bouton pour commencer une partie
    play_button = ctk.CTkButton(
        frame, 
        text="Jouer", 
        command=creer_ecran_choix_partie,  # Redirige vers l'écran de choix de partie
        font=("Arial", 20), 
        width=300
    )
    play_button.pack(pady=20)  # Ajoute un espace vertical autour du bouton

    # Bouton pour quitter le jeu
    quit_button = ctk.CTkButton(
        frame, 
        text="Quitter", 
        command=root.quit,  # Ferme l'application
        font=("Arial", 20), 
        width=300
    )
    quit_button.pack(pady=20)  # Ajoute un espace vertical autour du bouton

def creer_ecran_choix_partie():

    """
    Crée et affiche l'écran de sélection de partie.

    Cet écran permet au joueur de choisir entre démarrer une nouvelle partie,
    charger une partie sauvegardée ou revenir à l'écran d'accueil.

    Exceptions:
        FileNotFoundError: Si l'image de fond est introuvable, affiche un message d'erreur dans la console.
    """
    frame = frames["choix_partie"]  # Récupère le cadre associé à l'écran de choix de partie
    frame.lift()  # Amène ce cadre au premier plan

    # Supprime les widgets existants dans le cadre
    for widget in frame.winfo_children():
        widget.destroy()

    # Ajout d'un fond d'écran
    try:
        bg_image = CTkImage(
            light_image=Image.open("images/Backg.jpg"),  # Charge l'image de fond
            size=(root.winfo_screenwidth(), root.winfo_screenheight())  # Adapte à la taille de l'écran
        )
        background_label = ctk.CTkLabel(frame, image=bg_image, text="")
        background_label.place(relwidth=1, relheight=1)  # Étend l'image sur tout le cadre
    except FileNotFoundError:
        print("Erreur : L'image de fond n'a pas été trouvée.")  # Log l'erreur

    # Titre
    title_label = ctk.CTkLabel(
        frame,
        text="Repair Rush",
        font=("Arial", 50, "bold")  # Police stylisée pour le titre
    )
    title_label.place(relx=0.5, y=100, anchor="center")  # Centre le titre horizontalement

    # Bouton pour une nouvelle partie
    new_game_button = ctk.CTkButton(
        frame,
        text="Nouvelle Partie",
        command=demander_nom,  # Redirige vers la fonction pour demander un nom
        font=("Arial", 20),
        width=300
    )
    new_game_button.place(relx=0.5, y=200, anchor="center")  # Centre le bouton sous le titre

    # Bouton pour charger une partie
    load_game_button = ctk.CTkButton(
        frame,
        text="Charger Partie",
        command=charger_partie,  # Charge une partie sauvegardée
        font=("Arial", 20),
        width=300,
        state="normal" if verifier_sauvegarde() else "disabled"  # Désactive si aucune sauvegarde n'existe
    )
    load_game_button.place(relx=0.5, y=250, anchor="center")  # Centre le bouton sous celui de nouvelle partie

    # Bouton pour revenir à l'écran d'accueil
    back_button = ctk.CTkButton(
        frame,
        text="Retour",
        command=creer_ecran_accueil,  # Redirige vers l'écran d'accueil
        font=("Arial", 20),
        width=300
    )
    back_button.place(relx=0.5, y=300, anchor="center")  # Centre le bouton sous celui de chargement

def demander_nom():
    """
    Affiche l'écran pour saisir le nom du joueur et le nom de l'entreprise.

    Cette fonction demande au joueur de saisir son nom et le nom de son entreprise,
    puis valide les entrées avant de passer à l'étape suivante.

    Exceptions:
        - Affiche un message d'erreur si les noms fournis ne respectent pas les critères.
    """
    frame = frames["nom_joueur"]  # Accède au cadre dédié à cette étape
    frame.lift()  # Amène ce cadre au premier plan

    # Nettoyage des widgets existants
    for widget in frame.winfo_children():
        widget.destroy()

    # Champ pour le nom du joueur
    ctk.CTkLabel(frame, text="Entrez votre nom :", font=("Arial", 20)).pack(pady=20)
    nom_entry = ctk.CTkEntry(frame)
    nom_entry.pack(pady=10)

    # Champ pour le nom de l'entreprise
    ctk.CTkLabel(frame, text="Nom de l'entreprise :", font=("Arial", 20)).pack(pady=20)
    entreprise_entry = ctk.CTkEntry(frame)
    entreprise_entry.pack(pady=10)

    # Zone pour afficher les erreurs
    error_label = ctk.CTkLabel(frame, text="", font=("Arial", 12), text_color="red")
    error_label.pack(pady=5)

    # Fonction de validation des entrées
    def valider_nom():
        """
        Valide les noms saisis et passe à l'écran de choix de la photo de profil si valides.

        Critères:
        - Les noms doivent contenir au moins 3 caractères.
        """
        nom = nom_entry.get().strip()  # Supprime les espaces inutiles
        entreprise = entreprise_entry.get().strip()
        if len(nom) < 3 or len(entreprise) < 3:  # Vérifie la longueur minimale
            error_label.configure(text="Nom et entreprise doivent avoir au moins 3 caractères.")
        else:
            # Enregistre les données du joueur et passe à l'étape suivante
            player_data["nom"] = nom
            player_data["entreprise"] = entreprise
            choisir_photo_profil()

    # Bouton pour valider et passer à l'étape suivante
    ctk.CTkButton(frame,text="Suivant",command=valider_nom,font=("Arial", 20)).pack(pady=20)

def choisir_photo_profil():
    """
    Affiche l'écran pour choisir une photo de profil.

    Permet au joueur de sélectionner une image parmi une liste d'options
    prédéfinies. Une fois la photo choisie, le joueur est redirigé vers le
    tutoriel avec son profil créé.

    Exceptions:
        - Affiche un message d'erreur si une image n'est pas trouvée.
    """
    frame = frames["photo_profil"]  # Cadre dédié à la sélection de la photo
    frame.lift()  # Amène ce cadre au premier plan

    # Nettoyage des widgets existants
    for widget in frame.winfo_children():
        widget.destroy()

    # Titre
    ctk.CTkLabel(frame, text="Choisissez une photo de profil :", font=("Arial", 20)).pack(pady=10)

    # Liste des chemins vers les images de profil disponibles
    images = [f"images/Profil{i}.png" for i in range(1, 7)]

    # Cadre pour afficher les images
    img_frame = ctk.CTkFrame(frame)
    img_frame.pack(pady=20)

    def selectionner_photo(path):
        """
        Enregistre la photo sélectionnée et crée le profil du joueur.

        Args:
            path (str): Chemin de l'image sélectionnée.
        """
        player_data["photo"] = path
        joueur = Joueur(
            nom=player_data["nom"],
            entreprise=player_data["entreprise"],
            photo=path
        )
        print(f"Profil créé : {joueur.nom} ({joueur.entreprise}), photo sélectionnée : {path}")
        lancer_tutoriel(joueur)  # Passe à l'étape suivante (tutoriel)

    # Génère les boutons d'images
    for img_path in images:
        try:
            # Charge l'image et crée un bouton associé
            img = CTkImage(light_image=Image.open(img_path), size=(100, 100))
            btn = ctk.CTkButton(
                img_frame,
                image=img,
                text="",
                command=lambda path=img_path: selectionner_photo(path)
            )
            btn.pack(side="left", padx=10)
        except FileNotFoundError:
            # Gestion des erreurs pour les images manquantes
            print(f"Erreur : L'image {img_path} est introuvable.")

def lancer_tutoriel(joueur):
    """
    Affiche le tutoriel pour guider le joueur après la création de son profil.

    Args:
        joueur (Joueur): L'instance du joueur contenant ses informations (nom, entreprise, etc.).
    """
    # Création du cadre principal pour le tutoriel
    tutoriel_frame = ctk.CTkFrame(root, width=1500, height=900, fg_color="#E8C36A")
    tutoriel_frame.place(relwidth=1, relheight=1)

    # Titre de bienvenue
    titre_label = ctk.CTkLabel(
        tutoriel_frame,
        text=f"Bienvenue, {joueur.nom} !",
        font=("Arial", 40, "bold"),
        text_color="black",
    )
    titre_label.pack(pady=20)

    # Introduction du tutoriel
    intro_label = ctk.CTkLabel(
        tutoriel_frame,
        text=(
            f"Vous êtes maintenant à la tête de l'atelier '{joueur.entreprise}'. "
            "Votre objectif est clair : maintenir vos machines en parfait état, "
            "gérer vos techniciens, et maximiser vos profits pour faire prospérer votre entreprise !"
        ),
        font=("Arial", 20),
        wraplength=1200,
        justify="center",
        text_color="black",
    )
    intro_label.pack(pady=20)

    # Liste des étapes du tutoriel
    étapes = [
        "1. Gardez vos machines dans le vert pour un rendement optimal.",
        "2. Engagez des techniciens et attribuez-les aux machines en panne.",
        "3. Faites attention à vos finances : ne dépensez pas plus que vous gagnez !",
        "4. Investissez dans des machines modernes pour maximiser vos profits.",
        "5. Chaque journée dure 2 minutes en temps réel. Planifiez rapidement !",
    ]

    étapes_label = ctk.CTkLabel(
        tutoriel_frame,
        text="\n".join(étapes),
        font=("Arial", 18),
        justify="left",
        text_color="black",
    )
    étapes_label.pack(pady=20)

    # Bouton pour lancer le jeu
    def lancer_jeu():
        """
        Détruit le tutoriel et charge l'interface principale du jeu.
        """
        tutoriel_frame.destroy()
        creer_interface_jeu()

    bouton_continuer = ctk.CTkButton(
        tutoriel_frame,
        text="Commencer votre aventure !",
        command=lancer_jeu,
        font=("Arial", 20, "bold"),
    )
    bouton_continuer.pack(pady=30)

    print(f"Tutoriel lancé pour le joueur {joueur.nom} ({joueur.entreprise}).")

def creer_interface_jeu():
    #region Créer les différents frames
    """Crée l'interface principale du jeu et affiche le menu principal."""
    # Ajoute les frames du jeu au dictionnaire global
    sound_manager.playmusic("sounds/mainost.mp3", loop=True)
    global joueur, machines_possedees, technicians
    joueur = Joueur(
        nom=player_data["nom"],
        entreprise=player_data["entreprise"],
        photo=player_data["photo"]
    )
    frames["menu_principal"] = ctk.CTkFrame(root, width=1500, height=900)
    frames["parametres"] = ctk.CTkFrame(root, width=1500, height=900, fg_color="#E8C36A")
    frames["partie"] = ctk.CTkFrame(root, width=1500, height=900, fg_color="#E8C36A")
    frames["son"] = ctk.CTkFrame(root, width=1500, height=900, fg_color="#E8C36A")
    frames["profil"] = ctk.CTkFrame(root, width=1500, height=900, fg_color="#E8C36A")
    
    # Ajouter le cadre des machines
    machines_frame = ctk.CTkFrame(frames["menu_principal"], width=1380, height=300)
    machines_frame.place(x=10, y=760)

    # Ajouter le cadre pour les techniciens engagés
    engaged_frame = ctk.CTkFrame(frames["menu_principal"], width=1160, height=200, fg_color="#333333")
    engaged_frame.place(x=10, y=500)

    # Ajouter les frames au layout principal
    for frame in frames.values():
        frame.place(relwidth=1, relheight=1)

    # Fonction pour afficher un frame et masquer les autres
    def afficher_frame(frame):
        frame.lift()  # Amène le frame au premier plan

    # Afficher le menu principal directement
    afficher_frame(frames["menu_principal"])


    #region Currency
    # Monnaie sélectionnée par défaut (euros)

    selected_currency = "€"

    def update_scrollable_frame():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        afficher_machines()  # Ou la méthode qui recrée l'affichage



    # Fonction pour mettre à jour la monnaie sélectionnée
    def update_labels_profil():
        labels_profil["argent"].configure(text=f"{int(joueur.argent)} {selected_currency}")
        labels_profil["revenu"].configure(text=f"{joueur.revenu} {selected_currency}")
        labels_profil["couts_fixes"].configure(text=f"{joueur.couts_fixes} {selected_currency}")
        labels_profil["solde_net"].configure(text=f"{joueur.solde_net} {selected_currency}")




    def update_currency(choice):
        global selected_currency
        selected_currency = choice
        afficher_machines() # Mettre à jour l'affichage des machines avec la nouvelle monnaie
        update_labels_profil()  # Mettre à jour les labels du profil
    #endregion






    # Créer les labels du profil et récupérer les références nécessaires
    labels_profil = creer_labels_profil(frames["menu_principal"], joueur, selected_currency)
    joueur.trigger_ui_update()




    progress_bar = ctk.CTkProgressBar(frames["menu_principal"], width=600, height=30, progress_color='green')
    progress_bar.place(x=10, y=350)

    #endregion



    # Barre de progression
    def update_progress_bar(i=0):
        if i == 0:
            joueur.payer_salaires()  # Payer les salaires au début du jour
        if i <= 3000:
            progress_bar.set(i / 3000)
            root.after(10, update_progress_bar, i + 1)
        else:
            progress_bar.set(0)
            root.after(10, update_progress_bar, 0)
            joueur.incrementer_jour()
            joueur.ajouter_revenu()
            Endgame()
            
            sound_manager.playsound("sounds/ca-ching.mp3")  # Jouer le son de gain d'argent

    def Endgame():
        if joueur.jour_actuel == 20:
            messagebox.showinfo(f"Félicitations", 
                                f"Vous avez fait tenir {joueur.entreprise} pendant 20 jours ! Vous êtes en bonne voie pour devenir un magnat de la réparation !\n "
                                f"Vous avez empoché {joueur.argent} {selected_currency}.")
            root.destroy()
            exit()  
        if joueur.argent < joueur.couts_fixes:
            messagebox.showerror(
                "Game Over", 
                f"Vous n'avez plus assez d'argent pour payer vos techniciens.\nVotre entreprise {joueur.entreprise} a fait faillite !"
            )
            root.destroy()
            exit()
        if all(machine.etat == 0 for machine in joueur.machines_possedees):
            messagebox.showerror(
                "Game Over", 
                f"Toutes vos machines sont hors d'état de marche.\nVotre entreprise {joueur.entreprise} doit fermer ses portes !"
            )
            root.destroy()
            exit()






    def start_progress():
        update_progress_bar()




    scrollable_frame = ctk.CTkScrollableFrame(frames["menu_principal"], width=660, height=300, fg_color="#FF7F7F")
    scrollable_frame.place(x=660, y=100)



    # Fonction pour afficher les machines
    def afficher_machines():
        global menu_ouvert
        menu_ouvert = 'machines'
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        # Ajouter les titres des colonnes
        col_titles = ["","Nom", "Niveau", "Type", "Revenu par période"]
        for idx, title in enumerate(col_titles):
            title_label = ctk.CTkLabel(scrollable_frame, text=title, text_color="white", font=("Arial", 12, "bold"))
            title_label.grid(row=0, column=idx, padx=10, pady=5, sticky="w")

        # Afficher les machines possédées
        for i, machine in enumerate(machines_possedees):
        # Ligne de séparation pour les machines possédées
            separator = ctk.CTkLabel(scrollable_frame, text="".ljust(150, "-"), text_color="gray")
            separator.grid(row=i * 2 + 1, column=0, columnspan=6, padx=5, pady=5, sticky="ew")

            # Chargement de l'image de la machine
            image = Image.open(machine.image_path).resize((80, 80))
            machine_image = ImageTk.PhotoImage(image)
            image_label = ctk.CTkLabel(scrollable_frame, image=machine_image, text="")
            image_label.image = machine_image
            image_label.grid(row=i * 2 + 2, column=0, padx=10, pady=5)

            # Informations sur la machine possédée
            nom_label = ctk.CTkLabel(scrollable_frame, text=f"{machine.nom}")
            nom_label.grid(row=i * 2 + 2, column=1, padx=10, pady=5, sticky="w")

            niveau_label = ctk.CTkLabel(scrollable_frame, text=f"{machine.niveau_machine}")
            niveau_label.grid(row=i * 2 + 2, column=2, padx=10, pady=5, sticky="w")

            type_machine_label = ctk.CTkLabel(scrollable_frame, text=f"{machine.type_machine}")
            type_machine_label.grid(row=i * 2 + 2, column=3, padx=10, pady=5, sticky="w")

            revenu_label = ctk.CTkLabel(scrollable_frame, text=f"{machine.revenu_par_periode} {selected_currency}")
            revenu_label.grid(row=i * 2 + 2, column=4, padx=10, pady=5, sticky="nsew")

            # Cadre indiquant que la machine est possédée
            possede_label = ctk.CTkLabel(scrollable_frame, text="Possédé", width=150, fg_color="#3d3d3d", corner_radius=8)
            possede_label.grid(row=i * 2 + 2, column=5, padx=10, pady=5)

    # Afficher les machines disponibles à l'achat
        row_offset = len(machines_possedees) * 2
        for j, machine in enumerate(machines_disponibles):
            # Ligne de séparation pour les machines disponibles
            separator = ctk.CTkLabel(scrollable_frame, text="".ljust(150, "-"), text_color="gray")
            separator.grid(row=row_offset + j * 2 + 1, column=0, columnspan=6, padx=5, pady=5, sticky="ew")

            # Chargement de l'image de la machine
            image = Image.open(machine.image_path).resize((80, 80))
            machine_image = ImageTk.PhotoImage(image)
            image_label = ctk.CTkLabel(scrollable_frame, image=machine_image, text="")
            image_label.image = machine_image
            image_label.grid(row=row_offset + j * 2 + 2, column=0, padx=10, pady=5)

            # Informations sur la machine disponible
            nom_label = ctk.CTkLabel(scrollable_frame, text=f"{machine.nom}")
            nom_label.grid(row=row_offset + j * 2 + 2, column=1, padx=10, pady=5, sticky="w")

            niveau_label = ctk.CTkLabel(scrollable_frame, text=f"{machine.niveau_machine}")
            niveau_label.grid(row=row_offset + j * 2 + 2, column=2, padx=10, pady=5, sticky="w")

            type_machine_label = ctk.CTkLabel(scrollable_frame, text=f"{machine.type_machine}")
            type_machine_label.grid(row=row_offset + j * 2 + 2, column=3, padx=10, pady=5, sticky="w")

            revenu_label = ctk.CTkLabel(scrollable_frame, text=f"{machine.revenu_par_periode} {selected_currency}")
            revenu_label.grid(row=row_offset + j * 2 + 2, column=4, padx=10, pady=5, sticky="nsew")

            # Bouton pour acheter la machine
            
            buy_button = ctk.CTkButton(
            scrollable_frame,
            text=f"{machine.cout_achat} {selected_currency}",
            width=150,
            state="disabled" if any(m.en_reparation_flag for m in joueur.machines_possedees) else "normal",  # Vérification des réparations
            command=lambda mach=machine: acheter_machine(mach, joueur, interface_machines, update_scrollable_frame)
            )
            buy_button.grid(row=row_offset + j * 2 + 2, column=5, padx=10, pady=5)
    
                

    # Fonction pour afficher les techniciens
    def afficher_techniciens():
        global menu_ouvert
        menu_ouvert = 'techniciens'
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        # Ajouter les titres des colonnes
        col_titles = ["Nom", "Spécialité", "Niveau", "Salaire", ""]
        for idx, title in enumerate(col_titles):
            title_label = ctk.CTkLabel(scrollable_frame, text=title, text_color="white", font=("Arial", 12, "bold"))
            title_label.grid(row=0, column=idx + 1, padx=10, pady=5, sticky="w")

        for i, technician in enumerate(technicians):
            # Ligne de séparation
            separator = ctk.CTkLabel(scrollable_frame, text="".ljust(150, "-"), text_color="gray")
            separator.grid(row=i * 2 + 1, column=0, columnspan=6, padx=5, pady=5, sticky="ew")

            # Chargement de l'image du technicien
            image = Image.open(technician.image_path).resize((80, 80))
            technician_image = ImageTk.PhotoImage(image)
            image_label = ctk.CTkLabel(scrollable_frame, image=technician_image, text="")
            image_label.image = technician_image  # Empêcher l'image d'être supprimée par le garbage collector
            image_label.grid(row=i * 2 + 2, column=0, padx=10, pady=5)

            # Informations sur le technicien
            technician_label = ctk.CTkLabel(scrollable_frame, text=f"{technician.nom}")
            technician_label.grid(row=i * 2 + 2, column=1, padx=10, pady=5, sticky="w")

            speciality_label = ctk.CTkLabel(scrollable_frame, text=f"{technician.specialite}")
            speciality_label.grid(row=i * 2 + 2, column=2, padx=10, pady=5, sticky="w")

            niveau_label = ctk.CTkLabel(scrollable_frame, text=f"{technician.niveau}")
            niveau_label.grid(row=i * 2 + 2, column=3, padx=10, pady=5, sticky="w")

            salaire_label = ctk.CTkLabel(scrollable_frame, text=f"{technician.salaire} {selected_currency}")
            salaire_label.grid(row=i * 2 + 2, column=4, padx=10, pady=5, sticky="w")

            # Bouton pour engager le technicien
            hire_button = ctk.CTkButton(scrollable_frame, text=f"Engager", width=150)
            
            # Ajouter le bouton au dictionnaire pour pouvoir le réactiver plus tard
            engagement_buttons[technician] = hire_button

            # Vérifier si le technicien est déjà engagé
            if technician in joueur.techniciens_possedes:
                hire_button.configure(state="disabled")

            # Fonction pour engager le technicien
            hire_button.configure(command=lambda t=technician, b=hire_button: engager_technicien(t, joueur, engaged_frame, labels_profil["argent"], engagement_buttons, b))
            hire_button.grid(row=i * 2 + 2, column=5, padx=10, pady=5)

    #region --- NOTIFICATIONS ---
    # Notifications pour les actions du joueur
    from modules.NotificationsManager import NotificationsManager, set_global_notifications_manager

    notifications_manager = NotificationsManager(frames["menu_principal"], x=1400, y=50, width=450, height=500)
    set_global_notifications_manager(notifications_manager)

    notifications_manager.ajouter_notification("Bienvenue dans le jeu !")
    #endregion
    #region Boutons tech et machines
    # Bouton "Machines"
    btn_machine = ctk.CTkButton(frames["menu_principal"], text="Machines", width=140, height=50, command=afficher_machines)
    btn_machine.place(x=650, y=20)

    # Bouton "Techniciens"
    btn_technicien = ctk.CTkButton(frames["menu_principal"], text="Techniciens", width=140, height=50, command=afficher_techniciens)
    btn_technicien.place(x=800, y=20)

    # Bouton "Paramètres" avec un symbole d'engrenage
    btn_parametres = ctk.CTkButton(
        frames["menu_principal"], 
        text="⚙️",  # Utilisation d'un emoji pour le symbole d'engrenage
        width=50, 
        height=50, 
        command=lambda: afficher_frame(frames["parametres"])  # Accès à la page des paramètres
    )
    btn_parametres.place(x=960, y=20)  # Position à côté des autres boutons


    #endregion
  



    # --- Section Profil ---
    profile_label = ctk.CTkLabel(frames["parametres"], text="Profil", font=("Arial", 20, "bold"), text_color="black")
    profile_label.place(x=50, y=20)

    name_label = ctk.CTkLabel(frames["parametres"], text="Nom:", text_color="black")
    name_label.place(x=50, y=60)

    name_entry = ctk.CTkEntry(frames["parametres"])
    name_entry.insert(0, joueur.nom)  # Pré-remplit l'entrée avec le nom actuel
    name_entry.place(x=150, y=60)

    # Bouton pour confirmer le changement de nom
    def confirmer_nom():
        nouveau_nom = name_entry.get().strip()
        if len(nouveau_nom) >= 3:  # Vérifie que le nom a au moins 3 caractères
            joueur.nom = nouveau_nom
            messagebox.showinfo("Confirmation", f"Nom changé avec succès en : {nouveau_nom}")
            print(f"Le nom du joueur a été changé en : {joueur.nom}")
            rafraichir_interface_principale()

            
        else:
            messagebox.showerror("Erreur", "Le nom doit contenir au moins 3 caractères.")
    def rafraichir_interface_principale():
        labels_profil["nom"].configure(text=f"{joueur.nom}")

    confirm_button = ctk.CTkButton(
        frames["parametres"],
        text="Confirmer",
        command=confirmer_nom
    )
    confirm_button.place(x=350, y=60)

    company_label = ctk.CTkLabel(frames["parametres"], text="Entreprise:", text_color="black")
    company_label.place(x=50, y=100)

    company_entry = ctk.CTkEntry(frames["parametres"])
    company_entry.insert(0, joueur.entreprise)  # Pré-remplit avec le nom actuel
    company_entry.place(x=150, y=100)

    def confirmer_entreprise():
        nouveau_nom_entreprise = company_entry.get().strip()
        if len(nouveau_nom_entreprise) >= 3:
            if joueur.argent >= 100:
                joueur.argent -= 100  # Retirer 100 balles pour les frais administratifs
                joueur.entreprise = nouveau_nom_entreprise
                labels_profil["argent"].configure(text=f"{joueur.argent} €")  # Met à jour l'affichage de l'argent
                messagebox.showinfo(
                    "Confirmation",
                    f"Le nom de votre entreprise a été changé en : {nouveau_nom_entreprise} pour 100 €"
                )
                print(f"Le nom de l'entreprise a été changé en : {joueur.entreprise}")
            else:
                messagebox.showerror("Erreur", "Pas assez d'argent pour changer le nom de l'entreprise.")
        else:
            messagebox.showerror("Erreur", "Le nom de l'entreprise doit contenir au moins 3 caractères.")

    confirm_company_button = ctk.CTkButton(
        frames["parametres"],
        text="Changer (100 €)",
        command=confirmer_entreprise
    )
    confirm_company_button.place(x=350, y=100)

    save_button = ctk.CTkButton(frames["parametres"], text="Sauvegarder",command=sauvegarder_partie)
    save_button.place(x=50, y=200)

    sound_label = ctk.CTkLabel(frames["parametres"], text="Son", font=("Arial", 20, "bold"), text_color="black")
    sound_label.place(x=50, y=280)

    # Définit un volume par défaut (50%)
    DEFAULT_VOLUME = 50

    # Fonction pour mettre à jour le volume
    def update_volume(value):
        """Mets à jour le volume et synchronise l'état de la case à cocher."""
        sound_manager.setvolume(value)
        if value > 0:
            music_enabled_var.set(True)  # Active la musique si le volume est supérieur à 0
        else:
            music_enabled_var.set(False)  # Désactive la musique si le volume est à 0

    # Slider pour le volume
    sound_slider = ctk.CTkSlider(
        frames["parametres"],
        from_=0,  # Volume minimum
        to=100,  # Volume maximum
        command=lambda value: update_volume(int(value))  # Appelle une fonction pour gérer le volume
    )
    sound_slider.place(x=150, y=320)

    music_enabled_var = ctk.BooleanVar(value=True)  # Musique activée par défaut

    # Fonction pour activer/désactiver la musique
    def toggle_music():
        """Active ou désactive la musique selon l'état de la case à cocher."""
        if music_enabled_var.get():  # Si la musique est activée
            current_volume = int(sound_slider.get())  # Récupère la position du slider
            sound_manager.setvolume(current_volume)  # Utilise le volume du slider
            sound_manager.resumemusic()  # Reprend la musique si elle était en pause
            sound_slider.configure(state="normal")  # Réactive le slider
        else:  # Si la musique est désactivée
            sound_manager.setvolume(0)  # Coupe le son
            sound_slider.configure(state="disabled")  # Désactive le slider

    # Ajout de la case à cocher pour la musique
    music_toggle_checkbox = ctk.CTkCheckBox(
        frames["parametres"],
        text="🎵 Activer la musique",
        variable=music_enabled_var,
        onvalue=True,
        offvalue=False,
        command=toggle_music  # Appelle toggle_music lorsqu'elle est cliquée
    )
    music_toggle_checkbox.place(x=150, y=420)

    # Initialiser le slider et la case à cocher
    sound_slider.set(DEFAULT_VOLUME)  # Définit le slider à la moitié (50%)
    sound_manager.setvolume(DEFAULT_VOLUME)  # Définit également le volume du sound manager  



    # --- Bouton Retour ---
    back_button = ctk.CTkButton(frames["parametres"], text="← Menu Principal", width=200, command=lambda: afficher_frame(frames["menu_principal"]))
    back_button.place(x=800, y=20)



    #region --- INTERFACE DES MACHINES ---
    interface_machines = InterfaceGraphique(machines_frame, machines_possedees)
    #endregion
    # Lancer la barre de progression
    start_progress()

    # Afficher les machines au démarrage
    afficher_machines()


    try:
        with open(SAVE_FILE, "rb"):
            return True
    except FileNotFoundError:
        return False

# Vérifier si une sauvegarde existe
def verifier_sauvegarde():
    """
    Vérifie si le fichier de sauvegarde existe.

    Returns:
        bool: True si le fichier de sauvegarde existe, False sinon.
    """
    try:
        with open(SAVE_FILE, "rb"):
            return True
    except FileNotFoundError:
        return False


# Sauvegarder les données du joueur et de l'état du jeu
def sauvegarder_partie():
    """
    Sauvegarde l'état actuel de la partie dans un fichier JSON.

    Cette fonction enregistre les informations du joueur, les machines possédées,
    les techniciens engagés, ainsi que d'autres données importantes.

    Raises:
        Exception: En cas d'erreur pendant la sauvegarde, une exception est levée et affichée.
    """
    try:
        # Vérifie et crée le dossier de sauvegarde si nécessaire
        save_dir = os.path.dirname(SAVE_FILE)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Prépare les données des machines possédées
        possessed_machines = [
            {"nom": machine.nom, "niveau": machine.niveau_machine}
            for machine in joueur.machines_possedees
        ]

        # Prépare les données des techniciens engagés
        possessed_technicians = [technician.nom for technician in joueur.techniciens_possedes]

        # Structure des données à sauvegarder
        data = {
            "player_data": player_data,  # Données générales du joueur
            "machines_possedees": possessed_machines,  # Machines possédées avec leurs niveaux
            "techniciens_possedes": possessed_technicians,  # Techniciens engagés
            "joueur": {  # Informations détaillées sur le joueur
                "nom": joueur.nom,
                "entreprise": joueur.entreprise,
                "photo": joueur.photo,
                "argent": joueur.argent,
                "jour_actuel": joueur.jour_actuel,
            },
        }

        # Sauvegarde des données dans un fichier JSON
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=4)

        print("Données sauvegardées avec succès en JSON.")
        messagebox.showinfo("Sauvegarde", "Données sauvegardées avec succès.")
    except Exception as e:
        # Gestion des erreurs pendant la sauvegarde
        print(f"Erreur lors de la sauvegarde des données : {e}")
        messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde des données : {e}")

# Dictionnaire pour stocker les labels du profil
labels_profil = {
    "argent": None
}

def charger_partie():
    """
    Charge une partie sauvegardée depuis un fichier JSON.

    Cette fonction restaure l'état du joueur, les machines possédées,
    les techniciens engagés et réinitialise les interfaces associées.

    Raises:
        Exception: En cas de problème lors du chargement des données.
    """
    try:
        # Charger les données depuis le fichier de sauvegarde
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)

        # Rendre accessibles les variables globales nécessaires
        global player_data, joueur, machines_possedees, technicians, frames, labels_profil, engagement_buttons

        # Restaurer les données du joueur
        player_data = data["player_data"]
        joueur = Joueur(
            nom=data["joueur"]["nom"],
            entreprise=data["joueur"]["entreprise"],
            photo=data["joueur"]["photo"],
            argent=data["joueur"]["argent"]
        )

        # Initialiser le frame pour afficher les machines
        machines_frame = ctk.CTkFrame(frames["menu_principal"], width=1380, height=300)
        machines_frame.place(x=10, y=760)

        # Restaurer les machines possédées par le joueur
        for m in data["machines_possedees"]:
            machine = next(
                (mach for mach in machines_disponibles if mach.nom == m["nom"] and mach.niveau_machine == m["niveau"]),
                None
            )
            if machine:
                joueur.acheter_machine(machine)
            else:
                print(f"Machine non trouvée : {m['nom']} ({m['niveau']})")

        # Mettre à jour l'interface des machines
        InterfaceGraphique(machines_frame, joueur.machines_possedees).create_machines_interface()

        # Initialiser le frame pour les techniciens engagés
        engaged_frame = ctk.CTkFrame(frames["menu_principal"], width=1160, height=200, fg_color="#333333")

        # Restaurer les techniciens engagés
        creer_interface_jeu()  # Réinitialiser l'interface du jeu
        joueur.argent = data["joueur"]["argent"]
        joueur.jour_actuel = data["joueur"]["jour_actuel"]

        for nom in data["techniciens_possedes"]:
            technician = next((tech for tech in technicians if tech.nom == nom), None)
            if technician:
                # Engage directement le technicien sans bouton
                technician.engager(joueur)
                print(f"Technicien restauré et engagé : {technician.nom}")
            else:
                print(f"Technicien non trouvé : {nom}")

        # Réinitialisation de l'affichage des techniciens
        engaged_frame.destroy()  # Supprime l'ancien cadre
        engaged_frame = ctk.CTkFrame(frames["menu_principal"], width=1160, height=200, fg_color="#333333")
        engaged_frame.place(x=10, y=500)

        # Met à jour l'interface des techniciens
        update_engaged_frame(
            engaged_frame=engaged_frame,
            joueur=joueur,
            argent_label=labels_profil["argent"],
            engagement_buttons=engagement_buttons
        )
        print("Engaged frame réinitialisé.")

        # Confirmation du succès du chargement
        print("Partie chargée avec succès.")
        messagebox.showinfo("Chargement", "Partie chargée avec succès.")

    except Exception as e:
        # Gestion des erreurs lors du chargement
        print(f"Erreur lors du chargement des données : {e}")
        messagebox.showerror("Erreur", f"Erreur lors du chargement des données : {e}")

# Lancer l'écran d'accueil
creer_ecran_accueil()

# Boucle principale de l'application
root.mainloop()
