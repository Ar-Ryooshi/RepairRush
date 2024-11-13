from Machines import machines_disponibles, machines_possedees

class Joueur:
    def __init__(self, nom, entreprise, argent=100000):
        self.nom = nom
        self.entreprise = entreprise
        self.argent = argent
        self.jour_actuel = 1
        self.machines_possedees = machines_possedees  # Initialiser avec les machines de départ
        self.techniciens_possedes = []
        self.periodes_ecoulees = 0

    def calculer_revenu(self):
        revenu_total = sum(machine.revenu_par_periode for machine in self.machines_possedees)
        return revenu_total

    def calculer_couts_fixes(self):
        couts_fixes = sum(technicien.salaire for technicien in self.techniciens_possedes)
        return couts_fixes

    def calculer_solde_net(self):
        revenu_total = self.calculer_revenu()
        couts_fixes = self.calculer_couts_fixes()
        return revenu_total - couts_fixes
    
    
    def acheter_machine(self, machine):
        if self.argent >= machine.cout_achat:
            self.argent -= machine.cout_achat
            self.machines_possedees.append(machine)  # Ajouter la machine aux machines possédées
            machines_disponibles.remove(machine)  # Retirer la machine de la liste des machines disponibles
            return True
        return False

    
    def incrementer_jour(self):
        """Incrémente le jour après 4 périodes."""
        self.periodes_ecoulees += 1
        if self.periodes_ecoulees >= 4:
            self.jour_actuel += 1
            self.periodes_ecoulees = 0
            print(f"Jour {self.jour_actuel} atteint.")

    def ajouter_revenu(self):
        """Ajoute le revenu des machines au total de l'argent du joueur."""
        revenu = self.calculer_revenu()
        self.argent += revenu
        print(f"Revenu de {revenu} ajouté. Argent total : {self.argent}")
