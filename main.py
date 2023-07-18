from presentation import user_interface as ui
import traceback


# open main window and poll for events
def main():

    try:
        ui.runEventLoop()
    except Exception as e:
        traceback.print_exception(e)


# necessary to run main function
if __name__ == "__main__":
    main()

