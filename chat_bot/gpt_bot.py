import os

import openai

SYSTEM_PROMPT = '''
You are an AI assistant. 
You will answer the question as truthfully as possible.
If you're unsure of the answer, say Sorry, I don't know.
'''

from dotenv import find_dotenv,load_dotenv
# Load environment variables from the root .env file
root_env_path = find_dotenv()
load_dotenv(root_env_path)

openai.api_key = os.getenv("OPEN_AI_API_KEY")
def process_message(message):
    message_text = message['text']
    return message_text

messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
]

# def system_prompt():
#     global messages
#     try:
#         openai_response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#
#         )
#         print(openai_response)
#     except Exception as e:
#         print("Exception occurred", e)


def chat_bot():
    global messages
    try:
        while True:
            user_prompt = input("User:")
            if user_prompt:
                messages.append(
                    {"role": "user", "content": user_prompt},
                )

            openai_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                ]
            )

            reply = openai_response.choices[0].message.content
            completion_tokens = openai_response.usage.completion_tokens
            prompt_tokens = openai_response.usage.prompt_tokens
            total_tokens = openai_response.usage.total_tokens
            print("ChatGPT reply: ", reply)
            print("completion_tokens", completion_tokens)
            print("prompt_tokens", prompt_tokens)
            print("total_tokens", total_tokens)
            messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        print("Exception occurred", e)


def fetch_paid_openai_response(user_prompt: str):
    try:
        chat_history = [{"role": "system", "content": user_prompt}]
        print("Waiting for Paid open ai response")
        openai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history
        )

        reply = openai_response.choices[0].message.content
        completion_tokens = openai_response.usage.completion_tokens
        prompt_tokens = openai_response.usage.prompt_tokens
        total_tokens = openai_response.usage.total_tokens
        print("OpenAi Paid API reply: ", reply)
        print("completion_tokens", completion_tokens)
        print("prompt_tokens", prompt_tokens)
        print("total_tokens", total_tokens)
        chat_history.append({"role": "assistant", "content": reply})
        print("wait over")
        return reply
    except Exception as e:
        print("Exception occurred while fetching response from openai", e)
        return None


def run_bot():
    # system_prompt()
    chat_bot()

if __name__ == "__main__":
    run_bot()
