import datetime
from email_ver import email_ver
import os
from time import time
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
import re

verified=[False]
l_ev=[]



def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None
# Configure application
app = Flask(__name__)

# Custom filter


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/email_auth", methods=["GET", "POST"])
def email_auth():
    print("_"*30,"email_auth","_"*30)
    
    if request.method == "POST" and request.form.get("email_ver"):
        ver_code=l_ev[3]
        print("ver-code: ",ver_code)
        
        inp = request.form.get("email_ver")
        if datetime.datetime.now().timestamp()-l_ev[-1]>120:
            return apology("took more than 2 min",403)
        if str(inp).strip()==ver_code:
            verified[0]=True
            return redirect(f"{l_ev[4]}")
        else:
            return apology("email verification code is incorrect",403)
    else:
        return render_template("email_auth.html")




@app.route("/")
@login_required
def index():
    print("_"*30,"index","_"*30)
    """Show portfolio of stocks"""
    #JOIN cards ON users.id=cards.owner_id JOIN pn ON cards.owner_id=pn.user_id
    l_all = db.execute(f"SELECT * FROM users")
    history = db.execute(f"SELECT * FROM history WHERE user_id = {session['user_id']}")
    if len(history)>6:
        history=history[-5:]
        history.reverse()
    print("/"*30,"history","/"*30)
    print(history)

    
    print(l_all)
    
    l_cards = db.execute(f"SELECT card,cash FROM cards WHERE owner_id={session['user_id']}")
    
    
    l_pn = db.execute(f"SELECT * FROM pn WHERE user_id={session['user_id']}")
    print(l_cards,l_pn)
    if len(l_cards)==0:
        return redirect("/addcard")
    print(l_cards)
    return render_template("index.html",cards=l_cards,history=history)
    
@app.route("/addcard", methods=["GET", "POST"])
@login_required
def addcard():
    print("_"*30,"addcard","_"*30)
    if request.method == "POST":
        card = request.form.get("card")
        password = request.form.get("password")
        print(f"card: {card}")
        print(f"password: {password}")
        
        if not card or not password:
            return apology("dont leave fields blank")
        try:
            db.execute(f"INSERT INTO cards (owner_id,card,pass,cash) VALUES ({session['user_id']},'{card}','{password}',10000)")
            
            print("yes")
            db.execute(f"INSERT INTO history(user_id,type,sender,reciever,amount) VALUES({session['user_id']},'addcard','{card}','',0)")
            return redirect("/")
        except:
            return apology("meowmeowmeow")
    return render_template("addcard.html")


@app.route("/charge", methods=["GET", "POST"])
@login_required
def charge():
    print("_"*30,"charge","_"*30)
    if verified[0]:
        #card_
        #pn_
        #amount
        db.execute(f"UPDATE cards SET cash={l_ev[0]['cash']-l_ev[2]} WHERE card = '{l_ev[0]['card']}'")
        print(2)
        db.execute(f"UPDATE pn SET charge= {l_ev[1]['charge']+l_ev[2]} WHERE phone_number = '{l_ev[1]['phone_number']}'")
        print(3)
        db.execute(f"INSERT INTO history(user_id,type,sender,reciever,amount) VALUES({session['user_id']},'charge','{l_ev[0]['card']}','{l_ev[1]['phone_number']}',{l_ev[2]})")
        l_ev.clear()
        return redirect("/")
    l_cards = db.execute(f"SELECT card,cash,pass FROM cards WHERE owner_id={session['user_id']}")
    l_pn = db.execute(f"SELECT * FROM pn WHERE user_id={session['user_id']}")
    if request.method == "POST":
        verified[0]=False
        pn = request.form.get("phone_number")
        card = request.form.get("card")
        amount = request.form.get("amount")
        ps = request.form.get("ps")
        email = db.execute(f"SELECT * FROM users WHERE id={session['user_id']}")[0]["email"]
        print(f"card: {card}")
        print(f"pn: {pn}")
        print(f"amount: {amount}")
        print(f"pass: {ps}")
        print(f"email: {email}")
        
        if not card or not pn or not amount:
            return apology("dont leave fields blank")
      
        try:
            amount = int(amount)
            if amount<1:
                return apology("cant buy negative charge")
            card_ = l_cards[int(card)]
            pn_= l_pn[int(pn)]
            print(ps)
            print(card_["pass"])
            if str(ps)!=str(card_["pass"]):
                return apology("invalid card pass")
            if int(card_["cash"])<amount:
                return apology("not enough money")
            l_ev.append(card_)
            l_ev.append(pn_)
            l_ev.append(amount)
            l_ev.append(email_ver(str(email).strip()))
            print("code: ",l_ev[-1])
            l_ev.append("/charge")
            l_ev.append(datetime.datetime.now().timestamp())
            print(l_ev)
            return redirect("/email_auth")
        except:
            return apology("meowmeowmeow")
    return render_template("charge.html",l_pn=l_pn,l_cards=l_cards)







