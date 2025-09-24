from flask import Flask, render_template, request
from monitoring.collector import VMCollector
from monitoring.analyzer import VMAnalyzer
from monitoring.recommender import VMRecommender

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def dashboard():
    csp = request.form.get("csp", "AWS")
    subscription = request.form.get("subscription", "")

    metrics = VMCollector(csp, subscription).collect()
    analysis = VMAnalyzer(metrics).analyze()
    recommendations = VMRecommender(analysis).generate()

    return render_template("dashboard.html",
                           csp=csp,
                           subscription=subscription,
                           analysis=analysis,
                           recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)
