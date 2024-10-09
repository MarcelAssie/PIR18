from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
import time

# Texte à analyser
doc = """
L'égalité des genres est essentielle pour le développement durable d'une société. Elle garantit que toutes les personnes, indépendamment de leur sexe, ont les mêmes droits et opportunités.
Les femmes doivent avoir la possibilité de poursuivre des études supérieures et d'accéder à des carrières qui leur permettent de réaliser leur potentiel.
"""

# Modèles à tester
models = {
    "all-MiniLM-L6-v2": "all-MiniLM-L6-v2",
    "paraphrase-MiniLM-L6-v2": "paraphrase-MiniLM-L6-v2",
    "distilbert-base-nli-mean-tokens": "distilbert-base-nli-mean-tokens",
    "paraphrase-distilroberta-base-v1": "paraphrase-distilroberta-base-v1",
    # "roberta-large": "roberta-large",
    # "bert-base-uncased": "bert-base-uncased",
    "bert-base-cased": "bert-base-cased",
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
            nr_candidates=50,
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
