"""Субагент: построение графиков для отчета."""

import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def build_traffic_sources_chart(traffic_sources):
    names = [s["name"] for s in traffic_sources]
    visits = [s["visits"] for s in traffic_sources]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(names, visits, color="#4a90d9")
    ax.set_title("Источники трафика (визиты за неделю)")
    ax.set_ylabel("Визиты")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf
