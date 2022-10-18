from typing import List
import PySimpleGUI as sg
from crack import crack, crack_cypher_length
from encryption import EncodingAlphabet, transform_vigenere

LANGUAGE_KEY = "language"
CRACK_KEY = "crack"
LOAD_KEY = "load"
LISTBOX_KEY = "listbox"
LISTBOX_WORD_KEY = "listbox_word"


language_button = sg.Button(
    button_text=EncodingAlphabet.RUSSIAN, key=LANGUAGE_KEY)

textfield_size = (10, 5)


browse = sg.FileBrowse()

input_field = sg.Multiline(
    expand_x=True, expand_y=True, size=textfield_size, tooltip="шифротекст")
output_field = sg.Multiline(
    expand_x=True, expand_y=True,  size=textfield_size, tooltip="текст")
load_button = sg.Button(button_text="открыть...", key=LOAD_KEY)

input_area = sg.Column(
    [[load_button], [input_field], ], expand_x=True, expand_y=True)

crack_button = sg.Button(button_text="взломать", key=CRACK_KEY)

key_size_variants = sg.Listbox([], size=(10, 7), expand_x=False,
                               expand_y=True, enable_events=True, key=LISTBOX_KEY, select_mode="LISTBOX_SELECT_MODE_SINGLE")

password_variants = sg.Listbox([], size=(20+4, 7), expand_x=False, expand_y=True,
                               enable_events=True, key=LISTBOX_WORD_KEY, select_mode="LISTBOX_SELECT_MODE_SINGLE")

variants_area = sg.Column(
    [[crack_button], [key_size_variants, password_variants], ], expand_x=False, expand_y=True)

output_area = sg.Column(
    [[output_field]], expand_x=True, expand_y=True)

top_row = sg.Column(
    [[language_button]],
    element_justification="right",
    expand_x=True)

fields = sg.Column([[input_area, variants_area, output_area]],
                   expand_x=True, expand_y=True)

layout = [[top_row],
          [fields]
          ]
window = sg.Window('Шифр Вижинера', layout, font=("Consolas", 16),
                   resizable=True, size=(1000, 500))


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

    elif event == LOAD_KEY:
        if file := sg.popup_get_file("выберите файл..."):
            try:
                with open(file) as f:
                    text = f.read()
                    input_field.Update(value=text)
            except:
                sg.Popup(
                    f"ошибка при чтении файла",
                    keep_on_top=True)
                continue

    elif event == CRACK_KEY:

        text = input_field.get().lower()
        if not text:
            continue

        try:
            possible_offsets = crack_cypher_length(
                text, language_button.ButtonText)

        except ValueError as e:
            errors = prettify_error_list(e.args[0])
            sg.Popup(
                f"недопустимые символы в поле текста: {errors}",
                keep_on_top=True)
            continue

        top_candidates = sorted(possible_offsets.items(),
                                key=lambda item: item[1], reverse=True)

        key_size_variants.Update(
            list(map(lambda item: f"{item[0]: >2} ({item[1]:.3f})", top_candidates)))

    elif event == LISTBOX_KEY:
        selection = values[event]
        key_size = int(selection[0].strip().split(" ")[0])
        try:

            offsets = crack(input_field.get().lower(),
                            language_button.ButtonText, key_size)

            top_k = sorted(offsets.items(),
                           key=lambda item: item[1], reverse=True)[:10]

            password_variants.Update(
                list(
                    map(lambda item: f"{item[0]} ({item[1]:.3f})", top_k))
            )

            """text = transform_vigenere(language_button.ButtonText,
                                      input_field.get().lower(), key_size)
            output_field.Update(value=text)"""

        except ValueError as e:
            print(e)
            errors = prettify_error_list(e.args[0])
            sg.Popup(
                f"недопустимые символы в поле шифротекста: {errors}",
                keep_on_top=True)

    elif event == LISTBOX_WORD_KEY:
        selection = values[event]
        key = selection[0].strip().split(" ")[0]
        try:
            decoded = transform_vigenere(language_button.ButtonText, input_field.get().lower(),
                                         key, inv=True, skip_ws=True
                                         )
            output_field.Update(value=decoded)
        except ValueError as e:
            print(e)
            errors = prettify_error_list(e.args[0])
            sg.Popup(
                f"недопустимые символы в поле шифротекста: {errors}",
                keep_on_top=True)

window.close()
