from flask import Flask, jsonify,render_template as rt,request
from werkzeug.utils import secure_filename
from config import aws_config
import os
import boto3
import random


# 非同步新增組件 Redis, Celery
from celery import Celery



ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__, static_folder="static",
            static_url_path="/", instance_relative_config=True)

# 因應非同步新增設置 請先確認是否有完成安裝 redis
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


s3 = boto3.client("s3",
                    aws_access_key_id = aws_config.ACCESS_KEY_ID,
                    aws_secret_access_key = aws_config.ACCESS_SECRET_ID
                    )

BUCKET_NAME = "motivetag"

@app.route('/')
def index():
    return rt("index.html")


@app.route("/upload",methods=["POST"])
def upload():
    try:
        img = request.files["image"]
        if img:
            filename = secure_filename(img.filename)
            img.save(filename)

            async_uploader.delay(filename)
            return jsonify({"ok":"upload complete!","msg":"ok"})
        else:
            return jsonify({"error":True})
    except Exception as e:
        print("type error: " + str(e))
        print(f"failed to upload file, delete file{filename}")
        os.remove(filename)

@celery.task
def async_uploader(filename):
    with app.app_context():
        print("start upload")
        s3.upload_file(
            Bucket = BUCKET_NAME,
            Filename = filename,
            Key = "test_"+str(random.randint(1,1000))
        )
        print("upload complete! delete file")
        os.remove(filename)
        return jsonify({"status":"ok"})


@app.route("/imgs",methods=["GET"])
def get_all_img():
    return jsonify({"data": result })



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
