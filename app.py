from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        url = request.form.get("url")

        try:
            r = requests.get(url, timeout=5)
            soup = BeautifulSoup(r.text, "html.parser")

            text = soup.get_text().lower()
            score = 0

            if "limited" in text:
                score += 20
            if "only" in text:
                score += 20
            if "hurry" in text:
                score += 20

            result = f"Manipulation Score: {score}/100"

        except:
            result = "Error fetching URL"

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
