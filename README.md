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
    - Le téléchargement des métadonnées
    - L'extraction des mots-clés.  
    - La création et la visualisation des graphes de connaissances.  
    - L'extraction des noms et des descriptions des SDGs
    - Le traitement de question

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
   - Créer le DBMS (Database Management System)
   - Activer le plugin **APOC** pour bénéficier de fonctionnalités avancées.  
   

4. **Configurer LM Studio**
   - Télécharger et installer l'application LM Studio (https://lmstudio.ai/)
   - Télécharger les modèles _Mistral 7B_ et _LLaMA 2-7B_ dans la section _Discover_.


6. **Lancer l'interaction**
    ```bash
    python .\Scripts\start.py
   ```
> NB : Pour un lancement du programme depuis le début, voici les scripts que vous devez exécuter dans l'ordre suivant :
>
>    1. **Chargement et organisation des métadonnées :**
>      - `.\Scripts\get_manage_metadata.py` 
>    2. **Téléchargement des descriptions des ODD, cibles et indicateurs :**
>       - `.\Scripts\get_sdg_names.ipynb` 
>    3. **Extraction des mots-clés des métadonnées :**
>       - `.\Scripts\extraction_entities_llama.ipynb` (Pour l'extraction avec le modèle llama)
>       - `.\Scripts\extraction_entities_mistral.ipynb` (Pour l'extraction avec le modèle mistral)
>       - `.\Scripts\extraction_entities_lm.ipynb` (Pour l'extraction avec les LM)
>    4. **Construction du graphe de Connaissance :**
>       - `.\Scripts\graph_construction.ipynb` 
>    5. **Interaction :**
>       - `.\Scripts\start.py`
>       
> N'oubliez pas d'exécuter chaque script dans cet ordre pour garantir un lancement correct du programme.


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

---

## ✨ **Fonctionnalités principales**

- **Téléchargement et organisation automatisés** des métadonnées sur le site officiel [UN SDG Metadata](https://unstats.un.org/sdgs/metadata). 
- **Extraction automatisée** des mots-clés et topics des ODD.  
- **Création de graphes interactifs** pour explorer les relations sémantiques.  
- **Visualisation avancée** des liens entre indicateurs, cibles et objectifs.  

---

## 🚀 **Prochaines étapes**

1. **Optimisation du temps d'exécution**  
   - Intégrer des outils afin d'accélérer le temps de traitement de certaines opérations.  

2. **Publication scientifique**  
   - Documenter les résultats obtenus dans un **article scientifique** et le soumettre à une revue ou conférence. 

---

## 💡 **Contributeurs**

- **Étudiants**   
  - Liam Longfier  
  - Marcel Assie 

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

🛠️ **Outils utilisés** : Python, Neo4j, LM Studio, HuggingFace, PyCharm, Jupyter Notebook.  
