# Downloader 

## Requirements
- Python 3.7.1

## Usage
```
cd src
pip install -r requirements.txt
python main.py --url_file example.txt
```

## Help
```
python main.py -h
```

## Run in Docker

```
# docker build -t downloader .
# docker run downloader --url_file example.txt
2018-11-25 01:28:44,150 [MainThread  ] [INFO ]  File size: 14
2018-11-25 01:28:44,151 [MainThread  ] [INFO ]  http://ya.ru
2018-11-25 01:28:44,777 [MainThread  ] [INFO ]  Success! Processed: 1
```
