FROM ubuntu:16.04

RUN apt-get update && apt-get install -y default-jre curl python python-pip

RUN mkdir -p /app/minecraft

WORKDIR /app/minecraft

RUN curl -o server.jar https://launcher.mojang.com/v1/objects/fe123682e9cb30031eae351764f653500b7396c9/server.jar
RUN echo eula=true >> eula.txt
COPY entrypoint.sh ./
COPY handler.py ./
RUN chmod a+x entrypoint.sh
RUN chmod a+x handler.py

CMD /app/minecraft/entrypoint.sh
