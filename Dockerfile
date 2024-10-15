FROM alpine:3.18.4

# Install python/pip and ssh
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python \
    && python3 -m ensurepip \
    && pip3 install --no-cache --upgrade pip setuptools

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY run.py .

EXPOSE 5000

CMD ["gunicorn", "run:app", "-b", "0.0.0.0:5000", "-w", "4"]