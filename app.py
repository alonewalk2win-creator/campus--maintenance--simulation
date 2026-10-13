from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/simulation")
def simulation():
    return render_template("simulation.html")

@app.route("/health")
def health():
    return jsonify({"status": "ok", "application": "Campus Maintenance Simulation"})

if __name__ == "__main__":
    app.run(debug=True)
