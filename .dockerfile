FROM python:latest
USER root

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y libx11-6 libxext-dev libxrender-dev libxinerama-dev libxi-dev libxrandr-dev libxcursor-dev libxtst-dev && rm -rf /var/lib/apt/lists/*

ADD controller projet/controller
ADD data projet/data
ADD models projet/models
ADD vue projet/vue
COPY app.py projet/app.py

CMD [ "python", "projet/app.py" ]