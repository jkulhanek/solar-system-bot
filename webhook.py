from flask import Flask
from flask_assistant import Assistant, ask, tell, request
from flask_assistant import context_manager
from dialmonkey.conversation_handler import ConversationHandler
from dialmonkey.dialogue import Dialogue
from dialmonkey.utils import load_conf
import os
import logging
import json

app = Flask(__name__)
assist = Assistant(app, route='/', project_id='solaragent-kkdkcp')
conf = load_conf(os.path.join(os.path.dirname(__file__), 'config.yaml'))
logger = logging.getLogger('flask_assistant').setLevel(logging.DEBUG) 

def serialize_dialogue(dial):
    return json.dumps(dict(dial.state))

def deserialize_dialogue(state):
    if state is None: return Dialogue()
    state = json.loads(state)

    # We cannot serialize Dialogue object nor can we set its state directly
    d = Dialogue()
    for k, v in state.items():
        d.state[k] = v
    return d

@assist.action('Default Fallback Intent')
def respond():
    context_manager.add('dialogue')
    handler = ConversationHandler(conf, logger)
    user_query = request['queryResult']['queryText']

    # restore dialogue
    dialogue = context_manager.get('dialogue').parameters.get('serialized')
    dialogue = deserialize_dialogue(dialogue)

    resp, isend = handler.get_response(dialogue, user_query)
    context_manager.set('dialogue', 'serialized', serialize_dialogue(dialogue))
    return tell(resp)
