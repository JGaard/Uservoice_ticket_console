#!/usr/bin/env python
#The following was written by Jamie Gaard.
#She does NOT give permision to use her work without consulting her first.
#Copyright@JamieGaard


from flask import *
import urllib
import uservoice_console
import gspread_uservoice

#Initizalizeing the flask framework
app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.CSRF_ENABLED = True

##Authorization credentials. Used to pull and push to the uservoice servers.
SUBDOMAIN_NAME = ''
API_KEY = ''
API_SECRET = ''


@app.route("/")
def home():
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        global SUBDOMAIN_NAME
        SUBDOMAIN_NAME = request.form.get('SUBDOMAIN_NAME')
        global API_KEY
        API_KEY = request.form.get('API_KEY')
        global API_SECRET
        API_SECRET = request.form.get('API_SECRET')
        
        return redirect(url_for('helpdesk'))
        
    if request.method == 'GET':
        return render_template('login.html')

@app.route("/helpdesk", methods=['GET', 'POST'])
def helpdesk():
    if request.method == 'POST':
        tickets = uservoice_console.Tickets(SUBDOMAIN_NAME, API_KEY, API_SECRET)
        articles = uservoice_console.Articles(SUBDOMAIN_NAME, API_KEY, API_SECRET)
        ticket_id = int(request.form.get('current_ticket_value'))
        
        if request.form.get('ticket_state') == 'yes':
            tickets.close_ticket(ticket_id)
        else:
            article_id = int(request.form.get('response_article_value'))    
            ticket_response = articles.get_raw_articles()[article_id]['text'].replace('&nbsp;', ' ').replace('\n', ' ').replace('Hi twiner!', '').replace("PS: Can you help us out? If you've been having fun on twine, please rate us 5 stars:", '').replace('- Etan (@etanb)', '').replace('Twitter and Facebook', '').replace('Head of twine Customer ExperienceGet informative and entertaining updates on:', '').replace('App Store: http://bit.ly/twineappleGoogle Play: http://bit.ly/twinegoogle', '')
            append_spreadsheet(article_id, tickets.open_tickets[ticket_id])
            tickets.post_response(ticket_id, ticket_response)
            
        return redirect(url_for('helpdesk'))
    
    if request.method == 'GET':
        return render_template('helpdesk.html', tickets = uservoice_console.Tickets(SUBDOMAIN_NAME, API_KEY, API_SECRET),
                                                articles = uservoice_console.Articles(SUBDOMAIN_NAME, API_KEY, API_SECRET))
    
def append_spreadsheet(article_id, ticket):
    #article_dict is a dict of features to be appended to a googlevoice spreadsheet. The dict's keys are based according to the article_id #. This allows for easy refrence when posting the article_id from the client.
    #Can be expanded upon as number of articles grows.
    article_dict={249174:'Delete old conversations', 249177:'Alternatives to Facebook login', 232636:'Faster Juice refill/No juice',
                  232628:'More accurate location matching', 232630:'More accurate age matching', 260726: 'Add photo from device library',
                  234822:'More OS support', 234850:'No replies/No matches', 248316:'Recover conversations'}
    #Two articles act differently than most. Bug_reporting and Users_to_delete call their own functions to be be appended to the google spreadsheet. They are referenced by their article_id number. 
    if article_id == 241772:
        gspread_uservoice.gs.update_users_to_delete(ticket['sender_email'])
    elif article_id == 234816:
        gspread_uservoice.gs.update_bugs(ticket['message'], ticket['devices'])
    else:
        if article_id in article_dict.keys():
            gspread_uservoice.gs.update_features(article_dict[article_id])
        else:
            return None 

#Test page for display bugs.                     
@app.route('/test_page')
def test_page():
    return render_template('test.html')

if __name__ == "__main__":
    app.run(debug=True)