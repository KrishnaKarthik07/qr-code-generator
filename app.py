from flask import Flask, render_template, request
import qrcode
import io
import base64
from PIL import Image

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_image = None
    if request.method == 'POST':
        data = request.form['data']
        if data:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H, # H = High, needed for logo
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
            
            # Add Logo
            try:
                logo = Image.open('logo.png')
                # Resize logo to 20% of QR size
                qr_width, qr_height = img.size
                logo_size = qr_width // 5
                logo = logo.resize((logo_size, logo_size))
                
                # Put logo in center
                pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
                img.paste(logo, pos)
            except:
                pass # If no logo.png found, just skip

            buf = io.BytesIO()
            img.save(buf, format='PNG')
            qr_image = base64.b64encode(buf.getvalue()).decode('utf-8')

    return render_template('index.html', qr_image=qr_image)

if __name__ == '__main__':
    app.run(debug=True)
