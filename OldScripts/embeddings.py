from huggingface_model import analyser_entites as huggingface_analyse_entites
from spacy_model import analyser_entites as spacy_analyse_entites
from sentence_transformers import SentenceTransformer

# Chargement du modèle Sentence-BERT pour la fusion des modèles
model = SentenceTransformer('all-MiniLM-L6-v2')

def embeddings(indicator):
    """
    Combine les analyses de l'entités avec Hugging Face et Spacy pour un PDF donnée.

    paramètres:
        indicator: Le chemin du PDF à analyser.
    return:
        Une liste de tuples contenant les entités détectées (texte, label).
    """

    print("Lecture du PDF...")

    print("Analyse des entités avec Hugging face...")
    huggingface_entites = huggingface_analyse_entites(indicator)
    print("Analyse des entités avec Spacy...  ")
    spacy_entites = spacy_analyse_entites(indicator)

    print("Union des entités détectées...  ")
    results = []
    for ent in spacy_entites.ents:
        results.append((ent.text, ent.label_, "N/A"))
    results.extend([(ent['word'], ent['entity_group'], ent['score']) for ent in huggingface_entites])

    print("Suppression des doublons...  ")
    results = list(set(results))

    print("Génération des embeddings pour les entités avec Sentence-BERT...  ")
    list_entites = [ent[0] for ent in results]
    embeddings = model.encode(list_entites)

    print("Association des embeddings aux entités...  ")
    results_with_embeddings = []
    for i, entite in enumerate(results):
        results_with_embeddings.append((entite[0], entite[1], entite[2], embeddings[i]))


    # print("Entités détectées avec embeddings (Hugging Face + SpaCy):")
    # print("--------------------------------------------------------------------------------------------------------------------------------------------\n")
    # print("Entité | Type | Score | Embedding (dimensions réduites)\n")
    # for entite in results_with_embeddings:
    #     print(
    #         f"{entite[0]} : {entite[1]} => {entite[2]} (Score) | Embedding: {entite[3][:5]}...")
    #
    # print(
    #     "\n--------------------------------------------------------------------------------------------------------------------------------------------")
    # print("Nombre d'entités détectées :", len(results_with_embeddings))
    print("Extraction embeddings terminée.")
    return results_with_embeddings




