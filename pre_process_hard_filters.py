from insights.get_filters_from_insights import analyse_user_prompt_insights, analyse_user_purchase_insights
from insights.prompt_insights import get_prompt

def pre_process_filters():
    user_prompt = get_prompt()
    user_purchase_csv = 'dataset/user_history_data/gwen.csv'
    hard_filters_prompt, soft_filters_prompt = analyse_user_prompt_insights(user_prompt)
    hard_filters_purchase, soft_filters_purchase = analyse_user_purchase_insights(user_purchase_csv)