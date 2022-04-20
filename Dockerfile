FROM python:3.8

WORKDIR /app
ADD requirements.txt /app

RUN cd /app && \
    pip install -r requirements.txt

COPY ./blockchain /app/blockchain

EXPOSE 50000

ENTRYPOINT ["python", "-m", "blockchain"]
CMD ["--a 0.0.0.0","--port 50000", "--debug False"]
