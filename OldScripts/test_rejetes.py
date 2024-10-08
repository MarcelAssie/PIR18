from spellchecker import SpellChecker

def txt_to_string(txt_file):
    """
    Convertit un fichier texte en une chaîne de caractères.

    Paramètres:
    txt_file (str): Chemin du fichier texte à convertir

    Returns:
    str: Chaîne de caractères contenant le texte du fichier
    """
    spell = SpellChecker()
    corrected_text = []
    # Ouvrir le fichier texte et lire son contenu
    try:
        with open(txt_file, "r", encoding="utf-8") as f:
            for line in f:
                # Correction orthographique pour chaque mot dans la ligne
                line_corrected = " ".join(spell.correction(word) if spell.correction(word) is not None else word for word in line.split())
                corrected_text.append(line_corrected)
        return "\n".join(corrected_text)
    except FileNotFoundError:
        print(f"Le fichier {txt_file} n'existe pas.")
        return ""
