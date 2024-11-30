import docx
import requests
from bs4 import BeautifulSoup
import os

def getAllMetaFiles():
    # URL du site
    url = 'https://unstats.un.org/sdgs/metadata'

    # Effectuer une requête pour obtenir le contenu de la page
    response = requests.get(url)

    # Vérifier si la requête est réussie
    if response.status_code == 200:
        # Parser le contenu HTML avec BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Trouver tous les liens word
        word_links = soup.find_all('a', href=True, title="View in Word")

        # Parcourir les liens et télécharger les fichiers word
        for link in word_links:
            href = link['href']
            if href.endswith('.docx'):
                # Construire l'URL complète si nécessaire
                word_url = href if href.startswith('http') else f'https://unstats.un.org{href}'

                # Créer le dossier pour sauvegarder le fichier word
                path_doc_word = f'../MetaData/ODD{word_url[52:54]}'
                os.makedirs(path_doc_word, exist_ok=True)

                # Obtenir le nom du fichier
                word_name = os.path.join(path_doc_word, os.path.basename(word_url))

                # Télécharger le fichier word
                word_response = requests.get(word_url)

                # Sauvegarder le fichier word
                with open(word_name, 'wb') as word_file:
                    word_file.write(word_response.content)

                print(f'Téléchargé : {word_name}')
    else:
        return f"Impossible d'accéder à la page : {response.status_code}"




# Fonction pour convertir le fichier .docx en fichier .txt
def docx_to_txt(docx_path, txt_path):
    # Ouvrir le fichier Word
    doc = docx.Document(docx_path)

    # Extraire tout le texte
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])

    # Extraction spécifique du texte entre "2.a. Definition" et "2.b."
    debut = text.find("2.a. Definition") + 44
    fin = text.find("2.b. ")

    nouveau_text = text[debut:fin].replace("Definition:", "").replace("Concepts:", "")

    # Supprimer les espaces ou les nouvelles lignes en début de texte
    while nouveau_text[0] == ' ' or nouveau_text[0] == '\n':
        nouveau_text = nouveau_text[1:]

    # Écrire le texte dans un fichier .txt
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(nouveau_text)


# Fonction pour traiter un dossier contenant des fichiers .docx
def ODD_MD(dossier):
    # Extraction du nom de tous les fichiers dans le dossier
    fichiers = os.listdir(dossier)

    # Filtre les fichiers .docx
    fichiers_docx = [fichier for fichier in fichiers if fichier.lower().endswith('.docx')]

    for fichier in fichiers_docx:
        docx_file_path = f'{dossier}/{fichier}'
        txt_file_path = f'{dossier}/{fichier}'[:-5] + '.txt'  # Remplacer .docx par .txt

        # Convertir le fichier .docx en fichier .txt
        docx_to_txt(docx_file_path, txt_file_path)


if __name__ == '__main__':
    # getAllMetaFiles()
    for dossier in os.listdir("../MetaData"):
        ODD_MD(f"../MetaData/{dossier}")
