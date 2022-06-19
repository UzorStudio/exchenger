import pymongo
from bson import ObjectId

from datetime import datetime
from datetime import timedelta


class Base():
    def __init__(self, classterMongo):
        self.classterMongo = classterMongo
        self.classter = pymongo.MongoClient(self.classterMongo)

    def createTicet(self, coinDrop, coinGet, count, wallet, telegram, email, sesId, price, admin_wallet):
        db = self.classter["Skam"]
        Ticet = db["Ticet"]

        post = {"sesId": sesId,
                "coinDrop": coinDrop,
                "coinGet": coinGet,
                "count": count,
                "wallet": wallet,
                "admin_wallet": admin_wallet,
                "telegram": telegram,
                "email": email,
                "price": price,
                "status": "in_process"}

        return Ticet.insert_one(post).inserted_id

    def setPayment(self, id):
        db = self.classter["Skam"]
        Ticet = db["Ticet"]

        Ticet.update_one({"_id": ObjectId(id)}, {"$set": {"status": "payment"}})

    def setDecline(self, id):
        db = self.classter["Skam"]
        Ticet = db["Ticet"]

        Ticet.update_one({"_id": ObjectId(id)}, {"$set": {"status": "decline"}})

    def setSuccess(self, id):
        db = self.classter["Skam"]
        Ticet = db["Ticet"]

        Ticet.update_one({"_id": ObjectId(id)}, {"$set": {"status": "success"}})

    def getTiketsBySesId(self, sesId):
        db = self.classter["Skam"]
        Ticet = db["Ticet"]
        tikets = []

        for cursor in Ticet.find({}):
            if cursor["sesId"] == sesId:
                tikets.append(cursor)

        return tikets

    def APIgetTikets(self):
        db = self.classter["Skam"]
        Ticet = db["Ticet"]
        tikets = []

        for cursor in Ticet.find({}):

            if cursor["status"] != "in_process":
                post = {"id": str(cursor["_id"]),
                        "status": cursor["status"],
                        "currency_from": cursor["coinDrop"],
                        "currency_to": cursor["coinGet"],
                        "count": cursor["count"],
                        "price": cursor["price"],
                        "client_wallet": cursor["wallet"],
                        "admin_wallet": cursor["admin_wallet"],
                        "created": ObjectId(str(cursor["_id"])).generation_time.now()
                        }
                tikets.append(post)

        return tikets


    def APIsetTicketStatus(self,id,status):
        db = self.classter["Skam"]
        Ticet = db["Ticet"]

        Ticet.update_one({"_id": ObjectId(id)}, {"$set": {"status": status}})


    def getTicetByTicId(self, id):
        db = self.classter["Skam"]
        Ticet = db["Ticet"]
        return Ticet.find_one({"_id": ObjectId(id)})

    def createCryptoAdress(self, addr, coin):
        db = self.classter["Skam"]
        CryptAdr = db["CryptAdr"]

        post = {'coin': coin,
                'addr': addr}
        CryptAdr.insert_one(post)

    def getAdresForDrop(self, coin):
        db = self.classter["Skam"]
        CryptAdr = db["CryptAdr"]

        return CryptAdr.find_one({"coin": coin})["addr"]
