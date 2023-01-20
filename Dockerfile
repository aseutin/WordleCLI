FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH="/usr/src/app:$PYTHONPATH"
RUN export PYTHONPATH

ENV MYPYPATH=$PYTHONPATH
RUN export MYPYPATH

RUN apt-get update && apt-get install wamerican  # install English language dict at /usr/share/dict/

CMD [ "python", "main.py" ]
