from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.form['input_data']
    
    cookies = []
    current_cookie = ''

    for line in data.splitlines():
        line = line.strip()
        if line.startswith('.'):
            parts = line.split('\t')
            if len(parts) == 7:
                cookie = f"{parts[5]}={parts[6]}"
                current_cookie += cookie + '; '
        elif current_cookie:
            cookies.append(current_cookie.strip('; '))
            current_cookie = ''

    result = '\n\n'.join(cookies)

    unique_lines = set()
    duplicate_count = 0

    for line in result.splitlines():
        if 'c_user=' in line:
            user_id = line.split('c_user=')[1].split(';')[0]
            if user_id not in unique_lines:
                unique_lines.add(user_id)
            else:
                duplicate_count += 1

    result_lines = [line for line in result.splitlines() if 'c_user=' in line]
    result_text = "\n".join(result_lines)

    processed_data = result_text
    duplicate_info = f"Đã xử lý xong! Có {duplicate_count} hàng dữ liệu trùng đã bị xóa."

    return render_template('result.html', processed_data=processed_data, duplicate_info=duplicate_info)

if __name__ == '__main__':
    app.run()
