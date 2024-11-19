import customtkinter as ctk
from customtkinter import CTk
import time
from PIL import Image, ImageTk
from Machines import Machine, machines_disponibles,machines_possedees, InterfaceGraphique, acheter_machine
from Technician import technicians, engagement_buttons, update_engaged_frame, engager_technicien


# from sound_manager import SoundManager
from joueur_class import Joueur
from interface_label import creer_labels_profil

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
# sound_manager = SoundManager()
joueur = Joueur(nom="Mr Boss", entreprise="Boss International")

# Fenêtre principale
root = ctk.CTk()
root.title("Repair Rush")
root.after(100, lambda: root.state('zoomed'))





#region Créer les différents frames

menu_principal_frame = ctk.CTkFrame(root, width=1500, height=900)
parametres_frame = ctk.CTkFrame(root, width=1500, height=900, fg_color="#E8C36A")
partie_frame = ctk.CTkFrame(root, width=1500, height=900, fg_color="#E8C36A")
son_frame = ctk.CTkFrame(root, width=1500, height=900, fg_color="#E8C36A")
profil_frame = ctk.CTkFrame(root, width=1500, height=900, fg_color="#E8C36A")



#endregion

# Placer tous les frames sur la fenêtre principale
for frame in (menu_principal_frame, parametres_frame, partie_frame, son_frame, profil_frame):
    frame.place(x=0, y=0, relwidth=1, relheight=1)
# Fonction pour afficher un frame et masquer les autres
def afficher_frame(frame):
    frame.lift()  # Amène le frame au premier plan



# --- MENU PRINCIPAL ---

#region --- PROFILE ---
# Profil du joueur (données principales)


# Frame des techniciens engagés (limité à 6)
engaged_frame = ctk.CTkFrame(menu_principal_frame, width=1160, height=200, fg_color="#333333")
engaged_frame.place(x=10, y=500)


# Créer les labels du profil et récupérer les références nécessaires
labels_profil = creer_labels_profil(menu_principal_frame, joueur)
argent_value = labels_profil["argent_value"]
jour_value = labels_profil["jour_value"]
revenu_value = labels_profil["revenu_value"]
couts_fixes_value = labels_profil["couts_fixes_value"]
solde_net_value = labels_profil["solde_net_value"]

# Fonction pour mettre à jour le profil
def update_profil():
    argent_value.configure(text=f"{joueur.argent} €")
    jour_value.configure(text=f"{joueur.jour_actuel}")
    revenu_value.configure(text=f"{joueur.calculer_revenu()} €")
    couts_fixes_value.configure(text=f"{joueur.calculer_couts_fixes()} €")
    solde_net_value.configure(text=f"{joueur.calculer_solde_net()} €")
    
# Mettre à jour les données du profil initialement
update_profil()

# Mettre à jour les données du profil initialement
update_profil()

progress_bar = ctk.CTkProgressBar(menu_principal_frame, width=600, height=30, progress_color='green')
progress_bar.place(x=10, y=350)

#endregion
# Barre de progression
def update_progress_bar(i=0):
    if i <= 3000:
        progress_bar.set(i / 3000)
        root.after(10, update_progress_bar, i + 1)
    else:
        progress_bar.set(0)
        root.after(10, update_progress_bar, 0)
        argent_value.configure(text=f"{joueur.argent} €")  # Mettre à jour l'affichage de l'argent
        joueur.incrementer_jour()  # Incrémenter le jour
        joueur.ajouter_revenu()  # Ajouter le revenu des machines
        jour_value.configure(text=f"{joueur.jour_actuel}")
        update_profil()  # Mettre à jour l'affichage du jour
        # sound_manager.play_effect("sounds/ca-ching.mp3")  # Jouer le son de gain d'argent

def start_progress():
    update_progress_bar()
#region Currency
# Monnaie sélectionnée par défaut (euros)
selected_currency = "€"

# Menu déroulant pour sélectionner la monnaie
currency_options = ["€", "$", "£"]
currency_var = ctk.StringVar(value=selected_currency)

