import PyPDF2
import os


# Fonction pour convertir le PDF en fichier .txt
def pdf_to_txt(pdf_path, txt_path):
    # Ouvrir le fichier PDF
    with open(pdf_path, 'rb') as pdf_file:
        # Créer un lecteur PDF
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Extraire tout le texte
        text = ""
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()

        debut = text.find("2.a. Definition") + 44
        fin = text.find("2.b. ")

        nouveau_text = text[debut:fin].replace("Definition:", "")
        nouveau_text = nouveau_text.replace("Concepts:", "")

        while nouveau_text[0] == ' ' or nouveau_text[0] == '\n':
            nouveau_text = nouveau_text[1:]

        # Écrire le texte dans un fichier .txt
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(nouveau_text)


def ODD_MD(dossier):
    # Extraction du nom de tous les fichiers de métadonnées
    fichiers = os.listdir(dossier)

    # Filtre les fichiers pdf
    fichiers_pdfs = [fichier for fichier in fichiers if fichier.lower().endswith('.pdf')]

    for fichier in fichiers_pdfs:
        pdf_file_path = f'{dossier}/{fichier}'
        txt_file_path = f'{dossier}/{fichier}'[:-4] + '.txt'

        # Convertir le PDF en fichier .txt
        pdf_to_txt(pdf_file_path, txt_file_path)

if __name__ == '__main__':
    for dossier in os.listdir("../MetaD"):
        ODD_MD("../MetaD/" + dossier)
