import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
from modules.Machines import Machine, machines_disponibles,machines_possedees, InterfaceGraphique, acheter_machine
from modules.Technician import Technician, technicians, engagement_buttons, update_engaged_frame, engager_technicien
from modules.Joueur import Joueur, creer_labels_profil
import json
import tkinter.messagebox as messagebox
import customtkinter as ctk
import os
from PIL import Image, ImageTk

from sound_manager import SoundManager
sound_manager = SoundManager()

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

    def selectionner_photo(path):
        player_data["photo"] = path
        joueur = Joueur(
            nom=player_data["nom"],
            entreprise=player_data["entreprise"],
            photo=path
        )
        print(f"Profil créé : {joueur.nom} ({joueur.entreprise}), photo sélectionnée : {path}")
        lancer_tutoriel(joueur)

    for img_path in images:
        try:
            img = CTkImage(light_image=Image.open(img_path), size=(100, 100))
            btn = ctk.CTkButton(img_frame, image=img, text="", command=lambda path=img_path: selectionner_photo(path))
            btn.pack(side="left", padx=10)
        except FileNotFoundError:
            print(f"Erreur : L'image {img_path} est introuvable.")


def lancer_tutoriel(joueur):
    tutoriel_frame = ctk.CTkFrame(root, width=1500, height=900, fg_color="#E8C36A")
    tutoriel_frame.place(relwidth=1, relheight=1)

    titre_label = ctk.CTkLabel(
        tutoriel_frame,
        text=f"Bienvenue, {joueur.nom} !",
        font=("Arial", 40, "bold"),
        text_color="black",
    )
    titre_label.pack(pady=20)

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

    def lancer_jeu():
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
            
            sound_manager.play_effect("sounds/ca-ching.mp3")  # Jouer le son de gain d'argent

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
            hire_button.configure(command=lambda t=technician, b=hire_button: engager_technicien(t, joueur, engaged_frame, labels_profil["argent"], engagement_buttons, b))
            hire_button.grid(row=i * 2 + 2, column=5, padx=10, pady=5)

    #region --- NOTIFICATIONS ---
    # Notifications pour les actions du joueur
    from NotificationsManager import NotificationsManager, set_global_notifications_manager

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
    # Fonction pour afficher les techniciens

    #region --- PARAMÈTRES ---
    # Boutons pour les différentes sections des options (Partie, Son, Profil)

    # Position des boutons dans le frame des paramètres

    #endregion
    #region --- PAGE PARTIE ---

    # Page unique pour toutes les fonctionnalités


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

    # --- Section Son ---
    sound_label = ctk.CTkLabel(frames["parametres"], text="Son", font=("Arial", 20, "bold"),text_color="black")
    sound_label.place(x=50, y=280)

    sound_label = ctk.CTkLabel(frames["parametres"], text="Son",text_color="black")
    sound_label.place(x=50, y=320)
    sound_slider = ctk.CTkSlider(
        frames["parametres"],
        from_=0,  # Volume minimum
        to=100,  # Volume maximum
        command=lambda value: sound_manager.setvolume(int(value))  # Appelle setvolume avec la valeur du slider
    )
    sound_slider.place(x=150, y=320)
    #region --- BOUTONS DE SON ---
    music_enabled_var = ctk.BooleanVar(value=True)  # Musique activée par défaut

    # Fonction pour activer/désactiver la musique
    def toggle_music(sound_manager, music_var):
        """Active ou désactive la musique selon l'état de la case à cocher."""
        if music_var.get():  # Si la case est cochée
            current_volume = sound_manager.getvolume()
            if current_volume == 0:  # Si le volume est à 0, remets un volume par défaut
                sound_manager.setvolume(50)  # Remets le volume à 50%
            sound_manager.resumemusic()  # Reprends la musique si elle est en pause
        else:  # Si la case est décochée
            sound_manager.setvolume(0)  # Mets le volume à 0 pour couper la musique

    # Initialisation pour synchroniser la case avec l'état réel de la musique
    if sound_manager.getvolume() == 0:
        music_enabled_var.set(False)
    else:
        music_enabled_var.set(True)

    # Ajout de la case à cocher dans les paramètres
    music_toggle_checkbox = ctk.CTkCheckBox(
        frames["parametres"],
        text="🎵 Activer la musique",
        variable=music_enabled_var,
        onvalue=True,
        offvalue=False,
        command=lambda: toggle_music(sound_manager, music_enabled_var)
    )
    music_toggle_checkbox.place(x=150, y=420)
    #endregion
    # Synchroniser la position initiale du slider avec le volume actuel
    current_volume = sound_manager.getvolume()  # Récupère le volume actuel
    sound_slider.set(current_volume) 


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


    try:
        with open(SAVE_FILE, "rb"):
            return True
    except FileNotFoundError:
        return False


