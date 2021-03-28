install:
	go build -buildmode=c-shared -o main.so
	chmod +x Tameshite.py setup.py
	python3 setup.py
