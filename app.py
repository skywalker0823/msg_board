from flask import Flask, jsonify,render_template as rt,request
from werkzeug.utils import secure_filename
from config import aws_config
import os
import boto3
import random, time
from dotenv import load_dotenv


from celery import Celery
# from modules.celery_app import celery

load_dotenv()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__, static_folder="static",
            static_url_path="/", instance_relative_config=True)


#自動連接
# routes = ["localhost","b_redis"]
# for route in routes:
#     try:
#         app.config['CELERY_BROKER_URL'] = f'redis://{route}:6379'
#         print(f"redis connect to {route} success")
#         break
#     except Exception as e:
#         print("redis connect all fail")
#         print(e)
#         continue
app.config['CELERY_BROKER_URL'] = os.getenv('REDIS_CONN')
app.config['CELERY_RESULT_BACKEND'] = os.getenv('REDIS_CONN')
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


@app.route('/call',methods=["GET"])
def call():
    return jsonify({"ok":"ok"})


@app.route("/upload",methods=["POST"])
def upload():
    try:
        img = request.files["image"]
        says = request.form["says"]
        type = request.form["type"]
        print(says)
        filename = secure_filename(img.filename)
        filename = str(random.randint(1,100000))+"_"+filename
        if img and type=="async":
            img.save(filename)

            async_uploader.delay(filename)

            print("upload response")
            return jsonify({"ok":"upload complete!","msg":"async"})
        elif img and type=="sync":
            img.save(filename)
            print("uploading please wait")
            time.sleep(5)
            s3.upload_file(
                Bucket = BUCKET_NAME,
                Filename = filename,
                Key = "test_"+str(random.randint(1,100000))
            )
            print("upload complete! delete file")
            os.remove(filename)
            return jsonify({"ok":"upload complete!","msg":"sync"})    
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
        time.sleep(5)
        s3.upload_file(
            Bucket = BUCKET_NAME,
            Filename = filename,
            Key = "test_"+str(random.randint(1,1000))
        )
        print("upload complete! delete file")
        os.remove(filename)
        # return jsonify({"status":"ok"})


@app.route("/imgs",methods=["GET"])
def get_all_img():
    return jsonify({"data": result })



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)




# Note:
# Redis: docker run -dp 6379:6379 redis:5
# Celery: celery -A app.celery worker --loglevel=info
# docker-compose -f docker-compose.yaml up -d --build 