SAVE_FILE = "save/Save.json"
current_step = 0
tutorial_steps = [
    {"text": "Bienvenue dans Repair Rush !", "color": "yellow"},
    {"text": "Votre but est de gérer des machines et techniciens pour maximiser vos profits.", "color": "orange"},
    {"text": "Planifiez, entretenez et réparez vos machines avant qu'elles ne tombent en panne !", "color": "red"}
]


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
        save_dir = os.path.dirname(SAVE_FILE)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Sauvegarder les noms et niveaux des machines possédées
        possessed_machines = [{"nom": machine.nom, "niveau": machine.niveau_machine} for machine in joueur.machines_possedees]
        # Sauvegarder les noms des techniciens possédés
        possessed_technicians = [technician.nom for technician in joueur.techniciens_possedes]

        # Préparer les données à sauvegarder
        data = {
            "player_data": player_data,
            "machines_possedees": possessed_machines,
            "techniciens_possedes": possessed_technicians,
            "joueur": {
                "nom": joueur.nom,
                "entreprise": joueur.entreprise,
                "photo": joueur.photo,
                "argent": joueur.argent,
                "jour_actuel": joueur.jour_actuel
            }
        }
        print("Machines possédées :", possessed_machines)

        # Sauvegarder les données au format JSON
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=4)

        print("Données sauvegardées avec succès en JSON.")
        messagebox.showinfo("Sauvegarde", "Données sauvegardées avec succès.")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des données : {e}")
        messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde des données : {e}")
labels_profil = {
    "argent": None
}
class FakeProgressBar:
    """Barre de progression factice pour simuler une journée complète."""
    def get(self):
        return 1.0  # Retourne toujours une progression complète
fake_progress_bar = FakeProgressBar()
def charger_partie():
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)

        global player_data, joueur, machines_possedees, technicians, frames, labels_profil, engagement_buttons

        # Restaurer les données du joueur
        player_data = data["player_data"]
        joueur = Joueur(
            nom=data["joueur"]["nom"],
            entreprise=data["joueur"]["entreprise"],
            photo=data["joueur"]["photo"],
            argent=data["joueur"]["argent"],
        )

        # Initialiser le frame pour les machines
        machines_frame = ctk.CTkFrame(frames["menu_principal"], width=1380, height=300)
        machines_frame.place(x=10, y=760)

        # Restaurer les machines possédées
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
        

        # Restaurer les techniciens possédés
        creer_interface_jeu()
        joueur.argent = data["joueur"]["argent"]
        joueur.jour_actuel = data["joueur"]["jour_actuel"]
        for nom in data["techniciens_possedes"]:
            technician = next((tech for tech in technicians if tech.nom == nom), None)
            if technician:
                # Engage directement le technicien (sans bouton)
                technician.engager(joueur)
                print(f"Technicien restauré et engagé : {technician.nom}")
            else:
                print(f"Technicien non trouvé : {nom}")

        # Après avoir restauré les techniciens, force la réinitialisation de la frame
        engaged_frame.destroy()  # Supprime le cadre existant
        engaged_frame = ctk.CTkFrame(frames["menu_principal"], width=1160, height=200, fg_color="#333333")
        engaged_frame.place(x=10, y=500)

        # Réinitialise l'affichage des techniciens
        update_engaged_frame(
            engaged_frame=engaged_frame,
            joueur=joueur,
            argent_label=labels_profil["argent"],
            engagement_buttons=engagement_buttons
        )
        print("Engaged frame réinitialisé.")

        print("Partie chargée avec succès.")
        messagebox.showinfo("Chargement", "Partie chargée avec succès.")

    except Exception as e:
        print(f"Erreur lors du chargement des données : {e}")
        messagebox.showerror("Erreur", f"Erreur lors du chargement des données : {e}")








# Lancer l'écran d'accueil
creer_ecran_accueil()

# Boucle principale de l'application
root.mainloop()
