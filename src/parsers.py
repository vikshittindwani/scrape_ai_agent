# src/parsers.py

from .llm import parse_user_query

def route(parsed: dict):
    """
    Return list of site‑specific job descriptors for downstream scraping.
    Supports 'product' and 'flight' query types.
    """
    query_type = parsed.get("type")
    sites = parsed.get("sites") or []

    if query_type == "product":
        # If no sites explicitly mentioned, default to Amazon + Flipkart
        return [{"site": site, **parsed} for site in (sites or ["amazon", "flipkart"])]

    elif query_type == "flight":
        # Only one meta-handler exists for flights
        return [{"site": "flights", **parsed}]
    
    else:
        raise ValueError(f"Unsupported query type: {query_type}")
