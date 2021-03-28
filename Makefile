install:
	go build -buildmode=c-shared -o main.so
	pip install requirements.txt
	chmod +x Tameshite.py
