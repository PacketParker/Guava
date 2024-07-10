FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/PacketParker/Guava"
LABEL org.opencontainers.image.authors="parker <mailto:contact@pkrm.dev>"

WORKDIR /

COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "-u",  "code/bot.py" ]