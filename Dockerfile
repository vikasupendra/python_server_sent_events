FROM python:3.9 

RUN mkdir /home/app
COPY app.py /home/app
COPY requirements.txt /home/app/requirements.txt

RUN pip3 install -r /home/app/requirements.txt

CMD ["python3", "/home/app/app.py", "--student_name", "Logan_Harber74", "--exam_id", "1234"]