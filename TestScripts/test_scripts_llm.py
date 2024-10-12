from transformers import pipeline

# Créer un pipeline de génération de texte avec Bloom
bloom_pipeline = pipeline("text-generation", model="bigscience/bloom-560m")

# Indicateurs à tester (par exemple, indicateur 11.7.1 de l'ODD 11)
indicators_text = """
L'indicateur 11.7.1 mesure la proportion de la population ayant un accès facile aux espaces verts et aux espaces publics, y compris les jeunes, les personnes âgées et les personnes en situation de handicap. 
Cet indicateur fait partie des Objectifs de Développement Durable de l'ONU, plus précisément l'ODD 11, qui concerne les villes et les communautés durables.
"""

# Formulation du prompt pour extraire les mots-clés ou analyser l'indicateur
prompt = f"Quels sont les mots-clés les plus importants de ce texte sur les ODD : {indicators_text}"

# Générer les mots-clés en passant directement le prompt
response = bloom_pipeline(prompt, max_length=100, num_return_sequences=1, truncation=True)

# Afficher la réponse générée par Bloom
generated_text = response[0]['generated_text']
print("Mots-clés extraits :", generated_text)
