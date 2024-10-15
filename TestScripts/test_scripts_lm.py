from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
import time
from ActivesScripts.filters import filter_similar_entities
# Texte à analyser
doc = """
Expenditure is defined in Chapter 4 (paragraphs 4.24 and 6.1) of the Government Finance Statistics Manual 2014 (GFSM 2014) as a decrease in net worth resulting from a transaction. It is a fiscal indicator for assessing the sustainability of fiscal activities. The GFSM 2014 presents expense according to the economic classification (paragraphs 6.8-6.11) and as functions of government (paragraphs 6.126-6.132). General government units have ten distinct types of expense according to functions of government. Among them there are expense on health (code 707), on education (code 709) and on social protection (code 710). 
The key concepts and terms associated with the indicator are outlined in Government Finance Statistics Manual (GFSM) 2014, as are the associated classifications. As stated in paragraph 6.126, the Classification of Functions of Government (COFOG) is a detailed classification of the functions, or socioeconomic objectives, that general government units aim to achieve through various kinds of expenditure. While the COFOG as used in the GFSM 2014 fully agrees with the The Organisation for Economic Co-operation and Development (OECD)/UN classification, the concept is applied slightly differently in government finance statistics (GFS). Final outlays are referred to in a general sense by the OECD/UN, and therefore include grants, loans, and/or subsidies. In GFS, COFOG is applied only to expenditure, comprising expense and the net investment in nonfinancial assets. Transactions in financial assets and liabilities, such as loans, are excluded when compiling COFOG data for GFS reporting purposes.
Government expenditure on health includes expenditure on services provided to individual persons and services provided on a collective basis. Collective health services are concerned with matters such as formulation and administration of government policy; setting and enforcement of standards for medical and paramedical personnel and for hospitals, clinics, surgeries, etc.; regulation and licensing of providers of health services; and applied research and experimental development into medical and health-related matters. However, overhead expenditure connected with administration or functioning of a group of hospitals, clinics, surgeries, etc. is considered to be individual expenditure.
Government expenditure on education includes expenditure on services provided to individual pupils and students and expenditure on services provided on a collective basis. Collective educational services are concerned with matters such as formulation and administration of government policy; setting and enforcement of standards; regulation, licensing, and supervision of educational establishments; and applied research and experimental development into education affairs and services. However, overhead expenditure connected with administration or functioning of a group of schools, colleges, etc. is considered to be individual expenditure.
Government expenditure on social protection includes expenditure on services and transfers provided to individual persons and households and expenditure on services provided on a collective basis. Collective social protection services are concerned with matters such as formulation and administration of government policy; formulation and enforcement of legislation and standards for providing social protection; and applied research and experimental development into social protection affairs and services. Expenditure on individual services and transfers are allocated to sickness and disability, old age, survivors, family and children, unemployment, housing and social exclusion. 
"""

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
with open("TestsModels_performance.txt", "w", encoding="utf-8") as result_file:
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
        entities_filtered = filter_similar_entities(keywords, threshold=80)
        filtered_keywords = [(kw[0], kw[1]) for kw in entities_filtered if kw[1] > 0.4]


        # Enregistrer l'heure de fin et calculer la durée d'exécution
        end_time = time.time()
        duree = end_time - start_time

        # Écrire les résultats dans le fichier
        result_file.write(f"Résultats pour le modèle {model_name}:\n")
        for keyword in filtered_keywords:
            result_file.write(f"{keyword[0]} : {keyword[1]:.4f}\n")

        result_file.write(f"Durée d'exécution : {duree:.4f} secondes\n")
        result_file.write("------------------------------------------------------------------------------------------------\n\n")

        # Afficher les résultats
        print(f"Résultats de {model_name} enregistrés dans le fichier.")


