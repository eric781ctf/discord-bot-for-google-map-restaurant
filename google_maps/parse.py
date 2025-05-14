def check_keywords(reviews: list, keywords: list):
    matched_reviews = []
    for review in reviews:
        for word in keywords:
            if word in review:
                matched_reviews.append(review)
                break
    return matched_reviews
