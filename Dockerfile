FROM node:10-alpine AS frontend

WORKDIR /app
COPY package.json .babelrc yarn.lock /app/
RUN yarn
COPY static/ /app/static/
RUN yarn run build

FROM python:3.7-alpine
WORKDIR /app
COPY --from=frontend /app/static/dist /app/static/dist
COPY requirements.txt /app/
RUN apk add --virtual builddeps gcc python3-dev build-base \
    && pip install -r requirements.txt \
    && apk del builddeps
COPY app.py /app/
COPY mirror/ /app/mirror/
COPY templates/ /app/templates/

EXPOSE 5000

CMD python -u app.py
