FROM golang:1.21 as builder

WORKDIR /build

ADD .  .

RUN make all 

FROM alpine:latest

COPY --from=builder /build/bin/* /bin/

CMD [ "/bin/server" ]


