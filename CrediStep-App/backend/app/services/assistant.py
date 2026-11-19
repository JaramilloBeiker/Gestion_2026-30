"""Asistente 'Step': soporte dentro de la app (Canvas: asistencia personal).

Versión inicial basada en reglas: normaliza la pregunta y busca la respuesta
de la base FAQ con más coincidencias. Se puede reemplazar por un modelo de
lenguaje más adelante sin cambiar el contrato de la API.
"""
import re
import unicodedata

from ..content import FAQ, GLOSSARY

STOPWORDS = {"que", "como", "el", "la", "los", "las", "de", "del", "un", "una", "mi", "me", "es", "y", "o", "en", "si", "por", "para", "se", "lo", "al", "tu", "a", "hay", "mis"}


def normalize(text: str) -> list[str]:
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return [w for w in re.findall(r"[a-z0-9]+", text) if w not in STOPWORDS]


def _stem(word: str) -> str:
    return word[:-1] if len(word) > 4 and word.endswith("s") else word


def answer(question: str) -> dict:
    words = {_stem(w) for w in normalize(question)}
    if not words:
        return {"answer": "¡Hola! Soy Step 👋 Pregúntame sobre historial, puntaje, cupo, tasas o qué pasa si te atrasas.", "lesson": None, "confidence": 0}

    # ¿Pregunta por un término del glosario?
    for item in GLOSSARY:
        term_words = {_stem(w) for w in normalize(item["term"].split("(")[0])}
        if term_words and term_words <= words and len(words) <= len(term_words) + 2:
            return {"answer": f"{item['term']}: {item['definition']}", "lesson": None, "confidence": 1}

    best, best_score = None, 0
    for item in FAQ:
        keys = {_stem(k) for k in item["keywords"]}
        score = len(words & keys)
        if score > best_score:
            best, best_score = item, score
    if best is None:
        return {
            "answer": "Todavía no sé responder eso 🤔. Intenta preguntarme por historial, puntaje, cupo, tasas de interés, atrasos, ahorro o presupuesto. También puedes revisar el glosario.",
            "lesson": None,
            "confidence": 0,
        }
    return {"answer": best["answer"], "lesson": best["lesson"], "confidence": min(best_score / 3, 1)}
