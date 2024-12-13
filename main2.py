import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
from modules.Machines import Machine, machines_disponibles,machines_possedees, InterfaceGraphique, acheter_machine
from modules.Technician import Technician, technicians, engagement_buttons, update_engaged_frame, engager_technicien
from modules.Joueur import Joueur, creer_labels_profil
import pickle
import tkinter.messagebox as messagebox
import customtkinter as ctk
import time
from PIL import Image, ImageTk
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

player_data = {}
selected_currency = "€"

# Fenêtre principale
root = ctk.CTk()
root.title("Repair Rush")
root.after(100, lambda: root.state('zoomed'))

# Créer les frames
frames = {}
for frame_name in ["menu_principal", "parametres","accueil", "choix_partie", "nom_joueur", "photo_profil"]:
    frame = ctk.CTkFrame(root)
    frame.place(relwidth=1, relheight=1)
    frames[frame_name] = frame

def creer_ecran_accueil():
    frame = frames["accueil"]
    frame.lift()
    for widget in frame.winfo_children():
        widget.destroy()

    # Fond d'écran
    try:
        bg_image = CTkImage(light_image=Image.open("images/Backg.jpg"), size=(root.winfo_screenwidth(), root.winfo_screenheight()))
        background_label = ctk.CTkLabel(frame, image=bg_image, text="")
        background_label.place(relwidth=1, relheight=1)
    except FileNotFoundError:
        print("Erreur : L'image de fond n'a pas été trouvée.")

    # Titre et boutons
    title_label = ctk.CTkLabel(frame, text="Repair Rush", font=("Arial", 50, "bold"))
    title_label.pack(pady=100)
    play_button = ctk.CTkButton(frame, text="Jouer", command=creer_ecran_choix_partie, font=("Arial", 20), width=300)
    play_button.pack(pady=20)
    quit_button = ctk.CTkButton(frame, text="Quitter", command=root.quit, font=("Arial", 20), width=300)
    quit_button.pack(pady=20)

def creer_ecran_choix_partie():
    frame = frames["choix_partie"]
    frame.lift()
    for widget in frame.winfo_children():
        widget.destroy()

    # Fond d'écran
    try:
        bg_image = CTkImage(light_image=Image.open("images/Backg.jpg"), size=(root.winfo_screenwidth(), root.winfo_screenheight()))
        background_label = ctk.CTkLabel(frame, image=bg_image, text="")
        background_label.place(relwidth=1, relheight=1)
    except FileNotFoundError:
        print("Erreur : L'image de fond n'a pas été trouvée.")

    # Titre
    title_label = ctk.CTkLabel(frame, text="Repair Rush", font=("Arial", 50, "bold"))
    title_label.place(relx=0.5, y=100, anchor="center")

    # Boutons
    new_game_button = ctk.CTkButton(
        frame, text="Nouvelle Partie", command=demander_nom,
        font=("Arial", 20), width=300
    )
    new_game_button.place(relx=0.5, y=200, anchor="center")

    load_game_button = ctk.CTkButton(
        frame, text="Charger Partie", command=charger_partie,
        font=("Arial", 20), width=300,
        state="normal" if verifier_sauvegarde() else "disabled"
    )
    load_game_button.place(relx=0.5, y=250, anchor="center")

    back_button = ctk.CTkButton(
        frame, text="Retour", command=creer_ecran_accueil,
        font=("Arial", 20), width=300
    )
    back_button.place(relx=0.5, y=300, anchor="center")

def demander_nom():
    frame = frames["nom_joueur"]
    frame.lift()
    for widget in frame.winfo_children():
        widget.destroy()

    ctk.CTkLabel(frame, text="Entrez votre nom :", font=("Arial", 20)).pack(pady=20)
    nom_entry = ctk.CTkEntry(frame)
    nom_entry.pack(pady=10)

    ctk.CTkLabel(frame, text="Nom de l'entreprise :", font=("Arial", 20)).pack(pady=20)
    entreprise_entry = ctk.CTkEntry(frame)
    entreprise_entry.pack(pady=10)

    error_label = ctk.CTkLabel(frame, text="", font=("Arial", 12), text_color="red")
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

    ctk.CTkButton(frame, text="Suivant", command=valider_nom, font=("Arial", 20)).pack(pady=20)

