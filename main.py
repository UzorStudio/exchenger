from flask import Flask, render_template, request, redirect, session, jsonify
from random import randint
import base
import requests
import json

db = base.Base("localhost")

app = Flask(__name__)
app.secret_key = "mimoza1122"

procent = [{"coindrop":"","coinget":"","proc":0}]
#procent = [{"coindrop":"BTC","coinget":"BTC","proc":2}]

def regSess(sesid):
    session["sesid"] = sesid
    session["ticetid"] = ""


def delSess():
    try:
        session.pop("sesid", None)
        session.pop("ticetid", None)
    except:
        pass

def getPrice(froms,to):
    return requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={froms}&tsyms={to}&api_key=a5954b421dc01b9547ef9972a87ffbbaa58cf2308696439c6d2a5556199d761a").json()

@app.route('/tiket_<string:id>', methods=["POST", "GET"])
def Finish(id):
    if request.method == "POST":
        pass
    else:
        tiket = db.getTicetByTicId(id)
        db.setPayment(id)

        return render_template("tiket.html",ticet=tiket)


@app.route('/tikets', methods=["POST", "GET"])
def myTicket():
    if request.method == "POST":
        pass
    else:
        tikets = db.getTiketsBySesId(session['sesid'])
        print(tikets)

        return render_template("tikets.html",tikets=tikets)


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        coinDrop = request.form["coindrop"]
        coinGet = request.form["coinget"]
        count = request.form["countdrop"]
        wallet = request.form["wallet"]
        telegram = request.form["telegram"]
        email = request.form["email"]
        mass = request.form.to_dict()
        price = (float(getPrice(coinDrop,coinGet)[coinGet]) * float(count))

        for p in procent:
            if coinGet == p['coinget'] and coinDrop == p['coindrop']:
                price = price + (price * (float(p['proc'])*0.01))
            else:
                price = price - (price * (2 * 0.01))
        mass["price"] = str(price)
        mass["addr"] = db.getAdresForDrop(coinDrop)
        print(price)

        ticid = db.createTicet(coinDrop,coinGet,count,wallet,telegram,email,session['sesid'],price,mass["addr"])
        session['ticetid'] = str(ticid)
        mass["ticetid"] = session['ticetid']
        return render_template("twostep.html",ticet=mass)

    else:
        if "sesid" in session:
            print(session['sesid'])
            return render_template("index.html")
        else:
            regSess(str(randint(0,10000)))
            print(session['sesid'])
            return render_template("index.html")


#####API
@app.route('/d02a99eb-159f-4fde-83e6-ad2d92ab0833/getTickets', methods=["POST", "GET"])
def apiGetTickets():
    if request.method == "POST":
        pass
    else:
        tikets = db.APIgetTikets()
        print(tikets)

        return jsonify(tikets)

@app.route('/d02a99eb-159f-4fde-83e6-ad2d92ab0833/changeTicketStatus', methods=["POST", "GET"])
def changeTicketStatus():
    if request.method == "POST":
        status = request.form["status"]
        id = request.form["id"]
        print(id)

        db.APIsetTicketStatus(id,status)
        return "ok"
    else:

        return "0"


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)