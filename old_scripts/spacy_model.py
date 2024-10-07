import spacy
from extract_text import extraire_texte_pdf


def analyser_entites(indicator):

    # Charger le "en_core_web_trf" de Spacy sur des transformers
    nlp = spacy.load("en_core_web_trf")
    # print("Extraction du texte du PDF...")
    texte = extraire_texte_pdf(indicator)
    # print("Analyse des entités dans le texte...")
    doc = nlp(texte)
    # print("Entités détectées:")
    # for entite in doc.ents:
    #     print(f"{entite.text} : {entite.label_}")
    return doc

