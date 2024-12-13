"""
Module Technician pour la gestion des techniciens dans RepairRush.

Ce fichier contient la classe `Technician` et les méthodes nécessaires pour gérer les techniciens,
leurs interactions avec les machines et leurs statuts.
"""
import customtkinter as ctk
from customtkinter import CTkButton, CTkFrame, CTkLabel
from PIL import Image, ImageTk
from modules.NotificationsManager import get_global_notifications_manager

class Technician:
    """
    Classe représentant un technicien dans le jeu.

    Attributs :
        nom (str) : Nom du technicien.
        specialite (str) : Spécialité du technicien (Mécanique, Électrique, Informatique).
        niveau (str) : Niveau d'expertise (Débutant, Moyen, Expert).
        salaire (int) : Salaire du technicien.
        facteur_reparation (float) : Facteur influençant la durée de réparation.
        image_path (str) : Chemin de l'image du technicien.
        assigned_machine (Machine) : Machine actuellement assignée (None si non assigné).
        machine_image_label (CTkLabel) : Label pour afficher une image sur la machine associée.
    """

    def __init__(self, nom, specialite, niveau, salaire, facteur_reparation, image_path):
        """
        Initialise un technicien.

        Args :
            nom (str) : Nom du technicien.
            specialite (str) : Spécialité du technicien.
            niveau (str) : Niveau d'expertise.
            salaire (int) : Salaire du technicien.
            facteur_reparation (float) : Facteur influençant la durée de réparation.
            image_path (str) : Chemin de l'image du technicien.
        """
        self.nom = nom
        self.specialite = specialite
        self.niveau = niveau
        self.salaire = salaire
        self.facteur_reparation = facteur_reparation
        self.image_path = image_path
        self.assigned_machine = None
        self.machine_image_label = None

    def assign_to_machine(self, machine, assign_button, joueur, tech_frame):
        """
        Assigne le technicien à une machine compatible.

        Args :
            machine (Machine) : Machine à assigner.
            assign_button (CTkButton) : Bouton pour gérer l'affectation.
            joueur (Joueur) : Instance du joueur.
            tech_frame : Cadre contenant le technicien.

        Returns :
            bool : True si l'affectation réussit, False sinon.
        """
        manager = get_global_notifications_manager()

        if self.assigned_machine is not None:
            if manager:
                manager.ajouter_notification(f"{self.nom} est déjà assigné à une machine.")
            return False

        if self.specialite != machine.type_machine:
            if manager:
                manager.ajouter_notification(
                    f"{self.nom} ne peut pas être assigné à la machine {machine.nom} ({machine.niveau_machine})."
                )
            return False

        self.assigned_machine = machine
        machine.technicien = self
        if manager:
            manager.ajouter_notification(
                f"{self.nom} a été assigné à la machine {machine.nom} ({machine.niveau_machine})."
            )

        assign_button.configure(
            text="Désaffecter", 
            command=lambda: self.unassign_from_machine(assign_button, joueur)
        )

        if not machine.en_reparation_flag:
            machine.repair_button.configure(state="normal")
        return True

    def unassign_from_machine(self, assign_button=None, joueur=None):
        """
        Désassigne le technicien de la machine actuelle.

        Args :
            assign_button (CTkButton) : Bouton à mettre à jour après désaffectation.
            joueur (Joueur) : Instance du joueur.

        Returns :
            bool : True si la désaffectation réussit, False sinon.
        """
        manager = get_global_notifications_manager()

        if self.assigned_machine is None:
            if manager:
                manager.ajouter_notification(f"{self.nom} n'est pas assigné à une machine.")
            return False

        if self.assigned_machine.en_reparation_flag:
            if manager:
                manager.ajouter_notification(
                    f"{self.nom} ne peut pas être désassigné car la machine {self.assigned_machine.nom} est en réparation."
                )
            return False

        if manager:
            manager.ajouter_notification(
                f"{self.nom} a été désassigné de la machine {self.assigned_machine.nom}."
            )

        # Désassigner le technicien de la machine
        self.assigned_machine.technicien = None
        self.assigned_machine = None

        if assign_button:
            assign_button.configure(
                text="Attribuer", 
                command=lambda: open_assign_window(self, joueur, assign_button)
            )

        # Supprimer l'image associée à la machine
        if self.machine_image_label:
            self.machine_image_label.place_forget()
            self.machine_image_label = None

        return True

    def engager(self, joueur, progression_jour=1.5):
        """
        Engage le technicien avec un coût basé sur le temps restant dans la journée.

        Args :
            joueur (Joueur) : Instance du joueur.
            progression_jour (float) : Fraction de la journée restante (entre 0 et 1).

        Returns :
            bool : True si l'engagement réussit, False sinon.
        """
        cout_restant = self.salaire * progression_jour
        if joueur.argent >= cout_restant:
            joueur.argent -= int(cout_restant)
            joueur.techniciens_possedes.append(self)
            return True
        return False

    def licencier(self, joueur):
        """
        Licencie le technicien.

        Args :
            joueur (Joueur) : Instance du joueur.

        Returns :
            bool : True si le licenciement réussit, False sinon.
        """
        manager = get_global_notifications_manager()

        if self in joueur.techniciens_possedes:
            joueur.techniciens_possedes.remove(self)
            joueur.trigger_ui_update()

            if manager:
                manager.ajouter_notification(f"{self.nom} licencié.")
            return True

        if manager:
            manager.ajouter_notification(
                f"{self.nom} n'est pas engagé, donc ne peut pas être licencié."
            )
        return False

