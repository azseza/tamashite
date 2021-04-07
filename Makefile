install:
	go build -o httpflood.so -buildmode=c-shared main.go
	chmod +x Tameshite.py setup.py ntpL4.py httpflood.so
	python3 setup.py install
	echo "Enjoy !! "