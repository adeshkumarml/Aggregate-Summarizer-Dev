import re

def clean_markdown(text: str) -> str:

    # Bold and italics marker
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text) 
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"_(.*?)_", r"\1", text)

    # Heading marker
    text = re.sub(r"^#{1,6}\s*(.+)$", r"\n\1\n", text, flags = re.MULTILINE)
    
    # Bullets marker
    text = re.sub(r"^\s*[-*+]\s*", "\n• ", text, flags = re.MULTILINE)
    
    # Numbered lists
    text = re.sub(r"^\s*(\d+)\.\s*", r"\1. ", text, flags = re.MULTILINE)
    
    # Horizontal rules marker
    text = re.sub(r"^-{3,}$", "", text, flags = re.MULTILINE)
    
    # Newline markers
    text = text.replace("\\n", "\n")
    
    # Excessive blank lines clear
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()