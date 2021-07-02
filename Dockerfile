FROM python:3.8-slim-buster

ENV PATH="/scripts:${PATH}"

COPY ./requirements.txt /requirements.txt
RUN apt-get update && apt-get install -y \
  gcc \
  libc-dev \
  && rm -rf /var/lib/{apt,dpkg,cache,log}/
RUN pip install -r /requirements.txt

RUN mkdir /climbersproject
COPY ./climbersproject /climbersproject/
WORKDIR /climbersproject
COPY ./scripts /scripts

RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser user

RUN chown -R user:user /usr/local/lib/python3.8/site-packages/allauth/account/migrations

RUN chown -R user:user /vol
RUN chmod -R 755 /vol

USER user

EXPOSE 8000

CMD ["entrypoint.sh"]
