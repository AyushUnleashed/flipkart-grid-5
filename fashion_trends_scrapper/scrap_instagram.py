import os
import requests
from dotenv import find_dotenv, load_dotenv
# Load environment variables from the root .env file
root_env_path = find_dotenv()
load_dotenv(root_env_path)
def save_image(url, directory, filename):
    response = requests.get(url)
    if response.status_code == 200:
        filepath = os.path.join(directory, filename)
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"Image saved as {filename}")
    else:
        print(f"Failed to download image {filename}")

def get_top_media_with_captions(user_id, access_token):
    base_url = "https://graph.facebook.com"
    endpoint = f"/{user_id}/top_media"

    params = {
        "fields": "id,media_type,caption,media_url",
        "access_token": access_token
    }

    response = requests.get(base_url + endpoint, params=params)

    if response.status_code == 200:
        data = response.json().get("data", [])
        return data
    else:
        print("Error fetching data")
        return []

if __name__ == "__main__":
    # Replace these with your actual user ID and access token
    USER_ID = os.getenv("USER_ID")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    SAVE_DIRECTORY = "scrapped_images"

    top_media_with_captions = get_top_media_with_captions(USER_ID, ACCESS_TOKEN)

    if not os.path.exists(SAVE_DIRECTORY):
        os.makedirs(SAVE_DIRECTORY)

    for media in top_media_with_captions[:10]:  # Limit to top 10
        media_id = media.get("id")
        media_type = media.get("media_type")
        caption = media.get("caption", "No caption available")
        media_url = media.get("media_url")

        print("Media ID:", media_id)
        print("Media Type:", media_type)
        print("Caption:", caption)
        print("Media URL:", media_url)
        print("=" * 30)

        if media_url and media_type == "IMAGE":
            filename = f"{media_id}.jpg"
            save_image(media_url, SAVE_DIRECTORY, filename)