def choisir_photo_profil():
    frame = frames["photo_profil"]
    frame.lift()
    for widget in frame.winfo_children():
        widget.destroy()

    ctk.CTkLabel(frame, text="Choisissez une photo de profil :", font=("Arial", 20)).pack(pady=10)
    images = [f"images/Profil{i}.png" for i in range(1, 7)]
    img_frame = ctk.CTkFrame(frame)
    img_frame.pack(pady=20)

    for img_path in images:
        try:
            img = CTkImage(light_image=Image.open(img_path), size=(100, 100))
            btn = ctk.CTkButton(img_frame, image=img, text="", command=lambda path=img_path: pre_lancer_jeu(path))
            btn.pack(side="left", padx=10)
        except FileNotFoundError:
            print(f"Erreur : L'image {img_path} est introuvable.")

def pre_lancer_jeu(photo_path):
    player_data["photo"] = photo_path
    creer_interface_jeu()

def creer_interface_jeu():
    #region Créer les différents frames
    """Crée l'interface principale du jeu et affiche le menu principal."""
    # Ajoute les frames du jeu au dictionnaire global
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
    # Menu déroulant pour sélectionner la monnaie
    currency_options = ["€", "$", "£"]
    currency_var = ctk.StringVar(value=selected_currency)
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

    joueur.jour_actuel
    if joueur.jour_actuel == 20:
        messagebox.showinfo("Fin de la partie", "La partie est terminée !")
        root.destroy()
        exit()

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
            
            # sound_manager.play_effect("sounds/ca-ching.mp3")  # Jouer le son de gain d'argent





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
            
            buy_button = ctk.CTkButton(scrollable_frame,text=f"{machine.cout_achat} {selected_currency}",width=150,command=lambda mach=machine: acheter_machine(mach, joueur, interface_machines, update_scrollable_frame))

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
            hire_button.configure(command=lambda t=technician, b=hire_button: engager_technicien(t, joueur, engaged_frame, labels_profil["argent"], engagement_buttons, b, progress_bar))
            hire_button.grid(row=i * 2 + 2, column=5, padx=10, pady=5)

    #region --- NOTIFICATIONS ---
    # Notifications pour les actions du joueur
    from NotificationsManager import NotificationsManager, set_global_notifications_manager

    notifications_manager = NotificationsManager(frames["menu_principal"], x=1400, y=50, width=300, height=500)
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
    # Fonction pour afficher les techniciens

    #region --- PARAMÈTRES ---
    # Boutons pour les différentes sections des options (Partie, Son, Profil)

    # Position des boutons dans le frame des paramètres

    #endregion
    #region --- PAGE PARTIE ---

    # Page unique pour toutes les fonctionnalités


    # --- Section Profil ---
    profile_label = ctk.CTkLabel(frames["parametres"], text="Profil", font=("Arial", 20, "bold"),text_color="black")
    profile_label.place(x=50, y=20)

    name_label = ctk.CTkLabel(frames["parametres"], text="Nom:",text_color="black")
    name_label.place(x=50, y=60)
    name_entry = ctk.CTkEntry(frames["parametres"])
    name_entry.place(x=150, y=60)

    currency_label = ctk.CTkLabel(frames["parametres"], text="Monnaie:",text_color="black")
    currency_label.place(x=50, y=100)
    currency_dropdown = ctk.CTkComboBox(frames["parametres"], values=["€", "$", "£"], command=update_currency)
    currency_dropdown.place(x=150, y=100)

    # --- Section Sauvegarde/Chargement ---
    save_label = ctk.CTkLabel(frames["parametres"], text="Partie", font=("Arial", 20, "bold"),text_color="black")
    save_label.place(x=50, y=160)

    save_button = ctk.CTkButton(frames["parametres"], text="Sauvegarder",command=sauvegarder_partie)
    save_button.place(x=50, y=200)

    # --- Section Son ---
    sound_label = ctk.CTkLabel(frames["parametres"], text="Son", font=("Arial", 20, "bold"),text_color="black")
    sound_label.place(x=50, y=280)

    music_label = ctk.CTkLabel(frames["parametres"], text="Musique:",text_color="black")
    music_label.place(x=50, y=320)
    music_slider = ctk.CTkSlider(frames["parametres"], from_=0, to=100, command=lambda value: sound_manager.set_music_volume(int(value)))
    music_slider.place(x=150, y=320)

    effects_label = ctk.CTkLabel(frames["parametres"], text="Effets Sonores:",text_color="black")
    effects_label.place(x=50, y=360)
    effects_slider = ctk.CTkSlider(frames["parametres"], from_=0, to=100, command=lambda value: sound_manager.set_effect_volume(int(value)))
    effects_slider.place(x=150, y=360)

    # --- Bouton Retour ---
    back_button = ctk.CTkButton(frames["parametres"], text="← Menu Principal", width=200, command=lambda: afficher_frame(frames["menu_principal"]))
    back_button.place(x=800, y=20)

    #endregion

    #region --- INTERFACE DES MACHINES ---
    interface_machines = InterfaceGraphique(machines_frame, machines_possedees)
    #endregion
    # Lancer la barre de progression
    start_progress()

    # Afficher les machines au démarrage
    afficher_machines()

