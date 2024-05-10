from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color
import Connection
import ListeExercices
import AjouterExercice
class SupprinerExercice(App):
    def build(self):
        pass

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
