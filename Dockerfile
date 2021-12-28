# syntax=docker/dockerfile:experimental

FROM python
WORKDIR /app
COPY . /app
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install cmake
RUN --mount=type=cache,target=/root/.cache/pip pip install -r ./requirements.txt

CMD [ "python", "/app/main.py"]