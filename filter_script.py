def file_callback(filename, data):
    """Remove secret from all files"""
    return data.replace(b'[REMOVED]', b'[REMOVED]')

def message_callback(message):
    """Remove secret from commit messages"""
    return message.replace(b'[REMOVED]', b'[REMOVED]')
