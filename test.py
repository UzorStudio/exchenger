import base
import requests

db = base.Base("localhost")

print(requests.post("http://localhost:5000/d02a99eb-159f-4fde-83e6-ad2d92ab0833/changeTicketStatus",data={"status": 'success', "id": '62acd4bd57fb411c6127a9c9'}))

#db.createCryptoAdress(addr="bc1qjgmk8rgjpu73xnqx8yzn3etku6t3pf8jp6kca7",coin="BTC")
#db.createCryptoAdress(addr="DFDV4VV5b51KMcV26DjdjJJijRGMQkK9Gg",coin="DOGE")
#db.createCryptoAdress(addr="0x7cdFcC3151670037f692Ef9cC31ae2a1a597569F",coin="ETH")
#db.createCryptoAdress(addr="ltc1q2rvnv8sq7mh2vaalg8xstu9gn76ye0zjmfkrhd",coin="LTC")
#db.createCryptoAdress(addr="TC6s9oA7GiDcv1kR1SspcB5d2WGmNT5LHS",coin="TRX")