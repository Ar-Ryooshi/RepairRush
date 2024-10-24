import customtkinter as ctk
import sound_manager as sm
import time
import threading
from PIL import Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

sound_manager = sm.SoundManager()

def play_sound():
    sound_manager.playsound('./sounds/ca-ching.mp3')

root = ctk.CTk()
root.title("Repair Rush")
root.geometry("1280x720")

menu_ouvert = None

# Profil du joueur (élargi pour correspondre à la barre de progression)
profile_frame = ctk.CTkFrame(root, width=600, height=150, corner_radius=10, fg_color="#FFA500")
profile_frame.place(x=10, y=10)

# Ajout de l'image du joueur


#cadre de profil
profile_frame = ctk.CTkFrame(root, width=600, height=150, corner_radius=10, fg_color="#FFA500")
profile_frame.place(x=10, y=10)

# Image de profil
image_path = "Images/qatari_boss.png"  
image = Image.open(image_path)  # Charger l'image
profile_image = ctk.CTkLabel(root, text="")
img = ctk.CTkImage(light_image=image, size=(80, 80))  
profile_image.configure(image=img)
profile_image.place(x=500, y=30)

# Informations de profil sous forme de liste de tuples (nom_label, valeur_label)
info = [
    ("Jour actuel:", "5"),
    ("Argent actuel:", "$2000"),
    ("Revenus par période:", "$500"),
    ("Coûts fixes:", "$100"),
    ("Solde net:", "$2400")
]

# Nom du joueur et entreprise
profile_label = ctk.CTkLabel(profile_frame, text="Mr Boss", font=("Arial", 16), text_color="black")
profile_label.place(x=100, y=10)

entreprise_label = ctk.CTkLabel(profile_frame, text="Boss International", font=("Arial", 10), text_color="black")
entreprise_label.place(x=100, y=40)

# Boucle pour générer les informations (nom_label, valeur_label)
for i, (nom, valeur) in enumerate(info):
    # Positionnement dynamique avec l'index i pour éviter la répétition
    info_label = ctk.CTkLabel(profile_frame, text=nom, font=("Arial", 10), text_color="black")
    info_label.place(x=100, y=70 + i * 20)

    valeur_label = ctk.CTkLabel(profile_frame, text=valeur, font=("Arial", 10), text_color="black")
    valeur_label.place(x=250, y=70 + i * 20)


progress_bar = ctk.CTkProgressBar(root, width=600, height=30, progress_color='green')
progress_bar.place(x=10, y=170)

def update_progress_bar():
    while True:
        for i in range(3001):
            progress_bar.set(i / 3000)
            time.sleep(0.01)
        play_sound()
        progress_bar.set(0)

def start_progress():
    threading.Thread(target=update_progress_bar, daemon=True).start()

scrollable_frame = ctk.CTkScrollableFrame(root, width=600, height=300, fg_color="#FF7F7F")
scrollable_frame.place(x=650, y=100)

def afficher_machines():
    global menu_ouvert
    menu_ouvert = 'machines'
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    machine_info = [
        {"Nom": "Machine 1", "Durée": "5 sec", "Apport": "$100", "Type": "X"},
        {"Nom": "Machine 2", "Durée": "10 sec", "Apport": "$200", "Type": "X"},
        {"Nom": "Machine 3", "Durée": "15 sec", "Apport": "$300", "Type": "X"},
        {"Nom": "Machine 4", "Durée": "20 sec", "Apport": "$400", "Type": "X"},
        {"Nom": "Machine 5", "Durée": "25 sec", "Apport": "$500", "Type": "X"}
    ]
    for i, machine in enumerate(machine_info):
        machine_label = ctk.CTkLabel(scrollable_frame, text=f"{machine['Nom']} - {machine['Durée']} - {machine['Apport']} - {machine['Type']}")
        machine_label.grid(row=i, column=0, padx=10, pady=5, sticky="ew")
        buy_button = ctk.CTkButton(scrollable_frame, text="Acheter", width=100)
        buy_button.grid(row=i, column=1, padx=10, pady=5)

def afficher_techniciens():
    global menu_ouvert
    menu_ouvert = 'techniciens'
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    technician_info = [
        {"Nom": "Technicien 1", "Spécialité": "Mécanique", "Durée": "5 sec", "Salaire": "$100"},
        {"Nom": "Technicien 2", "Spécialité": "Électrique", "Durée": "10 sec", "Salaire": "$200"},
        {"Nom": "Technicien 3", "Spécialité": "Informatique", "Durée": "15 sec", "Salaire": "$300"},
        {"Nom": "Technicien 4", "Spécialité": "Mécanique", "Durée": "20 sec", "Salaire": "$400"},
        {"Nom": "Technicien 5", "Spécialité": "Électrique", "Durée": "25 sec", "Salaire": "$500"}
    ]
    for i, technician in enumerate(technician_info):
        technician_label = ctk.CTkLabel(scrollable_frame, text=f"{technician['Nom']} - {technician['Spécialité']} - {technician['Durée']} - {technician['Salaire']}")
        technician_label.grid(row=i, column=0, padx=10, pady=5, sticky="ew")
        hire_button = ctk.CTkButton(scrollable_frame, text="Engager", width=100)
        hire_button.grid(row=i, column=1, padx=10, pady=5)

