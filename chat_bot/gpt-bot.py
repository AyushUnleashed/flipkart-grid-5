import openai

SYSTEM_PROMPT = '''
You are an AI assistant. 
You will answer the question as truthfully as possible.
If you're unsure of the answer, say Sorry, I don't know.
'''

OPEN_AI_API_KEY = "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"
openai.api_key = OPEN_AI_API_KEY
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

def run_bot():
    # system_prompt()
    chat_bot()

run_bot()
