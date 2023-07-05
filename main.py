import PySimpleGUI as sg
import sys
sys.path.append("./logic")
import web_scraper as ws

# return main window (tracking a new product and button to see all tracked products)
def createPrimaryWindow():
    # Track a product
    track_header = [sg.Text('Track a Product', font=("Default", 12, "bold"), justification='left')]
    track_title = [sg.Text('Enter the URL:', key='-OUT-'), sg.InputText()]
    track_button = [sg.Button('Add', key='-ADD-')]
    track_layout = [track_header, track_title, track_button]

    # Look at existing tracked products
    list_header = [sg.Text('\n\nView All Tracked Products', font=("Default", 12, "bold"), justification='left')]
    list_button = [sg.Button('Go', key='-GO-')]
    list_layout = [list_header, list_button]

    # entire layout for the main window
    layout_main = [track_layout, list_layout]

    return sg.Window('Amazon Price Tracker', layout_main, finalize=True)


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
                    window.close()

                    if window == window_tracked_products:   # Second window is closed, so mark as closed
                        window_tracked_products = None
                    elif window == window_main:             # First window is closed, so end program
                        ws.closeWebDriver()
                        break
                
                # Add a new product to the tracking list
                elif event == '-ADD-':
                    product = ws.createProduct(driver, values[0])       # Get a product object back
                    # database_manager.insert(product)

                # Open new window and show all tracked products
                elif event == '-GO-':
                    layout_tracked_products = [[sg.Text('Products')]]
                    window = sg.Window('All Tracked Products', layout_tracked_products, finalize=True)
            except:
                pass
    except:
        pass

runEventLoop()