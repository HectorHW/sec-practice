import re
from typing import Iterable, List
import PySimpleGUI as sg
import string
from rsa_alg import PrivateKey, PublicKey, encrypt, decrypt, generate_keypair

bitness_text = sg.Text("bitness")
bitness_field = sg.InputText(enable_events=True, key="bitness", size=(6, 1))

generate = sg.Button("generate", key="generate")

e_text = sg.Text("e")
e_field = sg.InputText(enable_events=True, key="e")

n_text = sg.Text("n")
n_field = sg.InputText(enable_events=True, key="n")

d_text = sg.Text("d")
d_field = sg.InputText(enable_events=True, key="d")


message_text = sg.InputText(enable_events=True, key="message_text")
message_data = sg.InputText(enable_events=True, key="message_data")

encrypt_bttn = sg.Button("encrypt", key="encrypt")
decrypt_bttn = sg.Button("decrypt", key="decrypt")

cypher_data = sg.InputText(enable_events=True, key="cypher_data")


layout = [
    [bitness_text, bitness_field, generate],
    [e_text, e_field],
    [n_text, n_field],
    [d_text, d_field],

    [sg.HorizontalSeparator()],

    [sg.Text("text")],

    [message_text],
    [message_data],

    [encrypt_bttn, decrypt_bttn],

    [cypher_data]
]

window = sg.Window('RSA', layout, font=("Consolas", 16),
                   resizable=True, size=(800, 400))

digits_and_space = string.digits + " "

REPLACEMENT = u"\ufffd"


def decode_symbol_safe(data: int) -> str:
    try:
        return re.sub('[\0-\7]', REPLACEMENT, chr(data))
    except ValueError:
        return REPLACEMENT


def decode_safe(data: Iterable[int]) -> str:
    return "".join(map(decode_symbol_safe, data))


def fetch_value(ptr: str) -> int:
    try:
        return int(globals()[ptr+"_field"].get())
    except ValueError:
        raise ValueError(ptr)


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    elif event.endswith("_data"):
        edited_field = globals()[event]
        text = edited_field.get()
        text: str = "".join(filter(lambda c: c in digits_and_space, text))
        edited_field.update(value=text, move_cursor_to=None)

        if event == "message_data":
            numbers = map(int, re.split(r"\s+", text.strip())
                          ) if text.strip() else []

            message_text.update(value=decode_safe(numbers))
    elif event == "message_text":
        message_data.update(value=" ".join(
            map(str, map(ord, message_text.get()))))
    elif event in ["bitness", "e", "n", "d"]:
        edited_field = globals()[event+"_field"]
        text = edited_field.get()
        text: str = "".join(filter(lambda c: c in string.digits, text))
        edited_field.update(value=text, move_cursor_to=None)

    elif event == "generate":
        try:
            bitness = int(bitness_field.get())
        except ValueError:
            sg.Popup("недопустимое значение в поле размера")
            continue
        if bitness < 4:
            sg.Popup("слишком маленькая длина")
            continue
        data = generate_keypair(primes_size=bitness)
        keypair = data.keypair
        e_field.update(value=keypair.public.e)
        n_field.update(value=keypair.public.n)
        d_field.update(value=keypair.private.d)

    elif event == "encrypt":
        print("encrypt")
        try:
            n = fetch_value("n")
            e = fetch_value("e")
        except ValueError as e:
            sg.Popup(f"недопустимое значение {e.args[0]}")
            continue

        text = message_data.get()

        numbers = list(map(int, re.split(r"\s+", text.strip())
                           )) if text.strip() else []

        if any(num >= n for num in numbers):
            sg.Popup(
                "недопустимое значение: некоторые значения ввода больше значения модуля")
            continue

        encrypted = [encrypt(data, PublicKey(n, e)) for data in numbers]

        cypher_data.update(value=" ".join(map(str, encrypted)))

    elif event == "decrypt":
        try:
            d = fetch_value("d")
            n = fetch_value("n")
        except ValueError as e:
            sg.Popup(f"недопустимое значение {e.args[0]}")
            continue

        text = cypher_data.get()

        numbers = list(map(int, re.split(r"\s+", text.strip())
                           )) if text.strip() else []

        if any(num >= n for num in numbers):
            sg.Popup(
                "недопустимое значение: некоторые значения ввода больше значения модуля")
            continue

        decrypted = [decrypt(data, PrivateKey(n, d)) for data in numbers]

        message_data.update(value=" ".join(map(str, decrypted)))
        message_text.update(value=decode_safe(decrypted))
