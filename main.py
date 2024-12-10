import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
from modules.Machines import Machine, machines_disponibles,machines_possedees, InterfaceGraphique, acheter_machine
from modules.Technician import Technician, technicians, engagement_buttons, update_engaged_frame, engager_technicien
from modules.Joueur import Joueur, creer_labels_profil
import pickle
import tkinter.messagebox as messagebox

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
    frame = frames["menu_principal"]
    frame.lift()
    for widget in frame.winfo_children():
        widget.destroy()

    global joueur
    joueur = Joueur(nom=player_data["nom"], entreprise=player_data["entreprise"], photo=player_data["photo"])
    labels_profil = creer_labels_profil(frame, joueur, selected_currency)
    joueur.trigger_ui_update()

    progress_bar = ctk.CTkProgressBar(frame, width=600, height=30, progress_color='green')
    progress_bar.place(x=10, y=350)

    def update_progress_bar(i=0):
        if i == 0:
            joueur.payer_salaires()
        if i <= 3000:
            progress_bar.set(i / 3000)
            root.after(10, update_progress_bar, i + 1)
        else:
            progress_bar.set(0)
            root.after(10, update_progress_bar, 0)
            joueur.incrementer_jour()
            joueur.ajouter_revenu()

    update_progress_bar()

    global scrollable_frame
    scrollable_frame = ctk.CTkScrollableFrame(frame, width=660, height=300, fg_color="#FF7F7F")
    scrollable_frame.place(x=660, y=100)

    def afficher_machines():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        col_titles = ["Nom", "Niveau", "Type", "Revenu par période", "Action"]
        for idx, title in enumerate(col_titles):
            title_label = ctk.CTkLabel(scrollable_frame, text=title, text_color="white", font=("Arial", 12, "bold"))
            title_label.grid(row=0, column=idx, padx=10, pady=5, sticky="w")

        for i, machine in enumerate(machines_possedees):
            separator = ctk.CTkLabel(scrollable_frame, text="".ljust(150, "-"), text_color="gray")
            separator.grid(row=i * 2 + 1, column=0, columnspan=6, padx=5, pady=5, sticky="ew")

            machine_image = CTkImage(light_image=Image.open(machine.image_path), size=(80, 80))
            image_label = ctk.CTkLabel(scrollable_frame, image=machine_image, text="")
            image_label.grid(row=i * 2 + 2, column=0, padx=10, pady=5)

            nom_label = ctk.CTkLabel(scrollable_frame, text=f"{machine.nom}")
            nom_label.grid(row=i * 2 + 2, column=1, padx=10, pady=5, sticky="w")

            niveau_label = ctk.CTkLabel(scrollable_frame, text=f"{machine.niveau_machine}")
            niveau_label.grid(row=i * 2 + 2, column=2, padx=10, pady=5, sticky="w")

            type_machine_label = ctk.CTkLabel(scrollable_frame, text=f"{machine.type_machine}")
            type_machine_label.grid(row=i * 2 + 2, column=3, padx=10, pady=5, sticky="w")

            revenu_label = ctk.CTkLabel(scrollable_frame, text=f"{machine.revenu_par_periode} {selected_currency}")
            revenu_label.grid(row=i * 2 + 2, column=4, padx=10, pady=5, sticky="nsew")

            possede_label = ctk.CTkLabel(scrollable_frame, text="Possédé", width=150, fg_color="#3d3d3d", corner_radius=8)
            possede_label.grid(row=i * 2 + 2, column=5, padx=10, pady=5)

        row_offset = len(machines_possedees) * 2
        for j, machine in enumerate(machines_disponibles):
            separator = ctk.CTkLabel(scrollable_frame, text="".ljust(150, "-"), text_color="gray")
            separator.grid(row=row_offset + j * 2 + 1, column=0, columnspan=6, padx=5, pady=5, sticky="ew")

            machine_image = CTkImage(light_image=Image.open(machine.image_path), size=(80, 80))
            image_label = ctk.CTkLabel(scrollable_frame, image=machine_image, text="")
            image_label.grid(row=row_offset + j * 2 + 2, column=0, padx=10, pady=5)

            nom_label = ctk.CTkLabel(scrollable_frame, text=f"{machine.nom}")
            nom_label.grid(row=row_offset + j * 2 + 2, column=1, padx=10, pady=5, sticky="w")

            niveau_label = ctk.CTkLabel(scrollable_frame, text=f"{machine.niveau_machine}")
            niveau_label.grid(row=row_offset + j * 2 + 2, column=2, padx=10, pady=5, sticky="w")

            type_machine_label = ctk.CTkLabel(scrollable_frame, text=f"{machine.type_machine}")
            type_machine_label.grid(row=row_offset + j * 2 + 2, column=3, padx=10, pady=5, sticky="w")

            revenu_label = ctk.CTkLabel(scrollable_frame, text=f"{machine.revenu_par_periode} {selected_currency}")
            revenu_label.grid(row=row_offset + j * 2 + 2, column=4, padx=10, pady=5, sticky="nsew")

            buy_button = ctk.CTkButton(
                scrollable_frame,
                text=f"Acheter ({machine.cout_achat} {selected_currency})",
                width=150,
                command=lambda mach=machine: acheter_machine(mach, joueur, afficher_machines, None)
            )
            buy_button.grid(row=row_offset + j * 2 + 2, column=5, padx=10, pady=5)

    def afficher_techniciens():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        col_titles = ["Nom", "Spécialité", "Niveau", "Salaire", ""]
        for idx, title in enumerate(col_titles):
            title_label = ctk.CTkLabel(scrollable_frame, text=title, text_color="white", font=("Arial", 12, "bold"))
            title_label.grid(row=0, column=idx + 1, padx=10, pady=5, sticky="w")

        for i, technician in enumerate(technicians):
            separator = ctk.CTkLabel(scrollable_frame, text="".ljust(150, "-"), text_color="gray")
            separator.grid(row=i * 2 + 1, column=0, columnspan=6, padx=5, pady=5, sticky="ew")

            technician_image = CTkImage(light_image=Image.open(technician.image_path), size=(80, 80))
            image_label = ctk.CTkLabel(scrollable_frame, image=technician_image, text="")
            image_label.grid(row=i * 2 + 2, column=0, padx=10, pady=5)

            technician_label = ctk.CTkLabel(scrollable_frame, text=f"{technician.nom}")
            technician_label.grid(row=i * 2 + 2, column=1, padx=10, pady=5, sticky="w")

            speciality_label = ctk.CTkLabel(scrollable_frame, text=f"{technician.specialite}")
            speciality_label.grid(row=i * 2 + 2, column=2, padx=10, pady=5, sticky="w")

            niveau_label = ctk.CTkLabel(scrollable_frame, text=f"{technician.niveau}")
            niveau_label.grid(row=i * 2 + 2, column=3, padx=10, pady=5, sticky="w")

            salaire_label = ctk.CTkLabel(scrollable_frame, text=f"{technician.salaire} €")
            salaire_label.grid(row=i * 2 + 2, column=4, padx=10, pady=5, sticky="w")

            hire_button = ctk.CTkButton(scrollable_frame, text="Engager", width=150)
            engagement_buttons[technician] = hire_button

            if technician in joueur.techniciens_possedes:
                hire_button.configure(state="disabled")

            hire_button.configure(
                command=lambda t=technician, b=hire_button: engager_technicien(
                    t, joueur, None, labels_profil, engagement_buttons, b
                )
            )
            hire_button.grid(row=i * 2 + 2, column=5, padx=10, pady=5)

    btn_machine = ctk.CTkButton(frame, text="Machines", width=140, height=50, command=afficher_machines)
    btn_machine.place(x=650, y=20)

    btn_technicien = ctk.CTkButton(frame, text="Techniciens", width=140, height=50, command=afficher_techniciens)
    btn_technicien.place(x=800, y=20)
    # Page unique pour toutes les fonctionnalités
    main_page_frame = ctk.CTkFrame(root, width=1024, height=576)
    parametres_frame = frames["parametres"]
    main_page_frame.place(relwidth=1, relheight=1)

    # --- Section Profil ---
    profile_label = ctk.CTkLabel(parametres_frame, text="Profil", font=("Arial", 20, "bold"),text_color="black")
    profile_label.place(x=50, y=20)

    name_label = ctk.CTkLabel(parametres_frame, text="Nom:",text_color="black")
    name_label.place(x=50, y=60)
    name_entry = ctk.CTkEntry(parametres_frame)
    name_entry.place(x=150, y=60)

    currency_label = ctk.CTkLabel(parametres_frame, text="Monnaie:",text_color="black")
    currency_label.place(x=50, y=100)
    currency_dropdown = ctk.CTkComboBox(parametres_frame, values=["€", "$", "£"],)
    currency_dropdown.place(x=150, y=100)

    # --- Section Sauvegarde/Chargement ---
    save_label = ctk.CTkLabel(parametres_frame, text="Partie", font=("Arial", 20, "bold"),text_color="black")
    save_label.place(x=50, y=160)

    save_button = ctk.CTkButton(parametres_frame, text="Sauvegarder")
    save_button.place(x=50, y=200)

    # --- Section Son ---
    sound_label = ctk.CTkLabel(parametres_frame, text="Son", font=("Arial", 20, "bold"),text_color="black")
    sound_label.place(x=50, y=280)

    music_label = ctk.CTkLabel(parametres_frame, text="Musique:",text_color="black")
    music_label.place(x=50, y=320)
    music_slider = ctk.CTkSlider(parametres_frame, from_=0, to=100, command=lambda value: sound_manager.set_music_volume(int(value)))
    music_slider.place(x=150, y=320)

    effects_label = ctk.CTkLabel(parametres_frame, text="Effets Sonores:",text_color="black")
    effects_label.place(x=50, y=360)
    effects_slider = ctk.CTkSlider(parametres_frame, from_=0, to=100, command=lambda value: sound_manager.set_effect_volume(int(value)))
    effects_slider.place(x=150, y=360)

    # --- Bouton Retour ---
    back_button = ctk.CTkButton(parametres_frame, text="← Menu Principal", width=200, command= main_page_frame.place(relwidth=1, relheight=1))
    back_button.place(x=800, y=20)

    #endregion

    #--- INTERFACE DES MACHINES ---
    machines_frame = ctk.CTkFrame(main_page_frame, width=1380, height=300)
    machines_frame.place(x=10, y=800)
    interface_machines = InterfaceGraphique(machines_frame, machines_possedees)
    

    afficher_machines()

def sauvegarder_donnees():
    with open("sauvegarde.pkl", "wb") as f:
        pickle.dump(player_data, f)
    messagebox.showinfo("Sauvegarde", "Données sauvegardées avec succès.")

def charger_partie():
    global player_data
    try:
        with open("sauvegarde.pkl", "rb") as f:
            player_data = pickle.load(f)
        creer_interface_jeu()
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Aucune sauvegarde trouvée.")

def verifier_sauvegarde():
    try:
        with open("sauvegarde.pkl", "rb"):
            return True
    except FileNotFoundError:
        return False

# Lancer l'écran d'accueil
creer_ecran_accueil()

# Boucle principale de l'application
root.mainloop()