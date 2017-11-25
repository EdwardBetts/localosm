from flask import Flask, render_template, request, url_for, session, redirect
from itertools import dropwhile
from email.utils import formatdate
from . import lists, mail, nominatim, api

app = Flask(__name__)

def mail_contact_form():
    form = {f: request.form.get(f) or '[{} missing]'.format(f)
            for f in ('name', 'email', 'msg')}

    agent = request.headers.get('User-Agent', '[header missing]')
    subject = 'localosm contact: {form[name]} <{form[email]}>'
    body = '''localosm contact

name: {form[name]}
email: {form[email]}
agent: {agent}
IP: {ip}
time: {now}

message:

{form[msg]}'''.format(form=form,
                      agent=agent,
                      ip=request.remote_addr,
                      now=formatdate())
    mail.send(subject.format(form=form), body)

@app.route("/contact", methods=['GET', 'POST'])
def contact_page():
    if request.method == 'POST':
        session['msg_sent'] = True
        mail_contact_form()
        return redirect(url_for(request.endpoint))

    msg_sent = session.get('msg_sent')
    if msg_sent:
        del session['msg_sent']
    return render_template('contact.html', msg_sent=msg_sent)

@app.route("/api")
def api_docs():
    return render_template('api_docs.html')

@app.route("/api/1/lookup")
def api_lookup():
    return api.lookup()

def lookup_coords(lat, lon):
    r = nominatim.reverse_latlon(lat.strip(), lon.strip())
    result = nominatim.parse_json(r)
    address = result.get('address')
    ml = lists.lookup(address) or 'talk'

    if address:
        if 'city' in address:
            if 'postcode' in address:
                del address['postcode']
            address = list(dropwhile(lambda i: i[0] != 'city',
                           address.items()))
        else:
            address = address.items()

    return dict(address=address, ml=ml, lat=lat, lon=lon, result=result)

@app.route("/")
def index():
    q = request.args.get('q')
    if not q:
        return render_template('home.html', q=q)

    q = q.strip()
    coords = nominatim.parse_coords(q)
    if coords:
        q_type = 'latlon'
        params = lookup_coords(*coords)
    else:
        q_type = 'name'
        r = nominatim.lookup(q)
        result_list = nominatim.parse_json(r)
        result = result_list[0] if result_list else {}
        address = result.get('address')
        ml = lists.lookup(address) or 'talk'
        if address:
            address = address.items()

        params = dict(address=address, ml=ml, result=result)

    return render_template('home.html', q=q, q_type=q_type, **params)
