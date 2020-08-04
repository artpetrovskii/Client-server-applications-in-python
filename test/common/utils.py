import json
import sys
from common.variables import MAX_PACKAGE_LENGTH, ENCODING
from errors import IncorrectDataReceived, NoDictInput
from decos import log
sys.path.append('../')


@log
def get_message(client):
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise IncorrectDataReceived
    raise IncorrectDataReceived

@log
def send_message(sock, message):
    if not isinstance(message, dict):
        raise NoDictInput
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
