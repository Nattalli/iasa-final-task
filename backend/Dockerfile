FROM python:3.9.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /backend

COPY requirements.txt /backend/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python -m nltk.downloader punkt

COPY . /backend

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
