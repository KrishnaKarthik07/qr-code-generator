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
        logo_file = request.files.get('logo') # Get uploaded logo
        
        if data:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H, # H = High for logo
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
            
