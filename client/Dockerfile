FROM python:3.9-slim

COPY requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt

COPY app.py app.py
COPY pages/admin_page.py pages/admin_page.py

CMD ["streamlit", "run", "app.py"]