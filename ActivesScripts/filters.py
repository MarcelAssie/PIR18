from fuzzywuzzy import fuzz

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


