Voici une version mise à jour de votre README en fonction des informations du document fourni :  

---

# 🚀 **PIR18 - Extraction de données contextuelles pour les ODD à l'aide des LLM et des graphes de connaissances**

Ce dépôt regroupe l'ensemble des codes, ressources et documents liés au **Projet d'Initiation à la Recherche 18 (PIR18)**. L'objectif principal de ce projet est de développer une méthode avancée d'extraction de données contextuelles basée sur les **Grands Modèles de Langage (LLM)** et de les structurer sous forme de **graphes de connaissances**. Cette approche vise à faciliter l'analyse et la visualisation des relations entre les **Objectifs de Développement Durable (ODD)**, leurs cibles et leurs indicateurs.

---

## 📚 **Table des matières**

1. [🏆 Objectifs principaux](#-objectifs-principaux)  
2. [🗂️ Structure du dépôt](#️-structure-du-dépôt)  
3. [🛠️ Prérequis pour l'installation](#️-prérequis-pour-linstallation)  
4. [📈 Méthodologie utilisée](#-méthodologie-utilisée)  
5. [✨ Fonctionnalités principales](#-fonctionnalités-principales)  
6. [🚀 Prochaines étapes](#-prochaines-étapes)  
7. [💡 Contributeurs](#-contributeurs)  
8. [📫 Contact](#-contact)  

---

## 🏆 **Objectifs principaux**

1. **Extraction de données contextuelles**  
   - Utiliser des **LLM** pour identifier et extraire des topics, entités et mots-clés pertinents à partir de métadonnées textuelles liées aux ODD.  

2. **Généralisation de l'approche**  
   - Adapter les algorithmes d'extraction pour couvrir l'ensemble des 17 ODD et leurs 169 cibles, en prenant en compte les différences de structure et de format des données.  

3. **Création et visualisation des graphes de connaissances**  
   - Modéliser les données extraites sous forme de **nœuds** et **relations**, et les intégrer dans des **graphes de connaissances interactifs**.  

4. **Analyse des relations complexes**  
   - Étudier les interconnexions entre les objectifs, cibles, indicateurs et données externes grâce à des outils de visualisation avancés (ex. Neo4j).  

---

## 🗂️ **Structure du dépôt**  


- **`/MetaData/`**  
  Contient des fichiers de métadonnées extraits de format _.docx_ sur le site https://unstats.un.org/sdgs/metadata et convertis en formats _txt_. Ces metadonnées sont classées par ODD.

- **`/Other/`**  
  Contient tous les documents annexes utilisés dans des scripts 

- **`/Output/`**  
  Dossiers contenant les résultats générés. Ce sont les mots-clés extraits par les LLM et les LM, organisés comme suit :

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
   Assurez-vous que **Python 3.9** ou une version ultérieure est installé :  
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurer Neo4j**  
   - Installer Neo4j (https://neo4j.com/use-cases/knowledge-graph/).  
   - Activer le plugin **APOC** pour bénéficier de fonctionnalités avancées.  

4. **Lancer le projet**  
   *(Fonctionnalité en développement)*.  

---

## 📈 **Méthodologie utilisée**

1. **Revue de la littérature**  
   Étudier les approches actuelles pour :  
   - L'extraction de données contextuelles.  
   - La création et l'optimisation de graphes de connaissances (KG).  

2. **Collecte et préparation des données**  
   Préparer les métadonnées disponibles sur [UN SDG Metadata](https://unstats.un.org/sdgs/metadata) pour une exploitation optimale.  

3. **Développement de modèles LLM**  
   Adapter et tester des modèles comme **Mistral 7B** et **LLaMA 2-7B Chat** pour l'extraction de topics et d'entités liés aux ODD.  

4. **Construction des graphes de connaissances**  
   - Structurer les données extraites sous forme de nœuds et relations dans Neo4j.  
   - Exemple de relations :  
     - **Goal → contains → Target**  
     - **Target → contains → Indicator**  
     - **Indicator → measuredBy → Keyword**  

5. **Validation et visualisation**  
   Manipuler et interroger les graphes à travers des cas pratiques pour valider l'approche.  

   I 

---

## ✨ **Fonctionnalités principales**

- **Extraction automatisée** des mots-clés et topics des ODD.  
- **Création de graphes interactifs** pour explorer les relations sémantiques.  
- **Visualisation avancée** des liens entre indicateurs, cibles et objectifs.  

---

## 🚀 **Prochaines étapes**

1. **Optimisation des modèles**  
   - Intégrer des techniques de nettoyage et d'enrichissement des données.  

2. **Amélioration des graphes**  
   - Ajouter des propriétés enrichies aux nœuds et relations.  

3. **Développement d'un outil interactif**  
   - Proposer une interface utilisateur (chatbot) simplifiée pour discuter.  

4. **Publication scientifique**  
   - Documenter les résultats obtenus dans un **article scientifique** et le soumettre à une revue ou conférence. 

---

## 💡 **Contributeurs**

- **Étudiants**  
  - Marcel Assie  
  - Liam Longfier  

- **Encadrants**  
  - Malika GRIM-YEFSAH  
  - Wissal BENJIRA  

Projet réalisé dans le cadre de l'Initiation à la Recherche des étudiants de 2ème année d'ingénieur à l'Ecole Nationale des Sciences Géographiques, France.  

---

## 📫 **Contact**
Pour toute question ou suggestion : 

📧 **Emails** :  
- Liam.Longfier@ensg.eu  
- Kouakou-Kan-Jose-Marcel.Assie@ensg.eu

🛠️ **Outils utilisés** : Python, Neo4j, PyCharm, Jupyter Notebook.  
