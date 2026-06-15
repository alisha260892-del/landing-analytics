"""Субагент: анализ данных лендинга."""

BOUNCE_RATE_THRESHOLD = 50  # %
AVG_DURATION_THRESHOLD = 30  # секунд


def analyze(data):
    insights = []

    if data["bounce_rate"] > BOUNCE_RATE_THRESHOLD:
        insights.append(
            f"Высокий показатель отказов: {data['bounce_rate']:.1f}% "
            f"(норма до {BOUNCE_RATE_THRESHOLD}%)"
        )
    else:
        insights.append(f"Показатель отказов в норме: {data['bounce_rate']:.1f}%")

    if data["avg_visit_duration"] < AVG_DURATION_THRESHOLD:
        insights.append(
            f"Короткое время на сайте: {data['avg_visit_duration']:.0f} сек "
            f"(норма от {AVG_DURATION_THRESHOLD} сек)"
        )
    else:
        insights.append(f"Время на сайте в норме: {data['avg_visit_duration']:.0f} сек")

    return {
        "visits": data["visits"],
        "pageviews": data["pageviews"],
        "users": data["users"],
        "bounce_rate": data["bounce_rate"],
        "avg_visit_duration": data["avg_visit_duration"],
        "insights": insights,
    }
