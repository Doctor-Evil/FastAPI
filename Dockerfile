FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
# COPY ./backend_fast /code/app

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]