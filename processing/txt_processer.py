import re
from pathlib import Path
from typing import List

class ParagraphExtractor:
    """
    Extrait les paragraphes d'un fichier texte selon les règles :
    - Début : alinéa (indentation) + majuscule
    - Fin : point + saut de ligne
    """
    def __init__(self, txt_file: Path):
        self.txt_file = Path(txt_file)

    def extract_paragraphs(self) -> List[str]:
        paragraphs = []
        current_paragraph = []
        with open(self.txt_file, 'r', encoding='utf-8') as f:
            for line in f:
                # Début de paragraphe : indentation + majuscule
                if re.match(r'^[ \t]+[A-ZÉÈÀÂÎÔÙÛÇ]', line):
                    if current_paragraph:
                        # On termine le paragraphe précédent
                        paragraph = ''.join(current_paragraph).strip()
                        if paragraph:
                            paragraphs.append(paragraph)
                        current_paragraph = []
                current_paragraph.append(line)
                # Fin de paragraphe : point suivi d'un saut de ligne
                if re.search(r'\.[ \t]*\n$', line):
                    paragraph = ''.join(current_paragraph).strip()
                    if paragraph:
                        paragraphs.append(paragraph)
                    current_paragraph = []
            # Ajouter le dernier paragraphe s'il existe
            if current_paragraph:
                paragraph = ''.join(current_paragraph).strip()
                if paragraph:
                    paragraphs.append(paragraph)
        return paragraphs
