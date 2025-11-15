from flask import Flask, render_template, request, send_file, jsonify
import qrcode
import os
from io import BytesIO
from werkzeug.utils import secure_filename
from flask import url_for

app = Flask(__name__)

# 设置二维码存储的目录
QR_CODE_FOLDER = 'static/qr_codes'
if not os.path.exists(QR_CODE_FOLDER):
    os.makedirs(QR_CODE_FOLDER)

# 主页路由，展示网页表单
@app.route('/')
def index():
    return render_template('index.html')

# 生成二维码的路由
@app.route('/generate', methods=['POST'])
def generate():
    data = request.form.get('data')  # 获取用户输入的数据

    if not data:
        return jsonify({'error': '请输入二维码数据！'}), 400

    # 生成二维码
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    # 创建二维码图片
    img = qr.make_image(fill='black', back_color='white')

    # 使用用户输入数据的前 10 个字符作为文件名，避免文件名太长
    filename = secure_filename(f"{data[:10]}.png")
    file_path = os.path.join(QR_CODE_FOLDER, filename)

    # 保存二维码图片到文件系统
    img.save(file_path)

    # 使用 Flask 的 url_for 动态生成图片的 URL
    qr_code_url = url_for('static', filename=f'qr_codes/{filename}')

    # 返回二维码图片的 URL 作为 JSON
    return jsonify({'qr_code_url': qr_code_url})

if __name__ == '__main__':
    app.run(debug=True)
