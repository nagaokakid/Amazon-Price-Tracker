import PySimpleGUI as sg
import logic.database_manager as dbm
import logic.web_scraper as ws
from logic.exception import *
import logic.product_updater as pu
from datetime import datetime

# return main window (tracking a new product)


def createPrimaryWindow():
    # Track a product
    track_title = [sg.Text('Track a Product', font=(
        "Default", 14, "bold"), justification='left')]
    track_input = [sg.Text('Enter the URL:', key='-OUT-'), sg.InputText()]
    track_button = [sg.Button('Add', key='-ADD-')]
    track_error_msg = [sg.Text('', key="-ERROR-", text_color='Red')]
    track_layout = [track_title, track_input, track_button, track_error_msg]

    # Look at existing tracked products
    list_header = [sg.Text('\nView All Tracked Products', font=(
        "Default", 14, "bold"), justification='left')]
    list_button = [sg.Button('Go', key='-GO-')]
    list_layout = [list_header, list_button]

    # entire layout for the main window
    layout_main = [track_layout, list_layout]

    return sg.Window('Amazon Price Tracker', layout_main, finalize=True)


# return second window (all tracked products)
def createSecondaryWindow(table_entries):

    # header info
    products_title = [sg.Text('All Tracked Products', font=(
        "Default", 14, "bold"), justification='left')]
    products_button = [sg.Button("Refresh", key='-REFRESH-')]

    new_line = [sg.Text("\n")]

    # tracked products in table form
    table = [sg.Table(table_entries, headings=["ID", "Name", "Current Price", "Reduced"], auto_size_columns=False,
                      col_widths=[8, 60, 12, 8], num_rows=10, justification="center", enable_events=True,
                      enable_click_events=True, key="-TABLE-")]

    # delete a tracked product via this button
    delete_button = [sg.Button("Delete", key="-DELETE-")]

    layout = [[products_title, products_button],
              [new_line], [table], [delete_button]]

    return sg.Window('Tracking List', layout, finalize=True)


# return a list of all tracked products to be used as table entries in secondary window
def createProductsTableEntries():
    table_entries = []

    products = dbm.getAllProducts()     # read JSON file and get list of products

    for product in products:
        id = product["id"]
        name = product["name"]
        price = product["current_price"]
        bool = product["is_lower_price"]

        if len(name) > 82:
            name = name[0:79] + "..."
        if bool is True:
            bool = "Yes"
        elif bool is False:
            bool = "No"

        table_entries.append([id, name, price, bool])

    return table_entries


# update all products every hour
def checkUpdateInterval(driver, time_stamp):
    curr_time_stamp = getCurrentTimeAsInteger()

    if curr_time_stamp - time_stamp > 3600:
        pu.updateProducts(driver)
        return curr_time_stamp

    return time_stamp


# get current time as number of seconds
def getCurrentTimeAsInteger():
    curr_time = datetime.now()
    curr_time_stamp = int(round(curr_time.timestamp()))

    return curr_time_stamp


# open main window and poll for events
def runEventLoop():

    try:
        driver = ws.createWebDriver()   # init web driver
    except Exception as e:
        print("\nFailed to download and execute the Chrome web driver. Please check your Internet connection.")
        raise e

    try:
        # set color scheme for UI
        sg.theme('BlueMono')

        sg.popup_no_wait("Checking the current price for products on your tracking list. Please wait a moment...",
                         title="Updating", non_blocking=True, auto_close=True, auto_close_duration=60)
        
        pu.updateProducts(driver)   # update price of all products on tracking list (if changed)
    except Exception as e:
        print("\nFailed to update one or more products on the tracking list.")
        raise e

    try:
        # open the main window and set secondary window to null
        window_main = createPrimaryWindow()
        window_tracked_products = None
        table_entries = createProductsTableEntries()

        time = getCurrentTimeAsInteger()
    except Exception as e:
        print("\nFailed to obtain product information from the tracking list database.")
        raise e

        # event loop
    while True:
        try:
            time = checkUpdateInterval(driver, time)
            window, event, values = sg.read_all_windows()

            # Window has been closed
            if event == sg.WIN_CLOSED:

                window.close()

                if window == window_tracked_products:   # Second window is closed, so mark as closed
                    window_tracked_products = None
                elif window == window_main:             # First window is closed, so end program
                    window_main = None
                    ws.closeWebDriver(driver)

                if window_main == None and window_tracked_products == None:
                    break

            # Add a new product to the tracking list
            elif event == '-ADD-':
                if values[0] != "":
                    window['-ERROR-'].update('')
                    window['-ERROR-'].update(text_color='Red')
                    # create product with URL (values[0])
                    product = ws.createProduct(driver, values[0])
                    dbm.insertProduct(product)
                    window['-ERROR-'].update(text_color='Green')
                    window['-ERROR-'].update(
                        'The product has been added to your tracking list.')

                    if window_tracked_products:
                        table_entries = createProductsTableEntries()
                        window_tracked_products['-TABLE-'].update(
                            values=table_entries)

            # Open new window and show all tracked products if window doesn't already exist
            elif event == '-GO-':
                if window_tracked_products is None:
                    window_tracked_products = createSecondaryWindow(
                        table_entries)

            # Imitate refresh; close window, re-read JSON file, and show all products
            elif event == '-REFRESH-':
                table_entries = createProductsTableEntries()
                window['-TABLE-'].update(values=table_entries)

            # Delete a tracked product
            elif event == '-DELETE-':
                if values["-TABLE-"] == []:
                    sg.popup("No Row Selected.", title=None)
                else:
                    if sg.popup_ok_cancel("Are you sure you want to delete this product from your tracking list?", title="Delete Tracked Product") == 'OK':
                        dbm.deleteProduct(
                            (table_entries[values['-TABLE-'][0]])[0])
                        del table_entries[values['-TABLE-'][0]]
                        window['-TABLE-'].update(values=table_entries)

        except NoProductPriceFound:
            window['-ERROR-'].update(
                'ERROR: The price of the product could not be found.')
        except NoProductNameFound:
            window['-ERROR-'].update(
                'ERROR: The name of the product could not be found.')
        except InvalidUrl:
            window['-ERROR-'].update('ERROR: Invalid URL provided.')
        except DatabaseError as e:
            sg.popup_error
            raise e
        except Exception as e:
            raise e
