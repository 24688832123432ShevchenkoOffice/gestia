from src.content.legal_copy import get_legal
from src.content.models_legal import LegalPage
from src.core.utils import localized


def legal_document(slug: str) -> dict | None:
    fallback = get_legal(slug)
    if fallback is None:
        return None
    doc = {
        "slug": fallback["slug"],
        "title": fallback["title"],
        "seo_title": fallback["seo_title"],
        "seo_description": fallback["seo_description"],
        "updated": fallback["updated"],
        "sections": fallback["sections"],
        "html": "",
    }
    page = LegalPage.objects.filter(key=slug).first()
    if page is None:
        return doc
    title = (page.title or "").strip()
    if title:
        doc["title"] = title
    seo_title = localized(page, "seo_title").strip()
    if seo_title:
        doc["seo_title"] = seo_title
    seo_description = localized(page, "seo_description").strip()
    if seo_description:
        doc["seo_description"] = seo_description
    if page.updated_on:
        doc["updated"] = page.updated_on.strftime("%d.%m.%Y")
    body = (page.body or "").strip()
    if body:
        doc["html"] = body
    return doc
