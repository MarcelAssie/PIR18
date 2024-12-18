# In[ ]:
# #### Importations des modules
import requests, json, re, spacy, pandas as pd
from neo4j import GraphDatabase
from deep_translator import GoogleTranslator


# In[ ]:


# Configuration API LM Studio
API_URL = "http://localhost:1234/v1/chat/completions"
HEADERS = {"Content-Type": "application/json"}

# Configuration API Neo4j
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "@Martiale01"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))


# #### Fonctions utilisées pour le traitement :
# - `clean_keywords()`: permet le nettoyage des mots clés extraits d'une question donnée
# - `translate_to_english()` et `translate_to_french()` : permettent la traduction d'une phrase respectivement en anglais et français
# - `compare_keyword_to_keywords()` : permet récupérer tous les mots clés de base de données graphe et d'effectuer une recherche de similitude
# - `extract_keywords()` : permet d'identifier les mots clés d'une phrase
# - `reformulate_question()` : permet de reformuler le besoin de l'utilisateur
# - `search_graph()` : permet de rechercher les mots clés dans la base de données graphe
# - `create_context_answer()` : permet de créer un context pour le llm afin de générer une réponse basée sur les informations du graphe
# - `generate_graph_answer()` : permet de générer une réponse en se basant sur les informations récupérées dans la base de données graphe
# - `generate_raw_answer()` : permet de générer une réponse sans informations en appuis

# In[ ]:


def clean_keywords(raw_keywords, max_words=3):
    cleaned_keywords = [kw.replace("keywords:", "").strip() for kw in raw_keywords]
    cleaned_keywords = [kw.lower() for kw in cleaned_keywords]
    cleaned_keywords = [kw.strip() for kw in cleaned_keywords]
    cleaned_keywords = list(dict.fromkeys(cleaned_keywords))
    cleaned_keywords = [kw.replace("keywords:", "").strip() for kw in cleaned_keywords]
    exclusion_terms = ['sdg', 'sdgs', 'sustainable development', 'indicator', 'sdg indicator', 'keywords', 'keyword']
    filtered_keywords = [kw for kw in cleaned_keywords if not any(excluded in kw for excluded in exclusion_terms)]
    results = [kw for kw in filtered_keywords if 1 <= len(kw.split()) <= max_words and not re.search(r'\d+', kw)]
    return results


# In[ ]:


def translate_to_english(text):
    translated = GoogleTranslator(source="auto", target="en").translate(text)
    return translated


# In[ ]:


def translate_to_french(text):
    translated = GoogleTranslator(source="auto", target="fr").translate(text)
    return translated


# In[ ]:


def extract_keywords(question, model):
    # Préparation de la requête
    payload = {
        "model": model,
        "messages": [
        {"role": "system",
         "content": "You are an expert in natural language processing and sustainable development. Your task is to extract only the most relevant keywords from the user's question."},
        {"role": "user",
         "content": f"""
            Extract the most relevant keywords from the following question.
            Do not include any explanations, definitions, or irrelevant terms. Return only the keywords as a comma-separated list python.

            Question: {question}"""}
        ],
        "max_tokens": 500,
        "temperature": 0.0,
        "top_p": 0.9,
    }

    # Envoyer la requête
    response = requests.post(API_URL, headers=HEADERS, data=json.dumps(payload))

    # Gérer la réponse
    if response.status_code == 200:
        raw_output = response.json()["choices"][0]["message"]["content"]
        # Nettoyer les mots-clés
        cleaned_keywords = clean_keywords(raw_output.split(','))
        print("\nMots-clés extraits de la question :", cleaned_keywords)
        return cleaned_keywords
    else:
        print("Erreur API :", response.status_code, response.text)
        return []


# In[ ]:


def compare_keyword_to_keywords(graph_words):

    nlp = spacy.load("en_core_web_md")

    query = """
    MATCH (n)
    WHERE n:Keyword OR n:Topic
    RETURN n.word AS keyword
    """
    keywords = []
    with driver.session() as session:
        result = session.run(query)
        for record in result:
            keywords.append(record["keyword"])

    global_results = []
    for graph_word in graph_words:
        token1 = nlp(graph_word)
        for word in keywords:
            token2 = nlp(word)

            if token1.vector_norm > 0 and token2.vector_norm > 0:
                similarity = token1.similarity(token2)
                if similarity > 0.95:
                    global_results.append(word)
    keywords = list(dict.fromkeys(global_results))
    return keywords


# In[ ]:


