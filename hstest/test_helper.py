
def failed(message: str):
    """ Reports failure """
    lines = message.splitlines()
    print("\n#educational_plugin FAILED + " + lines[0])
    for line in lines[1:]:
        print("#educational_plugin " + line)
    return -1, message


def passed():
    """ Reports success """
    print("\n#educational_plugin test OK")
    return 0, 'test OK'
