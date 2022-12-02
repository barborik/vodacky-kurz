from flask import Flask, request, render_template, url_for, redirect, abort
import json
import re

app = Flask(__name__)

"""
+======================================================+
|                                                      |
|                      chat :-)                        |
|                                                      |
+======================================================+
"""


@ app.route("/chat",  methods=["GET"])
def chat():
    return render_template("chat.html")


@ app.route("/chat/new",  methods=["POST"])
def chat_new():
    f = open("static/messages.txt", "a")
    f.write("\n" + request.form["text"])
    f.close()
    return redirect(url_for("chat"), code=302)


"""
+======================================================+
|                                                      |
|                   konec chatu :-(                    |
|                                                      |
+======================================================+
"""


@ app.route("/",  methods=["GET"])
def root():
    f = open("static/kamaradi.txt", "r")
    kamaradi = json.load(f)
    f.close()
    return render_template("index.html", kamaradi=kamaradi)


@ app.route("/register",  methods=["GET", "POST"])
def register():
    if(request.method == "POST"):
        f = open("static/kamaradi.txt", "r")
        kamaradi = json.load(f)
        f.close()

        nick = request.form.get("nick")
        je_plavec = request.form.get("je_plavec")
        kanoe_kamarad = request.form.get("kanoe_kamarad")

        if (nick == "" or je_plavec == None):
            return render_template("register.html", error="vyplňte povinná pole (ta s hvězdičkou)"), 400

        if (len(nick) < 2 or len(nick) > 20 or not re.match('^[\w-]+$', nick)):
            return render_template("register.html", error="přezdívka musí být v rozmezí 2-20 alfanumerických znaků"), 400

        if (int(je_plavec) == 0):
            return render_template("register.html", error="nejste plavec :-("), 400

        kamaradi[len(kamaradi)] = {
            "nick": nick,
            "je_plavec": je_plavec,
            "kanoe_kamarad": kanoe_kamarad
        }

        f = open("static/kamaradi.txt", "w")
        json.dump(kamaradi, f)
        f.close()

    return render_template("register.html"), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=80, debug=False)
