from flask import Flask, request, session, redirect
from flask import render_template
from CASAuthenticator import CASAuthenticator
app = Flask(__name__)
# don't leak this lol, it's used for encrypting session tokens (JWT)
app.secret_key = b"\x81V\xc8\x0b\xd4Sh>'BF\xa7\xd29\x92S2\xf8\x93Z\x7f\xce\x98\xc5"


@app.route('/')
def hello(name=None):
    return render_template('index.html')
	
@app.route('/start/')
def about():
    return render_template('start.html')

@app.route('/authorize')
def authorize():
    """
    Begin CAS authorization for the user
    :return: A redirect to the CAS endpoint (uses the OCF trampoline)
    """
    return redirect(CASAuthenticator.get_authentication_redirect_URL(), 302)

@app.route('/authorizationComplete')
def didAuthorize():
    """
    Handles setting the session["uid"] using the ticket query parameter from the URL using CAS
    """
    ticket = request.args.get("ticket")
    if not ticket:
        return "Response did not include a ticket!", 400

    uid = CASAuthenticator.validate(ticket)
    if not uid:
        return "CAS rejected the token", 401

    session["uid"] = uid
    return f"Authorization success.<br/>Hello UID {uid}!", 200

if __name__ == '__main__':
    app.run(debug=True)
