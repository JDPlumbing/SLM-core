import re
import difflib

def normalize_tokens(raw_text, valid_words, cutoff=0.85):
    tokens = re.findall(r"\b[a-zA-Z0-9\-]+\b", raw_text.lower())
    cleaned = []

    for token in tokens:
        if token in valid_words:
            cleaned.append(token)
        else:
            # Try fuzzy match
            matches = difflib.get_close_matches(token, valid_words, n=1, cutoff=cutoff)
            if matches:
                cleaned.append(matches[0])
            else:
                cleaned.append(token)  # fallback: pass through
    return cleaned
