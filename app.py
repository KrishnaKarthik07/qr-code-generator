from flask import Flask, render_template, request
import qrcode
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    qr_image = None

    if request.method == "POST":
        data = request.form["data"]

        qr = qrcode.make(data)

        os.makedirs("static", exist_ok=True)
        qr.save("static/qrcode.png")

        qr_image = "/static/qrcode.png"

    return render_template("index.html", qr_image=qr_image)


if __name__ == "__main__":
    app.run(debug=True)