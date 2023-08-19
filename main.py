from pydantic import BaseModel


class UserPromptInput(BaseModel):
    user_prompt: str


from pre_process_hard_filters import get_outfit_from_prompt, pre_process_filters
from fastapi import APIRouter

endpoint_router = APIRouter()

GET_OUTFIT_ENDPOINT_COUNT = 0

OUTFIT_HISTORY = []

user_purchase_csv = 'dataset/user_history_data/gwen_2.csv'

@endpoint_router.get("/reset_chat")
def reset_chat():
    global GET_OUTFIT_ENDPOINT_COUNT, OUTFIT_HISTORY
    GET_OUTFIT_ENDPOINT_COUNT = 0
    OUTFIT_HISTORY.clear()
    return {"message": "Chat reset was successful"}


@endpoint_router.post("/get_outfit")
def get_outfit(user_prompt_object: UserPromptInput):
    global GET_OUTFIT_ENDPOINT_COUNT, OUTFIT_HISTORY, user_purchase_csv
    user_prompt = user_prompt_object.user_prompt
    GET_OUTFIT_ENDPOINT_COUNT += 1

    print(GET_OUTFIT_ENDPOINT_COUNT, " time get_outfit is runnning ")
    response = None
    outfit = None
    if GET_OUTFIT_ENDPOINT_COUNT == 1:

        outfit = get_outfit_from_prompt(user_prompt, user_purchase_csv)
    else:
        prev_outfit_index = GET_OUTFIT_ENDPOINT_COUNT - 2
        from handle_change_prompt import handle_change_prompt, handle_next_prompt
        handle_change_prompt(OUTFIT_HISTORY[prev_outfit_index])  # handle 2nd prompt onwards
        outfit = handle_next_prompt(user_prompt, prev_outfit_index)

    response = {"outfit": outfit}
    OUTFIT_HISTORY.append(response)
    return response


# @endpoint_router.post("/change_outfit")
# def get_outfit(user_prompt_object: UserPromptInput):
#     user_prompt = user_prompt_object.user_prompt
#     #
#     return {"outfit": outfit}

def main(user_prompt):
    user_purchase_csv = 'dataset/user_history_data/gwen.csv'
    pinecone_filters, pinecone_queries, pinecone_queries_purchase = pre_process_filters(user_prompt, user_purchase_csv)
    print("pinecone_filters:", pinecone_filters)
    print("pinecone_queries", pinecone_queries)
    print("pinecone_queries_purchase", pinecone_queries_purchase)
    outfit = get_outfit_from_prompt(user_prompt)
    print("\noutfit is: \n", outfit)


if __name__ == "__main__":

    while True:
        user_prompt = input("Enter outfit description:")
        if (user_prompt == ""):
            print("user prompt cannot be empty\n")
            continue

        main(user_prompt=user_prompt)