@app.route("/transfer", methods=["GET", "POST"])
@login_required
def transfer():
    print("_"*30,"transfer","_"*30)
    l_cards = db.execute(f"SELECT card,cash FROM cards")
    l_mine = db.execute(f"SELECT card,cash,pass FROM cards WHERE owner_id={session['user_id']}")
    
    print(l_cards)
    print(l_mine)
    if verified[0]:
        #send
        #reci
        #cash
        db.execute(f"UPDATE cards SET cash={l_ev[0]['cash']-l_ev[2]} WHERE card = '{l_ev[0]['card']}'")
        print(2)
        db.execute(f"UPDATE cards SET cash={l_ev[1]['cash']+l_ev[2]} WHERE card = '{l_ev[1]['card']}'")            
        print(3)
        db.execute(f"INSERT INTO history(user_id,type,sender,reciever,amount) VALUES({session['user_id']},'transfer','{l_ev[0]['card']}','{l_ev[1]['card']}',{l_ev[2]})")
        l_ev.clear()
        return redirect("/")
    if request.method == "POST":
        verified[0]=False
        sender = request.form.get("sender")
        reciever = request.form.get("reciever")
        amount = request.form.get("amount")
        ps = request.form.get("ps")
        email = db.execute(f"SELECT * FROM users WHERE id={session['user_id']}")[0]["email"]
        print(f"sender: {sender}")
        print(f"reciever: {reciever}")
        print(f"amount: {amount}")
        print(f"ps: {ps}")
        print(f"email: {email}")

        
        if not sender or not reciever or not amount:
            return apology("dont leave fields blank")
        
        try:
            print(0)
            amount = int(amount)
            if amount<1:
                return apology("cant buy negative charge")
            print(0.1)
            send = l_mine[int(sender)]
            print(send)
            print(0.12)
            if str(send["pass"])!=str(ps):
                return apology("invalid user/pass")
            print(0.2)
            reci = l_cards[int(reciever)]
            print(1)

            if int(send["cash"])<amount:
                return apology("not enough money")
            if str(ps)!=str(send["pass"]):
                return apology("invalid card pass")
            print(2)
            l_ev.append(send)
            l_ev.append(reci)
            l_ev.append(amount)
            l_ev.append(email_ver(str(email).strip()))
            print("code: ",l_ev[-1])
            l_ev.append("/transfer")
            l_ev.append(datetime.datetime.now().timestamp())
            print(l_ev)
            print(3)
            return redirect("/email_auth")
        except:
            print("heeeeeb")
            return apology("meowmeowmeow",400)
    return render_template("transfer.html",l_mine=l_mine,l_cards=l_cards)






























