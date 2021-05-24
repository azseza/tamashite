install:
	go build -o httpflood.so -buildmode=c-shared main.go
	chmod +x
	python3 setup.py install
	echo "Enjoy !! "