technicians = [
    Technician("Rémy Tourneur", "Mécanique", "Débutant", 800, 1.5, 'images/Tech1.png'),
    Technician("Jack Soudey", "Mécanique", "Moyen", 1500, 1.2, 'images/Tech2.png'),
    Technician("Claude Piston", "Mécanique", "Expert", 2500, 1.0, 'images/Tech6.png'),
    Technician("Hubert Volt", "Électrique", "Débutant", 1000, 1.5, 'images/Tech3.png'),
    Technician("Fred Fraiseuse", "Électrique", "Moyen", 1800, 1.2, 'images/Tech5.png'),
    Technician("Léon Laser", "Électrique", "Expert", 3000, 1.0, 'images/Tech9.png'),
    Technician("Alex Byte", "Informatique", "Débutant", 1200, 1.5, 'images/Tech7.png'),
    Technician("Lucas Pixel", "Informatique", "Moyen", 2200, 1.2, 'images/Tech4.png'),
    Technician("Dave Data", "Informatique", "Expert", 4000, 1.0, 'images/Tech8.png')
]
# Dictionnaire global pour les boutons d'engagement
engagement_buttons = {}

def update_engaged_frame(engaged_frame, joueur, argent_label, engagement_buttons):
    """
    Met à jour l'affichage des techniciens engagés.

    Args :
        engaged_frame (CTkFrame) : Cadre contenant les techniciens engagés.
        joueur (Joueur) : Instance du joueur.
        argent_label (CTkLabel) : Label pour afficher l'argent du joueur.
        engagement_buttons (dict) : Boutons d'engagement des techniciens.
    """
    # Effacer les widgets existants
    for widget in engaged_frame.winfo_children():
        widget.destroy()

    # Ajouter un cadre pour chaque technicien engagé
    for idx, technician in enumerate(joueur.techniciens_possedes):
        tech_frame = CTkFrame(engaged_frame, width=180, height=150, fg_color="#444444", corner_radius=10)
        tech_frame.grid(row=0, column=idx, padx=10, pady=10)

        # Image du technicien
        image = Image.open(technician.image_path).resize((60, 60))
        tech_image = ImageTk.PhotoImage(image)
        image_label = CTkLabel(tech_frame, text="", image=tech_image)
        image_label.image = tech_image
        image_label.pack(pady=5)

        # Nom du technicien
        name_label = CTkLabel(tech_frame, text=technician.nom, font=("Arial", 10))
        name_label.pack()

        # Bouton pour assigner ou désassigner le technicien
        assign_button = CTkButton(tech_frame, font=("Arial", 10))
        if technician.assigned_machine is None:
            assign_button.configure(
                text="Attribuer",
                command=lambda tech=technician, btn=assign_button: open_assign_window(tech, joueur, btn)
            )
        else:
            assign_button.configure(
                text="Désaffecter",
                command=lambda tech=technician, btn=assign_button: tech.unassign_from_machine(btn, joueur)
            )
        assign_button.pack(pady=5)

        # Bouton pour licencier le technicien
        def licencier_technicien(tech=technician):
            manager = get_global_notifications_manager()
            if tech in joueur.techniciens_possedes:
                # Vérifier si le technicien est assigné à une machine en réparation
                if tech.assigned_machine is not None:
                    if tech.assigned_machine.en_reparation_flag:
                        if manager:
                            manager.ajouter_notification(
                                f"{tech.nom} ne peut pas être licencié car la machine {tech.assigned_machine.nom} ({tech.assigned_machine.niveau_machine}) est en réparation."
                            )
                        return False
                    tech.unassign_from_machine(None, None)
                joueur.techniciens_possedes.remove(tech)
                update_engaged_frame(engaged_frame, joueur, argent_label, engagement_buttons)
                engagement_buttons[tech].configure(state="normal")
                if manager:
                    manager.ajouter_notification(f"{tech.nom} licencié.")
                return True
            if manager:
                manager.ajouter_notification(
                    f"{tech.nom} n'est pas engagé, donc ne peut pas être licencié."
                )
            return False

        fire_button = CTkButton(tech_frame, text="Licencier", font=("Arial", 10), command=licencier_technicien)
        fire_button.pack(pady=5)

