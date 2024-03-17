FROM python:3.12

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV TZ=Europe/Amsterdam

COPY requirements.txt /usr/src/app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --index-url https://test.pypi.org/simple/ --extra-index-url=https://pypi.org/simple/ -r requirements.txt

COPY /*.py /usr/src/app/

CMD [ "python", "-u", "." ]
