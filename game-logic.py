import customtkinter as ctk
import sound_manager as sm
import time
import threading

# Instanciation de SoundManager
sound_manager = sm.SoundManager()
# son de la caisse
def play_sound():
    sound_manager.playsound('./sounds/ca-ching.mp3')  # Remplace par le chemin correct de ton fichier son

# Créer la fenêtre principale
root = ctk.CTk()
root.title("Barre de progression")
root.geometry("400x200")

# Initialiser une barre de progression
progress_bar = ctk.CTkProgressBar(master=root, width=300, height=30, progress_color='green')
progress_bar.place(relx=0.5, rely=0.5, anchor='center')

# Fonction pour mettre à jour la barre de progression
def update_progress_bar():
    while True:
        for i in range(3001):  # 31 étapes pour 30 secondes
            progress_bar.set(i / 3000)  # Met à jour la barre (0 à 1)
            time.sleep(0.001)  # Attend 1 seconde entre chaque étape
        play_sound()
        progress_bar.set(0)  # Réinitialise la barre

# Lancer la barre de progression dans un thread séparé
def start_progress():
    threading.Thread(target=update_progress_bar).start()
# Fonction pour fermer la fenêtre
def close_window():
    root.destroy()

# Créer le bouton de fermeture
close_button = ctk.CTkButton(master=root, text="Fermer", command=close_window)
close_button.place(relx=0.5, rely=0.8, anchor='center')  # Positionne le bouton en bas au centre

# Démarrer la progression au lancement de l'application
start_progress()

# Boucle principale de l'application Tkinter
root.mainloop()

