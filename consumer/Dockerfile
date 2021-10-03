FROM python:3.7

RUN mkdir /app
ADD /app/. /app/
RUN pip install -r /app/requirements.txt

EXPOSE 5000
CMD ["python", "-u", "/app/main.py"]
