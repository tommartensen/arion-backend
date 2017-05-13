FROM django:1.10.4-python3

COPY . /usr/src/app

RUN pip install -r /usr/src/app/requirements/common.txt
EXPOSE 8000

CMD ["python", "/usr/src/app/manage.py", "runserver", "0.0.0.0:8000"]