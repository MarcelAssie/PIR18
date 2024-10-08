from transformers import pipeline
import os
from extract_text import extraire_texte_pdf

# Désactiver l'avertissement de symlink sur Windows
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"


def analyser_entites(indicator):

    # Utilisation de Hugging Face avec un modèle spécifique
    ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", grouped_entities=True)
    # print("Extraction du texte du PDF...")
    texte = extraire_texte_pdf(indicator)
    # print("Analyse des entités dans le texte...")
    entites = ner_pipeline(texte)
    # print("Entités détectées:")
    # for entite in entites:
    #     print(f"Entité : {entite['word']} : {entite['entity_group']} (Type) => {entite['score']}(Score)")
    return entites


