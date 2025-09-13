import re
from pathlib import Path
from typing import List

class SentenceExtractor:
    """
    Extract sentences from a text file according to rules:
    - Start: capital letter (at beginning of line or after a period)
    - End: period followed by a capital letter or line break
    """
    def __init__(self, txt_file: Path):
        self.txt_file = Path(txt_file)

    def extract_sentences(self, start_phrase: str = None) -> List[str]:
        sentences = []
        
        with open(self.txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Clean content
        content = content.replace('\r\n', '\n').replace('\r', '\n')
        
        # Normalize multiple spaces and tabs
        content = re.sub(r'[ \t]+', ' ', content)
        
        # If a starting phrase is specified, filter content
        if start_phrase:
            content = self._filter_content_from_start_phrase(content, start_phrase)
        
        # Split into paragraphs (separated by empty lines)
        paragraphs = re.split(r'\n\s*\n', content)
        
        for paragraph in paragraphs:
            if paragraph.strip():
                # Clean notes and references from paragraph
                cleaned_paragraph = self._clean_notes_and_references(paragraph.strip())
                if cleaned_paragraph:
                    paragraph_sentences = self._extract_sentences_from_paragraph(cleaned_paragraph)
                    sentences.extend(paragraph_sentences)
        
        return sentences
    
    def _extract_sentences_from_paragraph(self, paragraph: str) -> List[str]:
        """
        Extract sentences from a paragraph
        """
        sentences = []
        
        # Replace line breaks with spaces
        paragraph = re.sub(r'\n+', ' ', paragraph)
        
        # Pattern to detect sentences
        # A sentence ends with a period followed by a space and a capital letter
        # or by a period at the end of the paragraph
        pattern = r'[^.]*\.(?=\s+[A-ZÉÈÀÂÎÔÙÛÇ]|$)'
        
        matches = re.finditer(pattern, paragraph, re.MULTILINE)
        
        for match in matches:
            sentence = match.group().strip()
            
            # Clean notes and references from sentence
            sentence = self._clean_notes_and_references(sentence)
            
            # Clean multiple spaces
            sentence = re.sub(r'\s+', ' ', sentence)
            
            # Check that it's not an abbreviation and the sentence is not empty
            if sentence and not self._is_abbreviation(sentence) and len(sentence) > 10:
                sentences.append(sentence)
        
        return sentences
    
    def _is_abbreviation(self, text: str) -> bool:
        """
        Check if the period is part of an abbreviation
        """
        # List of common abbreviations
        abbreviations = [
            'M.', 'Mme.', 'Mlle.', 'Dr.', 'Pr.', 'Prof.', 'St.', 'Ste.',
            'etc.', 'cf.', 'vs.', 'i.e.', 'e.g.', 'p.', 'pp.', 'vol.',
            'n°', 'N°', 'n°s', 'N°s', 't.', 'T.', 's.', 'S.'
        ]
        
        # Check if text ends with an abbreviation
        for abbr in abbreviations:
            if text.strip().endswith(abbr):
                return True
        
        # Check abbreviations with spaces
        words = text.split()
        if len(words) >= 2:
            last_word = words[-1]
            for abbr in abbreviations:
                if last_word == abbr:
                    return True
        
        return False
    
    def _filter_content_from_start_phrase(self, content: str, start_phrase: str) -> str:
        """
        Filter content to start from a specific phrase
        Args:
            content: Complete file content
            start_phrase: Starting phrase (can be partial)
        Returns:
            Content filtered from the starting phrase
        """
        # Normalize the starting phrase
        start_phrase = start_phrase.strip()
        
        # Split content into lines to search for the starting phrase
        lines = content.split('\n')
        
        # Search for the line containing the starting phrase
        start_line_index = -1
        for i, line in enumerate(lines):
            if start_phrase.lower() in line.lower():
                start_line_index = i
                break
        
        if start_line_index == -1:
            print(f"⚠️ Starting phrase '{start_phrase}' not found. Using complete content.")
            return content
        
        # Find the exact start of the phrase in the line
        line = lines[start_line_index]
        phrase_start_pos = line.lower().find(start_phrase.lower())
        
        if phrase_start_pos == -1:
            # If phrase not found in line, start from next line
            start_line_index += 1
            phrase_start_pos = 0
        
        # Reconstruct content from the starting phrase
        if start_line_index < len(lines):
            # Take the part of the starting line from the phrase
            filtered_lines = [lines[start_line_index][phrase_start_pos:]]
            # Add all following lines
            filtered_lines.extend(lines[start_line_index + 1:])
            return '\n'.join(filtered_lines)
        
        return content
    
    def _clean_notes_and_references(self, text: str) -> str:
        """
        Clean notes and references from text
        Args:
            text: Text to clean
        Returns:
            Cleaned text without notes and references
        """
        # Remove references in brackets [X]
        text = re.sub(r'\[[^\]]*\]', '', text)
        
        # Remove notes in parentheses (X)
        text = re.sub(r'\([^)]*\)', '', text)
        
        # Remove paragraph/section numbers at the beginning of sentences (e.g., "62 It will be time...")
        text = re.sub(r'^\d+\s+', '', text)
        
        # Remove isolated paragraph/section numbers in text (e.g., "...things 65 and that...")
        text = re.sub(r'\s+\d+\s+', ' ', text)
        
        # Remove arrows and reference symbols (e.g., "↑ Like truth...")
        text = re.sub(r'[↑↓→←]', '', text)
        
        # Remove words and phrases entirely in uppercase with more than 4 characters
        # This includes titles, headers, etc. like "RELATIVES TO THE TREATISE ON THE REFORM OF THE UNDERSTANDING"
        text = re.sub(r'\b[A-ZÉÈÀÂÎÔÙÛÇ]{5,}\b', '', text)
        
        # Clean multiple spaces that may result from cleaning
        text = re.sub(r'\s+', ' ', text)
        
        # Clean spaces at the beginning and end
        text = text.strip()
        
        return text
