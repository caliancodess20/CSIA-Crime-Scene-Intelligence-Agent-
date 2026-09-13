"""
backend/app/nlp_engine/entity_extraction.py
--------------------------------------------
CSIA — NLP Engine + Relationship Graph track (Anmol Panjwani)

Core logic (no web framework code here — routes.py wires this into the API):
  1. Entity extraction (spaCy)       -> names, locations, orgs
  2. Statement summarization (Sentence Transformers, extractive)
  3. Relationship graph construction -> witness -> shop -> suspect style links

Output is a single structured dict, meant to be written into an
evidence item's `extra_metadata` field per the case-management schema
(see backend/app/case_management/API_REFERENCE.md).

Install:
    pip install spacy sentence-transformers numpy
    python -m spacy download en_core_web_sm
"""

from itertools import combinations

import numpy as np
import spacy
from sentence_transformers import SentenceTransformer

# ---------------------------------------------------------------------------
# 1. Setup — load models once at import time (they're slow to load per-call)
# ---------------------------------------------------------------------------
nlp = spacy.load("en_core_web_sm")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Entity types we care about for a crime-scene statement.
# PERSON = witnesses/suspects, GPE/LOC = locations, ORG/FAC = shops/buildings
ENTITY_LABELS_OF_INTEREST = {"PERSON", "GPE", "LOC", "ORG", "FAC", "NORP"}


# ---------------------------------------------------------------------------
# 2. Entity extraction
# ---------------------------------------------------------------------------
def extract_entities(text: str) -> list[dict]:
    """Pull names, locations, and orgs out of a witness statement."""
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        if ent.label_ in ENTITY_LABELS_OF_INTEREST:
            entities.append(
                {
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char,
                }
            )
    return entities


# ---------------------------------------------------------------------------
# 3. Statement summarization (extractive, via sentence embeddings)
# ---------------------------------------------------------------------------
def summarize_statement(text: str, top_n: int = 3) -> list[str]:
    """
    Rank sentences by how close they are to the 'average meaning' of the
    whole statement (centroid similarity), then return the top N in their
    original order. Lightweight TextRank-style approach — only needs
    Sentence Transformers, no separate summarization model.
    """
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]

    if len(sentences) <= top_n:
        return sentences

    embeddings = embedder.encode(sentences)
    doc_embedding = np.mean(embeddings, axis=0)

    norms = np.linalg.norm(embeddings, axis=1) * np.linalg.norm(doc_embedding)
    scores = (embeddings @ doc_embedding) / (norms + 1e-8)

    top_idx = np.argsort(scores)[::-1][:top_n]
    top_idx = sorted(top_idx)  # restore original sentence order
    return [sentences[i] for i in top_idx]


# ---------------------------------------------------------------------------
# 4. Relationship graph (witness -> shop -> suspect style links)
# ---------------------------------------------------------------------------
def build_relationship_graph(text: str, entities: list[dict]) -> dict:
    """
    Co-occurrence graph: any two entities mentioned in the same sentence
    get an edge, tagged with that sentence as context. Rule-based/lightweight
    for v1 — enough to draw witness -> shop -> suspect chains without a
    full relation-extraction model.
    """
    doc = nlp(text)
    nodes = {}
    edges = []

    for ent in entities:
        nodes[ent["text"]] = ent["label"]

    for sent in doc.sents:
        sent_entities = [
            e["text"]
            for e in entities
            if e["start"] >= sent.start_char and e["end"] <= sent.end_char
        ]
        for e1, e2 in combinations(sorted(set(sent_entities)), 2):
            edges.append(
                {"source": e1, "target": e2, "context": sent.text.strip()}
            )

    return {
        "nodes": [{"id": name, "type": label} for name, label in nodes.items()],
        "edges": edges,
    }


# ---------------------------------------------------------------------------
# 5. Orchestrator — the function routes.py calls
# ---------------------------------------------------------------------------
def process_statement(case_id: str, statement_text: str) -> dict:
    """
    Single entry point: takes a raw witness statement, returns everything
    downstream modules need — summary, entities, and relationship graph.
    This dict is what gets written into an evidence item's `extra_metadata`.
    """
    entities = extract_entities(statement_text)
    summary = summarize_statement(statement_text)
    graph = build_relationship_graph(statement_text, entities)

    return {
        "case_id": case_id,
        "summary": summary,
        "entities": entities,
        "relationship_graph": graph,
    }
