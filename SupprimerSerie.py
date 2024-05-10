from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.graphics import Color
import Connection
from AjouterSerie import AjouterSerie
from ListeSerie import  ListeSerie
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
if __name__ == '__main__':
    SupprimerSerie().run()