from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
import os
import csv
import pandas as pd

from toolbox import read_txt_file, filter_similar_entities

# Création du dossier des résultats
# results_path = "./OutputDatalm"
results_path = "../OutputDatalm"
os.makedirs(results_path, exist_ok=True)

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
        None : La fonction ne retourne rien, mais crée des fichiers texte et csv contenant les mots-clés et leurs scores de façon ordonnée.
    """
    # Création du sous dossier de stockage des différentes données
    odd_number = dossier[-2:]
    dossier_path = f"{results_path}/ODD{odd_number}"
    os.makedirs(dossier_path, exist_ok=True)

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
        texte = read_txt_file(f"{dossier}/{txt_file}")
        # Ajouter les données extraites dans la liste
        extracted_data.append((txt_file, texte))
        # print(extracted_data)
        # break

    keywords_ODD = []
    print("Extraction des mots clés...\n")
    for data in extracted_data:
        # Récupérer le fichier texte extrait
        doc = data[1]
        # Configurer du modèle KeyBert pour la recherche de mots/phrases clé(e)s
        kw_model = KeyBERT(model=sentence_model)
        keywords = kw_model.extract_keywords(
            doc,
            keyphrase_ngram_range=(1, 2),   # Taille de mots/phrases clé(e)s
            stop_words='english',           # Eliminer les mots usuels en anglais
            use_maxsum=True,                # Eviter de séléectionner trop proches de sens
            nr_candidates=20,               # Nombre d'éléments à étudier
            top_n=10                        # Nombre d'éléments choisis
        )
        # Suppression des entités similaires d'un point de vue orthographique
        entities_filtered = filter_similar_entities(keywords, threshold=80)

        # Filtrer les résultats par score
        filtered_keywords = [(kw[0], kw[1], data[0][12:14]) for kw in entities_filtered if kw[1] > 0.5]
        keywords_ODD.extend(filtered_keywords)
        # Chemin de sortie de l'indicateur
        metadata = data[0].replace(".txt","")
        output_path_file = f"./{dossier}/{metadata}_keywords.txt"
        with open(output_path_file, "w", encoding="utf-8") as f:
            f.write("Mots-clés extraits et scores :\n")
            f.write("----------------------------------------------------\n")
            for keyword in filtered_keywords:
                f.write(f"{keyword[0]} : {keyword[1]:.4f}\n")
            f.write("----------------------------------------------------\n")


    print("Regroupement des mots clées par cible...\n")
    # Stockage des mot-clés dans un dataframe
    df = pd.DataFrame(keywords_ODD, columns=["Mots-cles", "Scores", "Cibles"])
    # Grouper les mots-clés par cibles
    grouped = df.groupby("Cibles")
    # Créer un fichier texte pour chaque cible
    for target, group in grouped:
        # Créer le nom de fichier pour la cible
        output_filename = f"{dossier_path}/Cible_{target}_keywords.txt"

        # Écrire les mots-clés et leurs scores dans le fichier texte
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(f"Mots-clés pour la cible {target} :\n")
            f.write("----------------------------------------------------\n")
            for index, row in group.iterrows():
                f.write(f"{row['Mots-cles']} : {row['Scores']:.4f}\n")
            f.write("----------------------------------------------------\n")



    print("Regroupement des mots-clés par ODD...\n")
    output_path = f"{dossier_path}/ODD{odd_number}.csv"
    with open(output_path, mode="w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        # Écrire l'en-tête
        writer.writerow(["Mots-cles", "Scores", "cibles"])
        # Écrire les mots-clés et leurs scores
        for keyword in keywords_ODD:
            writer.writerow([keyword[0], keyword[1],keyword[2]])


    print(f"...Fin de traitement de l'ODD {odd_number}")

    return None

print(entities_extractions("../MetaData/ODD01"))

