FROM apache/airflow:3.0.4
COPY docker-context-files/requirements.txt /
# --user option casts errors
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt