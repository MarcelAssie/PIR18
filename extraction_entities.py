from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
import os
import re
import csv

from filters import txt_to_string, filter_similar_entities


def entities_extractions(dossier):
    """
        Extrait les mots-clés de fichiers texte dans un dossier et enregistre les résultats dans des fichiers séparés.

        Cette fonction parcourt un dossier donné, extrait le contenu de chaque fichier texte, puis utilise
        le modèle KeyBERT pour extraire les mots-clés les plus pertinents. Les résultats sont ensuite sauvegardés
        dans un fichier texte correspondant à chaque fichier analysé.

        Paramètres:
        -----------
        dossier : str
            Chemin vers le dossier contenant les fichiers texte (.txt).

        Retour:
        -------
        None : La fonction ne retourne rien, mais crée des fichiers texte contenant les mots-clés et leurs scores.
    """
    odd_number = re.search(r'\d+', dossier).group()
    print("------------------------------------------------------------------------------------------------")
    print(f"Début de traitement de l'ODD {odd_number}...\n")
    sentence_model = SentenceTransformer("all-MiniLM-L6-v2")

    # Liste des noms de fichiers texte dans le dossier
    # J'utilise la condition supplementaire pour éviter de selectionner les fichiers traités
    txt_files = [fichier for fichier in os.listdir(dossier)
                 if fichier.endswith(".txt") and "keywords" not in fichier]

    # Liste des données extraites
    extracted_data = []

    for txt_file in txt_files:
        # Convertir le fichier texte en une chaîne de caractères
        texte = txt_to_string(f"{dossier}/{txt_file}")
        # Ajouter les données extraites dans la liste
        extracted_data.append((txt_file, texte))
        # break

    keywords_ODD = []
    for data in extracted_data:
        # Récupérer le fichier texte extrait
        doc = data[1]
        # Configurer du modèle KeyBert pour la recherche de mots/phrases clé(e)s
        kw_model = KeyBERT(model=sentence_model)
        keywords = kw_model.extract_keywords(
            doc,
            keyphrase_ngram_range=(1, 3),   # Taille de mots/phrases clé(e)s
            stop_words='english',           # Eliminer les mots usuels en anglais
            nr_candidates=100,               # Nombre d'éléments à étudier
            top_n=10                        # Nomnre d'éléments choisis
        )
        # Suppression des entités similaires d'un point de vue orthographique
        entities_filtered = filter_similar_entities(keywords, threshold=80)

        # Filtrer les résultats par score
        filtered_keywords = [kw for kw in entities_filtered if kw[1] > 0.4]
        # Ajouter les mots-clés extraits et leurs scores dans la liste des mots-clés pour l'ODD'
        for k in filtered_keywords:
            keywords_ODD.append((k[0], k[1]))
        # Chemin de sortie du fichier
        metadata = data[0].replace(".txt","")
        output_path = f"{dossier}/{metadata}_keywords.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("Mots-clés extraits et scores :\n")
            f.write("----------------------------------------------------\n")
            for keyword in filtered_keywords:
                f.write(f"{keyword[0]} : {keyword[1]:.4f}\n")
            f.write("----------------------------------------------------\n")

    output_path = f"Keywords_odd/ODD{odd_number}.csv"
    with open(output_path, mode="w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        # Écrire l'en-tête
        writer.writerow(["Mots-cles", "Scores"])
        # Écrire les mots-clés et leurs scores
        for keyword in keywords_ODD:
            writer.writerow([keyword[0], keyword[1]])


    print(f"...Fin de traitement de l'ODD {odd_number}")

    return None

# print(entities_extractions("MetaD/ODD01"))
if __name__ == "__main__":
    # Exécution de tous les ODD
    odd_files = os.listdir("MetaD")
    for odd_file in odd_files:
        entities_extractions(f"MetaD/{odd_file}")



