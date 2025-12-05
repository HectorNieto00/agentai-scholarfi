# services/discounts_service.py
import logging
import streamlit as st
from utils.scraper import get_products_by_categories, get_best_store_info
from utils.openai import analyze_products_with_llm
import random

logging.basicConfig(level=logging.INFO)

@st.cache_data(ttl=3600)
def get_top_discounts_simple(products: list, num_to_select: int = 5) -> list:
    if not products:
        return []

    selected = random.sample(products, min(num_to_select, len(products)))

    ai_templates = [
        "According to your recent spending patterns, you might benefit from reducing your expenses in the {category} category. I found an offer at {store}: the product '{title}' is available for £{price}. You can check it here: {link}.",
        "Based on how you've been spending lately, you seem to be investing quite a bit in {category}. A good deal I found for you is at {store}: '{title}' for only £{price}. Here is the direct link: {link}.",
        "Your recent purchases suggest you frequently buy items related to {category}. To help you save, I located an offer at {store}: '{title}' priced at £{price}. You can access it here: {link}.",
    ]

    messages = []
    for i, p in enumerate(selected):
        template = ai_templates[i % len(ai_templates)]
        msg = template.format(
            category=p.get("category", "this category"),
            store=p.get("store", "Unknown Store"),
            title=p.get("title", "Unknown Product"),
            price=p.get("best_price", "?"),
            link=p.get("store_link", "#")
        )
        messages.append({"text": msg})
    return messages[:num_to_select]

@st.cache_data(ttl=3600)
def get_top_discounts(queries: list[str], user_context: dict = None) -> list:
    """
    Scrapea categorías → obtiene mejores precios → manda a IA → fallback si falla.
    """
    # 1) Scraping de productos
    scraped = get_products_by_categories(queries)

    if not scraped:
        logging.warning("No products scraped.")
        return []

    # 2) Agregar info de tienda y precio
    detailed = get_best_store_info(scraped)

    # Filtrar solo productos válidos
    detailed_products = [
        p for p in detailed if p.get("store") and p.get("best_price")
    ]

    if not detailed_products:
        return get_top_discounts_simple([], 5)

    # 3) Payload para IA
    payload = {
        "user_summary": user_context or {},
        "products": detailed_products
    }

    try:
        result = analyze_products_with_llm(payload)

        if result and isinstance(result, dict) and result.get("selected"):
            formatted = []

            for item in result["selected"][:5]:
                offer = (
                    f"<a href='{item.get('store_link', '#')}' target='_blank' "
                    f"style='color: inherit; text-decoration: none;'>"
                    f"{item.get('title')} — £{item.get('best_price')} "
                    f"({item.get('justification', '')})"
                    "</a>"
                )

                formatted.append({
                    "store": item.get("store", "Unknown"),
                    "offer": offer
                })

            # Rellenar si hay menos de 3
            while len(formatted) < 3:
                extra = get_top_discounts_simple(detailed_products, 1)
                if not extra:
                    break
                formatted.extend(extra)

            return formatted[:3]

        # IA falló → fallback
        return get_top_discounts_simple(detailed_products, 3)

    except Exception as e:
        logging.error(f"IA error: {str(e)}")
        return get_top_discounts_simple(detailed_products, 3)
