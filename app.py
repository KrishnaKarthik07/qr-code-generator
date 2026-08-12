from flask import Flask, render_template, request
import qrcode
import io
import base64

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    qr_image = None
    if request.method == "POST":
        data = request.form.get("data")
        if data:
            qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
            qr.add_data(data)
            qr.make(fit=True)
            image = qr.make_image(fill_color="black", back_color="white")

            # Convert to base64 instead of saving to file
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            qr_image = base64.b64encode(buf.getvalue()).decode()

    return render_template("index.html", qr_image=qr_image)

# Vercel needs this
app = app
