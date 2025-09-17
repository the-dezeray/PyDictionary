import re
from rich.text import Text
def truncate_definition( text, word_limit):
        """Truncate definition text to specified word limit while preserving Rich markup structure"""
        # Convert Text object to string if needed
        text_str = str(text) if hasattr(text, 'plain') else text
        
        # Remove Rich markup for word counting
        clean_text = re.sub(r'\[/?[a-zA-Z0-9\s]*\]', '', text_str)
        words = clean_text.split()
        
        if len(words) <= word_limit:
            return text, False  # No truncation needed
        
        # Find the position to truncate in the original text
        truncated_words = words[:word_limit]
        truncated_clean = ' '.join(truncated_words)
        
        # Simple approach: find approximate position in original text
        # This is a basic implementation that may need refinement for complex markup
        words_so_far = 0
        result = ""
        i = 0
        
        while i < len(text_str) and words_so_far < word_limit:
            char = text_str[i]
            result += char
            
            # Check if we've completed a word (not inside markup)
            if char == ' ' and not _inside_markup(text_str, i):
                words_so_far += 1
            
            i += 1
        
        return result + "...", True  # Return truncated text and truncation flag

def _inside_markup( text, position):
    """Helper method to check if position is inside Rich markup tags"""
    # Look backwards for the last [ or ]
    last_bracket = -1
    for i in range(position - 1, -1, -1):
        if text[i] in ['[', ']']:
            last_bracket = i
            ##
            break
    
    if last_bracket == -1:
        return False
    
    return text[last_bracket] == '['


def format_definition(definition):
    """Format definition text with styling"""
    if not definition:
        return ""
    
    processed_def = definition
    
    # Style scientific names (e.g., "(Salvelinus malma)")
    processed_def = re.sub(
        r'(\([A-Z][a-z]+ [a-z]+\))',
        r'[italic]\1[/italic]',
        processed_def
    )

    # Style usage tags (e.g., "[Obs.]")
    processed_def = re.sub(
        r'(\[[A-Za-z\.\s,]+\])',
        r'[dim italic]\1[/dim italic]',
        processed_def
    )
    
    # Style special notes (e.g., "Note: ...")
    processed_def = re.sub(
        r'Note: (.*?)(?=\s\d\.\s|$)',
        r'\n    [bold]Note[/bold]: [dim]\1[/dim]',
        processed_def,
        flags=re.DOTALL
    )

    # Style quotes and attributions (e.g., "Sentence. Author.")
    processed_def = re.sub(
        r'([A-Z][^."]*?\.)\s+([A-Z][a-z]+\.)',
        r'\n    [italic]" \1"[/italic]\n    — \2',
        processed_def
    )

    # Style alternative names (e.g., "-- called also ...")
    processed_def = re.sub(
        r'--\s*called also\s*(.*)',
        lambda m: f"\nCalled also: [bold]{m.group(1).strip('.')}[/bold]",
        processed_def
    )
    
    # Split definitions into numbered parts
    parts = re.split(r'\s(?=\d\.\s)', processed_def)
    
    # If there are numbered parts, format them
    if len(parts) > 1 or definition.strip().startswith('1.'):
        formatted_text = Text()
        for i, part in enumerate(parts):
            part = part.strip()
            # Find the number and the text
            match = re.match(r'(\d\.)\s*(.*)', part, re.DOTALL)
            if match:
                num, text = match.groups()
                formatted_text.append(f"\n[bold cyan]{num}[/bold cyan] ")
                formatted_text.append(text.strip())
            else: # Handles the text before the first '1.' if any
                formatted_text.append(part.strip())
        return formatted_text
    else:
        # Handle definitions without numbers
        return processed_def.strip()