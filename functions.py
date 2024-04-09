import json

import requests
from duckduckgo_search import DDGS

import utils
from dialogue_management import DialogueManagement
from home_assistant.home_assistant import HomeAssistant
from home_assistant.light import Light
from text_to_speech_service import TextToSpeechService, ServiceType


def search_online(user_query):
    results = DDGS().news(keywords=user_query, region="it-it", max_results=5, safesearch="off")
    final_result = []

    for result in results:
        final_result.append({"description": result['body']})

    return __invoke_chat_gpt_to_response(
        f"you have to extract all the descriptions, clean the text  and give me a discursive summary. Max 20 words",
        str(final_result))


def home_assistant(device, device_name, all=None, action=None):
    ha = HomeAssistant()
    states = ha.get_my_states()
    result = utils.filter_device(states, device, device_name)

    chat_gtp_response = __invoke_chat_gpt_to_response(
        prompt=f'These are all device: {str(states)}. In input you receive the name and the device. You need to figure out which ones are in the json. You need to respond with json with key result: <entity_id>.',
        text=f'name: {device_name} and device: {device}')

    response_chat_gpt = json.loads(chat_gtp_response)

    if len(result) > 1 and all is False:
        return __invoke_chat_gpt_to_response(
            prompt="You must inform the user that you have found matching devices. You must ask him the exact name of the device he wants to operate",
            text="There are many devices!")

    entity_id = response_chat_gpt['result']
    domain = entity_id.split('.')[0]

    invoke = {
        'light': Light(ha)
    }

    invoke[domain].activate(entity_id) if action == 'ON' else invoke[domain].deactivate(entity_id)

    return __invoke_chat_gpt_to_response(
        prompt="You must inform the user that the device has been turned on or turned off",
        text=f"Device is:{response_chat_gpt['result'].split('.')[1]}   action is: {action}")


def get_exchange(amount, currency_from, currency_to):
    response = requests.get("https://open.er-api.com/v6/latest/" + currency_from)
    exchange_rate = response.json()["rates"][currency_to]
    result = amount * exchange_rate
    result = round(result, 2)
    return __invoke_chat_gpt_to_response(
        prompt="You need to generate a phrase for this currency exchange",
        text=f"amount:{amount} currency_from{currency_from} currency_to:{currency_to} result_conversion:{result} ")


def __invoke_chat_gpt_to_response(prompt, text):
    new_management = DialogueManagement()
    new_management.clear()
    if prompt is not None:
        new_management.add_dialogue('system', prompt)

    new_management.add_dialogue('user', text)
    chat_gpt_answer = new_management.chat_completion()
    return chat_gpt_answer.choices[0].message.content


def fun_voice():
    response = __invoke_chat_gpt_to_response(prompt=None, text='Generate a funny sentence with 10 words!')
    tts_service = TextToSpeechService(service=ServiceType.FUN_VOICE)
    tts_service.play_audio_from_text(response)
    TextToSpeechService.play = False
    return response


def handle_function(response_message):
    function_response = None
    function_name = None
    tool_call_id = None
    response_chat_gpt = None
    tool_calls = response_message.tool_calls

    available_functions = {
        "get_currency_exchange": get_exchange,
        "fun_voice": fun_voice,
        "search_online": search_online,
        "home_assistant": home_assistant
    }

    if tool_calls:
        for tool_call in tool_calls:
            if tool_call.function.name in available_functions:
                function_args = json.loads(tool_call.function.arguments)
                function_response = available_functions[tool_call.function.name](**function_args)
                function_name = tool_call.function.name
                tool_call_id = tool_call.id
            break
    else:
        response_chat_gpt = response_message.content

    return response_chat_gpt, function_response, function_name, tool_call_id
