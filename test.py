import re

# Chaîne d'exemple
chaine = "ODD01"

# Utiliser une expression régulière pour extraire le nombre
print(re.search(r'\d+', chaine).group())


    # Afficher le nombre extrait
