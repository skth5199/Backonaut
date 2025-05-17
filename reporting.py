

import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
import datetime

def generate_pdf_report(history: pd.DataFrame, output_path="backtest_report.pdf"):
    # Compute metrics
    returns = history['nav'].pct_change().dropna()
    total_return = (history['nav'].iloc[-1] / history['nav'].iloc[0]) - 1
    cagr = (1 + total_return) ** (252 / len(history)) - 1
    volatility = returns.std() * (252 ** 0.5)
    sharpe = returns.mean() / returns.std() * (252 ** 0.5)
    max_drawdown = (history['nav'] / history['nav'].cummax() - 1).min()

    # Plot NAV
    fig, ax = plt.subplots()
    history['nav'].plot(ax=ax, title="Net Asset Value Over Time")
    ax.set_ylabel("NAV")
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    nav_plot = ImageReader(buf)
    plt.close(fig)

    # Start PDF generation
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "Backtest Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 70, f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Metrics
    y = height - 110
    metrics = [
        ("Total Return", f"{total_return:.2%}"),
        ("CAGR", f"{cagr:.2%}"),
        ("Volatility", f"{volatility:.2%}"),
        ("Sharpe Ratio", f"{sharpe:.2f}"),
        ("Max Drawdown", f"{max_drawdown:.2%}")
    ]
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Performance Metrics")
    c.setFont("Helvetica", 12)
    for label, value in metrics:
        y -= 20
        c.drawString(70, y, f"{label}: {value}")

    # NAV Chart
    y -= 40
    c.drawImage(nav_plot, 50, y - 200, width=500, height=200)

    c.showPage()
    c.save()
    print(f"Report saved to {output_path}")