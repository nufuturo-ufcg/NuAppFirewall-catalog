FROM python

WORKDIR /app

COPY rules-catalog/ ./rules-catalog/

RUN pip install --no-cache-dir -r rules-catalog/requirements.txt

WORKDIR /app/rules-catalog

ENTRYPOINT ["python", "main.py"]