from kivy.app import App
from kivy.core.window import Window
from Serie import ListeSerie
import id
Window.size = (500, 600)
class Accueil(App):
    def build(self):
        self.title = "Minuteur d'Intervalles pour Entraînements"

    def Commencer(self):
        print(id.user_id)  # Utilisez id au lieu de globals
        self.stop()
        ListeSerie().run()
