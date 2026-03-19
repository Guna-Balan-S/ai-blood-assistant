from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import re

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Data
donors = [
    "Arun, O+, Karur",
    "Siva, O+, Karur",
    "Ravi, A+, Trichy",
    "Kumar, B+, Chennai"
]

# Embeddings
embeddings = model.encode(donors)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))


def extract_entities(query):
    query_lower = query.lower()

    # 🔥 Detect blood group using regex
    blood_match = re.search(r'(a|b|ab|o)[+-]', query_lower)
    blood = blood_match.group() if blood_match else None

    # 🔥 Remove common words
    ignore_words = ["need", "blood", "group", "i", "want", "require", "looking", "for", "urgent"]

    words = query_lower.split()

    location = None
    for w in words:
        if w not in ignore_words and not re.match(r'(a|b|ab|o)[+-]', w):
            location = w

    return blood, location


def search_donors(query):
    query_embedding = model.encode([query])

    # 🔥 Get more candidates
    _, indices = index.search(np.array(query_embedding), 4)

    results = [donors[i] for i in indices[0]]

    # 🔥 Extract smart info
    blood, location = extract_entities(query)

    filtered = []

    for donor in results:
        donor_lower = donor.lower()

        if blood and location:
            if blood in donor_lower and location in donor_lower:
                filtered.append(donor)

        elif blood:
            if blood in donor_lower:
                filtered.append(donor)

        elif location:
            if location in donor_lower:
                filtered.append(donor)

    return filtered if filtered else results