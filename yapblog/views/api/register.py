__all__=["api_register"]

from flask import request
from yapblog import app
from yapblog.lib.api import ok,not_ok

@app.route("/api/register",methods=["POST"])
def api_register():
    """
    Register
    Methof:POST
    Parameters:name email passwd confirm passwd
    Erro:{
            "ok": False,
	    "message","Entered password differ!"
          }
    Sucess:{
          "ok" : True
	   "msg":"Register scucessfully!"

    }
    """
    try:
        name = request.form["name"]
    except KeyError:
        return not_ok("no name")
   
    try:
       email = request.form["email"]
    except KeyError:
         return not_ok["no email"]
    
    try:
        passwd =  request.form["passwd"]
    except KeyError:
         return not_ok["no passwd"]
    
    try:
        confirm_passwd =  request.form["confirm_passwd"]
    except KeyError:
         return not_ok["no confirm_passwd"]
    

    if passwd != confirm_passwd:
       return not_ok["Entered password differ!"]
    else:
       # TODO
       return ok["Register sucessfully!"]

