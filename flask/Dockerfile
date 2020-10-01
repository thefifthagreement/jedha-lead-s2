FROM python:rc-alpine

WORKDIR /opt/project/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY aws-cred.json .
EXPOSE 5000/tcp
ENTRYPOINT ["python3", "app.py"]