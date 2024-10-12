from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
import time

# Texte à analyser
doc = """
Supervised learning is the machine learning task of learning a function that
         maps an input to an output based on example input-output pairs.[1] It infers a
         function from labeled training data consisting of a set of training examples.[2]
         In supervised learning, each example is a pair consisting of an input object
         (typically a vector) and a desired output value (also called the supervisory signal).
         A supervised learning algorithm analyzes the training data and produces an inferred function,
         which can be used for mapping new examples. An optimal scenario will allow for the
         algorithm to correctly determine the class labels for unseen instances. This requires
         the learning algorithm to generalize from the training data to unseen situations in a
         'reasonable' way (see inductive bias)."""

# Modèles à tester
models = {
    "all-MiniLM-L6-v2": "all-MiniLM-L6-v2",
    # "paraphrase-MiniLM-L6-v2": "paraphrase-MiniLM-L6-v2",
    # "distilbert-base-nli-mean-tokens": "distilbert-base-nli-mean-tokens",
    # "paraphrase-distilroberta-base-v1": "paraphrase-distilroberta-base-v1",
    # "roberta-large": "roberta-large",
    # "bert-base-uncased": "bert-base-uncased",
    # "bert-base-cased": "bert-base-cased",
    # "t5-base": "t5-base",
}

# Ouvrir le fichier en mode écriture (append) pour stocker les résultats
with open("TestsModels_performance.txt", "a", encoding="utf-8") as result_file:
    # Tester chaque modèle
    for model_name, model_path in models.items():
        print(f"Test du modèle {model_name}...")

        # Charger le modèle SentenceTransformer
        sentence_model = SentenceTransformer(model_path)

        # Créer un modèle KeyBERT à partir de SentenceTransformer
        kw_model = KeyBERT(model=sentence_model)

        # Enregistrer l'heure de début
        start_time = time.time()

        # Extraire les mots-clés
        keywords = kw_model.extract_keywords(
            doc,
            keyphrase_ngram_range=(1, 2),
            stop_words='english',
            use_maxsum=True,
            nr_candidates=20,
            top_n=10
        )

        # Enregistrer l'heure de fin et calculer la durée d'exécution
        end_time = time.time()
        duree = end_time - start_time

        # Écrire les résultats dans le fichier
        result_file.write(f"Résultats pour le modèle {model_name}:\n")
        for keyword in keywords:
            result_file.write(f"{keyword[0]} : {keyword[1]:.4f}\n")

        result_file.write(f"Durée d'exécution : {duree:.4f} secondes\n")
        result_file.write("------------------------------------------------------------------------------------------------\n\n")

        # Afficher les résultats
        print(f"Résultats de {model_name} enregistrés dans le fichier.")
