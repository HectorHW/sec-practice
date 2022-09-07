import PySimpleGUI as sg
from encryption import EncodingAlphabet, encode_ceasar, decode_ceasar


LANGUAGE_KEY = "language"
ENCODE_KEY = "encode"
DECODE_KEY = "decode"


language_button = sg.Button(
    button_text=EncodingAlphabet.RUSSIAN, key=LANGUAGE_KEY, pad=0)

textfield_size = (10, 1)

input_field = sg.InputText(key="input", expand_x=True, size=textfield_size)
output_field = sg.InputText(key="output", expand_x=True,  size=textfield_size)
offset_field = sg.InputText(key="offset", size=(5, 1), default_text="3")
offset_text = sg.Text("offset")
encode_button = sg.Button(button_text="encode", key=ENCODE_KEY)
decode_button = sg.Button(button_text="decode", key=DECODE_KEY)

encoding_area = sg.Column([[encode_button], [input_field]], expand_x=True)
decoding_area = sg.Column([[decode_button], [output_field]], expand_x=True)

top_row = sg.Column(
    [[offset_text, offset_field, language_button]], element_justification="right", expand_x=True)

fields = sg.Column([[encoding_area, decoding_area]], expand_x=True)

layout = [[top_row],
          [fields]
          ]
window = sg.Window('Ceasar', layout, font=("Consolas", 16), resizable=True)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    elif event == LANGUAGE_KEY:
        language_variants = [EncodingAlphabet.ENGLISH,
                             EncodingAlphabet.RUSSIAN]
        new_option = language_variants[
            1 - language_variants.index(language_button.ButtonText)]
        language_button.Update(text=new_option)
    elif event == ENCODE_KEY:
        try:
            offset = int(offset_field.get())
        except ValueError:
            sg.Popup("invalid offset value", keep_on_top=True)
            continue

        try:
            message = input_field.get().lower()
            encoded = encode_ceasar(
                language_button.ButtonText, message, offset)
            output_field.Update(value=encoded)
        except ValueError:
            sg.Popup("unexpected characters in encoding field", keep_on_top=True)
    elif event == DECODE_KEY:
        try:
            offset = int(offset_field.get())
        except ValueError:
            sg.Popup("invalid offset value", keep_on_top=True)
            continue

        try:
            message = output_field.get().lower()
            encoded = decode_ceasar(
                language_button.ButtonText, message, offset)
            input_field.Update(value=encoded)
        except ValueError:
            sg.Popup("unexpected characters in decoding field", keep_on_top=True)

window.close()
