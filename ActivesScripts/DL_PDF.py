import requests
from bs4 import BeautifulSoup
import os

# URL du site
url = 'https://unstats.un.org/sdgs/metadata'

# Effectuer une requête pour obtenir le contenu de la page
response = requests.get(url)

# Vérifier si la requête est réussie
if response.status_code == 200:
    # Parser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Trouver tous les liens PDF
    pdf_links = soup.find_all('a', href=True, title="View in PDF")

    # Créer un dossier pour sauvegarder les fichiers PDF
    dossier_pdf = 'pdfs_sdgs'
    if not os.path.exists(dossier_pdf):
        os.makedirs(dossier_pdf)

    # Parcourir les liens et télécharger les fichiers PDF
    for link in pdf_links:
        href = link['href']
        if href.endswith('.pdf'):
            # Construire l'URL complète si nécessaire
            pdf_url = href if href.startswith('http') else f'https://unstats.un.org{href}'

            # Obtenir le nom du fichier
            pdf_name = os.path.join(dossier_pdf, os.path.basename(pdf_url))

            # Télécharger le fichier PDF
            pdf_response = requests.get(pdf_url)

            # Sauvegarder le fichier PDF
            with open(pdf_name, 'wb') as pdf_file:
                pdf_file.write(pdf_response.content)

            print(f'Téléchargé : {pdf_name}')
else:
    print(f"Impossible d'accéder à la page : {response.status_code}")
