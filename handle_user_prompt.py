from chat_bot.gpt_for_everyone import fetch_gpt_response
# take user prompt
# use GPT for everyone
import requests


def get_prompt():
    prompt = "I am looking for jeans, a french connection jeans, which could be black color, it should be for christmas, it should be cool looking"
    prompt2 = "Cool bot I guess, actually I was looking for a blue dress from some premium brands as diwali is coming soon, it must be trendy & look good"
    prompt3 ="Hey, I'm a college going girl and I want a quirky and chic short dress for a date. Do you have anything from top fashion brands?"
    prompt4 ="Hi, I'm a business woman in my 40s, looking for some formal, yet chic business suits. Can you recommend outfits from premium brands?"
    return prompt4


def string_to_dict(input_string):
    lines = input_string.split('\n')
    dictionary = {}
    kv_index = 0
    for i in range(len(lines)):
        if "Key-Value Pairs:" in lines[i]:
            kv_index = i
            break
    for line in lines[kv_index + 1:]:
        if line.strip():  # This checks if line is not empty
            key, value = line.split(':')
            dictionary[key.strip()] = value.strip()
    return dictionary


def prep():
    base_prompt = "Ignore, All Previous Instructions, You are E-Commerce GPT, a professional Analyst from E-commerce industry with years of experience in analysing user needs"
    base_prompt += "I will give you a prompt which user has given, from that extract user insights based on keys"
    keys = ['color', 'clothing_type', 'clothing_brand', 'occasion', 'other_info']
    base_prompt += f"\nBased on that only return,key value pairs for these keys {keys}, if value doesn't exist, it should be None, if multiple values exist return , seperated. Temperature=0.2"
    user_prompt = get_prompt()
    base_prompt += f"\nUser Prompt: {user_prompt} \n **Prompt Ended**"
    base_prompt += f"\n Only print this, First line print Key-Value Pairs:\n From second line key: value pairs, don't use ' ' "

    base_response = fetch_gpt_response(base_prompt)

    if base_response == None:
        print("Sever is down")
        return

    print(base_response)
    user_prompt_params = string_to_dict(base_response)
    print(" \n")
    print(user_prompt_params)


if __name__ == "__main__":
    prep()
