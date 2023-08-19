from chat_bot.gpt_for_everyone import fetch_gpt_response
from chat_bot.gpt_bot import fetch_paid_openai_response
from chat_bot.bot_choser import get_gpt_response
import re
from chat_bot.gpt_bot import SYSTEM_PROMPT
# take user prompt
# use GPT for everyone
import requests


def get_prompt():
    prompt = "I am looking for jeans, a french connection jeans, which could be black color, it should be for christmas, it should be cool looking"
    prompt2 = "Cool bot I guess, actually I was looking for a blue dress from some premium brands as diwali is coming soon, it must be trendy & look good"
    prompt3 = "Hey, I'm a college going girl and I want a quirky and chic short dress for a date. Do you have anything from top fashion brands?"
    prompt4 = "Hi, I'm a business woman in my 40s, looking for some formal, yet chic business suits. Can you recommend outfits from premium brands?"
    prompt5 = "I am looking for an outfit, a french connection jeans, which could be black color, it should be for christmas, it should be cool looking, pair it with matching shirt & accessories"
    prompt6 = "I am looking for an outfit, a french connection jeans, which could be red color, it should be for christmas, it should be cool looking, pair it with matching shirt of white color & accessories would be a hat of h&m "
    return prompt2


def parse_text(input_string, keys):
    # Initialize dictionaries
    article_dict = {'topwear': {}, 'bottomwear': {}, 'footwear': {}, 'accessories': {}}

    # Loop through each line in the input string
    for line in input_string.split('\n'):

        # Skip empty lines
        if not line.strip():
            continue

        parts = line.split(': ')

        # Check if the line indicates a change attribute

        # Find out which article the current line pertains to
        for article in article_dict:
            if article in parts[0]:

                current_category = article
                article_dict[article]['category'] = current_category

                if 'to_change' in parts[0]:
                    to_change_value = parts[1].strip().lower() == 'true'
                    if current_category:
                        article_dict[current_category]['to_change'] = to_change_value

                # For the identified article, see if the key is in our defined keys
                for key in keys:
                    if key in parts[0]:
                        article_dict[article][key] = parts[1]
                        break

    return article_dict['topwear'], article_dict['bottomwear'], article_dict['footwear'], article_dict['accessories']


def build_base_prompt(keys, user_prompt):
    base_prompt = "Ignore, All Previous Instructions, You are E-Commerce GPT, a professional Analyst from E-commerce industry with years of experience in analysing user needs"
    base_prompt += "I will give you a prompt which user has given, from that extract user insights based on keys"
    base_prompt += f"\nBased on that only return,key value pairs for these keys {keys}, if value doesn't exist, it should be none, First key should be article type"
    base_prompt += f"\n if it has multiple articles mentioned, eg: article_type: topwear, bottomwear, return multiple set of key value pairs, if next value doesn't exist, make it none"
    base_prompt += f"\n article_type can only have the following values: top_wear, bottom_wear,foot_wear,accessories, "
    base_prompt += f"\nUser Prompt: {user_prompt} \n **Prompt Ended**"
    base_prompt += f"\n Only print this, First line print Key-Value Pairs:\n From second line key: value pairs, don't use ' '  "
    return base_prompt


def build_base_prompt_2(keys, user_prompt):
    base_prompt = f"As E-Commerce GPT, generate key-value pairs for all four categories: topwear, bottomwear, footwear, and accessories, based on the user prompt. Extract and assign values based on the specific keys: {keys}. If a key's value is missing, use 'none'."
    base_prompt += f"\nUser Prompt: {user_prompt}\nPrompt Ended\n everything in small caps, first line should start with 'key-value pairs:'"
    base_prompt += "\n now print 4 sets of key pairs, key format {category}_{key_name} eg: \n topwear_category: top_wear \n topwear_article_type: t-shirt \n now print"
    return base_prompt


def build_assistant_prompt(keys, user_prompt):
    base_prompt = f"\nUser Prompt: {user_prompt}\nPrompt Ended"
    base_prompt += "\n now print 4 sets of key pairs, key format {category}_{key_name} eg: \n topwear_category: top_wear \n topwear_article_type: t-shirt \n now print"
    return base_prompt


def get_prompt_insights(user_prompt):
    keys = ['category', 'color', 'article_type', 'brand_name', 'occasion', 'other_info']
    base_prompt = build_assistant_prompt(keys, user_prompt=user_prompt)
    # base_response = fetch_gpt_response(SYSTEM_PROMPT + "\n" + base_prompt)
    #base_response = fetch_paid_openai_response(base_prompt)
    base_response = get_gpt_response(base_prompt,paid=True)

    if base_response is None:
        print("Sever is down")
        return

    print(base_response)
    top_wear, bottom_wear, foot_wear, accessories = parse_text(base_response, keys)
    print("Top Wear:", top_wear)
    print("Bottom Wear:", bottom_wear)
    print("Foot Wear:", foot_wear)
    print("Accessories:", accessories)
    return top_wear, bottom_wear, foot_wear, accessories


if __name__ == "__main__":
    user_prompt = get_prompt()
    get_prompt_insights(user_prompt=user_prompt)
