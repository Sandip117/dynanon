FROM docker.io/python:3.11.0-slim-bullseye

# set working directory
WORKDIR /app

# copy requirements file
COPY ./requirements.txt /app/requirements.txt

# install dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
copy . .

CMD ["python", "main.py"]