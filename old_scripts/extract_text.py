import re
import pdfplumber


def nettoyer_texte(texte):
    """
    Nettoie le texte extrait en supprimant les caractères spéciaux, les espaces multiples et les lignes vides.

    paramètres:
        texte: Le texte brut extrait du PDF.
    return:
        Le texte nettoyé.
    """
    # Supprimer les caractères spéciaux non désirés (sauf ponctuation de base)
    texte = re.sub(r'[^a-zA-Z0-9\s.,!?\'"-]', '', texte)

    # Remplacer les espaces multiples par un seul espace
    texte = re.sub(r'\s+', ' ', texte)

    # Supprimer les lignes vides ou contenant seulement des espaces
    texte = '\n'.join([ligne.strip() for ligne in texte.splitlines() if ligne.strip()])

    return texte


def extraire_texte_pdf(indicator):
    """
    Extrait le texte d'un PDF à partir du chemin donné et le nettoie.

    paramètres :
        indicator: Chemin vers le PDF à analyser.
    return:
        Texte extrait et nettoyé du PDF.
    """

    result = "-" + indicator.split("-")[1] + "-" + indicator.split("-")[2] + "-" + indicator.split("-")[3].split(".")[0]
    file_name = f"output_data/extract_indicator{result}.txt"

    with open(file_name, "w", encoding="utf-8") as f:
        texte_complet = ""
        with pdfplumber.open(indicator) as pdf:
            for page in pdf.pages:
                texte_page = page.extract_text()
                if texte_page:
                    texte_complet += texte_page + "\n"

        # Nettoyage du texte extrait
        texte_nettoye = nettoyer_texte(texte_complet)

        # Écriture dans un fichier après nettoyage
        f.write(texte_nettoye)

    return texte_nettoye
