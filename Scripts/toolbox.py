from ctransformers import AutoModelForCausalLM
from huggingface_hub import login
from transformers import AutoTokenizer, pipeline
from keybert.llm import TextGeneration
from keybert import KeyLLM
import re, os, pandas as pd
from fuzzywuzzy import fuzz


# ------------------------------------------------------------------------------------------------
#  Chargement du fichier contenant les ODD, Cibles et Indicateurs et leurs informations

file_path = "../Other/odd_target_indicator.csv"
data = pd.read_csv(f"{file_path}", delimiter=";")
# ------------------------------------------------------------------------------------------------

# Connection à Hugging Face
def login_hf():
    file_path = "C:/Users/jeanm/Desktop/Ensg/Semestre3/ProjetRecherche/Ressources"
    api_keys = [api_keys for api_keys in os.listdir(file_path) if "api_keys" in api_keys]
    with open(f"{file_path}/{api_keys[0]}", 'r', encoding='utf-8') as file:
        file = file.read()
        hugging_face_api_key = file.split("\n")[3]
        return hugging_face_api_key

login(token=login_hf())


# Fonction pour lire le contenu d'un fichier texte
def read_txt_file(txt_file):
    try:
        with open(txt_file, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Le fichier {txt_file} n'existe pas.")
        return ""


# Fonction pour découper un texte en morceaux de 512 tokens
def chunk_text(text):
    paragraphs = text.split("\n")
    results = []
    for paragraph in paragraphs:
        if paragraph.strip():
            results.append(paragraph)
    return results


# Fonction pour extraire les mots-clés
def extract_keywords_from_chunks(chunks, test_model):
    # Charger le modèle et le tokenizer
    model = AutoModelForCausalLM.from_pretrained(
        "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
        model_file=test_model,
        model_type="mistral",
        gpu_layers=0,
        hf=True
    )

    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")

    generator = pipeline(
        model=model,
        tokenizer=tokenizer,
        task='text-generation',
        max_new_tokens=50,
        repetition_penalty=1.1
    )

    # Prompt pour extraire les mots-clés
    keyword_prompt = """
    [INST]

    I have the following document:
    - [DOCUMENT]
    
    Please extract only the keywords related to the Sustainable Development Goals (SDGs) that are explicitly mentioned in this document. 
    The keywords should consist of 2 to 3 words and should be meaningful within the context of this document. 
    Ensure that the keywords are derived solely from the text provided and do not include any external references or interpretations. 
    Return the keywords in a structured and readable format, without adding any extra explanations or phrases such as:
    "Here are the keywords present in the document."
    [/INST]

    """
    keywords = []
    count = 0
    for chunk in chunks:
        count += 1
        prompt = keyword_prompt.replace("[DOCUMENT]", chunk)
        llm = TextGeneration(generator, prompt=prompt)
        kw_model = KeyLLM(llm)
        extracted_keywords = kw_model.extract_keywords([chunk])

        # Nettoyage préliminaire des mots-clés extraits
        cleaned_keywords = [kw.replace('* ', '').strip() for kw in extracted_keywords[0][0].split('\n') if kw]
        keywords.append(cleaned_keywords)
    return keywords


def clean_keywords(keywords, max_words=2):
    # Étape 1: Nettoyer les mots-clés des caractères
    cleaned_keywords = []
    for kw in keywords:
        cleaned_kw = kw.lstrip('- ').strip()
        cleaned_keywords.append(cleaned_kw)

    # Étape 2: Supprimer les doublons tout en conservant l'ordre
    cleaned_keywords = list(dict.fromkeys([kw.lower() for kw in cleaned_keywords]))

    # Etape 3 : Retirer les numéros et points
    filtered_keywords = [re.sub(r"^\d+\.\s*", "", keyword) for keyword in cleaned_keywords]

    # Etape 4 : # Retirer les mots-clés spécifiques
    exclusion_terms = ['sdg','sdgs', 'sustainable development', 'sustainable development goals', 'indicator', 'sdg indicator']
    filtered_keywords = [kw for kw in filtered_keywords if not any(excluded in kw.lower() for excluded in exclusion_terms)]


    # Étape 5 : Filtrer par nombre de mots et les expressions numériques
    data_cleaned = []
    for kw in filtered_keywords:
        if len(kw.split()) == max_words and not re.search(r'\d+', kw):
            data_cleaned.append(kw)

    return data_cleaned


def processing(odd_number, txt_file, model):

    # Charger le fichier texte
    document_content = read_txt_file(txt_file)

    # Découper le texte en paragraphes
    chunks = chunk_text(document_content)

    # Extraire les mots-clés de chaque morceau
    keywords = extract_keywords_from_chunks(chunks, model)

    # Aplatir les mots-clés dans une unique liste
    list_keywords = [keyword for sublist in keywords for keyword in sublist]

    # Nettoyer les mots-clés
    cleaned_keywords = clean_keywords(list_keywords)

    # Organisation du fichier pour l'affichage
    cible = txt_file[30:32].upper()
    indicator = txt_file[27:35].upper()
    output_keywords = []
    for keyword in cleaned_keywords:
        output_keywords.append((f"ODD{odd_number}", f"Cible {odd_number}-{cible}", f"Indicateur {indicator}", keyword))

    return output_keywords

def addTitles(dataframe) :
    odd_list = []
    target_list = []
    indicator_list = []
    for _, row in data.iterrows():
        odd_list.append(row["Objectif"])
        target_list.append(row["Cible"])
        indicator_list.append(row["Indicateur"])

    odd_names = list(dict.fromkeys(odd_list))
    target_names = list(dict.fromkeys(target_list))
    indicator_names = list(dict.fromkeys(indicator_list))

    odd_sans_numeros = [titre.split('. ', 1)[1] for titre in odd_names]
    odd_dict = {f"ODD{str(i).zfill(2)}": titre for i, titre in enumerate(odd_sans_numeros, start=1)}

    target_titres_ord = [titre.split(': ', 1) for titre in target_names]
    target_dict = {
        f"Cible {'-'.join([f"{int(part):02d}" if part.isdigit() else part.upper().zfill(2) for part in titre[0].split('.')])}":
            titre[1] for titre in target_titres_ord}

    indicator_titres_ord = [titre.split(': ', 1) for titre in indicator_names]
    indicator_titres_ord = [indicator for indicator in indicator_titres_ord if len(indicator) != 1]
    indicator_dict = {
        f"Indicateur {'-'.join([f"{int(part):02d}" if part.isdigit() else part.upper().zfill(2) for part in titre[0].split('.')])}":
            titre[1] for titre in indicator_titres_ord}

    dataframe["ODD"] = dataframe["ODD"].map(lambda x: f"{x} : {odd_dict.get(x, '')}")
    dataframe["Cible"] = dataframe["Cible"].map(lambda x: f"{x} : {target_dict.get(x, '')}")
    dataframe["Indicateur"] = dataframe["Indicateur"].map(lambda x: f"{x} : {indicator_dict.get(x, '')}")

    return dataframe


def filter_similar_entities(entities, threshold=60):

    filtered_entities = []
    seen = set()

    for entity, score in entities:
        # Vérifier si l'entité a déjà été vue
        if any(fuzz.ratio(entity, seen_entity) > threshold for seen_entity in seen):
            continue
        else:
            # Ajouter entités filtrées et entités vues
            filtered_entities.append((entity, score))
            seen.add(entity)

    return filtered_entities