# Fonction pour mettre à jour la monnaie sélectionnée
def update_currency(choice):
    global selected_currency
    selected_currency = choice
    afficher_machines()  # Mettre à jour l'affichage des machines avec la nouvelle monnaie
#endregion
scrollable_frame = ctk.CTkScrollableFrame(menu_principal_frame, width=660, height=300, fg_color="#FF7F7F")
scrollable_frame.place(x=660, y=100)

# Fonction pour afficher les machines
def afficher_machines():
    global menu_ouvert
    menu_ouvert = 'machines'
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    # Ajouter les titres des colonnes
    col_titles = ["Nom", "Niveau", "Type", "Revenu par période", "Action"]
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
        buy_button = ctk.CTkButton(scrollable_frame, text=f"Acheter ({machine.cout_achat} {selected_currency})", width=150,
                                    command=lambda mach=machine: acheter_machine(mach, joueur, argent_value, scrollable_frame, interface_machines))
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

        salaire_label = ctk.CTkLabel(scrollable_frame, text=f"{technician.salaire} €")
        salaire_label.grid(row=i * 2 + 2, column=4, padx=10, pady=5, sticky="w")

        # Bouton pour engager le technicien
        hire_button = ctk.CTkButton(scrollable_frame, text=f"Engager", width=150)
        
        # Ajouter le bouton au dictionnaire pour pouvoir le réactiver plus tard
        engagement_buttons[technician] = hire_button

        # Vérifier si le technicien est déjà engagé
        if technician in joueur.techniciens_possedes:
            hire_button.configure(state="disabled")

        # Fonction pour engager le technicien
        hire_button.configure(command=lambda t=technician, b=hire_button: engager_technicien(t, joueur, argent_value, engaged_frame, engagement_buttons, b))
        hire_button.grid(row=i * 2 + 2, column=5, padx=10, pady=5)



#region Boutons tech et machines
btn_machine = ctk.CTkButton(menu_principal_frame, text="Machines", width=140, height=50, command=afficher_machines)
btn_machine.place(x=650, y=20)

btn_technicien = ctk.CTkButton(menu_principal_frame, text="Techniciens", width=140, height=50, command=afficher_techniciens)
btn_technicien.place(x=800, y=20)
#endregion
# Fonction pour afficher les techniciens

#region --- PARAMÈTRES ---
# Boutons pour les différentes sections des options (Partie, Son, Profil)
partie_button = ctk.CTkButton(parametres_frame, text="Partie", width=200, command=lambda: afficher_frame(partie_frame))
son_button = ctk.CTkButton(parametres_frame, text="Son", width=200, command=lambda: afficher_frame(son_frame))
profil_button = ctk.CTkButton(parametres_frame, text="Profil", width=200, command=lambda: afficher_frame(profil_frame))

# Position des boutons dans le frame des paramètres
partie_button.place(x=100, y=20)
son_button.place(x=350, y=20)
profil_button.place(x=600, y=20)
#endregion
#region --- PAGE PARTIE ---
save_button = ctk.CTkButton(partie_frame, text="Sauvegarder")
load_button = ctk.CTkButton(partie_frame, text="Charger une partie")
reset_button = ctk.CTkButton(partie_frame, text="Réinitialiser la partie")

# Position des boutons sur la page Partie
save_button.place(x=100, y=100)
load_button.place(x=100, y=160)
reset_button.place(x=100, y=220)

# Garder les boutons Partie, Son, Profil dans chaque sous-menu
partie_button = ctk.CTkButton(partie_frame, text="Partie", width=200, command=lambda: afficher_frame(partie_frame))
son_button = ctk.CTkButton(partie_frame, text="Son", width=200, command=lambda: afficher_frame(son_frame))
profil_button = ctk.CTkButton(partie_frame, text="Profil", width=200, command=lambda: afficher_frame(profil_frame))

# Position des boutons
partie_button.place(x=100, y=20)
son_button.place(x=350, y=20)
profil_button.place(x=600, y=20)

