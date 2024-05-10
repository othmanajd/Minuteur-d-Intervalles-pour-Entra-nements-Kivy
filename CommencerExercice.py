from kivy.app import App
from kivy.clock import Clock
import Connection
from Serie import  ListeSerie
from Exercices import AjouterExercice,SupprinerExercice

class CommencerExercice(App):
    def build(self):
        # Connexion à la base de données MySQL
        self.conn = Connection.connection()
        self.cursor = self.conn.cursor()

        # Charger les données des exercices
        self.load_exercises()
        self.nouveauExo()
        self.commencerExo()

        return self.root

    def load_exercises(self):
        self.exercises = []
        self.cursor.execute("SELECT nom, tempexercice, tempRepo FROM exercice")
        self.exercises = self.cursor.fetchall()

    def start_pose(self, dt=None):
        self.fct = 1
        self.repos -= 1
        if self.repos >= 0:
            self.modifier_label(self.exercise_name, self.repos)
            Clock.schedule_once(self.start_pose, 1)
        else:
            self.nouveauExo()
            Clock.schedule_once(self.commencerExo, 0)  # Démarrer le prochain exercice sans délai

    def commencerExo(self, dt=None):
        self.fct = 2
        self.modifier_label(self.exercise_name, self.exercise_time)
        self.exercise_time -= 1
        if self.exercise_time >= -1:
            Clock.schedule_once(self.commencerExo, 1)
        else:
            self.nouveauExo()
            Clock.schedule_once(self.start_pose, 0)  # Commencer le repos sans délai

    def nouveauExo(self):
        if self.exercises:
            exercise = self.exercises.pop(0)
            self.exercise_name, exercise_time, self.repos = exercise
            self.exercise_time = int(exercise_time)
            self.repos = int(self.repos) + 1
        else:
            Clock.unschedule(self.start_pose)
            Clock.unschedule(self.commencerExo)
            self.root.ids.remaining_time_label.text = 'Terminé'

    def modifier_label(self, nom, temps):
        self.root.ids.nom_label.text = str(nom)
        hours = temps // 3600
        minutes = (temps % 3600) // 60
        seconds = temps % 60
        temps = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.root.ids.remaining_time_label.text = temps

    def stop(self):
        if self.fct == 2:
            Clock.unschedule(self.commencerExo)
        else:
            Clock.unschedule(self.start_pose)
        # Masquer le bouton "Continuer" et afficher le bouton "Arrêter"
        self.root.ids.stop_button.opacity = 0
        self.root.ids.continue_button.pos_hint = {'center_x': 0.2, 'center_y': 0.3}
        self.root.ids.stop_button.pos_hint = {'center_x': 0.5, 'center_y': 0.3}
        self.root.ids.continue_button.opacity = 1

    def continuer(self):
        if self.fct == 2:
            Clock.schedule_once(self.commencerExo, 1)
        else:
            Clock.schedule_once(self.start_pose, 1)
        # Masquer le bouton "Continuer" et afficher le bouton "Arrêter"
        self.root.ids.continue_button.opacity = 0
        self.root.ids.continue_button.pos_hint = {'center_x': 0.5, 'center_y': 0.3}
        self.root.ids.stop_button.pos_hint = {'center_x': 0.2, 'center_y': 0.3}
        self.root.ids.stop_button.opacity = 1

    def restart(self):
        self.load_exercises()
        self.nouveauExo()
    def exerciceListe(self):
        self.stop()
        ListeSerie().run()
    def ajouterExercice(self):
        self.stop()
        AjouterExercice().run()
    def supprimerExercice(self):
        self.stop()
        SupprinerExercice().run()