FROM python:3.9.11-slim
RUN apt-get update
RUN apt-get install curl gcc ffmpeg xvfb swig g++ freeglut3-dev -y
RUN pip install pipenv==2022.5.2
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED=1
WORKDIR /home/ds-user/
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv install --dev