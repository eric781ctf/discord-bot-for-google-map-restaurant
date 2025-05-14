def check_keywords(comment: str, keywords: list):
    matched_keywords = []
    for word in keywords:
        if word in comment:
            matched_keywords.append(word)
            break
    return matched_keywords
