FROM postgres:16-alpine


COPY ./docker/local/postgres/maintenance /usr/local/bin/maintenance

RUN chmod +x /usr/local/bin/maintenance/* \
    && mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rm -rf /usr/local/bin/maintenance \
    && mkdir /usr/local/bin/maintenance