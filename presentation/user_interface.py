import PySimpleGUI as sg
from logic import database_manager as dbm
from logic import web_scraper as ws
from logic.exception import *


# return main window (tracking a new product and button to see all tracked products)
def createPrimaryWindow():
    # Track a product
    track_title = [sg.Text('Track a Product', font=("Default", 14, "bold"), justification='left')]
    track_input = [sg.Text('Enter the URL:', key='-OUT-'), sg.InputText()]
    track_button = [sg.Button('Add', key='-ADD-')]
    track_error_msg = [sg.Text('', key="-ERROR-", text_color='Red')]
    track_layout = [track_title, track_input, track_button, track_error_msg]

    # Look at existing tracked products
    list_header = [sg.Text('\nView All Tracked Products', font=("Default", 14, "bold"), justification='left')]
    list_button = [sg.Button('Go', key='-GO-')]
    list_layout = [list_header, list_button]

    # entire layout for the main window
    layout_main = [track_layout, list_layout]

    return sg.Window('Amazon Price Tracker', layout_main, finalize=True)


# return window for all tracked products
def createSecondaryWindow():
    # header info
    products_title = [sg.Text('All Tracked Products', font=("Default", 14, "bold"), justification='left')]
    products_button = [sg.Button("Refresh", key='-REFRESH-')]

    new_line = [sg.Text("\n")]

    # all product objects from JSON file
    products = dbm.getAllProducts()

    table_entries = []

    for product in products:
        name = product["name"]
        price = product["current_price"]
        bool = product["is_lower_price"]

        if len(name) > 82:
            name = name[0:79] + "..."
        if bool is True:
            bool = "Yes"
        elif bool is False:
            bool = "No"

        table_entries.append([name, price, bool])

    max_rows = len(table_entries)

    table = [sg.Table(table_entries, headings=["Name", "Current Price", "Reduced"], auto_size_columns=False, 
                      col_widths=[60, 12, 8], num_rows=max_rows, justification="center")]
    
    layout = [[products_title, products_button], [new_line], [table]]

    return sg.Window('Tracking List', layout, finalize=True, resizable=True)


# open main window and poll for events
def runEventLoop():

    try:
        # init web driver
        driver = ws.createWebDriver()

        # set color scheme
        sg.theme('BlueMono')

        # open the main window and set secondary window to null
        window_main = createPrimaryWindow()
        window_tracked_products = None

        # event loop
        while True:
            try:
                window, event, values = sg.read_all_windows()

                # Window has been closed
                if event == sg.WIN_CLOSED:
                    
                    if window:
                        window.close()
                    
                    if window == window_tracked_products:   # Second window is closed, so mark as closed
                        window_tracked_products = None
                    elif window == window_main:             # First window is closed, so end program
                        ws.closeWebDriver(driver)
                        break
                
                # Add a new product to the tracking list
                elif event == '-ADD-':
                    if values[0] != "":
                        window['-ERROR-'].update('')
                        window['-ERROR-'].update(text_color='Red')
                        product = ws.createProduct(driver, values[0]) # create product with URL (values[0])
                        dbm.insertProduct(product)
                        window['-ERROR-'].update(text_color='Green')
                        window['-ERROR-'].update('The product has been added to your tracking list.')

                # Open new window and show all tracked products if window doesn't already exist
                elif event == '-GO-':
                    if window_tracked_products is None:
                        window_tracked_products = createSecondaryWindow()
                
                # Imitate refresh; close window, re-read JSON file, and show all products
                elif event == '-REFRESH-':
                    window.close()
                    window_tracked_products = createSecondaryWindow()

            except NoProductPriceFound:
                window['-ERROR-'].update('ERROR: The price of the product could not be found.')
            except NoProductNameFound:
                window['-ERROR-'].update('ERROR: The name of the product could not be found.')
            except InvalidUrl:
                window['-ERROR-'].update('ERROR: Invalid URL provided.')
            except Exception:
                pass

    except Exception as e:
        raise e