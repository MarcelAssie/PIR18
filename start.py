import os
from ActivesScripts.extraction_entities import entities_extractions

if __name__ == "__main__":
    # Exécution de tous les ODD
    odd_files = os.listdir("MetaD")
    for odd_file in odd_files:
        entities_extractions(f"MetaD/{odd_file}")
