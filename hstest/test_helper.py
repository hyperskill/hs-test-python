
def set_congratulation_message(message):
    """ Overrides default 'Congratulations!' message """
    print("#educational_plugin CONGRATS_MESSAGE " + message)


def failed(message: str):
    """ Reports failure """
    lines = message.splitlines()
    print("\n#educational_plugin FAILED + " + lines[0])
    for line in lines[1:]:
        print("#educational_plugin " + line)


def passed():
    """ Reports success """
    print("\n#educational_plugin test OK")
