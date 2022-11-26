import PySimpleGUI as sg
import string
from log import baby_giant

size = (10, 1)

y_field = sg.InputText(
    expand_x=True, tooltip="y", enable_events=True, key="y", size=size)
y_text = sg.Text("y:")


g_field = sg.InputText(expand_x=True, tooltip="g",
                       enable_events=True, key="g", size=size)
g_text = sg.Text("g:")

m_field = sg.InputText(expand_x=True, tooltip="m",
                       enable_events=True, key="m", size=size)

compute = sg.Button(button_text="вычислить", key="compute")

result_field = sg.InputText(tooltip="x:", disabled=True, size=size)
result_text = sg.Text("x:")

layout = [
    [y_text, y_field, sg.Text("≡"), g_text, g_field, sg.Text(
        " ^ x"), sg.Text("mod "), m_field],
    [compute],
    [result_text, result_field]
]

window = sg.Window('дискретное логарифмирование', layout, font=("Consolas", 16),
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
            y, g, m = fetch_field("y"), fetch_field("g"), fetch_field("m")
        except ValueError as e:
            sg.Popup(f"недопустимое значение в поле {e.args[0]}")
            continue
        if y >= m:
            sg.Popup(f"y должен быть < m")
            continue
        if g >= m:
            sg.Popup(f"g должен быть < m")
            continue
        try:
            result = baby_giant(y, g, m)
            if result is None:
                sg.Popup("для данных параметров ответа нет")
                continue
            else:
                result_field.update(value=result)
        except ValueError:
            sg.Popup("для данных параметров ответа нет")
            continue
