"""Субагент: получение данных из Яндекс Метрики (Stat API)."""

import requests
from config import YANDEX_METRIKA_TOKEN, YANDEX_METRIKA_COUNTER_ID

API_URL = "https://api-metrika.yandex.net/stat/v1/data"

METRICS = "ym:s:visits,ym:s:pageviews,ym:s:users,ym:s:bounceRate,ym:s:avgVisitDurationSeconds"


def get_metrika_data(landing_path=None, date1="7daysAgo", date2="yesterday"):
    headers = {"Authorization": f"OAuth {YANDEX_METRIKA_TOKEN}"}
    params = {
        "ids": YANDEX_METRIKA_COUNTER_ID,
        "metrics": METRICS,
        "date1": date1,
        "date2": date2,
    }

    if landing_path:
        params["filters"] = f"ym:s:startURL=~'{landing_path}'"

    response = requests.get(API_URL, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    totals = data["totals"]
    return {
        "visits": totals[0],
        "pageviews": totals[1],
        "users": totals[2],
        "bounce_rate": totals[3],
        "avg_visit_duration": totals[4],
    }


def _get_dimension_breakdown(dimension, landing_path=None, date1="7daysAgo", date2="yesterday"):
    headers = {"Authorization": f"OAuth {YANDEX_METRIKA_TOKEN}"}
    params = {
        "ids": YANDEX_METRIKA_COUNTER_ID,
        "metrics": "ym:s:visits",
        "dimensions": dimension,
        "date1": date1,
        "date2": date2,
        "sort": "-ym:s:visits",
    }

    if landing_path:
        params["filters"] = f"ym:s:startURL=~'{landing_path}'"

    response = requests.get(API_URL, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    items = []
    for row in data["data"]:
        name = row["dimensions"][0]["name"]
        visits = row["metrics"][0]
        items.append({"name": name, "visits": visits})

    return items


def get_traffic_sources(landing_path=None, date1="7daysAgo", date2="yesterday"):
    return _get_dimension_breakdown("ym:s:lastTrafficSource", landing_path, date1, date2)


def get_utm_sources(landing_path=None, date1="7daysAgo", date2="yesterday"):
    return _get_dimension_breakdown("ym:s:UTMSource", landing_path, date1, date2)
