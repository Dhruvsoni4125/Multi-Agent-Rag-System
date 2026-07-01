FROM python:3.11-slim
WORKDIR /code
COPY ./requirement.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . .
# Hugging Face runs on port 7860 by default
CMD ["streamlit", "run", "app.py", "--server.port", "7860", "--server.address", "0.0.0.0"]
