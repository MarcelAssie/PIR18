#!/usr/bin/env python
# coding: utf-8

# In[43]:


import os, csv, pandas as pd
from py2neo import Graph


# In[44]:


files_path = "../Output/DataLLM/llama"
files = os.listdir(files_path)


# In[45]:


graph = Graph("bolt://localhost:7687", auth=("neo4j", "@Martiale01"))


# In[46]:


Ontology_final = "../Other/Ontology_final.csv"

with open(Ontology_final, encoding="utf-8") as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter=';')
    data = list(csvreader)
df_Ontology_final = pd.DataFrame(data)


# In[47]:


for data in files :
    df = pd.read_csv(f"{files_path}/{data}", delimiter=";")
    for _, row in df.iterrows():
        odd = row['ODD']
        cible = row['Cible']
        indicateur = row['Indicateur']
        mot_cle = row['Mots-cles']

         # Nous utilisons MERGE au lieu de CREATE afin de créer les nœuds ODD, Cible, Indicateur, Mots-clés sans doublons. Si le nœud existe déjà, il ne sera pas recréé
        graph.run(f"MERGE (s:SDG {{code: 'SDG{odd[3:5]}'}}) SET s.title = '{odd[8:]}'")
        graph.run(f"MERGE (t:Target {{code: '{cible[6:11]}'}}) SET t.description = '{cible[14:]}'")
        graph.run(f"MERGE (i:Indicator {{code: '{indicateur[11:19]}'}}) SET i.description = '{indicateur[22:]}'")
        graph.run(f'MERGE (k:Keyword {{word: "{mot_cle}"}})')

        # Les relations entre les nœuds
        graph.run(f"""
            MATCH (s:SDG {{code: 'SDG{odd[3:5]}'}})
            MATCH (t:Target {{code: '{cible[6:11]}'}})
            MATCH (i:Indicator {{code: '{indicateur[11:19]}'}})
            MATCH (k:Keyword {{word: "{mot_cle}"}})
            MERGE (s)-[:contains]->(t)
            MERGE (t)-[:contains]->(i)
            MERGE (i)-[:measuredBy]->(k)
        """)


# In[48]:


for _, row in df_Ontology_final.iterrows():
    mot_cle = row['﻿keyword']
    odd = row['classification']
    odd = odd.replace(str(odd[3:]),str(f"{int(odd[3:])+ 0:02}"))
    graph.run(f'MERGE (m:Topic {{word: "{mot_cle}"}})')
    graph.run(f"MERGE (s:SDG {{code: 'SDG{odd[3:5]}'}})")
    graph.run(f"""
    MATCH (m:Topic {{word: "{mot_cle}"}}), (s:SDG {{code: "SDG{odd[3:5]}"}})
    MERGE (s)-[:measuredBy]->(m)
    """)

