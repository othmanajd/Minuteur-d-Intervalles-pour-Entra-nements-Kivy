from kivy.app import App
import Connection
import  SupprinerExercice
import  ListeExercices
class AjouterExercice(App):
    def build(self):
       pass
    def supprimerExercice(self):
        self.stop()
        SupprinerExercice().run()
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