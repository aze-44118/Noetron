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
        
        # Diviser en lignes
        lines = content.split('\n')
        
        # Initialiser la phrase en cours
        current_sentence = ""
        in_sentence = False
        
        for line_num, line in enumerate(lines):
            line = line.strip()
            if not line:  # Ligne vide
                if in_sentence and current_sentence.strip():
                    # Fin de phrase à la ligne vide
                    sentence = current_sentence.strip()
                    if sentence and sentence.endswith('.'):
                        sentences.append(sentence)
                    current_sentence = ""
                    in_sentence = False
                continue
            
            # Traiter la ligne caractère par caractère
            i = 0
            while i < len(line):
                char = line[i]
                
                # Vérifier si c'est le début d'une phrase
                # Cas 1: Majuscule après un point ou au début de ligne
                if (char.isupper() or char in 'ÉÈÀÂÎÔÙÛÇ') and (i == 0 or line[i-1] in ' .'):
                    # Commencer une nouvelle phrase
                    if in_sentence and current_sentence.strip():
                        # Sauvegarder la phrase précédente
                        sentence = current_sentence.strip()
                        if sentence and sentence.endswith('.'):
                            sentences.append(sentence)
                    
                    current_sentence = char
                    in_sentence = True
                    i += 1
                    
                    # Chercher la fin de la phrase
                    while i < len(line):
                        current_sentence += line[i]
                        
                        if line[i] == '.':
                            # Vérifier si c'est vraiment la fin de la phrase
                            if i + 1 < len(line):
                                next_char = line[i + 1]
                                # Si le caractère suivant est une majuscule, c'est probablement la fin
                                if next_char.isupper() or next_char in 'ÉÈÀÂÎÔÙÛÇ':
                                    # Mais vérifier que ce n'est pas une abréviation
                                    if not self._is_abbreviation(current_sentence):
                                        break
                            else:
                                # Point à la fin de la ligne
                                break
                        i += 1
                    
                    # Si on a trouvé une fin de phrase
                    if i < len(line):
                        sentence = current_sentence.strip()
                        if sentence:
                            sentences.append(sentence)
                        current_sentence = ""
                        in_sentence = False
                    else:
                        # La phrase continue sur la ligne suivante
                        current_sentence += " "
                        break
                
                # Cas 2: Guillemets français (début de citation)
                elif char == '«' and (i == 0 or line[i-1] in ' .'):
                    # Commencer une nouvelle phrase avec guillemets
                    if in_sentence and current_sentence.strip():
                        # Sauvegarder la phrase précédente
                        sentence = current_sentence.strip()
                        if sentence and sentence.endswith('.'):
                            sentences.append(sentence)
                    
                    current_sentence = char
                    in_sentence = True
                    i += 1
                    
                    # Chercher la fin de la phrase (guillemets fermants + point)
                    while i < len(line):
                        current_sentence += line[i]
                        
                        if line[i] == '»':
                            # Chercher le point après les guillemets
                            j = i + 1
                            while j < len(line) and line[j] == ' ':
                                j += 1
                            if j < len(line) and line[j] == '.':
                                current_sentence += line[i+1:j+1]
                                i = j
                                break
                        i += 1
                    
                    # Si on a trouvé une fin de phrase
                    if i < len(line):
                        sentence = current_sentence.strip()
                        if sentence:
                            sentences.append(sentence)
                        current_sentence = ""
                        in_sentence = False
                    else:
                        # La phrase continue sur la ligne suivante
                        current_sentence += " "
                        break
                
                else:
                    # Continuer la phrase en cours
                    if in_sentence:
                        current_sentence += char
                    i += 1
        
        # Ajouter la dernière phrase si elle existe
        if in_sentence and current_sentence.strip():
            sentence = current_sentence.strip()
            if sentence and sentence.endswith('.'):
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
