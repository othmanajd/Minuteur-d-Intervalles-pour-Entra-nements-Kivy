from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
import Connection
from kivy.clock import Clock
import id
Window.size = (500, 600)
class ListeSerie(App):
    def build(self):
        root = Builder.load_string('''
FloatLayout:
    canvas.before:
        Color:
            rgb: 1, 1, 1  # Couleur de fond de l'ensemble de la fenêtre
        Rectangle:
            source: 'k.png'  # Image de fond
            size: self.size  # Taille de l'image correspondant à la taille de la fenêtre
            pos: self.pos  # Position de l'image

    ActionBar:
        pos_hint: {'top': 1}  # Positionne l'ActionBar en haut de la page
        ActionView:
            use_separator: True
            ActionPrevious:
                title: ''
            ActionButton:
                text: "series"  
            ActionButton:
                text: "ajoutre serie"
                on_press: app.ajouterSerie()
            ActionButton:
                text: "Supprimer serie"
                on_press: app.supprimerSerie()
    GridLayout:
        id: grid
        cols: 5  # Augmenter le nombre de colonnes pour inclure la colonne "Edit"
        row_default_height: '40dp'
        row_force_default: True
        size_hint_y: None
        height: self.minimum_height
        pos_hint: {'x': 0.001, 'center_y': 0.75}  # Positionne la table au centre de l'écran
        spacing:0
''')

        self.populate_grid(root.ids.grid)
        return root

    def populate_grid(self, grid):
        # Ajout des titres de colonnes
        titles = ['ID', 'Nom', 'Exercices', 'Repos', 'Edit']
        for title in titles:
            label = Label(text=title, size_hint_x=None, width='100dp', color=(0, 0, 0, 1))
            label.canvas.before.add(Color(236, 116, 178, 1))  # Couleur de fond
            grid.add_widget(label)

        conn = Connection.connection()
        cursor = conn.cursor()
        cursor.execute("USE MyApp")
        cursor.execute("SELECT * FROM serie")
        series = cursor.fetchall()
        conn.close()

        for serie in series:
            for field in serie:
                label = Label(text=str(field), size_hint_x=None, width='100dp', color=(0, 0, 0, 1))
                grid.add_widget(label)
            button = Button(text="Commencer", 
                            size_hint_x=None, width='100dp',
                            background_color=(0, 0, 0, 0),
                            on_press=self.commencerSerie, 
                            color=(0, 0, 70, 1)
                            )
            button.id = str(serie[0])
            grid.add_widget(button)

    def ajouterSerie(self):
        self.stop()
        AjouterSerie().run()
   
    def commencerSerie(self, instance):
        id.serie_id = instance.id
        self.stop()
        ListeExercices().run()

    def supprimerSerie(self):
        self.stop()
        SupprimerSerie().run()
class SupprimerSerie(App):
    def build(self):
        root = Builder.load_string('''
FloatLayout:
    canvas.before:
        Color:
            rgb: 1, 1, 1  # Couleur de fond de l'ensemble de la fenêtre
        Rectangle:
            source: 'k.png'  # Image de fond
            size: self.size  # Taille de l'image correspondant à la taille de la fenêtre
            pos: self.pos  # Position de l'image

    ActionBar:
        pos_hint: {'top': 1}  # Positionne l'ActionBar en haut de la page
        ActionView:
            use_separator: True
            ActionPrevious:
                title: ''
            ActionButton:
                text: "series"
                on_press: app.listeSerie()  
            ActionButton:
                text: "ajoutre serie"
                on_press: app.ajouterSerie()
            ActionButton:
                text: "Supprimer serie"
    GridLayout:
        id: grid
        cols: 5  # Augmenter le nombre de colonnes pour inclure la colonne "Edit"
        row_default_height: '40dp'
        row_force_default: True
        size_hint_y: None
        height: self.minimum_height
        pos_hint: {'x': 0.001, 'center_y': 0.75}  # Positionne la table au centre de l'écran
        spacing:0
''')

        self.populate_grid(root.ids.grid)
        return root
    def populate_grid(self, grid):
    # Ajout des titres de colonnes
        titles = ['ID', 'Nom', 'Exercices', 'Repos', 'Edit']
        for title in titles:
           label = Label(text=title, size_hint_x=None, width='100dp', color=(0, 0, 0, 1))
           label.canvas.before.add(Color(236, 116, 178, 1))  # Couleur de fond
           grid.add_widget(label)

        conn = Connection.connection()
        cursor = conn.cursor()
        cursor.execute("USE MyApp")
        cursor.execute("SELECT * FROM serie")
        series = cursor.fetchall()
        conn.close()

        for serie in series:
            for field in serie:
                label = Label(text=str(field),
                            size_hint_x=None, 
                            width='100dp', 
                            color=(0, 0, 0, 1)
                            )
                grid.add_widget(label)
            button = Button(text="Supprimer", 
                size_hint_x=None, width='100dp',
                background_color=(0, 0, 0, 0),
                on_press=self.supprimerSerie,
                color=(0, 0, 70, 1)
                )
            button.id = str(serie[0]) 
            grid.add_widget(button)
    def supprimerSerie(self, instance):
        series_id = instance.id
        conn = Connection.connection()
        cursor = conn.cursor()
        cursor.execute("USE MyApp")
        cursor.execute("DELETE FROM serie WHERE id = %s", (series_id,))
        conn.commit()
        conn.close()
        parent_widget = instance.parent
        parent_widget.remove_widget(instance)
    def ajouterSerie(self):
        self.stop()
        AjouterSerie().run()
    def listeSerie(self):
        self.stop()
        ListeSerie().run()

