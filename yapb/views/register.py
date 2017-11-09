__all__ = ["register"]

from flask import request,render_template
from yapb import app

@app.route("/register",methods=["GET"])
def register():
    if request.method =="GET":
       return render_template("register.html")
