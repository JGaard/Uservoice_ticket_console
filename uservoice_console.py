""" Experimental Script to help pull in Uservoice API data and stream line the ticket response process. The following was written by Jamie Gaard.
She does NOT give express permission for anyone to use the following and will severly punish anyone who attempts to fraud her work. She is above the law"""
"""Copyright@JamieGaard"""

import uservoice
import re

##Authenticaion is a superclass that sets the client_login information used to create, update, change and view article and tickets.
class Authentication(object):
    def __init__(self, subdomain, api_key, api_secret=None):
        self.subdomain = subdomain
        self.api_key = api_key
        self.api_secret= api_secret
        self.client = self.client_login()
        
    def client_login(self):
        return uservoice.Client(self.subdomain, self.api_key, self.api_secret)

class Tickets(Authentication):
    def __init__(self, subdomain, api_key, api_secret):
        super(Tickets, self).__init__(subdomain, api_key, api_secret)
        #non-conforming tickets are 
        self.nonconforming_tickets = []
        self.open_tickets = self.set_open_tickets()
        self.current_ticket = self.set_current_ticket(self.open_tickets.iterkeys().next())
    
    def set_current_ticket(self, ticket_number):
        return self.open_tickets[ticket_number]
    
    def set_open_tickets(self):
        open_tickets = {}
        tickets = self.client.get_collection('/api/v1/tickets/search.json?query=status%3Aopen')
        for ticket in tickets:
            body = self.format_ticket(ticket)
            try:
                open_tickets[ticket['id']] = {'subject':ticket['subject'], 'sender_username':ticket['messages'][0]['sender']['name'],
                                                         'sender_email':ticket['messages'][0]['sender']['email'], 'devices':body['Device(s)'], 'sender_name':body['Name'],
                                                         'location':body['Location'], 'message':body['Message']}  
            except:
                self.nonconforming_tickets.append(body) 
        return open_tickets
    
    def retrieve_open_tickets(self):
        return self.open_tickets
    
    def retrieve_current_ticket(self):
        return self.current_ticket
    
    def retrieve_nonconforming_tickets(self):
        return self.nonconforming_tickets
    
    def format_message(self, ticket):
        ticket = ticket['messages'][0]['body']
        ticket = ticket.replace('\n\n','\n').splitlines()
        ticket = [x.strip(' ') for x in ticket]
        return ticket

    def format_body(self, ticket):
        try:
            message_index = ticket.index('Message:')
            message = ticket[message_index:-1]
            ticket = ticket[:message_index] + ticket[-1:]
    
        except ValueError:
            self.nonconforming_tickets.append(ticket)
            
    
        try:
            ticket = dict(s.split(':') for s in ticket)
            message = dict(s.split(':') for s in [''.join(message)])
            body_dict = ticket.copy()
            body_dict.update(message)
            return body_dict
    
        except ValueError, AttributeError:
            self.nonconforming_tickets.append(ticket)
        
    
    def format_ticket(self, ticket):
        message_dict = self.format_body(self.format_message(ticket))
        return message_dict
    
    def post_response(self, ticket_id, ticket_response):
        with self.client.login_as_owner() as owner:
            posted_response = owner.post("/api/v1/tickets/" + str(ticket_id) + "/ticket_messages.json?", {
            'ticket_message': {
                #Custom headers and signatures with the message_body append to the middle
                'text': 'Hi Twiner!' + '\n\n' +
                ticket_response + '\n' +
                "PS: Can you help us out? If you've been having fun on twine, please rate us 5 stars:" + '\n\n' +
                "App Store: http://bit.ly/twineapple" + '\n\n' +
                "Google Play: http://bit.ly/twinegoogle" + '\n\n' +
                "- Etan (@etanb)"  + '\n\n' +
                "Head of twine Customer Experience" + '\n\n' +
                "Get informative and entertaining updates on: Twitter and Facebook"
            }})
    
    def close_ticket(self, ticket_id):
        with self.client.login_as_owner() as owner:
            close_ticket = owner.put("/api/v1/tickets/" + str(ticket_id) + ".json", {
                'ticket': {
                    'state' : 'closed'
                }})
    
    def add_to_article_uses(self, ticket_id):
        with self.client.login_as_owner() as owner:
            update_article = owner.put("/api/v1/articles/" + str(article_id) + ".json", {
                'article': {
                    'uses' : article['uses']+1
                }})
    
    

class Articles(Authentication):
    def __init__(self, subdomain, api_key, api_secret):
        super(Articles, self).__init__(subdomain, api_key, api_secret)
        self.all_articles = self.set_all_articles()
        #Current_article is set to the first key in the self.all_articles list by default.
        self.current_article = self.all_articles.iterkeys().next()
    
    def retrieve_article_title(self):
        return self.current_article['title']
        
    def retrieve_article_body(self):
        return self.current_article['formatted_text']
    
    # Raw articles are differ from the list of all article in that they have not been editing of their HTML tags. Raw articles are already formatted for sending the reposnse to the user and should therefore be used in place or self.all_articles when responding to users.
    def get_raw_articles(self):
        raw_articles = {}
        articles = self.client.get_collection('/api/v1/articles.json?filter=all')
        for article in articles:
            raw_articles[article['id']] = {'title':article['title'], 'formatted_text':article['formatted_text'], 'uses':article['uses'], 'text': article['text']}
        return raw_articles
        
    def set_all_articles(self):
        all_articles = {}
        articles = self.client.get_collection('/api/v1/articles.json?filter=all')
        for article in articles:
            all_articles[article['id']] = {'title':article['title'], 'formatted_text':article['formatted_text'], 'uses':article['uses'], 'text':self.formatting(article['text'])}
        return all_articles
    
    def set_current_article(self, article_number):
        self.current_article = self.all_articles[article_number]
        
    def record_use(self):
        self.current_article['uses'] = self.current_article['uses'] + 1
    
    #formatting is only used for diplay purposes on the client and does not affect the response that is sent to the user.
    def formatting(self, text):
        return text.encode('ascii', 'ignore').replace('&nbsp;', ' ').replace("'", "").replace('\n', '')
    
    
    
    