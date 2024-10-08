import requests

def send_discord_notify(message, webhook_url):
    data = {
        'content': message
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("ส่งแจ้งเตือนสำเร็จ")
    else:
        print("การแจ้งเตือนล้มเหลว:", response.text)