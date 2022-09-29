from typing import List
import PySimpleGUI as sg
from encryption import EncodingAlphabet, UnsupportedKey, UnsupportedMessage, transform_vigenere


LANGUAGE_KEY = "language"
ENCODE_KEY = "encode"
DECODE_KEY = "decode"


language_button = sg.Button(
    button_text=EncodingAlphabet.RUSSIAN, key=LANGUAGE_KEY)

textfield_size = (10, 5)


input_field = sg.Multiline(
    expand_x=True, expand_y=True, size=textfield_size, tooltip="текст")
output_field = sg.Multiline(
    expand_x=True, expand_y=True,  size=textfield_size, tooltip="шифротекст")
offset_field = sg.InputText(size=(10, 1), default_text="")
offset_text = sg.Text("ключ")
encode_button = sg.Button(button_text="Зашифровать", key=ENCODE_KEY)
decode_button = sg.Button(button_text="Расшифровать", key=DECODE_KEY)

encoding_area = sg.Column(
    [[encode_button], [input_field]], expand_x=True, expand_y=True)
decoding_area = sg.Column(
    [[decode_button], [output_field]], expand_x=True, expand_y=True)

top_row = sg.Column(
    [[offset_text, offset_field, language_button]],
    element_justification="right",
    expand_x=True)

fields = sg.Column([[encoding_area, decoding_area]],
                   expand_x=True, expand_y=True)

layout = [[top_row],
          [fields]
          ]
window = sg.Window('Шифр Вижинера', layout, font=("Consolas", 16),
                   resizable=True, size=(800, 200))


def prettify_error_list(letters: List[str]) -> str:
    if len(letters) <= 3:
        return ", ".join(letters)
    return ", ".join(letters[:3]) + "..."


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

        key = offset_field.get()

        try:
            message = input_field.get().lower()
            encoded = transform_vigenere(
                language_button.ButtonText, message, key)
            output_field.Update(value=encoded)
        except UnsupportedMessage as e:
            errors = prettify_error_list(e.args[0])
            sg.Popup(
                f"недопустимые символы в поле текста: {errors}",
                keep_on_top=True)
        except UnsupportedKey as e:
            errors = prettify_error_list(e.args[0])
            sg.Popup(
                f"недопустимые символы в поле ключа: {errors}",
                keep_on_top=True)
    elif event == DECODE_KEY:

        key = offset_field.get()

        try:
            message = output_field.get().lower()
            decoded = transform_vigenere(
                language_button.ButtonText, message, key, inv=True)
            input_field.Update(value=decoded)
        except UnsupportedMessage as e:
            errors = prettify_error_list(e.args[0])
            sg.Popup(
                f"недопустимые символы в поле шифротекста: {errors}",
                keep_on_top=True)
        except UnsupportedKey as e:
            errors = prettify_error_list(e.args[0])
            sg.Popup(
                f"недопустимые символы в поле ключа: {errors}",
                keep_on_top=True)

window.close()
