
import customtkinter as ctk
from PIL import Image, ImageTk

def creer_labels_profil(root, joueur):
    # Profil du joueur (cadre principal)
    profile_frame = ctk.CTkFrame(root, width=600, height=325, corner_radius=10, fg_color="#FFA500")
    profile_frame.place(x=10, y=10)


    # Ajout de l'image du joueur
    image_path = "Images/qatari_boss.png"  # Assurez-vous que l'image est dans le dossier 'Images'
    image = Image.open(image_path)  # Charger l'image
    photo_de_profil = ctk.CTkImage(light_image=image, size=(80, 80))  # Création de l'image avec Pillow

    # Affichage de l'image dans le label
    profile_image_label = ctk.CTkLabel(profile_frame, text="", image=photo_de_profil)
    profile_image_label.place(x=20, y=20)  # Positionner l'image
   


    # Nom et entreprise
    profile_label = ctk.CTkLabel(profile_frame, text=joueur.nom, font=("Arial", 16), text_color="black")
    entreprise_label = ctk.CTkLabel(profile_frame, text=joueur.entreprise, font=("Arial", 12), text_color="black")


    # Argent du joueur
    argent_label = ctk.CTkLabel(profile_frame, text="Argent:", font=("Arial", 12), text_color="black")
    argent_value = ctk.CTkLabel(profile_frame, text=f"{joueur.argent} €", font=("Arial", 12), text_color="black")

    # Jour actuel
    jour_label = ctk.CTkLabel(profile_frame, text="Jour actuel:", font=("Arial", 12), text_color="black")
    jour_value = ctk.CTkLabel(profile_frame, text=f"{joueur.jour_actuel}", font=("Arial", 12), text_color="black")

    # Revenu par période
    revenu_label = ctk.CTkLabel(profile_frame, text="Revenu par période:", font=("Arial", 12), text_color="black")
    revenu_value = ctk.CTkLabel(profile_frame, text=f"{joueur.calculer_revenu()} €", font=("Arial", 12), text_color="black")

    # Coûts fixes
    couts_fixes_label = ctk.CTkLabel(profile_frame, text="Coûts fixes:", font=("Arial", 12), text_color="black")
    couts_fixes_value = ctk.CTkLabel(profile_frame, text=f"{joueur.calculer_couts_fixes()} €", font=("Arial", 12), text_color="black")

    # Solde net
    solde_net_label = ctk.CTkLabel(profile_frame, text="Solde net:", font=("Arial", 12), text_color="black")
    solde_net_value = ctk.CTkLabel(profile_frame, text=f"{joueur.calculer_solde_net()} €", font=("Arial", 12), text_color="black")
     # Nom et entreprise
    profile_label.place(x=120, y=20)
    entreprise_label.place(x=120, y=60)

    # Argent du joueur
    argent_label.place(x=120, y=100)
    argent_value.place(x=250, y=100)

    # Jour actuel
    jour_label.place(x=120, y=130)
    jour_value.place(x=250, y=130)

    # Revenu par période
    revenu_label.place(x=120, y=160)
    revenu_value.place(x=250, y=160)

    # Coûts fixes
    couts_fixes_label.place(x=120, y=190)
    couts_fixes_value.place(x=250, y=190)

    # Solde net
    solde_net_label.place(x=120, y=220)
    solde_net_value.place(x=250, y=220)

    return {
        "argent_value": argent_value,
        "jour_value": jour_value,
        "revenu_value": revenu_value,
        "couts_fixes_value": couts_fixes_value,
        "solde_net_value": solde_net_value,
    }
