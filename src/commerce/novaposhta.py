from __future__ import annotations

import logging
from typing import Any

import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

API_URL = "https://api.novaposhta.ua/v2.0/json/"
PAGE_SIZE = 500
REQUEST_TIMEOUT = 12


def _api_key() -> str:
    return (getattr(settings, "NOVA_POSHTA_API_KEY", "") or "").strip()


def configured() -> bool:
    return bool(_api_key())


def _post(model: str, method: str, props: dict[str, Any]) -> list[dict[str, Any]]:
    key = _api_key()
    if not key:
        return []
    try:
        response = requests.post(
            API_URL,
            json={
                "apiKey": key,
                "modelName": model,
                "calledMethod": method,
                "methodProperties": props,
            },
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, ValueError) as exc:
        logger.warning("novaposhta %s/%s failed: %s", model, method, exc)
        return []
    if not payload.get("success"):
        logger.warning("novaposhta %s/%s errors: %s", model, method, payload.get("errors"))
        return []
    data = payload.get("data") or []
    return data if isinstance(data, list) else []


def search_cities(query: str, *, limit: int = 8) -> list[dict[str, str]]:
    q = (query or "").strip()
    if len(q) < 2:
        return []
    cache_key = f"np:cities:{q.casefold()}:{limit}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    rows = _post(
        "Address",
        "searchSettlements",
        {"CityName": q, "Limit": str(limit)},
    )
    items: list[dict[str, str]] = []
    for row in rows:
        addresses = row.get("Addresses") if isinstance(row, dict) else None
        if not isinstance(addresses, list):
            continue
        for item in addresses:
            if not isinstance(item, dict):
                continue
            ref = (item.get("DeliveryCity") or item.get("Ref") or "").strip()
            present = (item.get("Present") or item.get("MainDescription") or "").strip()
            if not ref or not present:
                continue
            items.append({"ref": ref, "name": present})
            if len(items) >= limit:
                break
        if len(items) >= limit:
            break

    cache.set(cache_key, items, 60 * 60)
    return items


def _warehouse_kind(row: dict[str, Any]) -> str:
    category = (row.get("CategoryOfWarehouse") or "").strip().casefold()
    if "postomat" in category or "поштомат" in category:
        return "locker"
    return "branch"


def warehouses_for_city(city_ref: str, *, kind: str = "branch") -> list[dict[str, str]]:
    ref = (city_ref or "").strip()
    want = "locker" if kind == "locker" else "branch"
    if not ref:
        return []
    cache_key = f"np:wh:{ref}:{want}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    items: list[dict[str, str]] = []
    page = 1
    while page <= 20:
        rows = _post(
            "Address",
            "getWarehouses",
            {
                "CityRef": ref,
                "Page": str(page),
                "Limit": str(PAGE_SIZE),
            },
        )
        if not rows:
            break
        for row in rows:
            if not isinstance(row, dict):
                continue
            if _warehouse_kind(row) != want:
                continue
            description = (row.get("Description") or row.get("DescriptionRu") or "").strip()
            number = (row.get("Number") or "").strip()
            if not description:
                continue
            label = description if not number or number in description else f"№{number}: {description}"
            items.append(
                {
                    "ref": (row.get("Ref") or "").strip(),
                    "label": label,
                    "number": number,
                }
            )
        if len(rows) < PAGE_SIZE:
            break
        page += 1

    cache.set(cache_key, items, 60 * 60)
    return items


def find_warehouses(query: str, *, kind: str = "branch") -> dict[str, Any]:
    """Resolve city by first letters and return all matching warehouses."""
    cities = search_cities(query, limit=5)
    if not cities:
        return {"city": "", "city_ref": "", "items": []}
    city = cities[0]
    items = warehouses_for_city(city["ref"], kind=kind)
    return {"city": city["name"], "city_ref": city["ref"], "items": items, "cities": cities}
