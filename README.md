# Clash Design Anonymous Feedback Bot — Vercel Edition

This is the Vercel HTTP Interactions version of the supplied Discord feedback bot.
It does not run a persistent `discord.py` gateway process.

## Features
- Persistent Discord message button: **Leave Review**
- Modal with required review text and optional image upload
- Publishes the review and image in the configured public feedback channel
- Public post does not include the submitter's username, tag, avatar, ID, or mention
- Slash command `/setup_feedback` posts the panel

## Project layout
```text
api/
  interactions.py
register_commands.py
requirements.txt
vercel.json
.python-version
.env.example
README.md
```

## 1. Create / configure the Discord application
1. Open https://discord.com/developers/applications
2. Select your bot application.
3. Under **General Information**, copy:
   - Application ID
   - Public Key
4. Under **Bot**, copy/reset the bot token. Keep it private.
5. Invite the bot to your server with the `bot` and `applications.commands` scopes.
6. Give it these permissions in both panel and feedback channels:
   - View Channel
   - Send Messages
   - Embed Links
   - Attach Files
   - Read Message History

## 2. Deploy to Vercel
1. Extract this ZIP.
2. Upload the extracted project to a new GitHub repository, or import the folder using Vercel.
3. In Vercel, create a new project and import the repository.
4. Add the environment variables below under **Project → Settings → Environment Variables**.
5. Deploy the project.

Required Vercel environment variables:
- `DISCORD_PUBLIC_KEY` — from Discord Developer Portal → General Information
- `DISCORD_BOT_TOKEN` — from Discord Developer Portal → Bot
- `DISCORD_APPLICATION_ID` — Application ID
- `GUILD_ID` — your Discord server ID
- `PANEL_CHANNEL_ID` — channel where the Leave Review panel should appear
- `FEEDBACK_CHANNEL_ID` — public channel where reviews should be posted
- `BRAND_NAME` — Clash Design

After deployment, your interaction endpoint will be:
`https://YOUR-VERCEL-DOMAIN.vercel.app/api/interactions`

## 3. Set the Discord Interactions Endpoint URL
1. Return to Discord Developer Portal → your application → **General Information**.
2. Paste the Vercel endpoint URL into **Interactions Endpoint URL**.
3. Save. Discord sends a PING to validate the endpoint.
4. If Discord accepts it, the endpoint is connected.

## 4. Register `/setup_feedback`
Run this once from your computer after setting `DISCORD_BOT_TOKEN`, `DISCORD_APPLICATION_ID`, and `GUILD_ID` in your local environment:

```bash
pip install -r requirements.txt
python register_commands.py
```

Windows PowerShell example:
```powershell
$env:DISCORD_BOT_TOKEN="YOUR_BOT_TOKEN"
$env:DISCORD_APPLICATION_ID="YOUR_APPLICATION_ID"
$env:GUILD_ID="YOUR_SERVER_ID"
python register_commands.py
```

Then in your Discord server, run `/setup_feedback`. The user running it must have **Manage Server** permission. The bot posts the review panel in `PANEL_CHANNEL_ID` (or the current channel if that variable is blank).

## 5. Test the flow
1. Click **Leave Review**.
2. Enter review text and optionally upload an image.
3. Submit.
4. Check the configured feedback channel.

## Privacy note
The public embed does not display the submitter's identity. Discord and the application interaction payload necessarily process the interaction, and server administrators may have other audit or platform-level visibility. A client can also identify themselves in their own review text or image. Do not promise absolute anonymity.

## Troubleshooting
- **Discord says the endpoint URL is invalid:** confirm the URL ends in `/api/interactions`, the deployment is live, and `DISCORD_PUBLIC_KEY` is correct.
- **Interaction failed:** check Vercel → Project → Logs. Confirm all environment variables are set and redeploy after changing them.
- **Panel does not post:** check `PANEL_CHANNEL_ID` and the bot's View Channel, Send Messages, and Embed Links permissions.
- **Review does not publish:** check `FEEDBACK_CHANNEL_ID` and Attach Files permission if an image is included.
- **Slash command missing:** rerun `python register_commands.py` with the correct bot token, application ID, and server ID.
- Never commit `.env` files or publish your bot token / public credentials.

## Platform note
Vercel Functions handle each Discord interaction as an HTTP request. This replaces the original always-on Discord gateway bot process and is the correct architecture for this Vercel package.