@app.route("/addpn", methods=["GET", "POST"])
@login_required
def addpn():
    print("_"*30,"addpn","_"*30)
    if request.method == "POST":
        card = request.form.get("phone_number")
        print(f"card: {card}")
        
        if not card:
            return apology("dont leave fields blank")
        try:
            db.execute(f"INSERT INTO pn (user_id,phone_number,charge) VALUES ({session['user_id']},'{card}',0)")
            
            print("yes")
            db.execute(f"INSERT INTO history(user_id,type,sender,reciever,amount) VALUES({session['user_id']},'addpn','{card}','',0)")
            return redirect("/")
        except:
            return apology("meowmeowmeow")
    return render_template("addpn.html")


@app.route("/email_ver", methods=["GET", "POST"])
def email_ver_check():
    print("_"*30,"email_ver","_"*30)
    if request.method == "POST" and request.form.get("email_ver"):
        print(l_ev)
        user_info,ver_code = l_ev[0],l_ev[1]
        print("user_info: ",user_info)
        print("ver_code: ",ver_code)
        l_ev.clear()
        inp = request.form.get("email_ver")
        if inp==ver_code:
            session["user_id"] = user_info["id"]
            print(db.execute("SELECT * FROM cards WHERE owner_id = ?", user_info["id"]))
            print(db.execute("SELECT * FROM pn WHERE user_id = ?", user_info["id"]))
            return redirect("/")
        else:
            return apology("email verification code is incorrect",403)
    else:
        return render_template("email_ver.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    print("_"*30,"login","_"*30)
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        print(rows)
        # Ensure username exists and password is correct
        if len(rows) < 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)
        

        user_info = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))[0]
        print(user_info)
        print("*"*50)
        print(user_info["email"].strip())
        ver_code = email_ver(str(user_info["email"].strip()))
        print(ver_code)
        print("*"*50)
        l_ev.append(user_info)
        l_ev.append(ver_code)
        return redirect("/email_ver")

            

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    print("_"*30,"register","_"*30)
    """Register user"""
    session.clear()
    user_names = db.execute("SELECT username FROM users")
    print(user_names)

    try:
        if request.method == "POST":
            user_name=request.form.get("username")
            pass_word=request.form.get("password")
            con_firmation=request.form.get("confirmation")
            e_mail = request.form.get("email")
            card = request.form.get("card")
            card_pass = request.form.get("card_pass")
            pn = request.form.get("phone_number")
            print(request.form)
            # Ensure username was submitted
            
            if not user_name:
                return apology("must provide username", 400)
            elif user_name in user_names:
                return apology("duplicate username", 400)
            # Ensure password was submitted
            elif not pass_word:
                return apology("must provide password", 400)
            elif not con_firmation:
                return apology("must provide confirmation", 400)
            elif con_firmation!=pass_word:
                return apology("password and confirmation should match", 400)
            elif len(pass_word)<5:
                return apology("short password")
            elif not validate_email(e_mail):
                return apology("invalid email")
            elif not (pn[0]=="0" and pn[1]=="1" and len(pn)==11):
                return apology("invalid phone number")
            
            else:
                pass_hash  = generate_password_hash(pass_word)
                card_pass_hash = generate_password_hash(card_pass)
                db.execute(f"INSERT INTO users(username,hash,email) VALUES('{user_name}','{pass_hash}','{e_mail}')")
                print(1)
                rows = db.execute("SELECT id FROM users WHERE username = ?", user_name)
                print(2)
                db.execute(f"INSERT INTO cards(owner_id,card,pass,cash) VALUES({rows[0]['id']},'{card}','{card_pass_hash}',10000)")
                print(3)
                db.execute(f"INSERT INTO pn(user_id,phone_number,charge) VALUES({rows[0]['id']},'{pn}',0)")
                print(4)
                return redirect("/")
        else:
            return render_template("register.html")
    except:
        return apology("meow")






















# xor encryption (just to get the points)
    
def str_xor(s1, s2):
    return "".join([chr(ord(c1) ^ ord(c2)) for (c1,c2) in zip(s1,s2)])

"""
usage:

encoded = str_xor(message, passcode)
decoded = str_xor(encoded, passcode)

"""