btn_machine = ctk.CTkButton(root, text="Btn Machine", width=140, height=50, command=afficher_machines)
btn_machine.place(x=650, y=20)

btn_technicien = ctk.CTkButton(root, text="Btn Technicien", width=140, height=50, command=afficher_techniciens)
btn_technicien.place(x=800, y=20)

def open_partie():
    options_frame.lift()
    partie_button.configure(fg_color="gray")
    son_button.configure(fg_color="#FFA500")
    profil_button.configure(fg_color="#FFA500")
    save_button.place(x=100, y=100)
    load_button.place(x=100, y=160)
    reset_button.place(x=100, y=220)
    music_label.place_forget()
    music_slider.place_forget()
    effects_label.place_forget()
    effects_slider.place_forget()
    name_label.place_forget()
    name_entry.place_forget()
    currency_label.place_forget()
    currency_dropdown.place_forget()

def open_son():
    options_frame.lift()
    partie_button.configure(fg_color="#FFA500")
    son_button.configure(fg_color="gray")
    profil_button.configure(fg_color="#FFA500")
    music_label.place(x=350, y=100)
    music_slider.place(x=350, y=140)
    effects_label.place(x=350, y=180)
    effects_slider.place(x=350, y=220)
    save_button.place_forget()
    load_button.place_forget()
    reset_button.place_forget()
    name_label.place_forget()
    name_entry.place_forget()
    currency_label.place_forget()
    currency_dropdown.place_forget()

def open_profil():
    options_frame.lift()
    partie_button.configure(fg_color="#FFA500")
    son_button.configure(fg_color="#FFA500")
    profil_button.configure(fg_color="gray")
    name_label.place(x=600, y=100)
    name_entry.place(x=600, y=140)
    currency_label.place(x=600, y=180)
    currency_dropdown.place(x=600, y=220)
    save_button.place_forget()
    load_button.place_forget()
    reset_button.place_forget()
    music_label.place_forget()
    music_slider.place_forget()
    effects_label.place_forget()
    effects_slider.place_forget()

def hide_game_interface():
    profile_frame.place_forget()
    progress_bar.place_forget()
    scrollable_frame.place_forget()
    btn_machine.place_forget()
    btn_technicien.place_forget()
    options_button.place_forget()
    options_frame.place(x=0, y=0)

def show_game_interface():
    profile_frame.place(x=10, y=10)
    progress_bar.place(x=10, y=170)
    btn_machine.place(x=650, y=20)
    btn_technicien.place(x=800, y=20)
    options_button.place(x=950, y=20)
    options_frame.place_forget()
    if menu_ouvert == 'machines':
        scrollable_frame.place(x=650, y=100)
        afficher_machines()
    elif menu_ouvert == 'techniciens':
        scrollable_frame.place(x=650, y=100)
        afficher_techniciens()

options_button = ctk.CTkButton(root, text="⚙️", width=50, height=50, command=hide_game_interface)
options_button.place(x=950, y=20)

options_frame = ctk.CTkFrame(root, width=1280, height=720, fg_color="#E8C36A")
options_frame.place_forget()

partie_button = ctk.CTkButton(options_frame, text="Partie", width=200, command=open_partie)
son_button = ctk.CTkButton(options_frame, text="Son", width=200, command=open_son)
profil_button = ctk.CTkButton(options_frame, text="Profil", width=200, command=open_profil)

partie_button.place(x=100, y=20)
son_button.place(x=350, y=20)
profil_button.place(x=600, y=20)

save_button = ctk.CTkButton(options_frame, text="Sauvegarder")
load_button = ctk.CTkButton(options_frame, text="Charger une partie")
reset_button = ctk.CTkButton(options_frame, text="Réinitialiser la partie")

music_label = ctk.CTkLabel(options_frame, text="Musique")
music_slider = ctk.CTkSlider(options_frame)
effects_label = ctk.CTkLabel(options_frame, text="Effets Sonores")
effects_slider = ctk.CTkSlider(options_frame)

name_label = ctk.CTkLabel(options_frame, text="Nom:")
name_entry = ctk.CTkEntry(options_frame)
currency_label = ctk.CTkLabel(options_frame, text="Monnaie:")
currency_dropdown = ctk.CTkComboBox(options_frame, values=["€", "$", "£"])

def close_options():
    show_game_interface()

back_button = ctk.CTkButton(options_frame, text="←", width=50, command=close_options)
back_button.place(x=1200, y=20)

start_progress()
afficher_machines()
root.mainloop()
