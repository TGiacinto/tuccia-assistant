import json
import os

import requests

import api_client
from dialogue_management import DialogueManagement
from text_to_speech_service import TextToSpeechService, ServiceType


def get_exchange(amount, currency_from, currency_to):
    response = requests.get("https://open.er-api.com/v6/latest/" + currency_from)
    exchange_rate = response.json()["rates"][currency_to]
    result = amount * exchange_rate
    return f"Sono: {result} {currency_to}"


def fun_voice():
    new_management = DialogueManagement()
    new_management.clear()
    new_management.add_dialogue('user', 'Genera una frase divertente in italiano!')
    chat_gpt_answer = new_management.chat_completion()
    c = TextToSpeechService(service=ServiceType.FUN_VOICE)
    c.play_audio_from_text(chat_gpt_answer.choices[0].message.content)
    TextToSpeechService.play = False
    return chat_gpt_answer.choices[0].message.content


def get_weather_api(city):
    api_key = os.getenv("WEATHER_API_KEY")
    method = "get"
    url = "http://api.weatherapi.com/v1/current.json"
    params = {"q": city, "aqi": "no", "key": api_key, "lang": "it"}

    result = api_client.perform_request(method, url, params=params)
    new_management = DialogueManagement()
    new_management.clear()
    new_management.add_dialogue('system',
                                'Devi interpretare un json relativo al meteo e generare una frase di senso compiuto di massimo 30 parole')
    new_management.add_dialogue('user', str(result.content))
    chat_gpt_answer = new_management.chat_completion()
    return chat_gpt_answer.choices[0].message.content


def handle_function(response_message):
    function_response = None
    function_name = None
    tool_call_id = None
    response_chat_gpt = None
    tool_calls = response_message.tool_calls

    available_functions = {
        "get_currency_exchange": get_exchange,
        "get_weather_api": get_weather_api,
        "fun_voice": fun_voice

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