class AjouterSerie(App):
    def build(self):
        self.title = "Minuteur d'Intervalles pour Entraînements"
        self.error_label = self.root.ids.error_label
        pass
    def ajouterseriebd(self,nom, nbrexo,repo):
        if( not nom or not nbrexo or not repo):
            self.error_label.text = "Remplire tout les informatiom."
        else:
            conn=Connection.connection()
            cursor = conn.cursor()
            cursor.execute("USE MyApp")
    # Exécutez votre requête d'insertion ici
            cursor.execute("INSERT INTO serie (nom , nbrexercice , tempRepos) VALUES (%s, %s, %s)", (nom, nbrexo, repo))
            conn.commit()  # N'oubliez pas de commettre les modifications
            conn.close()
    def serieListe(self):
        self.stop()
        ListeSerie().run()
    def SupprimerListe(self):
        self.stop()
        SupprimerSerie().run()

class ListeExercices(App):
    def build(self):
        root = Builder.load_string('''
FloatLayout:
    canvas.before:
        Color:
            rgb: 1, 1, 1  # Couleur de fond de l'ensemble de la fenêtre
        Rectangle:
            source: 'k.png'  # Image de fond
            size: self.size  # Taille de l'image correspondant à la taille de la fenêtre
            pos: self.pos  # Position de l'image

    ActionBar:
        pos_hint: {'top': 1}  # Positionne l'ActionBar en haut de la page
        ActionView:
            use_separator: True
            ActionPrevious:
                title: ''
                on_press: app.listeSerie()  
            ActionButton:
                text: "Exercices"
            ActionButton:
                text: "ajoute Exercice"
                on_press: app.ajouterExercice()
            ActionButton:
                text: "Supprimer Exercice"
                on_press: app.supprinerExercice()
    Button:
        id: restart_button  # Attribuez un ID au bouton "Recommencer"
        text: "Commencer La Serie"
        size_hint: None, None
        size: 240, 100
        pos_hint: {'center_x': 0.5, 'center_y': 0.85}
        background_color: 0, 0, 0, 0
        on_press: app.commencerExercice(self)
        color:(0, 0, 70, 1)
    GridLayout:
        id: grid
        cols: 3  # Augmenter le nombre de colonnes pour inclure la colonne "Edit"
        row_default_height: '40dp'
        row_force_default: True
        size_hint_y: None
        height: self.minimum_height
        pos_hint: {'x': 0.001, 'center_y': 0.7}  # Positionne la table au centre de l'écran
        spacing:0
''')

        self.populate_grid(root.ids.grid)
        return root

    def populate_grid(self, grid):
    # Ajout des titres de colonnes
        titles = ['Nom', 'temps', 'Repos']
        for title in titles:
           label = Label(text=title, size_hint_x=None, width='166dp', color=(0, 0, 0, 1))
           label.canvas.before.add(Color(236, 116, 178, 1))  # Couleur de fond
           grid.add_widget(label)

        conn = Connection.connection()
        cursor = conn.cursor()
        cursor.execute("USE MyApp")
        cursor.execute("SELECT nom, tempExercice, tempRepo, id FROM exercice")
        exercises = cursor.fetchall()
        conn.close()
        for exercise in exercises:
            nom, tempExercice, tempRepo, id_exercise = exercise
            label_nom = Label(text=str(nom), size_hint_x=None, width='166dp', color=(0, 0, 0, 1))
            label_temp_exo = Label(text=str(tempExercice), size_hint_x=None, width='166dp', color=(0, 0, 0, 1))
            label_temp_repo = Label(text=str(tempRepo), size_hint_x=None, width='166dp', color=(0, 0, 0, 1))
            grid.add_widget(label_nom)
            grid.add_widget(label_temp_exo)
            grid.add_widget(label_temp_repo)
            
    def commencerExercice(self, instance):
        print("hhhh")
        self.stop()
        CommencerExercice().run()
    def supprinerExercice(self):
        self.stop()
        SupprimerExercice().run()
    def listeSerie(self):
        self.stop()
        ListeSerie().run()
    def ajouterExercice(self):
        self.stop()
        AjouterExercice().run()






