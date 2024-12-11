import customtkinter as ctk
from customtkinter import CTk
import time
from PIL import Image, ImageTk
from modules.Machines import Machine, machines_disponibles,machines_possedees, InterfaceGraphique, acheter_machine
from modules.Technician import Technician, technicians, engagement_buttons, update_engaged_frame, engager_technicien
# from sound_manager import SoundManager
from modules.Joueur import Joueur, creer_labels_profil
import pickle
import tkinter.messagebox as messagebox
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
# sound_manager = SoundManager()


# Fenêtre principale
root = ctk.CTk()
root.title("Repair Rush")
root.after(100, lambda: root.state('zoomed'))





#region Créer les différents frames
joueur = Joueur(nom="Mr Boss", entreprise="Boss International",photo= "images/Profil1.png")
menu_principal_frame = ctk.CTkFrame(root, width=1500, height=900)
parametres_frame = ctk.CTkFrame(root, width=1500, height=900, fg_color="#E8C36A")
partie_frame = ctk.CTkFrame(root, width=1500, height=900, fg_color="#E8C36A")
son_frame = ctk.CTkFrame(root, width=1500, height=900, fg_color="#E8C36A")
profil_frame = ctk.CTkFrame(root, width=1500, height=900, fg_color="#E8C36A")
machines_frame = ctk.CTkFrame(menu_principal_frame, width=1380, height=300)
machines_frame.place(x=10, y=760)


for frame in (menu_principal_frame, parametres_frame, partie_frame, son_frame, profil_frame):
    frame.place(x=0, y=0, relwidth=1, relheight=1)

# Fonction pour afficher un frame et masquer les autres
def afficher_frame(frame):
    frame.lift()  # Amène le frame au premier plan
engaged_frame = ctk.CTkFrame(menu_principal_frame, width=1160, height=200, fg_color="#333333")
engaged_frame.place(x=10, y=500)


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
labels_profil = creer_labels_profil(menu_principal_frame, joueur, selected_currency)
joueur.trigger_ui_update()

joueur.jour_actuel
if joueur.jour_actuel == 20:
    messagebox.showinfo("Fin de la partie", "La partie est terminée !")
    root.destroy()
    exit()

progress_bar = ctk.CTkProgressBar(menu_principal_frame, width=600, height=30, progress_color='green')
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




scrollable_frame = ctk.CTkScrollableFrame(menu_principal_frame, width=660, height=300, fg_color="#FF7F7F")
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

notifications_manager = NotificationsManager(menu_principal_frame, x=1400, y=50, width=300, height=500)
set_global_notifications_manager(notifications_manager)

notifications_manager.ajouter_notification("Bienvenue dans le jeu !")
#endregion
#region Boutons tech et machines
# Bouton "Machines"
btn_machine = ctk.CTkButton(menu_principal_frame, text="Machines", width=140, height=50, command=afficher_machines)
btn_machine.place(x=650, y=20)

# Bouton "Techniciens"
btn_technicien = ctk.CTkButton(menu_principal_frame, text="Techniciens", width=140, height=50, command=afficher_techniciens)
btn_technicien.place(x=800, y=20)

# Bouton "Paramètres" avec un symbole d'engrenage
btn_parametres = ctk.CTkButton(
    menu_principal_frame, 
    text="⚙️",  # Utilisation d'un emoji pour le symbole d'engrenage
    width=50, 
    height=50, 
    command=lambda: afficher_frame(parametres_frame)  # Accès à la page des paramètres
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
profile_label = ctk.CTkLabel(parametres_frame, text="Profil", font=("Arial", 20, "bold"),text_color="black")
profile_label.place(x=50, y=20)

name_label = ctk.CTkLabel(parametres_frame, text="Nom:",text_color="black")
name_label.place(x=50, y=60)
name_entry = ctk.CTkEntry(parametres_frame)
name_entry.place(x=150, y=60)

currency_label = ctk.CTkLabel(parametres_frame, text="Monnaie:",text_color="black")
currency_label.place(x=50, y=100)
currency_dropdown = ctk.CTkComboBox(parametres_frame, values=["€", "$", "£"], command=update_currency)
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
back_button = ctk.CTkButton(parametres_frame, text="← Menu Principal", width=200, command=lambda: afficher_frame(menu_principal_frame))
back_button.place(x=800, y=20)

#endregion

#region --- INTERFACE DES MACHINES ---
interface_machines = InterfaceGraphique(machines_frame, machines_possedees)
#endregion
# Lancer la barre de progression
start_progress()

# Afficher les machines au démarrage
afficher_machines()

# Lancer l'interface principale
afficher_frame(menu_principal_frame)
root.mainloop()
