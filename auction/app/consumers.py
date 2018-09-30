from channels import Group

# Connect to websocket.connect
def ws_add(message):
    Group("").add(message.reply_channel)
s
# Connect to websocket.receive
def ws_message(message):
    pass


# Connect to websocket.disconnect
def ws_disconnect(message):
    Group("").discard(message.reply_channel)