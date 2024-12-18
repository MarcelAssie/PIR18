import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QScreen
from response_toolbox import *
import time

class WorkerThread(QThread):
    update_status = pyqtSignal(str)
    response_ready = pyqtSignal(str)  # Signal pour renvoyer la réponse


    def __init__(self, question, model="llama-2-7b-chat"):
        super().__init__()
        self.question = question
        self.model = model

    def run(self):
        try:
            self.update_status.emit("Traduction de la question en cours...")
            translated_question = translate_to_english(self.question)
            self.update_status.emit(f"Question traduite : {translated_question}")

            self.update_status.emit("Extraction des mots-clés...")
            cleaned_keywords = extract_keywords(translated_question, self.model)

            if cleaned_keywords:
                self.update_status.emit("Recherche des mots-clés similaires à plus de 95% dans le graphe...")
                similitudes = compare_keyword_to_keywords(cleaned_keywords)
                if similitudes:
                    self.update_status.emit("Similitudes trouvées. Récupération des données du graphe...")
                    df = search_graph(similitudes)
                    self.update_status.emit("Génération de la réponse basée sur les données du graphe...")
                    context = create_context_answer(df, translated_question)
                    final_answer = generate_graph_answer(context, translated_question, model=self.model)
                else:
                    self.update_status.emit("Aucune similitude trouvée. Reformulation de la question...")
                    reformulated_question = reformulate_question(translated_question, self.model)
                    self.update_status.emit(f"Question reformulée : {reformulated_question}")
                    cleaned_keywords = extract_keywords(reformulated_question, self.model)
                    if cleaned_keywords:
                        self.update_status.emit("Recherche des mots-clés similaires à plus de 95% dans le graphe...")
                        similitudes = compare_keyword_to_keywords(cleaned_keywords)
                        if similitudes:
                            self.update_status.emit("Similitudes trouvées après reformulation. Récupération des données...")
                            df = search_graph(similitudes)
                            context = create_context_answer(df, translated_question)
                            final_answer = generate_graph_answer(context, translated_question, model=self.model)
                        else:
                            self.update_status.emit(
                                "Aucune similitude trouvée après reformulation. Génération d'une réponse brute...")
                            final_answer = generate_raw_answer(translated_question, model=self.model)
                    else:
                        final_answer = "Aucun mot-clé extrait après reformulation. Impossible de générer une réponse."
            else:
                final_answer = "Aucun mot-clé extrait. Impossible de générer une réponse."
        except Exception as e:
            final_answer = f"Erreur lors du traitement : {str(e)}"

            # Émettre la réponse finale
        self.response_ready.emit(final_answer)

class QuestionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Configuration de la fenêtre principale
        self.setWindowTitle("Question App")
        self.setFixedSize(1000, 800)
        self.center_window()

        # Layout principal
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(40, 40, 40, 40)  #
        self.layout.setSpacing(20)

        # Zone de texte modifiable pour entrer une question
        self.input_text = QLineEdit(self)
        self.input_text.setPlaceholderText("Entrez votre question ici...")
        self.input_text.setFixedHeight(50)
        self.input_text.setStyleSheet("""
        QLineEdit {background-color: #f7f7f7; border: 2px solid #ccc; border-radius: 10px; padding: 10px; font-size: 16px;}
        QLineEdit:focus {border-color: #4CAF50; background-color: #fff;}
        """)
        self.layout.addWidget(self.input_text)

        # Ajout d'un espace vertical
        self.layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Bouton Valider
        self.validate_button = QPushButton("Valider", self)
        self.validate_button.setFixedHeight(50)
        self.validate_button.setStyleSheet("""
            QPushButton {background-color: #4CAF50; color: white; border: none; padding: 10px; font-size: 16px; border-radius: 5px;}
            QPushButton:hover {background-color: #45a049;}
            QPushButton:pressed {background-color: #388e3c;}
            """)
        self.validate_button.clicked.connect(self.process_question)
        self.layout.addWidget(self.validate_button)

        # Ajout d'un autre espace vertical
        self.layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Zone de texte non modifiable pour afficher la réponse
        self.response_text = QTextEdit(self)
        self.response_text.setReadOnly(True)
        self.response_text.setPlaceholderText("Les étapes et la réponse apparaîtront ici...")
        self.response_text.setStyleSheet("""
            QTextEdit {background-color: #f7f7f7; border: 2px solid #ccc; border-radius: 10px; padding: 10px; font-size: 16px;}
            QTextEdit:focus {border-color: #4CAF50;}
            """)
        self.layout.addWidget(self.response_text)

        # Définir le layout principal
        self.setLayout(self.layout)
        self.setStyleSheet("""
        QWidget {background-color: #f2f2f2; font-family: 'Arial', sans-serif;}
        """)

    def center_window(self):
        # Centre la fenêtre sur l'écran principal
        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        x = (screen.width() - 1000) // 2
        y = (screen.height() - 800) // 2
        self.move(x, y)

    def process_question(self):
        # Bloquer la zone de texte et le bouton
        self.input_text.setEnabled(False)
        self.validate_button.setEnabled(False)
        self.validate_button.setText("Génération d'une réponse...")  # Modifier le texte du bouton

        # Récupérer la question entrée
        question = self.input_text.text()

        # Créer et lancer un thread de travail
        self.worker = WorkerThread(question)
        self.worker.update_status.connect(self.update_status)
        self.worker.response_ready.connect(self.display_response)
        self.worker.start()

    def update_status(self, message):
        self.response_text.setText(message)

    def display_response(self, response):
        # Afficher la réponse
        self.response_text.setText(response)

        # Réactiver la zone de texte et le bouton
        self.input_text.setEnabled(True)
        self.validate_button.setEnabled(True)
        self.validate_button.setText("Valider")  # Réinitialiser le texte du bouton

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuestionApp()
    window.show()
    sys.exit(app.exec_())