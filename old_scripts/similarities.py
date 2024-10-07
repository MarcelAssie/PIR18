from embeddings import embeddings
from sklearn.metrics.pairwise import cosine_similarity

def compare_indicators(indicator1, indicator2, seuil=0.7, seuil_evaluation=0.1):
    """
    Compare les similarités cosinus entre les entités d'un indicateur.

    Parameters:
        entite1_embedding : Vecteur d'embedding pour l'entité 1
        entite2_embedding : Vecteur d'embedding pour l'entité 2

    Returns:
        Similarité cosinus entre les deux entités
    """
    print("EXTRACTION DES EMBEDDINGS POUR LE PREMIER INDICATEUR...")
    embeddings_indicator1 = embeddings(indicator1)
    print("\n--------------------------------------------------------------------------------------------------------------------------------------------\n")
    print("EXTRACTION DES EMBEDDINGS POUR LE SECOND INDICATEUR...")
    embeddings_indicator2 = embeddings(indicator2)

    # Vérifier si les indicateurs contiennent des entités
    if not embeddings_indicator1 or not embeddings_indicator2:
        print("Un ou plusieurs indicateurs ne contiennent pas d'entités.")
        return None

    # Récupérer les embeddings et les entités des indicateurs
    entites1 = [ent[0] for ent in embeddings_indicator1]
    embeddings1 = [ent[3] for ent in embeddings_indicator1]

    entites2 = [ent[0] for ent in embeddings_indicator2]
    embeddings2 = [ent[3] for ent in embeddings_indicator2]

    # Calculer la similarité cosinus entre les embeddings des indicateurs
    similarites = cosine_similarity(embeddings1, embeddings2)

    # Calculer la longueur de la matrice des similarités cosinus
    similarites_length = similarites.shape[0]*similarites.shape[1]
    print("\n--------------------------------------------------------------------------------------------------------------------------------------------\n")
    print("MATRICE DES SIMILARITÉS COSINUS ENTRE LES ENTITÉS DES DEUX INDICATEURS:")
    print(similarites)

    # Afficher les paires d'entités les plus similaires
    # print(f"\nEntités avec une similarité cosinus supérieure à {seuil} :")

    counter = 0
    for i in range(len(entites1)):
        for j in range(len(entites2)):
            if similarites[i][j] > seuil:
                counter += 1
                # print(f"{entites1[i]} - {entites2[j]} : {similarites[i][j]:.4f}")

    # Evaluation de la proportion de paires d'entités similaires
    proportion_similaires = counter / similarites_length
    print(f"\nProportion de paires d'entités similaires : {proportion_similaires * 100:.2f}%")
    if proportion_similaires > seuil_evaluation:
        print(f"Ces 2 indicateurs sont similaires")
    else:
        print(f"Ces 2 indicateurs ne sont pas similaires")

    return similarites

# compare_indicators("input_data/Metadata-01-01-01a.pdf", "input_data/Metadata-01-01-01a.pdf", 0.7, 0.1)