class SupprimerExercice(App):
    def build(self):
        root = Builder.load_string('''
FloatLayout:
    canvas.before:
        Color:
            rgb: 1, 1, 1  # Couleur de fond de l'ensemble de la fenêtre
        Rectangle:
            source: 'k.png'  # Image de fond
            size: self.size  # Taille de l'image correspondant à la taille de la fenêtre
            pos: self.pos  # Position de l'image

    ActionBar:
        pos_hint: {'top': 1}  # Positionne l'ActionBar en haut de la page
        ActionView:
            use_separator: True
            ActionPrevious:
                title: ''
                on_press: app.listExecices()  
            ActionButton:
                text: "Exercices"
                on_press: app.listExecices()
            ActionButton:
                text: "ajoute Exercice"
                on_press: app.ajouterExercice()
            ActionButton:
                text: "Supprimer Exercice"
    GridLayout:
        id: grid
        cols: 4  # Augmenter le nombre de colonnes pour inclure la colonne "Edit"
        row_default_height: '40dp'
        row_force_default: True
        size_hint_y: None
        height: self.minimum_height
        pos_hint: {'x': 0.001, 'center_y': 0.8}  # Positionne la table au centre de l'écran
        spacing:0
''')

        self.populate_grid(root.ids.grid)
        return root

    def populate_grid(self, grid):
    # Ajout des titres de colonnes
        titles = ['Nom', 'temps', 'Repos', 'Edit']
        for title in titles:
           label = Label(text=title, size_hint_x=None, width='125dp', color=(0, 0, 0, 1))
           label.canvas.before.add(Color(236, 116, 178, 1))  # Couleur de fond
           grid.add_widget(label)

        conn = Connection.connection()
        cursor = conn.cursor()
        cursor.execute("USE MyApp")
        cursor.execute("SELECT nom, tempExercice, tempRepo, id FROM exercice")
        exercises = cursor.fetchall()
        conn.close()
        for exercise in exercises:
            nom, tempExercice, tempRepo, id_exercise = exercise
            label_nom = Label(text=str(nom), size_hint_x=None, width='125dp', color=(0, 0, 0, 1))
            label_temp_exo = Label(text=str(tempExercice), size_hint_x=None, width='125dp', color=(0, 0, 0, 1))
            label_temp_repo = Label(text=str(tempRepo), size_hint_x=None, width='125dp', color=(0, 0, 0, 1))
            grid.add_widget(label_nom)
            grid.add_widget(label_temp_exo)
            grid.add_widget(label_temp_repo)
            
            button = Button(text="Supprimer", 
                size_hint_x=None, width='100dp',
                background_color=(0, 0, 0, 0),
                on_press=self.supprimerExercice,
                color=(0, 0, 70, 1)
            )
            button.id = str(exercise[3]) 
            grid.add_widget(button)
    def listExecices(self):
        self.stop()
        ListeExercices().run()
    def ajouterExercice(self):
        self.stop()
        AjouterExercice().run()
    def supprimerExercice(self, instance):
        exercice_id = instance.id
        conn = Connection.connection()
        cursor = conn.cursor()
        cursor.execute("USE MyApp")
        cursor.execute("DELETE FROM exercice WHERE id = %s", (exercice_id,))
        conn.commit()
        conn.close()
        parent_widget = instance.parent
        parent_widget.remove_widget(instance)



class AjouterExercice(App):
    def build(self):
       pass
    def supprimerExercice(self):
        self.stop()
        SupprimerExercice().run()
    def exerciceListe(self):
        self.stop()
        ListeExercices().run()
    def ajouterExercicebd(self,nom, temps,repo):
        conn = Connection.connection() 
        cursor = conn.cursor()
        cursor.execute("USE MyApp")  
        cursor.execute("INSERT INTO exercice (nom, tempExercice, tempRepo,idSerie) VALUES (%s, %s, %s, %s)", (nom, temps, repo ,id.serie_id))
        conn.commit()  
        conn.close()  





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
        self.cursor.execute("USE MyApp")
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
        self.commencerExo()

    def exerciceListe(self):
        self.stop()
        ListeSerie().run()
    def ajouterExercice(self):
        self.stop()
        AjouterExercice().run()
    def supprimerExercice(self):
        self.stop()
        SupprimerExercice().run()

if __name__ == '__main__':
    CommencerExercice().run()
