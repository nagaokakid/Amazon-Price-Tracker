import PySimpleGUI as sg

sg.theme('BlueMono')

# Track a product
track_header = [sg.Text('Track a Product', font=("Default", 12, "bold"), justification='left')]
track_title = [sg.Text('Enter the URL for a product to track its price:', key='-OUT-')]
track_input = [sg.Input(key='-IN-')]
track_button = [sg.Button('Add', key='-ADD-')]
track_layout = [track_header, track_title, track_input, track_button]

# Look at existing tracked products
list_header = [sg.Text('\n\nView All Tracked Products', font=("Default", 12, "bold"), justification='left')]
list_button = [sg.Button('Go', key='-GO-')]
list_layout = [list_header, list_button]

# The whole layout for the window
layout = [track_layout, list_layout]

window = sg.Window('Amazon Price Tracker', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED:
        break
    if event == 'Show':
        # Update the "output" text element to be the value of "input" element
        window['-OUTPUT-'].update(values['-IN-'])

window.close()