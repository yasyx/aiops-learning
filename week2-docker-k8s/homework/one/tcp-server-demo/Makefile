
starts: cleans server
	chmod +x bin/server && ./bin/server

startc: cleanc client
	chmod +x bin/client && ./bin/client 

all: cleanc cleans server client

client:
	go build -o bin/client cmd/client/tcp_client.go

server:
	go build -o bin/server cmd/server/tcp_server.go 

cleanc:
	rm -rf bin/client
cleans:
	rm -rf bin/server	


