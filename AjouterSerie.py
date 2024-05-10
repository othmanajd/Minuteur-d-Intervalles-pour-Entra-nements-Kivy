from kivy.app import App
import Connection
import ListeSerie
import SupprimerSerie
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