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


REPLACEMENT = u"\ufffd"


def int_to_bytes(number: int) -> bytes:
    return number.to_bytes(length=(8 + (number + (number < 0)).bit_length()) // 8, byteorder='big', signed=True)


def decode_safe(data: int) -> str:
    data = int_to_bytes(data)
    return re.sub('[\0-\7]', REPLACEMENT, data.decode(errors="replace"))


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
        text: str = "".join(filter(lambda c: c in string.digits, text))
        edited_field.update(value=text, move_cursor_to=None)

        if event == "message_data":
            number = int(text) if text.strip() else 0
            message_text.update(value=decode_safe(number))
    elif event == "message_text":
        message_data.update(value=int.from_bytes(
            message_text.get().encode(), byteorder="big"))
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
        try:
            n = fetch_value("n")
            e = fetch_value("e")
        except ValueError as e:
            sg.Popup(f"недопустимое значение {e.args[0]}")
            continue

        text = message_data.get()

        number = int(text)

        if number >= n:
            sg.Popup(
                "недопустимое значение: численное представление ввода больше значения модуля")
            continue

        encrypted = encrypt(number, PublicKey(n, e))

        cypher_data.update(value=encrypted)

    elif event == "decrypt":
        try:
            d = fetch_value("d")
            n = fetch_value("n")
        except ValueError as e:
            sg.Popup(f"недопустимое значение {e.args[0]}")
            continue

        text = cypher_data.get()

        data = int(cypher_data.get()) if text.strip() else 0

        if data >= n:
            sg.Popup(
                "недопустимое значение: некоторые значения ввода больше значения модуля")
            continue

        decrypted = decrypt(data, PrivateKey(n, d))

        message_data.update(value=decrypted)
        message_text.update(value=decode_safe(decrypted))
