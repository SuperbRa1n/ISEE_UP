from flask import Flask, request, jsonify, render_template
import os
from cos import CosBucket

bucket = CosBucket(secret_id=os.getenv("COS_SECRET_ID"), secret_key=os.getenv("COS_SECRET_KEY"), region=os.getenv("COS_REGION"))

app = Flask(__name__)

# 存储提交数据的列表
submissions = []

# 设置文件上传的目录
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    class_name = request.form['class']
    student_id = request.form['student_id']
    file = request.files['file']

    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

    # 上传文件到 COS
    file_url = bucket.upload_file(file_path)

    submission = {
        'name': name,
        'class': class_name,
        'student_id': student_id,
        'file_url': file_url,
    }
    submissions.append(submission)

    return '提交成功'

@app.route('/submissions', methods=['GET'])
def get_submissions():
    return jsonify(submissions)

if __name__ == '__main__':
    app.run(debug=True)
