import json

from duckduckgo_search import DDGS

from dialogue.dialogue_management import DialogueManagement
from home_assistant.alarm import Alarm
from home_assistant.climate import Climate
from home_assistant.home_assistant import HomeAssistant
from home_assistant.light import Light
from text_to_speech.text_to_speech_service import TextToSpeechService
from utils import utils


def __inform_user(prompt, text):
    result = __invoke_chat_gpt_to_response(prompt=prompt, text=text)
    text_to_speech_service = TextToSpeechService()
    text_to_speech_service.play_audio_from_text(result)


def search_online(user_query):
    results = DDGS().news(keywords=user_query, region="it-it", max_results=5, safesearch="off")
    final_result = []

    for result in results:
        final_result.append({"description": result['body']})

    return __invoke_chat_gpt_to_response(
        f"you have to extract all the descriptions, clean the text  and give me a discursive summary. Max 20 words",
        str(final_result))


def get_devices_state(device=None, all=False):
    ha = HomeAssistant()
    states = ha.get_my_states()

    text = "Can you give me the status?" if all is True else f"Can you give me the information relating to the following device? Device: {device}"

    return __invoke_chat_gpt_to_response(
        prompt=f'You are an vocal assistant. You must create a sentence. You have to interpret the json: {str(states)}',
        text=text)


def home_assistant(device, device_name=None, all=None, action=None, location=None, color=None):
    if device_name is None:
        device_name = ''

    ha = HomeAssistant()
    states = ha.get_my_states()
    result = utils.filter_device(states, device, device_name)

    device_name += f' {location}' if device_name is not None else f' {location}'

    __inform_user(
        prompt=f"You are a voice assistant who must inform the user that the {device} are about to be {action} ",
        text="Inform the user!")

    chat_gtp_response = __invoke_chat_gpt_to_response(
        prompt=f'These are all device: {str(states)}. In input you receive the name or the device. You must recognize the entity_id variable. You need to respond with json with key result: <entity_id>.',
        text=f'name: {device_name} and device: {device}',
        response_json=True
    )

    if len(result) > 1 and all is False:
        return __invoke_chat_gpt_to_response(
            prompt="You must inform the user that you have found matching devices. You must ask him the exact name of the device he wants to operate",
            text="There are many devices!")

    try:
        entity_id = chat_gtp_response['result']
    except Exception as e:
        entity_id = json.loads(chat_gtp_response)['result']

    domain = entity_id.split('.')[0]

    invoke = {
        'light': Light(home_assistant=ha, color=color),
        'alarm_control_panel': Alarm(ha),
        'climate': Climate(ha)
    }

    invoke[domain].activate(entity_id) if action == 'ON' else invoke[domain].deactivate(entity_id)

    return __invoke_chat_gpt_to_response(
        prompt="You must inform the user that the device has been turned on or turned off",
        text=f"Device is:{entity_id.split('.')[1]}   action is: {action}")


def __invoke_chat_gpt_to_response(prompt, text, response_json=False):
    new_management = DialogueManagement()
    new_management.clear()
    if prompt is not None:
        new_management.add_dialogue('system', prompt)

    new_management.add_dialogue('user', text)
    chat_gpt_answer = new_management.chat_completion(response_json=response_json)
    return chat_gpt_answer.choices[0].message.content


def handle_function(response_message):
    function_name = None
    tool_call_id = None
    response_chat_gpt = None
    tool_calls = response_message.tool_calls

    available_functions = {
        "search_online": search_online,
        "home_assistant": home_assistant,
        "get_devices_state": get_devices_state
    }

    result_responses = []

    if tool_calls:
        for tool_call in tool_calls:
            if tool_call.function.name in available_functions:
                function_args = json.loads(tool_call.function.arguments)
                function_response = available_functions[tool_call.function.name](**function_args)
                function_name = tool_call.function.name
                tool_call_id = tool_call.id
                result_responses.append(function_response)

    else:
        response_chat_gpt = response_message.content

    return response_chat_gpt, result_responses, function_name, tool_call_id
