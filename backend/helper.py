import re

def extract_yt_term(query):
    """Extract search term from a YouTube query."""
    # Check for "play X on YouTube" pattern
    match = re.search(r'play\s+(.*?)\s+on\s+youtube', query.lower())
    if match:
        return match.group(1)
    
    # Check for "play X" pattern
    match = re.search(r'play\s+(.*)', query.lower())
    if match:
        return match.group(1)
    
    return None

def remove_words(text, words_to_remove):
    """Remove specific words from a text string."""
    result = text.lower()
    for word in words_to_remove:
        result = result.replace(word.lower(), "")
    
    # Clean up extra spaces
    result = re.sub(r'\s+', ' ', result).strip()
    return result

def extract_entity(query):
    """
    Extract potential named entities from a query.
    Returns a list of potential entities.
    """
    # List of common Indian celebrities
    celebrities = [
        "salman khan", "shahrukh khan", "shah rukh khan", "amitabh bachchan",
        "arijit singh", "atif aslam", "deepika padukone", "priyanka chopra",
        "aamir khan", "hrithik roshan", "akshay kumar", "ranveer singh",
        "ranbir kapoor", "alia bhatt", "katrina kaif", "kareena kapoor", 'Sami Ullah'
    ]
    
    # Check for exact matches
    query_lower = query.lower()
    for celeb in celebrities:
        if celeb in query_lower:
            return celeb
    
    # Check for partial matches (first name only)
    words = query_lower.split()
    for word in words:
        for celeb in celebrities:
            if celeb.startswith(word) and len(word) > 2:  # Avoid short words
                return celeb
    
    return None

