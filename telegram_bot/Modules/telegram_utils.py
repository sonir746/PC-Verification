import requests

def get_chat_id_by_username_and_msg(bot_token, target_username, verification_msg):
    """
    Find chat ID where username matches AND message text contains verification_msg.
    """

    try:
        response = requests.get(f"https://api.telegram.org/bot{bot_token}/getUpdates")
        data = response.json()

        if not data.get("ok"):
            return f"API request failed: {data.get('description', 'Unknown error')}"

        for update in data.get("result", []):
            message = update.get("message")
            if message:
                from_user = message.get("from")
                text = message.get("text", "")
                if from_user:
                    username = from_user.get("username")
                    if username and username.lower() == target_username.lower():
                        if verification_msg.lower() in text.lower():
                            return message["chat"]["id"]

        return f"No chat found with username '{target_username}' and message containing '{verification_msg}'"

    except requests.RequestException as e:
        return f"Request failed: {str(e)}"
