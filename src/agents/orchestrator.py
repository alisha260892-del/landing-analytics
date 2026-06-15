"""Главный агент: координирует субагентов."""

from agents import metrika_agent, analyzer_agent, report_agent, chart_agent


def run_weekly_report(landing_path=None, date1="7daysAgo", date2="yesterday"):
    data = metrika_agent.get_metrika_data(landing_path, date1, date2)
    traffic_sources = metrika_agent.get_traffic_sources(landing_path, date1, date2)
    utm_sources = metrika_agent.get_utm_sources(landing_path, date1, date2)
    analysis = analyzer_agent.analyze(data)
    analysis["traffic_sources"] = traffic_sources
    analysis["utm_sources"] = utm_sources
    report = report_agent.build_report(analysis, landing_path, date1, date2)
    chart = chart_agent.build_traffic_sources_chart(traffic_sources)
    return report, chart
