FROM python:latest
RUN apt-get update -y --fix-missing && apt-get install vim -y
WORKDIR /dadaforest
COPY ./requirements.txt .
RUN pip install pip uv --upgrade && pip install --no-cache-dir -r requirements.txt \
   && rm -rf /var/cache/apt/archives /var/lib/apt/lists/*