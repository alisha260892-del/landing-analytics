"""Субагент: формирование текста отчета."""

from datetime import datetime, timedelta


def resolve_date_range(date1, date2):
    today = datetime.now().date()

    def resolve(value):
        if value == "today":
            return today
        if value == "yesterday":
            return today - timedelta(days=1)
        if value.endswith("daysAgo"):
            days = int(value[: -len("daysAgo")])
            return today - timedelta(days=days)
        return datetime.strptime(value, "%Y-%m-%d").date()

    start = resolve(date1)
    end = resolve(date2)
    return f"{start.strftime('%d.%m.%Y')} – {end.strftime('%d.%m.%Y')}"


def build_report(analysis, landing_path=None, date1="7daysAgo", date2="yesterday"):
    title = "📊 Еженедельный отчет по лендингу"
    if landing_path:
        title += f" {landing_path}"

    lines = [
        title,
        f"Период: {resolve_date_range(date1, date2)}",
        "",
        f"Визиты: {analysis['visits']:.0f}",
        f"Просмотры: {analysis['pageviews']:.0f}",
        f"Пользователи: {analysis['users']:.0f}",
        f"Отказы: {analysis['bounce_rate']:.1f}%",
        f"Среднее время на сайте: {analysis['avg_visit_duration']:.0f} сек",
        "",
        "Выводы:",
    ]

    for insight in analysis["insights"]:
        lines.append(f"- {insight}")

    traffic_sources = analysis.get("traffic_sources")
    if traffic_sources:
        total_visits = sum(s["visits"] for s in traffic_sources)
        lines.append("")
        lines.append("Источники трафика:")
        for source in traffic_sources:
            share = source["visits"] / total_visits * 100 if total_visits else 0
            lines.append(f"- {source['name']}: {source['visits']:.0f} ({share:.1f}%)")

    utm_sources = analysis.get("utm_sources", [])
    total_visits = analysis["visits"]
    if total_visits:
        rows = [s for s in utm_sources if s["name"] != "(not set)"]
        not_set_visits = total_visits - sum(s["visits"] for s in rows)
        if not_set_visits > 0:
            rows.append({"name": "(не задано)", "visits": not_set_visits})

        lines.append("")
        lines.append("UTM-источники:")
        for source in rows:
            share = source["visits"] / total_visits * 100
            lines.append(f"- {source['name']}: {source['visits']:.0f} ({share:.1f}%)")

    return "\n".join(lines)
