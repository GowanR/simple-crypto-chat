# simple-crypto-chat
Encrypted chat in the command line written in python

## Usage:

Run server on port 8888.
```
python crypto_chat_server.py 8888
```
Run client connects to localhost on port 8888. Recieves messages on port 8887.

```
python crypto_chat_client.py 8887 localhost 8888
```

## Install dependencies

Just run a simple `pip install cryptopy`
