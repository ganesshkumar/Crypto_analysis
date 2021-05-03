FROM python:3.8-buster

WORKDIR /app
EXPOSE 8501 

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "streamlit", "run" , "main.py"]