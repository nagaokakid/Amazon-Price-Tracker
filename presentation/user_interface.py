import PySimpleGUI as sg
import json

from logic import database_manager as dbm
from logic import web_scraper as ws
from logic import exception

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

# return window for all tracked products
def createSecondaryWindow():
    products_title = [sg.Text('All Tracked Products', font=("Default", 12, "bold"), justification='left')]
    products_button = [sg.Button("Refresh", key='-REFRESH-')]
    
    products = generateProductsList()
    column = []

    for product in products:
        column.append([sg.Text(product["name"]), sg.Text(product["is_lower_price"]), 
                       sg.Text(product["current_price"])])

    layout = [products_title, products_button, column]

    return sg.Window('Tracking List', layout, finalize=True)

# return a list of all tracked products within JSON file
def generateProductsList():
    products_dict = {} # init as None?

    with open("./data/products.json", "r") as file:
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
                        break
                
                # Add a new product to the tracking list
                elif event == '-ADD-':
                    if values[0] != "":
                        product = ws.createProduct(driver, values[0]) # create product with URL (values[0])
                        dbm.insert(product)

                # Open new window and show all tracked products if window doesn't already exist
                elif event == '-GO-':
                    if window_tracked_products is None:
                        window_tracked_products = createSecondaryWindow()
                
                # Imitate refresh; close window, re-read JSON file, and display all products
                elif event == '-REFRESH-':
                    window.close()
                    window_tracked_products = createSecondaryWindow()
            except Exception as e:
                if e is exception.NoProductPriceFound:
                    pass
                elif e is exception.NoProductNameFound:
                    pass
                else:
                    pass
    except:
        raise Exception