def engager_technicien(technicien, joueur, engaged_frame, argent_label, engagement_buttons, button=None):
    """
    Engage un technicien, soustrait le coût et met à jour l'interface.

    Args :
        technicien (Technician) : Technicien à engager.
        joueur (Joueur) : Instance du joueur.
        engaged_frame (CTkFrame) : Cadre des techniciens engagés.
        argent_label (CTkLabel) : Label affichant l'argent.
        engagement_buttons (dict) : Boutons d'engagement.
        button (CTkButton) : Bouton pour ce technicien (facultatif).
    """
    manager = get_global_notifications_manager()
    salaire_proportionnel = int(technicien.salaire * 1.5)  # Coût d'engagement

    if len(joueur.techniciens_possedes) < 6 and technicien not in joueur.techniciens_possedes:
        if joueur.argent >= salaire_proportionnel:
            joueur.argent -= salaire_proportionnel
            if technicien.engager(joueur):
                joueur.trigger_ui_update()
                update_engaged_frame(engaged_frame, joueur, argent_label, engagement_buttons)
                if button:
                    button.configure(state="disabled")
                if manager:
                    manager.ajouter_notification(
                        f"{technicien.nom} engagé pour {salaire_proportionnel} €."
                    )
        else:
            if manager:
                manager.ajouter_notification(
                    f"Pas assez d'argent pour engager {technicien.nom} (coût : {salaire_proportionnel} €)."
                )
    else:
        if manager:
            manager.ajouter_notification(
                "Nombre maximum de techniciens atteint ou technicien déjà engagé !"
            )

def open_assign_window(technician, joueur, assign_button):
    """
    Ouvre une fenêtre pour assigner un technicien à une machine.

    Args :
        technician (Technician) : Technicien à assigner.
        joueur (Joueur) : Instance du joueur.
        assign_button (CTkButton) : Bouton de gestion d'assignation.
    """
    from .Machines import machines_possedees

    assign_window = ctk.CTkToplevel()
    assign_window.title("Attribuer un technicien à une machine")
    assign_window.geometry("400x300+1400+570")
    assign_window.transient()
    assign_window.grab_set()
    assign_window.focus_force()

    CTkLabel(assign_window, text=f"Attribuer {technician.nom} à une machine", font=("Arial", 14)).pack(pady=10)

    for machine in machines_possedees:
        machine_button = CTkButton(
            assign_window,
            text=f"{machine.nom} ({machine.niveau_machine})",
            command=lambda m=machine: assign_technician_to_machine(technician, m, assign_window, assign_button, joueur)
        )
        machine_button.pack(pady=5)

def assign_technician_to_machine(technician, machine, window, assign_button, joueur):
    """
    Assigne un technicien à une machine depuis la fenêtre d'attribution.

    Args :
        technician (Technician) : Technicien à assigner.
        machine (Machine) : Machine à laquelle le technicien est assigné.
        window (CTkToplevel) : Fenêtre d'attribution.
        assign_button (CTkButton) : Bouton de gestion d'assignation.
        joueur (Joueur) : Instance du joueur.
    """
    manager = get_global_notifications_manager()

    if machine.technicien is not None:
        if manager:
            manager.ajouter_notification(
                f"La machine {machine.nom} ({machine.niveau_machine}) est déjà assignée."
            )
        return

    if technician.assign_to_machine(machine, assign_button, joueur, tech_frame=None):
        assign_button.configure(
            text="Désaffecter",
            command=lambda tech=technician, btn=assign_button: tech.unassign_from_machine(btn, joueur)
        )
        window.destroy()
    else:
        if manager:
            manager.ajouter_notification(
                f"Impossible d'assigner {technician.nom} à la machine {machine.nom} ({machine.niveau_machine})."
            )