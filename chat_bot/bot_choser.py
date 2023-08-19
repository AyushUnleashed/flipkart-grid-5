from chat_bot.gpt_bot import fetch_paid_openai_response
from chat_bot.gpt_for_everyone import fetch_gpt_response



def get_gpt_response(user_prompt, paid):
    try:
        if paid:
            response = fetch_paid_openai_response(user_prompt)
        else:
            response = fetch_gpt_response(user_prompt)

        return response

    except Exception as e:
        return f"An error of type {type(e).__name__} occurred: {str(e)}"