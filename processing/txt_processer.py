import re
from pathlib import Path
from typing import List

class SentenceExtractor:
    """
    Extrait les phrases d'un fichier texte selon les règles :
    - Début : majuscule (au début de ligne ou après un point)
    - Fin : point suivi d'une majuscule ou d'un saut de ligne
    """
    def __init__(self, txt_file: Path):
        self.txt_file = Path(txt_file)

    def extract_sentences(self) -> List[str]:
        sentences = []
        
        with open(self.txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Nettoyer le contenu
        content = content.replace('\r\n', '\n').replace('\r', '\n')
        
        # Normaliser les espaces multiples et tabulations
        content = re.sub(r'[ \t]+', ' ', content)
        
        # Diviser en paragraphes (séparés par des lignes vides)
        paragraphs = re.split(r'\n\s*\n', content)
        
        for paragraph in paragraphs:
            if paragraph.strip():
                paragraph_sentences = self._extract_sentences_from_paragraph(paragraph.strip())
                sentences.extend(paragraph_sentences)
        
        return sentences
    
    def _extract_sentences_from_paragraph(self, paragraph: str) -> List[str]:
        """
        Extrait les phrases d'un paragraphe
        """
        sentences = []
        
        # Remplacer les retours à la ligne par des espaces
        paragraph = re.sub(r'\n+', ' ', paragraph)
        
        # Pattern pour détecter les phrases
        # Une phrase se termine par un point suivi d'un espace et d'une majuscule
        # ou par un point à la fin du paragraphe
        pattern = r'[^.]*\.(?=\s+[A-ZÉÈÀÂÎÔÙÛÇ]|$)'
        
        matches = re.finditer(pattern, paragraph, re.MULTILINE)
        
        for match in matches:
            sentence = match.group().strip()
            
            # Nettoyer la phrase
            sentence = re.sub(r'\s+', ' ', sentence)
            
            # Vérifier que ce n'est pas une abréviation et que la phrase n'est pas vide
            if sentence and not self._is_abbreviation(sentence) and len(sentence) > 10:
                sentences.append(sentence)
        
        return sentences
    
    def _is_abbreviation(self, text: str) -> bool:
        """
        Vérifie si le point fait partie d'une abréviation
        """
        # Liste d'abréviations communes
        abbreviations = [
            'M.', 'Mme.', 'Mlle.', 'Dr.', 'Pr.', 'Prof.', 'St.', 'Ste.',
            'etc.', 'cf.', 'vs.', 'i.e.', 'e.g.', 'p.', 'pp.', 'vol.',
            'n°', 'N°', 'n°s', 'N°s', 't.', 'T.', 's.', 'S.'
        ]
        
        # Vérifier si le texte se termine par une abréviation
        for abbr in abbreviations:
            if text.strip().endswith(abbr):
                return True
        
        # Vérifier les abréviations avec espaces
        words = text.split()
        if len(words) >= 2:
            last_word = words[-1]
            for abbr in abbreviations:
                if last_word == abbr:
                    return True
        
        return False
