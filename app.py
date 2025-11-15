from flask import Flask, render_template, request, send_file, jsonify
import qrcode
from io import BytesIO

app = Flask(__name__)

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

    # 将二维码图片保存到内存
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    # 使用 Flask 的 url_for 动态生成图片的 URL
    qr_code_url = '/static/qr_codes/' + 'temp.png'

    # 返回二维码图片的 URL 作为 JSON
    return jsonify({'qr_code_url': qr_code_url})

if __name__ == '__main__':
    app.run(debug=True)
