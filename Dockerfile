FROM python:3.8.3-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY voucher_api api_endpoint
COPY utils utils
EXPOSE 5000
ENTRYPOINT ["python3", "./api_endpoint/voucher_selection_api.py"]