def text2binary(text):
    """
    Converts the input text to binary format.

    Args:
        text (str): The input text to be converted.

    Returns:
        str: The binary representation of the input text.
    """
    # Convert each character in the text to its binary representation
    binary_list = [format(ord(c), '08b') for c in text]

    # Join the binary representations together to form a binary string
    binary_string = ''.join(binary_list)

    return binary_string


def binary2text(binary_string):
    """
    Converts the input binary string to text format.

    Args:
        binary_string (str): The binary string to be converted.

    Returns:
        str: The converted text.
    """
    text_back = ''
    # Iterate over the binary string in chunks of 8 characters
    for i in range(0, len(binary_string), 8):
        # Get the next 8 characters
        byte = binary_string[i:i + 8]
        # Convert the binary byte to its corresponding character and append it to the text
        text_back += chr(int(byte, 2))

    return text_back
