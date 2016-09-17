# -*- coding: utf-8 -*-
import json, urllib
from flask import Flask, request, abort
import requests
import config

app = Flask(__name__)

access_token = config.FACEBOOK_SECRET_KEY


@app.route("/", methods=["GET"])
def root():
  return "Hello World!"


# webhook for facebook to initialize the bot
@app.route('/webhook', methods=['GET'])
def get_webhook():
  if not 'hub.verify_token' in request.args or not 'hub.challenge' in request.args:
    abort(400)

  return request.args.get('hub.challenge')


@app.route('/webhook', methods=['POST'])
def post_webhook():
  data = request.json

  if data["object"] == "page":
    for entry in data['entry']:
      for messaging_event in entry['messaging']:

        if "message" in messaging_event:

          sender_id = messaging_event['sender']['id'] #sender id of person sending the message
          recipient_id = messaging_event["recipient"]["id"] #recipient id (facebook page id)

          if 'text' in messaging_event['message']:
            message_text = messaging_event['message']['text']
            #image = "http://cdn.shopify.com/s/files/1/0080/8372/products/tattly_jen_mussari_hello_script_web_design_01_grande.jpg"
            #element = create_generic_template_element("Hello", image, message_text)
            #reply_with_generic_template(sender_id, [element])
            welcome(sender_id, message_text)
            #reply(sender_id, 'Hello there!')

  return "ok", 200

def get_url(url):
    result = request.get(url)
    return json.loads(result.content)


def welcome(recipient_id, message_text):
    rules = {
        "hello": "hello",
        "hi": "Hi there and welcome to the Hotel am Brillantengrund. I can check if rooms are available and give you advice for daily activities.",
        "get started": "Hi there and welcome to the Hotel am Brillantengrund. I can check if rooms are available and give you advice for daily activities."
        #"Foo": "Bar"
    }

    if message_text in rules:
      reply_with_buttons(recipient_id)
        
    else:
        reply_with_text(recipient_id, "I'm sorry, I don't understand you. Click the button below to get started!")
        #get_started(recipient_id, )
    


def reply_with_text(recipient_id, message_text):
    message = {
        "text": message_text
    }
    reply_to_facebook(recipient_id, message)

def reply_with_buttons(recipient_id):
  message = {
    "attachment": {
      "type": "template",
      "payload": {
        "template_type": "button",
        "text": "Hi there and welcome to the Hotel am Brillantengrund. I can check if rooms are available and give you advice for daily activities.",
        "buttons":[
            {
              "type": "postback",
              "title": "Room Availability",
              "payload": "ROOM_AVAILABILITY"
            },
            {
              "type":"postback",
              "title":"Daily Tip",
              "payload":"DAILY_TIP"
            }
          ]
      }
    }
  }
  reply_to_facebook(recipient_id, message)
  #received_postback(sender_id, message)


def reply_with_generic_template(recipient_id, elements):
    message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": elements
            }
        }
    }
    reply_to_facebook(recipient_id, message)


def reply_to_facebook(recipient_id, message):
    params = {
        "access_token": access_token
    }

    headers = {
        "Content-Type": "application/json"
    }

    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": message
    })

    print data

    url = "https://graph.facebook.com/v2.6/me/messages?" + urllib.urlencode(params)
    r = requests.post(url=url, headers=headers, data=data)

    #print r.content

def create_generic_template_element(title, image_url, subtitle):
    return {
        "title": title,
        "image_url": image_url,
        "subtitle": subtitle
    }