# Variables globales
SAVE_FILE = "save/sauvegarde.pkl"
current_step = 0
tutorial_steps = [
    {"text": "Bienvenue dans Repair Rush !", "color": "yellow"},
    {"text": "Votre but est de gérer des machines et techniciens pour maximiser vos profits.", "color": "orange"},
    {"text": "Planifiez, entretenez et réparez vos machines avant qu'elles ne tombent en panne !", "color": "red"}
]
player_data = {"nom": "", "entreprise": "", "photo": ""}
machines_possedees = []
technicians = []
joueur = None

# Vérifier sauvegarde
def verifier_sauvegarde():
    try:
        with open(SAVE_FILE, "rb"):
            return True
    except FileNotFoundError:
        return False

# Sauvegarder les données
def sauvegarder_partie():
    try:
        # Vérifier et créer le dossier de sauvegarde si nécessaire
        save_dir = "/".join(SAVE_FILE.split("/")[:-1])
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # Collecter les données à sauvegarder
        data = {
            "player_data": player_data,
            "machines": machines_possedees,
            "technicians": technicians,
            "joueur": joueur.__dict__ if joueur else None,  # Sauvegarder les attributs de l'objet joueur
            "machine_data": [machine.__dict__ for machine in machines_possedees]
        }
        print(machines_possedees)
        print(data)
        # Sauvegarder les données dans un fichier pickle
        with open(SAVE_FILE, "wb") as f:
            pickle.dump(data, f)
        
        print("Données sauvegardées avec succès.")
        messagebox.showinfo("Sauvegarde", "Données sauvegardées avec succès.")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des données : {e}")
        messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde des données : {e}")

def charger_partie():
    if verifier_sauvegarde():
        try:
            with open(SAVE_FILE, "rb") as f:
                data = pickle.load(f)
            
            global player_data, machines_possedees, technicians, joueur
            player_data.update(data["player_data"])
            
            # Restaurer les machines possédées
            machines_possedees.clear()
            for machine_data in data["machines"]:
                machine = Machine()  # Assurez-vous que la classe Machine est importée
                machine.__dict__.update(machine_data)
                machines_possedees.append(machine)
            
            # Restaurer les techniciens
            technicians.clear()
            for technician_data in data["technicians"]:
                technician = Technician()  # Assurez-vous que la classe Technician est importée
                technician.__dict__.update(technician_data)
                technicians.append(technician)
            
            # Restaurer les attributs de l'objet joueur
            if data["joueur"]:
                joueur.__dict__.update(data["joueur"])
            print(machines_possedees)
            print("Données chargées avec succès.")
            creer_interface_jeu()
        except Exception as e:
            print(f"Erreur lors du chargement des données : {e}")
            messagebox.showerror("Erreur", f"Erreur lors du chargement des données : {e}")
    else:
        messagebox.showerror("Erreur", "Aucune sauvegarde trouvée.")
# Lancer l'écran d'accueil
creer_ecran_accueil()

# Boucle principale de l'application
root.mainloop()