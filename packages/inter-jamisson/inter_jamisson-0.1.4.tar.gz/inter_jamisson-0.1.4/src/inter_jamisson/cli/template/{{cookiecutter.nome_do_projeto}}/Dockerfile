FROM python:3.10.12-slim-bookworm AS inter-base

ARG USER_UID=1000
ARG USER_GID=20

WORKDIR /opt/inter

RUN adduser --gecos "First Last,RoomNumber,WorkPhone,HomePhone" --disabled-password \
    --quiet "inter" --uid ${USER_UID} --gid ${USER_GID} --home /opt/inter/ && chown -R "inter" /opt/inter/

RUN apt-get update && apt-get install -y ffmpeg
USER inter
RUN pip install --upgrade pip

COPY --chown=inter:0 requirements.txt /opt/inter/
ENV PATH=/opt/buora/.local/bin:${PATH}

FROM inter-base AS build-dependencies
RUN echo "fastapi==0.109.0" >> requirements.txt
RUN echo "uvicorn==0.24.0" >> requirements.txt
RUN cat requirements.txt | sort > requirements-sorted.txt
RUN mv requirements-sorted.txt requirements.txt
RUN mkdir /opt/inter/dependencies/
RUN cp requirements.txt /opt/inter/dependencies/requirements.txt

FROM inter-base AS inter
USER inter
COPY --from=build-dependencies /opt/inter/dependencies/ /opt/inter/dependencies/
RUN pip install -r /opt/inter/dependencies/requirements.txt
COPY --chown=inter:0 src/ /opt/inter/src/
COPY --chown=inter:0 data/ /opt/inter/data/

FROM inter AS inter-fastapi
EXPOSE 8000
ENTRYPOINT ["python3", "-m","uvicorn", "--host", "0.0.0.0", "src.deploy:app"]