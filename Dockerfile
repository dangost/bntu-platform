FROM alpine:3.17.3

WORKDIR /app

COPY alpine/ /app/

CMD ["./platform"]

EXPOSE 8080