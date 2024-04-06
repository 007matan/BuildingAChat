class MessageProtocol:
    HEADER_LENGTH = 5  # max message length 99999
    CHARS_IN_ROW = 30  # amount of chars in each row in chat
    PROTOCOL_ERR = "PROTOCOL_ERR"  # error sign from the protocol
    SYS_MSG = "SYS_MSG"  # signing messages from the system

    """
           Encodes a message by adding a header that contains the message's length.
           The function receive as parameter: message - The original message to encode.
           The function return: The encoded message with a header.
    """
    @staticmethod
    def encode(message: str) -> str:
        header = f"{len(message):0{MessageProtocol.HEADER_LENGTH}}"
        return f"{header}{message}"

    """
    Decodes a message by removing the header and validating the message length.
    The function receive as parameter: encoded_message - The encoded message with the header.
    The function return: The original message if valid; otherwise, an empty string.
    In addition, we had to differentiate between system messages and client messages
    , so we added, hidden from the client's view, an extra prefix to a system message.
     To avoid cases of messages from clients being distributed as if they came from the system itself.
    """
    @staticmethod
    def decode(encoded_message: str) -> str:
        prefix_space = encoded_message.split(" ", 1)[0]
        suffix_space = encoded_message.split(" ", 1)[1]
        if prefix_space != MessageProtocol.SYS_MSG:
            header = suffix_space[:MessageProtocol.HEADER_LENGTH]
            message = suffix_space[MessageProtocol.HEADER_LENGTH:]
            if len(message) == int(header):
                return prefix_space + " " + message
            else:
                return MessageProtocol.PROTOCOL_ERR
        else:
            return suffix_space


    """
    @staticmethod
    def splitLines(message: str) -> str:
        words = message.split()
        lines = []
        current_line = words.pop(0)
        for word in words:
            if len(current_line) + len(word) + 1 <= MessageProtocol.CHARS_IN_ROW:
                current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return '\n'.join(lines)
    """