from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re

def txt_to_string(txt_file):
    """
    Convertit un fichier texte en une chaîne de caractères.

    Paramètres:
    txt_file (str): Chemin du fichier texte à convertir

    Returns:
    str: Chaîne de caractères contenant le texte du fichier
    """
    # Ouvrir le fichier texte et lire son contenu
    try:
        with open(txt_file, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Le fichier {txt_file} n'existe pas.")
        return ""



def filter_similar_entities(entities, threshold=80):
    """
        Filtrer les entités similaires à partir du seuil de similarité donné.

        Paramètres:
        entities (list): Liste de tuples (entité, score) des entités à filtrer

        returns: Liste de tuples (entité, score)
    """

    filtered_entities = []
    seen = set()

    for entity, score in entities:
        # Vérifier si l'entité a déjà été vue
        if any(fuzz.ratio(entity, seen_entity) > threshold for seen_entity in seen):
            continue
        else:
            # Ajouter a entités filtrées et entités vues
            filtered_entities.append((entity, score))
            seen.add(entity)

    return filtered_entities




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
    print("------------------------------------------------------------------------------------------------")
    print(f"Début de traitement de l'ODD {re.search(r'\d+', dossier).group()}...\n")
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

    for data in extracted_data:
        # Récupérer le fichier texte extrait
        doc = data[1]
        # Configurer du modèle KeyBert pour la recherche de mots/phrases clé(e)s
        kw_model = KeyBERT(model=sentence_model)
        keywords = kw_model.extract_keywords(
            doc,
            keyphrase_ngram_range=(1, 2),   # Taille de mots/phrases clé(e)s
            stop_words='english',           # Eliminer les mots usuels en anglais
            nr_candidates=50,               # Nombre d'éléments à étudier
            top_n=10                        # Nomnre d'éléments choisis
        )
        # Suppression des entités similaires d'un point de vue orthographique
        entities_filtered = filter_similar_entities(keywords, threshold=80)

        # Filtrer les résultats par score
        filtered_keywords = [kw for kw in entities_filtered if kw[1] > 0.3]

        # Chemin de sortie du fichier
        metadata = data[0].replace(".txt","")
        output_path = f"{dossier}/{metadata}_keywords.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("Mots-clés extraits et scores :\n")
            f.write("----------------------------------------------------\n")
            for keyword in filtered_keywords:
                f.write(f"{keyword[0]} : {keyword[1]:.4f}\n")
            f.write("----------------------------------------------------\n")
    print(f"...Fin de traitement de l'ODD {re.search(r'\d+', dossier).group()}")

    return None


if __name__ == "__main__":
    # Exécution de tous les ODD
    odd_files = os.listdir("MetaD")
    for odd_file in odd_files:
        entities_extractions(f"MetaD/{odd_file}")



