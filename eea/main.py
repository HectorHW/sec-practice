import PySimpleGUI as sg
import string
from euclid import egcd

size = (5, 1)

a_field = sg.InputText(
    expand_x=True, tooltip="a", enable_events=True, key="a", size=size)
a_text = sg.Text("a:")


b_field = sg.InputText(expand_x=True, tooltip="b",
                       enable_events=True, key="b", size=size)
b_text = sg.Text("b:")

compute = sg.Button(button_text="вычислить", key="compute")

letter_size = (5, 1)

x_field = sg.InputText(size=letter_size)
y_field = sg.InputText(size=letter_size)
gcd_field = sg.InputText(tooltip="НОД(a, b)", size=(6, 1))

layout = [
    [a_text, a_field, b_text, b_field],
    [compute],
    [sg.Text("a * "), x_field, sg.Text(" + b * "),
     y_field, sg.Text(" = "), gcd_field, sg.Text("(НОД a b)")]
]

window = sg.Window('расширенный алгоритм евклида', layout, font=("Consolas", 16),
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
    elif event in ["a", "b"]:
        edited_field = globals()[event+"_field"]
        text = edited_field.get()
        text = "".join(filter(lambda c: c in string.digits, text))
        edited_field.update(value=text, move_cursor_to=None)
    elif event == "compute":
        try:
            a, b = fetch_field("a"), fetch_field("b")
        except ValueError as e:
            sg.Popup(f"недопустимое значение в поле {e.args[0]}")
            continue
        d, x, y = egcd(a, b)

        x_field.update(value=x)
        y_field.update(value=y)
        gcd_field.update(value=d)
