from flask import Flask, render_template, Response
# import pandas as pd
import io
import random
from detector.analysis import Analysis

app = Flask(__name__)

# initiate analysis from traders_data.csv
analysis = Analysis("traders_data.csv", ["AMZN"])


@app.route("/")
def index():
    html_body = generate_html_body()
    return render_template('index.html', records=u''.join(html_body))


def generate_html_body():

    html_body = []
    # header
    html_body.append(
        "<h1>Market Abuse Detection</h1>")
    start_date = analysis.start_date
    end_date = analysis.end_date
    html_body.append(
        "<h4><em>{} - {}</em></h4>".format(start_date, end_date))
    # title for table suspicious traders
    html_body.append("<br><h3>Suspicious Traders Ranking</h1>")
    # table suspicious traders
    suspicious_traders = analysis.count_suspicious_per_trader()
    html_body.append(suspicious_traders.to_html())
    # title for table suspicious trades by country
    html_body.append("<br><h3>Suspicious Trades By Country</h1>")
    # table suspicious trades by country
    country_monthly = analysis.count_suspicious_by_country_per_month()
    html_body.append(country_monthly.to_html())

    return html_body
