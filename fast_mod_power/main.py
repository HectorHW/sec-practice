import PySimpleGUI as sg
from power import fast_power
import string
size = (10, 1)

a_field = sg.InputText(
    expand_x=True, tooltip="a", enable_events=True, key="a", size=size)
a_text = sg.Text("a:")


b_field = sg.InputText(expand_x=True, tooltip="b",
                       enable_events=True, key="b", size=size)
b_text = sg.Text("b:")

m_field = sg.InputText(expand_x=True, tooltip="m",
                       enable_events=True, key="m", size=size)
m_text = sg.Text("m:")

compute = sg.Button(button_text="вычислить", key="compute")

result_field = sg.InputText(expand_x=True, tooltip="a^b % m")
result_text = sg.Text("a ^ b mod m:")

layout = [
    [a_text, a_field, b_text, b_field, m_text, m_field],
    [compute],
    [result_text, result_field]
]

window = sg.Window('быстрое возведение в степень', layout, font=("Consolas", 16),
                   resizable=True, size=(800, 400))


def fetch_field(field_name):
    edited_field = globals()[field_name+"_field"]
    text = edited_field.get()
    try:
        return int(text)
    except ValueError:
        raise ValueError(field_name)


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    elif event in ["a", "b", "m"]:
        edited_field = globals()[event+"_field"]
        text = edited_field.get()
        text = "".join(filter(lambda c: c in string.digits, text))
        edited_field.update(value=text, move_cursor_to=None)
    elif event == "compute":
        try:
            a, b, m = fetch_field("a"), fetch_field("b"), fetch_field("m")
        except ValueError as e:
            sg.Popup(f"недопустимое значение в поле {e.args[0]}")
            continue
        result_field.update(value=fast_power(a, b, m))
