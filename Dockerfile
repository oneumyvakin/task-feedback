FROM python:3.7.1-stretch

COPY src/ src/

WORKDIR src

RUN ls -la

RUN pip --no-cache-dir install --upgrade -r requirements.txt

ENTRYPOINT ["python", "main.py"]