# 🚀 **PIR18 - Extraction de données contextuelles pour les ODD à l'aide des LLM et des graphes de connaissances**  

Ce dépôt regroupe l'ensemble des codes, ressources et documents liés au **Projet d'Initiation à la Recherche (PIR18)**. L'objectif principal de ce projet est de développer une méthode avancée d'extraction de données contextuelles basée sur les **Grands Modèles de Langage (LLM)** et de les structurer sous forme de **graphes de connaissances** pour mieux comprendre et analyser les Objectifs de Développement Durable (ODD).  

---

## 📚 **Table des matières**

1. [🏆 Objectifs principaux](#-objectifs-principaux)  
2. [🗂️ Structure du dépôt](#️-structure-du-dépot)  
3. [🛠️ Prérequis pour l'installation](#️-prérequis-pour-linstallation)  
4. [📈 Méthodologie utilisée](#-méthodologie-utilisée)  
   - [🔍 Extraction des mots-clés](#-extraction-des-mots-clés)  
   - [📊 Création des graphes de connaissances](#-création-des-graphes-de-connaissances)  
   - [💻 Requêtes et visualisations](#-requêtes-et-visualisations)  
5. [✨ Fonctionnalités principales](#-fonctionnalités-principales)  
6. [🚀 Prochaines étapes](#-prochaines-étapes)  
7. [💡 Contributeurs](#-contributeurs)  
8. [📫 Contact](#-contact)  

---

## 🏆 **Objectifs principaux**  

1. **Extraction de données contextuelles**  
   - Utiliser des techniques liées aux **Grands Modèles de Langage (LLM)** pour identifier et extraire des informations pertinentes à partir de sources textuelles.  

2. **Création de graphes de connaissances**  
   - Représenter les informations extraites sous forme de graphes, en mettant en évidence les relations significatives entre les entités (ODD, cibles, indicateurs).  

3. **Utilisation de modèles avancés**  
   - Implémenter des **algorithmes basés sur les LLM** (comme LLaMA, Mistral) pour analyser les liens contextuels entre les **indicateurs des ODD** et les données extraites.  

---

## 🗂️ **Structure du dépôt**  


- **`/MetaData/`**  
  Contient des fichiers de métadonnées extraits de format _.docx_ sur le site https://unstats.un.org/sdgs/metadata et convertis en formats _txt_. Ces metadonnées sont classées par ODD.

- **`/Other/`**  
  Contient tous les documents annexes utilisés dans des scripts 

- **`/OutputData/`**  
  Dossiers contenant les **résultats générés**. Ce sont en les mots clés extraits par les LLM et LM: 

  - **`/DataLLM/`**
    - **`/llama/`**
        - Mots-clés extraits par le modèle LLaMA, classés selon les ODD, cibles et indicateurs.
    - **`/mistral/`**
        - Mots-clés extraits par le modèle Mistral, classés selon les ODD, cibles et indicateurs.
  - **`/DataLM/`**
    - Tous les mots-clés classés par ODD, cibles et indicateur et regroupé dans le dossier spécifié.  

- **`/Scripts/`**  
  Répertoire des **scripts actifs actuellement utilisés** pour :  
    - Le téléchargement des metadonnées
    - L'extraction des mots-clés.  
    - La création et la visualisation des graphes de connaissances.  
    - La traitement de question
    - L'extraction des noms et des descriptions des SDGs

- **`/Tests/`**  
  Contient des scripts expérimentaux et des algorithmes en cours de test.  

- **`requirements.txt`**  
  Liste des **dépendances Python** nécessaires pour l’exécution du projet.  

---

## 🛠️ **Prérequis pour l'installation**  

1. **Cloner le dépôt**  
   ```bash  
   git clone https://github.com/MarcelAssie/PIR18.git
   ```  

2. **Installer les dépendances**  
   Assurez-vous que Python 3.9 ou une version ultérieure est installé sur votre système. Ensuite, exécutez :  
   ```bash  
   pip install -r requirements.txt  
   ```  

3. **Configurer Neo4j**  
   - Installer et démarrer une instance de **Neo4j**.  
   - Ajouter le plugin **APOC** pour bénéficier de fonctionnalités avancées.  

4. **Lancer le projet (il faut créer cette fonction qui relancera toutes les étapes dde développement)**  
   ```bash  
   python start.py  
   ```
---

## 📈 **Méthodologie utilisée**  

1. **Extraction des mots-clés**  
   - Utilisation de modèles comme **Mistral 7B** et **LLaMA 2-7B Chat** pour identifier les mots-clés pertinents à partir des meta données.  
   - Nettoyage et classification automatique des mots-clés en fonction des **Objectifs, Cibles, et Indicateurs des ODD**.  

2. **Création des graphes de connaissances**  
   - Les mots-clés extraits sont structurés en **nœuds** et **relations** dans Neo4j pour représenter les liens contextuels.  
   - Exemple de relations :  
     - **Goal → contain → Target**  
     - **Target → contain → Indicator**  
     - **Indicator → measuredBy → Keyword**  

3. **Requêtes et visualisations**  
   - Utilisation de requêtes Cypher pour interroger et visualiser les graphes afin d’obtenir des analyses détaillées des relations entre les ODD, cibles, et indicateurs.
   
4. **Interaction**  
   - En cours de developpement...

---

## ✨ **Fonctionnalités principales**  

- **Extraction automatisée des mots-clés** à partir de documents textuels (meta données SDGs).  
- **Classification intelligente** des données en fonction des Objectifs de Développement Durable.  
- **Création de visualisations interactives** des graphes pour explorer les relations entre les ODD.  
- **Interface utilisateur** (en cours de développement) pour simplifier l’interaction avec le système.  

---

## 🚀 **Prochaines étapes**  

1. **Optimisation des algorithmes d'extraction**  
   - Intégrer des algorithmes de nettoyage de donnée pour des metadonnées plus riches.  

2. **Amélioration des graphes**  
   - Ajouter des métadonnées enrichies pour les nœuds et relations. 
   
3. **Amélioration de l'agorithme de traitement d'information**  
   - Améliorer le processus de traitement des informations par le llm pour la génération de réponse.  

4. **Publication scientifique**  
   - Documenter les résultats obtenus dans un **article scientifique** et le soumettre à une revue ou conférence.  

---

## 💡 **Contributeurs**

- **Etudiants**
  - Marcel Assie
  - Liam Longfier
  

- **Encadrants**
  - GRIM-YEFSAH Malika 
  - BENJIRA Wissal

Projet mené dans le cadre de l'Initiation à la Recherche des étudiants de la 2ème année d'ingénieur à l'Ecole Nationale des Sciences Géographiques, France.

---

## 📫 **Contact**  

Pour toute question ou suggestion :  

📧 Emails : Kouakou-Kan-Jose-Marcel.Assie@ensg.eu, Liam.Longfier@ensg.eu

🛠️ Outils : PyCharm, Neo4j (Cypher), Python, Jupyter NoteBook.  

