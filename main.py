
import json
import os
import shutil

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup


class VortexApp(App):

    def build(self):
        self.total = 0
        self.ventes = []

        ancien_fichier = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "ventes_vortex.json"
        )

        self.fichier = os.path.join(
            self.user_data_dir,
            "ventes_vortex.json"
        )

        if not os.path.exists(self.fichier):
            if os.path.exists(ancien_fichier):
                shutil.copy2(ancien_fichier, self.fichier)

        self.charger_ventes()

        ecran = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        titre = Label(
            text="VORTEX VENTES",
            font_size=28,
            size_hint_y=None,
            height=60
        )

        self.resultat = Label(
            text="TOTAL DES VENTES\n0 FC",
            font_size=28,
            bold=True,
            size_hint_y=None,
            height=90
        )

        self.montant = TextInput(
            hint_text="Entrez le montant en FC",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=55
        )

        bouton = Button(
            text="ENREGISTRER LA VENTE",
            size_hint_y=None,
            height=55
        )

        bouton_effacer = Button(
            text="EFFACER L'HISTORIQUE",
            size_hint_y=None,
            height=50
        )

        self.message = Label(
            text="",
            size_hint_y=None,
            height=35
        )

        historique_titre = Label(
            text="HISTORIQUE DES VENTES",
            size_hint_y=None,
            height=45
        )

        self.historique = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=5
        )

        self.historique.bind(
            minimum_height=self.historique.setter("height")
        )

        defiler = ScrollView()
        defiler.add_widget(self.historique)

        ecran.add_widget(titre)
        ecran.add_widget(self.resultat)
        ecran.add_widget(self.montant)
        ecran.add_widget(bouton)
        ecran.add_widget(bouton_effacer)
        ecran.add_widget(self.message)
        ecran.add_widget(historique_titre)
        ecran.add_widget(defiler)

        bouton.bind(on_press=self.enregistrer)
        bouton_effacer.bind(on_press=self.confirmer_suppression)

        self.actualiser()

        return ecran

    def charger_ventes(self):
        try:
            with open(self.fichier, "r", encoding="utf-8") as fichier:
                self.ventes = json.load(fichier)

            self.total = sum(self.ventes)

        except (FileNotFoundError, json.JSONDecodeError):
            self.ventes = []
            self.total = 0

    def enregistrer(self, instance):
        try:
            montant = float(self.montant.text)

            if montant <= 0:
                self.message.text = "Montant invalide"
                return

            nouvelles_ventes = self.ventes + [montant]

            with open(self.fichier, "w", encoding="utf-8") as fichier:
                json.dump(nouvelles_ventes, fichier)

            self.ventes = nouvelles_ventes
            self.total += montant

            self.actualiser()

            self.message.text = "Vente sauvegardée !"
            self.montant.text = ""

        except ValueError:
            self.message.text = "Entrez un montant valide"

        except OSError:
            self.message.text = "Erreur de sauvegarde"

    def confirmer_suppression(self, instance):

        contenu = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=15
        )

        message = Label(
            text="Voulez-vous vraiment supprimer toutes les ventes ?"
        )

        boutons = BoxLayout(
            spacing=10,
            size_hint_y=None,
            height=50
        )

        annuler = Button(text="ANNULER")
        confirmer = Button(text="SUPPRIMER")

        boutons.add_widget(annuler)
        boutons.add_widget(confirmer)

        contenu.add_widget(message)
        contenu.add_widget(boutons)

        self.popup = Popup(
            title="CONFIRMATION",
            content=contenu,
            size_hint=(0.9, 0.4)
        )

        annuler.bind(on_press=self.popup.dismiss)
        confirmer.bind(on_press=self.supprimer_ventes)

        self.popup.open()

    def supprimer_ventes(self, instance):
        try:
            with open(self.fichier, "w", encoding="utf-8") as fichier:
                json.dump([], fichier)

            self.ventes = []
            self.total = 0

            self.actualiser()
            self.message.text = "Historique supprimé !"

        except OSError:
            self.message.text = "Erreur de suppression"

        self.popup.dismiss()

    def actualiser(self):
        self.resultat.text = (
            f"TOTAL DES VENTES\n{self.total:,.0f} FC"
        ).replace(",", " ")

        self.historique.clear_widgets()

        for numero, montant in enumerate(self.ventes, start=1):
            vente = Label(
                text=f"Vente {numero} : {montant:,.0f} FC".replace(",", " "),
                size_hint_y=None,
                height=40
            )

            self.historique.add_widget(vente)


VortexApp().run()
