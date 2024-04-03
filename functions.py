import json
import os

import requests
from googlesearch import search

import api_client
from dialogue_management import DialogueManagement
from text_to_speech_service import TextToSpeechService, ServiceType


def search_online(user_query):
    results = search(user_query, lang="it", advanced=True, num_results=5)

    final_result = []
    for result in results:
        final_result.append({"description": result.description})
        final_result.append({"url": result.description})

    return __invoke_chat_gpt_to_response(
        f"you have to extract all the descriptions, and give me a discursive summary.", str(final_result))


def get_exchange(amount, currency_from, currency_to):
    response = requests.get("https://open.er-api.com/v6/latest/" + currency_from)
    exchange_rate = response.json()["rates"][currency_to]
    result = amount * exchange_rate
    result = round(result, 2)
    return __invoke_chat_gpt_to_response(
        prompt=None,
        text=f"You need to generate a phrase for this currency exchange: amount:{amount} currency_from{currency_from} currency_to:{currency_to} result_conversion:{result} ")


def __invoke_chat_gpt_to_response(prompt, text):
    new_management = DialogueManagement()
    new_management.clear()
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


def get_weather_api(city):
    api_key = os.getenv("WEATHER_API_KEY")
    method = "get"
    url = "http://api.weatherapi.com/v1/current.json"
    params = {"q": city, "aqi": "no", "key": api_key, "lang": "it"}

    result = api_client.perform_request(method, url, params=params)
    return __invoke_chat_gpt_to_response(
        f"You must interpret a json related to the weather and generate a meaningful sentence of maximum 30 words.",
        f' The json file is: {result.content}')


def handle_function(response_message):
    function_response = None
    function_name = None
    tool_call_id = None
    response_chat_gpt = None
    tool_calls = response_message.tool_calls

    available_functions = {
        "get_currency_exchange": get_exchange,
        "get_weather_api": get_weather_api,
        "fun_voice": fun_voice,
        "search_online": search_online

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
