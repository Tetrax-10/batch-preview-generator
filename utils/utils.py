import os


def wrap_text(text):
    available_length = os.get_terminal_size().columns - 42
    if len(text) > available_length:
        half_value = (available_length - 3) // 2
        text = text[:half_value] + "..." + text[-half_value:]

    text = text + " " * (available_length - len(text))

    return text
