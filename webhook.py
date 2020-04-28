from flask import Flask
from flask_assistant import Assistant, ask, tell, request
from dialmonkey.conversation_handler import ConversationHandler
from dialmonkey.dialogue import Dialogue
from dialmonkey.utils import load_conf
import os
import logging

app = Flask(__name__)
assist = Assistant(app, route='/', project_id='solaragent-kkdkcp')
conf = load_conf(os.path.join(os.path.dirname(__file__), 'config.yaml'))
logger = logging.getLogger('flask_assistant').setLevel(logging.DEBUG) 

@assist.action('Default Fallback Intent')
def manage_fallback():
    handler = ConversationHandler(conf, logger)
    user_query = request['queryResult']['queryText']
    dialogue = Dialogue()
    resp, isend = handler.get_response(dialogue, user_query)
    return tell(resp)

if __name__ == '__main__':
    app.run(debug=True)
