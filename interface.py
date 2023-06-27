import PySimpleGUI as sg

# set color theme
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

# entire layout for the window
layout_main = [track_layout, list_layout]

# open the window and give it a title
window_main = sg.Window('Amazon Price Tracker', layout_main, finalize=True)
window_tracked_products = None

# event loop
while True:
    window, event, values = sg.read_all_windows()
    print(event, values)
    if event == sg.WIN_CLOSED:
        window.close()

        if window == window_tracked_products:   # Second window is closed, so mark as closed
            window_tracked_products = None
        elif window == window_main:             # First window is closed, so end program
            break

    elif event == '-GO-':                       # Open a new window to show all tracked products
        layout_tracked_products = [[sg.Text('Products')]]
        window = sg.Window('All Tracked Products', layout_tracked_products, finalize=True)