def reformulate_question(question, model):
    payload = {
        "model": model,
        "messages": [
        {"role": "system",
         "content": """
         You are an expert in natural language processing. Your task is to reformulate questions to make them clearer, more specific, and easier to extract relevant keywords. The reformulation should explore alternative phrasing while retaining the original meaning.

         Examples:
         1. Original: "How can renewable energy help reduce greenhouse gas emissions?"
            Reformulated: "What role does renewable energy play in decreasing greenhouse gas emissions worldwide?"

         2. Original: "How can digital tools improve education for children in rural areas?"
            Reformulated: "In what ways can digital technologies enhance access to quality education in rural regions?"

         Do not provide explanations or extra text—output only the reformulated question as a single sentence.
         """},
        {"role": "user",
         "content": f"""
            Reformulate the following question to make it clearer and easier to extract relevant keywords for a knowledge graph search.

            Original Question: {question}
         """}
    ],
    "max_tokens": 100,
    "temperature": 0.3,
    "top_p": 0.9,
    }

    response = requests.post(API_URL, headers=HEADERS, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        print("Erreur API lors de la reformulation :", response.status_code, response.text)
        return question


# In[ ]:


def search_graph(keywords):
    with driver.session() as session:

        # Première requête : rechercher les ODD, cibles et indicateurs liés aux mots-clés
        query1 = f"""
        MATCH (s:SDG)-[:contain]->(t:Target)-[:contain]->(i:Indicator)-[:measuredBy]->(k:Keyword)
        WHERE k.word IN {keywords}
        RETURN s.code AS ODD, s.title AS OddDescription, t.code AS Cible, t.description AS CibleDescription,
               i.code AS Indicateur, i.description AS IndicateurDescription, collect(k.word) AS MotsCles
        """
        result1 = session.run(query1)

        odd, cible, indicateur, motsCles = [], [], [], []
        for record in result1:
            if record:
                odd.append(f"{record['ODD']}: {record['OddDescription']}")
                cible.append(f"{record['Cible']}: {record['CibleDescription']}")
                indicateur.append(f"{record['Indicateur']}: {record['IndicateurDescription']}")
                motsCles.append(','.join(record["MotsCles"]))

        df1 = pd.DataFrame({
            "ODD": odd,
            "Cible": cible,
            "Indicateur": indicateur,
            "Mots-clés": motsCles
        })

        # Deuxième requête : rechercher les Goals associés aux mots-clés
        query2 = f"""
        MATCH (s:SDG)-[:measuredBy]->(m:Topic)
        WHERE m.word IN {keywords}
        RETURN s.code AS Goal, collect(m.word) AS MotsCles
        """
        result2 = session.run(query2)

        goals, motsClesGoals = [], []
        for record in result2:
            if record:
                goals.append(record["Goal"])
                motsClesGoals.append(', '.join(record["MotsCles"]))

        df2 = pd.DataFrame({
            "Goal": goals,
            "Mots-clés": motsClesGoals
        })

        df_combined = pd.concat(
            [df1, df2],
            axis=0,
            ignore_index=True
        )
        return df_combined


# In[ ]:


def create_context_answer(df, question):

    context = f"Based on the information extracted from the graph, here is a detailed breakdown:\n\n"

    for _, row in df.iterrows():
        if pd.isna(row['ODD']) or pd.isna(row['Cible']) or pd.isna(row['Indicateur']):
            context += f"Goal {row['Goal']} which addresses themes such as {row['Mots-clés']}\n"
            continue

        context += f"Goal {row['ODD']}\n"
        context += f"Target {row['Cible']}\n"
        context += f"Indicator {row['Indicateur']}\n"

        context += "\n"

    context += f"To address your question: {question}\n\n"
    context += "Please ensure that your answer is based only on the information provided above, which outlines specific SDGs, targets, and indicators. Use this context to guide your response and explain the correlation between the SDG, the target, and the indicator with the question at hand."
    return context


# In[ ]:


def generate_graph_answer(context, question, model):

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an expert in Sustainable Development Goals (SDGs) and provide answers based on extracted data."},
            {"role": "user", "content": f"{context}. Now, answer the following question: {question}"}
        ],
        "temperature": 0.5,
        "max_tokens": 1000,
    }

    response = requests.post(API_URL, headers=HEADERS, data=json.dumps(payload))

    if response.status_code == 200:
        response_translated = translate_to_french(response.json()["choices"][0]["message"]["content"])
        return response_translated
    else:
        return f"Error: {response.status_code} - {response.text}"


# In[ ]:


def generate_raw_answer(question, model):
    context = f"""
            You are an AI specialized in the Sustainable Development Goals (SDGs).
            You must provide accurate, concise, and context-specific answers using your knowledge of the 17 SDGs, their associated targets, and indicators.
            Focus your responses only on the question asked, ensuring they align strictly with SDG data and terminology.
            Avoid adding any unrelated information or general context beyond what is necessary to answer the question.

            If the question references a specific goal, target, or indicator, structure your answer as follows:
            1. Briefly explain the goal or indicator if necessary.
            2. Provide the specific data or insights related to the question, ensuring alignment with SDG sources.
            3. Cite the SDG, target, or indicator explicitly if relevant.

            Ensure your answer is structured, clear, and directly addresses the user's inquiry.

            Now, answer the following question:
            {question}
        """

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an expert in SDGs and answer based on accurate data."},
            {"role": "user", "content": context}
        ],
        "temperature": 0.3,
        "max_tokens": 1000,
    }

    response = requests.post(API_URL, headers=HEADERS, data=json.dumps(payload))

    if response.status_code == 200:
        response_translated = translate_to_french(response.json()["choices"][0]["message"]["content"])
        return response_translated
    else:
        return f"Error: {response.status_code} - {response.text}"

