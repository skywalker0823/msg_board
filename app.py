from flask import Flask, jsonify,render_template as rt,request
from werkzeug.utils import secure_filename
from config import aws_config
import os
import boto3
from data import Board

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__, static_folder="static",
            static_url_path="/", instance_relative_config=True)


s3 = boto3.client("s3",
                    aws_access_key_id = aws_config.ACCESS_KEY_ID,
                    aws_secret_access_key = aws_config.ACCESS_SECRET_ID
                    # aws_session_token = aws_config.AWS_SESSION_TOKEN
                    )

BUCKET_NAME = "wehelp-3"

@app.route('/')
def index():
    return rt("index.html")


@app.route("/upload",methods=["POST"])
def upload():
    if request.method=="POST":
        img = request.files["image"]
        says = request.form["says"]
        if img:
            filename = secure_filename(img.filename)
            img.save(filename)
            s3.upload_file(
                Bucket = BUCKET_NAME,
                Filename = filename,
                Key = filename
            )
            msg = "Upload complete"
            Board.uploads(says,filename)
            #RDS~
            #上傳完畢之後 紀錄資料庫 說了什麼 圖片的key 對應CDN的尾(id)
            return jsonify({"ok":"upload complete!","msg":msg})
        else:
            return jsonify({"error":True})

@app.route("/imgs",methods=["GET"])
def get_all_img():
    result = Board.get_all()
    return jsonify({"data": result })



# @app.route("/imgs",methods=["GET"])
# def get_img():
#     key = request.args.get("key")
#     contents = show_image(BUCKET_NAME,key)
#     print("---->>>",contents,"<<<------")
#     return jsonify({"data": contents })


# def show_image(bucket,key):
#     urls=[]
#     # for item in s3.list_objects(Bucket=BUCKET_NAME):
#     #     print(item,"???")
#     presigned_url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': key}, ExpiresIn=100)
#     # urls.append(presigned_url)
#     return presigned_url



# def show_image(bucket):
#     public_urls = []
#     try:
#         for item in s3.list_objects(Bucket=bucket)['Contents']:
#             presigned_url = s3.generate_presigned_url(
#                 'get_object', Params={'Bucket': bucket, 'Key': item['Key']}, ExpiresIn=100)
#             public_urls.append(presigned_url)
#     except Exception as e:
#         pass
#     # print("[INFO] : The contents inside show_image = ", public_urls)
#     return public_urls




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
