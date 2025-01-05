#!/usr/bin/env python
# coding: utf-8

# #### Importations des modules

# In[211]:


import requests, json, re, spacy, pandas as pd, numpy as np
from neo4j import GraphDatabase
from deep_translator import GoogleTranslator
import time


# #### Configuration de l'API de LM Studio et de l'API de Neo4j

# In[212]:


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
# - `search_indicators()` : permet de rechercher indicateurs dans la base de données graphe
# - `generate_graph_answer()` : permet de générer une réponse complète et structurée basée sur les informations récupérées dans la base de données graphe
# - `generate_raw_answer()` : permet de générer une réponse claire et contextuelle sans informations issues du graphe en appuis

# In[213]:


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


# In[214]:


def translate_to_english(text):
    translated = GoogleTranslator(source="auto", target="en").translate(text)
    return translated


# In[215]:


def translate_to_french(text):
    translated = GoogleTranslator(source="auto", target="fr").translate(text)
    return translated


# In[216]:


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


# In[217]:


def compare_keyword_to_keywords(graph_words,  threshold):
    # Load Spacy model
    nlp = spacy.load("en_core_web_md")

    # Fetch keywords from the graph
    query = """
    MATCH (n)
    WHERE n:Keyword OR n:Topic
    RETURN n.word AS keyword
    """
    with driver.session() as session:
        result = session.run(query)
        keywords = [record["keyword"] for record in result]

    # Convert keywords into Spacy vectors
    keyword_vectors = np.array([nlp(word).vector for word in keywords if nlp(word).vector_norm > 0])
    graph_word_vectors = np.array([nlp(word).vector for word in graph_words if nlp(word).vector_norm > 0])

    # Compute cosine similarities in one operation
    similarities = np.dot(graph_word_vectors, keyword_vectors.T)  # Matrix multiplication
    norms = np.linalg.norm(graph_word_vectors, axis=1).reshape(-1, 1) * np.linalg.norm(keyword_vectors, axis=1)
    cosine_similarities = similarities / norms

    # Filter results above a similarity threshold
    matches = np.argwhere(cosine_similarities > threshold)
    matched_keywords = [keywords[j] for _, j in matches]
    return list(set(matched_keywords))  # Remove duplicates


# In[218]:


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


# In[219]:


def search_indicators(keywords):
    with driver.session() as session:
        # Requête principale : rechercher les ODD, cibles, indicateurs et mots-clés
        query1 = f"""
        MATCH (s:SDG)-[:contains]->(t:Target)-[:contains]->(i:Indicator)-[:measuredBy]->(k:Keyword)
        WHERE k.word IN {keywords}
        RETURN i.code AS Indicateur, i.description AS IndicateurDescription
        """
        result1 = session.run(query1)

        # Stocker les résultats de la première requête
        indicators_data = []
        for record in result1:
            if record:
                indicators_data.append({
                    "Indicateur": record["Indicateur"],
                    "Pertinence": "Très pertinent",
                })

        # Requête secondaire : rechercher les Goals associés aux mots-clés à travers les Topics
        query2 = f"""
        MATCH (s:SDG)-[:measuredBy]->(m:Topic)
        WHERE m.word IN {keywords}
        RETURN s.code AS Goal
        """
        result2 = session.run(query2)

        # Collecter les Goals associés
        goals = set()
        for record in result2:
            if record:
                goals.add(record["Goal"])

        # Si des Goals sont trouvés, récupérer les indicateurs associés à ces Goals
        if goals:
            query3 = f"""
            MATCH (s:SDG)-[:contains]->(t:Target)-[:contains]->(i:Indicator)
            WHERE s.code IN {list(goals)}
            RETURN i.code AS Indicateur, i.description AS IndicateurDescription
            """
            result3 = session.run(query3)

            for record in result3:
                if record:
                    indicators_data.append({
                        "Indicateur": record["Indicateur"],
                        "Pertinence": "Pertinent",
                    })

        df = pd.DataFrame(indicators_data).drop_duplicates(subset=["Indicateur"]).reset_index(drop=True)

    return df


# In[220]:


def generate_graph_answer(df, question):
    context = f"Pour répondre à la question : '{translate_to_french(question)}', voici les indicateurs pertinents :\n\n"
    for _, row in df.iterrows():
        context += f"{row['Indicateur']} : {row["Pertinence"]}\n"
    return context


# In[221]:


def generate_raw_answer(question, model="default-model-name"):

    payload = {
        "model": model,
        "messages": [
            {"role": "system",
             "content": "You are an AI expert in sustainable development and natural language processing. "
                        "Your task is to analyze the user's question and provide a clear, specific answer with "
                        "relevant SDG indicators and their relationships. If the question does not relate to the SDGs, "
                        "state that the question is not related to SDGs."},
            {"role": "user",
             "content": f"""
                Analyze the following question and extract relevant indicators from the context. If the question is unrelated to the SDGs, provide a clear statement indicating that.
                Answer concisely, focusing on the most relevant information.

                Question: {question}"""}
        ],
        "max_tokens": 500,
        "temperature": 0.2,
        "top_p": 0.9,
    }

    # Envoi de la requête à l'API
    response = requests.post(API_URL, headers=HEADERS, data=json.dumps(payload))

    if response.status_code == 200:
        return translate_to_french(response.json()["choices"][0]["message"]["content"].strip())
    else:
        print("Erreur API lors de la reformulation :", response.status_code, response.text)

        return "Impossible de générer une réponse. Vérifiez la configuration de l'API ou la requête."

