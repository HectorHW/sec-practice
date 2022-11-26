import random
import re
import PySimpleGUI as sg
import string
from primes import get_random_prime, fast_power
from algo import find_primitive_root

generate = sg.Button("generate", key="generate")

g_bitness = sg.InputText(
    enable_events=True, key="g_bitness", size=(4, 1)
)

g_field = sg.InputText(
    enable_events=True, key="g_field", size=(20, 1), expand_x=True
)

p_bitness = sg.InputText(
    enable_events=True, key="p_bitness", size=(4, 1))

p_field = sg.InputText(
    enable_events=True, key="p_field", size=(20, 1), expand_x=True
)


a_field = sg.InputText(
    enable_events=True, key="a_field", size=(20, 1), expand_x=True
)

compute_button = sg.Button("compute", key="compute")

cypher_data = sg.InputText(enable_events=True, key="cypher_data")

result_field = sg.InputText(disabled=True, size=(20, 1), expand_x=True)

layout = [
    [generate],
    [sg.Text("bitness:"), g_bitness, sg.Text("g:"), g_field],
    [sg.Text("bitness:"), p_bitness, sg.Text("p:"), p_field],
    [sg.Text("a:"), a_field],
    [sg.HorizontalSeparator()],

    [compute_button],

    [sg.Text(" g ^ a mod p ="), result_field]
]

window = sg.Window('Diffie-Hellman', layout, font=("Consolas", 16),
                   resizable=True, size=(800, 600))


REPLACEMENT = u"\ufffd"


def int_to_bytes(number: int) -> bytes:
    return number.to_bytes(length=(8 + (number + (number < 0)).bit_length()) // 8, byteorder='big', signed=True)


def decode_safe(data: int) -> str:
    data = int_to_bytes(data)
    return re.sub('[\0-\7]', REPLACEMENT, data.decode(errors="replace"))


def fetch_value(ptr: str) -> int:
    try:
        return int(globals()[ptr].get())
    except ValueError:
        raise ValueError(ptr)


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break

    elif event in ["g_bitness", "g_field", "p_bitness", "p_field", "a_field"]:
        edited_field = globals()[event]
        text = edited_field.get()
        text: str = "".join(filter(lambda c: c in string.digits, text))
        edited_field.update(value=text, move_cursor_to=None)

    elif event == "generate":
        try:
            g_bitness_value = fetch_value("g_bitness")
            p_bitness_value = fetch_value("p_bitness")
        except ValueError as e:
            sg.Popup(f"недопустимое значение {e.args[0]}")
            continue
        if g_bitness_value < 4:
            sg.Popup("слишком маленькая длина g")
            continue

        if p_bitness_value < 4:
            sg.Popup("слишком маленькая длина p")
            continue

        if p_bitness_value <= g_bitness_value:
            sg.Popup("длина g должна быть меньше p")
            continue

        p = get_random_prime(p_bitness_value)

        p_field.update(value=p)

        root = find_primitive_root(g_bitness_value, p)

        g_field.update(value=root)

        a_field.update(value=random.randint(2, p-1))

    elif event == "compute":
        try:
            g = fetch_value("g_field")
            p = fetch_value("p_field")
            a = fetch_value("a_field")
        except ValueError as e:
            sg.Popup(f"недопустимое значение {e.args[0]}")
            continue

        y = fast_power(g, a, p)

        result_field.update(value=y)
