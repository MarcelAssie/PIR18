import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QScreen
import time

class WorkerThread(QThread):
    response_ready = pyqtSignal(str)  # Signal pour renvoyer la réponse

    def __init__(self, question):
        super().__init__()
        self.question = question

    def run(self):
        # Appeler la fonction de génération du texte
        response = self.question
        self.response_ready.emit(response)  # Émettre la réponse une fois prête

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
        self.layout.setContentsMargins(70, 70, 70, 70)  # Marges autour du layout
        self.layout.setSpacing(20)  # Espacement entre les widgets

        # Zone de texte modifiable pour entrer une question
        self.input_text = QLineEdit(self)
        self.input_text.setPlaceholderText("Entrez votre question ici...")
        self.input_text.setFixedHeight(60)  # Hauteur doublée
        self.layout.addWidget(self.input_text)

        # Ajout d'un espace vertical
        self.layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Bouton Valider
        self.validate_button = QPushButton("Valider", self)
        self.validate_button.setFixedHeight(60)  # Hauteur doublée
        self.validate_button.clicked.connect(self.process_question)
        self.layout.addWidget(self.validate_button)

        # Ajout d'un autre espace vertical
        self.layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Zone de texte non modifiable pour afficher la réponse
        self.response_text = QTextEdit(self)
        self.response_text.setReadOnly(True)
        self.response_text.setPlaceholderText("La réponse apparaîtra ici...")
        self.layout.addWidget(self.response_text)

        # Définir le layout principal
        self.setLayout(self.layout)

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
        self.worker.response_ready.connect(self.display_response)
        self.worker.start()

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