# Bouton retour pour revenir au menu principal depuis chaque sous-menu
back_button = ctk.CTkButton(partie_frame, text="←", width=50, command=lambda: afficher_frame(menu_principal_frame))
back_button.place(x=1200, y=20)


#endregion
#region --- PAGE SON ---
music_label = ctk.CTkLabel(son_frame, text="Musique")
music_slider = ctk.CTkSlider(son_frame, from_=0, to=100, command=lambda value: sound_manager.set_music_volume(int(value)))

# Position des éléments sur la page Son
music_label.place(x=350, y=100)
music_slider.place(x=350, y=140)

effects_label = ctk.CTkLabel(son_frame, text="Effets Sonores")
effects_slider = ctk.CTkSlider(son_frame, from_=0, to=100, command=lambda value: sound_manager.set_effect_volume(int(value)))

effects_label.place(x=350, y=180)
effects_slider.place(x=350, y=220)

# Garder les boutons Partie, Son, Profil dans chaque sous-menu
partie_button = ctk.CTkButton(son_frame, text="Partie", width=200, command=lambda: afficher_frame(partie_frame))
son_button = ctk.CTkButton(son_frame, text="Son", width=200, command=lambda: afficher_frame(son_frame))
profil_button = ctk.CTkButton(son_frame, text="Profil", width=200, command=lambda: afficher_frame(profil_frame))

# Position des boutons
partie_button.place(x=100, y=20)
son_button.place(x=350, y=20)
profil_button.place(x=600, y=20)

# Bouton retour pour revenir au menu principal depuis chaque sous-menu
back_button = ctk.CTkButton(son_frame, text="←", width=50, command=lambda: afficher_frame(menu_principal_frame))
back_button.place(x=1200, y=20)
#endregion
#region --- PAGE PROFIL ---
name_label = ctk.CTkLabel(profil_frame, text="Nom:")
name_entry = ctk.CTkEntry(profil_frame)
currency_label = ctk.CTkLabel(profil_frame, text="Monnaie:")
currency_dropdown = ctk.CTkComboBox(profil_frame, values=currency_options, command=update_currency, variable=currency_var)

# Position des éléments sur la page Profil
name_label.place(x=600, y=100)
name_entry.place(x=600, y=140)
currency_label.place(x=600, y=180)
currency_dropdown.place(x=600, y=220)

# Bouton pour ouvrir le menu des paramètres
options_button = ctk.CTkButton(menu_principal_frame, text="⚙️", width=50, height=50, command=lambda: afficher_frame(parametres_frame))
options_button.place(x=950, y=20)

# Bouton retour pour revenir au menu principal depuis les paramètres
back_button = ctk.CTkButton(parametres_frame, text="←", width=50, command=lambda: afficher_frame(menu_principal_frame))
back_button.place(x=1200, y=20)

# Garder les boutons Partie, Son, Profil dans chaque sous-menu
partie_button = ctk.CTkButton(profil_frame, text="Partie", width=200, command=lambda: afficher_frame(partie_frame))
son_button = ctk.CTkButton(profil_frame, text="Son", width=200, command=lambda: afficher_frame(son_frame))
profil_button = ctk.CTkButton(profil_frame, text="Profil", width=200, command=lambda: afficher_frame(profil_frame))

# Position des boutons
partie_button.place(x=100, y=20)
son_button.place(x=350, y=20)
profil_button.place(x=600, y=20)

# Bouton retour pour revenir au menu principal depuis chaque sous-menu
back_button = ctk.CTkButton(profil_frame, text="←", width=50, command=lambda: afficher_frame(menu_principal_frame))
back_button.place(x=1200, y=20)
#endregion

#region --- INTERFACE DES MACHINES ---
machines_frame = ctk.CTkFrame(menu_principal_frame, width=1380, height=300)
machines_frame.place(x=10, y=800)
interface_machines = InterfaceGraphique(machines_frame, machines_possedees)
#endregion
# Lancer la barre de progression
start_progress()

# Afficher les machines au démarrage
afficher_machines()

# Lancer l'interface principale
afficher_frame(menu_principal_frame)
root.mainloop()