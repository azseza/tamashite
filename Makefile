install:
	go build -buildmode=c-shared -o main.so
	chmod +x Tameshite.py setup.py ntpL4.py
	python3 setup.py install
	echo "Enjoy !! "