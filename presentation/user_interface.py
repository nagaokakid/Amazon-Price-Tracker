import PySimpleGUI as sg
import sys
import os
import json

# add logic directory to system path for import
parent_dir = os.path.dirname(os.getcwd())
import_path = parent_dir + "\\" + "logic"
sys.path.append(import_path)

import database_manager as dbm
import web_scraper as ws

# return main window (tracking a new product and button to see all tracked products)
def createPrimaryWindow():
    # Track a product
    track_title = [sg.Text('Track a Product', font=("Default", 12, "bold"), justification='left')]
    track_text = [sg.Text('Enter the URL:', key='-OUT-'), sg.InputText()]
    track_button = [sg.Button('Add', key='-ADD-')]
    track_layout = [track_title, track_text, track_button]

    # Look at existing tracked products
    list_header = [sg.Text('\n\nView All Tracked Products', font=("Default", 12, "bold"), justification='left')]
    list_button = [sg.Button('Go', key='-GO-')]
    list_layout = [list_header, list_button]

    # entire layout for the main window
    layout_main = [track_layout, list_layout]

    return sg.Window('Amazon Price Tracker', layout_main, finalize=True)


def createSecondaryWindow():
    products_title = [sg.Text('All Tracked Products', font=("Default", 12, "bold"), justification='left')]
    products_button = [sg.Button("Refresh", key='-REFRESH-')]
    
    products_list = generateProductsList()
    column = []

    for product in products_list:
        column.append([sg.Text(product.getName())])

    column_layout = [sg.Column(layout=column, scrollable=True, vertical_scroll_only=True)]
    products_layout = [products_title, products_button, column_layout]

    return sg.Window('Tracking List', products_layout, finalize=True)


def generateProductsList():
    products_dict = None

    with open("../data/products.json", "r") as file:
        products_dict = json.loads(file.read())

    return products_dict["products"]    # return list of product items


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
                        sys.exit()
                
                # Add a new product to the tracking list
                elif event == '-ADD-':
                    product = ws.createProduct(driver, values[0])       # Get a product object back
                    dbm.insert(product)

                # Open new window and show all tracked products
                elif event == '-GO-':
                    window_tracked_products = createSecondaryWindow()
            except:
                raise Exception
    except:
        raise Exception

runEventLoop()