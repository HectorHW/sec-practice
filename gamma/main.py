import re
from typing import List
import PySimpleGUI as sg
from encryption import encrypt, generate_key
from textwrap import wrap

LANGUAGE_KEY = "language"
ENCODE_KEY = "encode"
DECODE_KEY = "decode"


input_field = sg.InputText(
    expand_x=True, tooltip="текст", enable_events=True, key='input_field')
input_bytes = sg.InputText(
    expand_x=True, tooltip="текст (байтики)", enable_events=True, key='input_bytes'
)
input_area = sg.Column([[input_field], [input_bytes]], expand_x=True)


output_field = sg.InputText(
    expand_x=True, tooltip="шифротекст", enable_events=True, key='output_field')
output_bytes = sg.InputText(
    expand_x=True, tooltip="шифротекст (байтики)", enable_events=True, key='output_bytes'
)
output_area = sg.Column([[output_field], [output_bytes]], expand_x=True)


key_field = sg.InputText(size=(20, 1), default_text="",
                         tooltip="ключ",
                         enable_events=True, key='key_field')
key_bytes = sg.InputText(size=(15, 1), expand_x=True,
                         tooltip="ключ (байтики)",
                         enable_events=True, key='key_bytes')
offset_text = sg.Text("ключ")

generate_button = sg.Button("сгенерировать", key='gen_key')

key_area = sg.Column([
    [offset_text, key_field, generate_button],
    [key_bytes]
], expand_x=True)


encode_button = sg.Button(button_text="Зашифровать", key=ENCODE_KEY)
decode_button = sg.Button(button_text="Расшифровать", key=DECODE_KEY)


buttons = sg.Column(
    [[encode_button, decode_button]]
)

layout = [[key_area],
          [sg.HorizontalSeparator()],
          [input_area],
          [buttons],
          [output_area]
          ]

window = sg.Window('Гаммирование', layout, font=("Consolas", 16),
                   resizable=True, size=(800, 400))


def bit_string(data: bytes) -> str:
    return "".join(map(lambda item: format(item, '08b'), data))


def bits_to_bytes(data: str) -> bytes:
    """
    note: extra digits will be cut off
    """
    if any(letter for letter in data if letter not in ['0', '1']):
        raise ValueError

    result = []

    for word in wrap(data, 8):
        if len(word) < 8:
            break
        result.append(int(word, 2).to_bytes(1, byteorder='little'))
    return b"".join(result)


def prettify_error_list(letters: List[str]) -> str:
    if len(letters) <= 3:
        return ", ".join(letters)
    return ", ".join(letters[:3]) + "..."


def update_from_bytes(field_bytes_name: str):
    edited_field = globals()[field_bytes_name]
    matching_field = globals()[field_bytes_name.replace("bytes", "field")]
    matching_field.update(
        value=decode_safe(bits_to_bytes(
            edited_field.get()))
    )


REPLACEMENT = u"\ufffd"


def decode_safe(data: bytes) -> str:
    return re.sub('[\0-\7]', REPLACEMENT, data.decode(errors='replace'))


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break

    elif event == ENCODE_KEY:

        key = key_bytes.get()
        message = input_bytes.get()

        coded = encrypt(message, key)
        output_bytes.update(value=coded)
        update_from_bytes("output_bytes")
    elif event == DECODE_KEY:
        key = key_bytes.get()
        message = output_bytes.get()

        coded = encrypt(message, key)
        input_bytes.update(value=coded)
        update_from_bytes("input_bytes")

    elif event.endswith('field'):
        matching_field = globals()[event.replace("field", "bytes")]
        matching_field.update(
            value=bit_string(values[event].encode())
        )

    elif event.endswith('bytes'):
        edited_field = globals()[event]
        text = edited_field.get()
        text = "".join(filter(lambda c: c in ['0', '1'], text))
        edited_field.update(value=text, move_cursor_to=None)

        matching_field = globals()[event.replace("bytes", "field")]
        matching_field.update(
            value=update_from_bytes(event)
        )

    elif event == "gen_key":
        key_bytes.update(value=generate_key(len(input_bytes.get())))
        update_from_bytes("key_bytes")


window.close()
