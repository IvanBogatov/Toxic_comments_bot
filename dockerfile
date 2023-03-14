FROM python:3.10.8
ENV TOKEN='<YOUR TOKEN>'
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD python main.py