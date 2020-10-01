from pathlib import Path
import json
import random
from flask import Flask, render_template, request
import boto3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nb_payment = int(request.form["number"])
        if nb_payment > 0:
            with open('aws-cred.json') as json_data_file:
                        config = json.load(json_data_file)
            print(config["ACCESS_KEY_ID"])

            session = boto3.Session(
                aws_access_key_id=config["ACCESS_KEY_ID"],
                aws_secret_access_key=config["SECRET_ACCESS_KEY"],
                region_name='eu-west-1'
                )

            BUCKET_NAME = "lead-s2-paysim"
            PREFIX = "model"

            s3 = session.client("s3")
            s3.download_file(BUCKET_NAME, 'model/valid/paysim-valid.csv', './data/paysim-valid.csv')

            with open("./paysim-valid.csv", "r") as file:
                lines = file.readlines()

                arn = "arn:aws:sns:eu-west-1:591262896876:paysim"

                payment = {"payment":",".join(random.choice(lines).split(",")[1:]).strip()}

                for n in range(nb_payment):
                    sns = session.client('sns', region_name='eu-west-1')

                    sns.publish(
                        TargetArn=arn,
                        Message=json.dumps({'default': json.dumps(payment)}),
                        MessageStructure='json'
                    )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0')