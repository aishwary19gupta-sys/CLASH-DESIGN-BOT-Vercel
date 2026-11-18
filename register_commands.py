"""Register /setup_feedback as a guild slash command."""
import os
import requests

token = os.environ["DISCORD_BOT_TOKEN"].strip()
application_id = os.environ["DISCORD_APPLICATION_ID"].strip()
guild_id = os.environ["GUILD_ID"].strip()

url = f"https://discord.com/api/v10/applications/{application_id}/guilds/{guild_id}/commands"
payload = [{
    "name": "setup_feedback",
    "description": "Post the Clash Design anonymous feedback panel",
    "default_member_permissions": "32",
    "type": 1
}]
response = requests.put(
    url,
    headers={"Authorization": f"Bot {token}", "Content-Type": "application/json"},
    json=payload,
    timeout=20
)
print("Status:", response.status_code)
print(response.text)
response.raise_for_status()
print("Slash command registered. It should appear in your server shortly.")
