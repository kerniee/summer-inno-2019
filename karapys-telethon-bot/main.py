from telethon import TelegramClient, events, sync

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = 930105
api_hash = 'ef4dec491716033d18d9c49bcbcb26ce'

with TelegramClient('session_name', api_id, api_hash) as client:
    #client.send_message(-394818057, '2')

    @client.on(events.NewMessage(chats=-394818057))
    async def handler(event):
        await event.respond(str(int(event.raw_text)//2))

    client.run_until_disconnected()