# Introduction

This repository serves as a desktop app that allows you to track the price of Amazon products by inserting its URL. It will look for price reductions every time the program is started, and every hour while the program is running. When the price of a tracked product is found to be reduced, it will signify this in the "All Tracked Products" window where the "Reduced" column will contain the field "Yes".


# Getting Started

### Clone the repository
- Go to the command line on Linux or Windows, and create a new folder.
- Ensure that git is installed for your system (for instructions, click here: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
- Type the command "git clone https://github.com/nagaokakid/AmazonPriceTracker.git" to download the repository onto your system.

### Run the app
You must have python3 installed on your system to run the app. For instructions on python3 installation, click here: https://phoenixnap.com/kb/how-to-install-python-3-windows
#### Windows
On the command line, type the command "python3 main.py" to run the app. It will take several minutes to download the necessary components and launch the app.
#### Linux
On the command line, type the command "make run" to run the app. It will take several minutes to create the virtual environment and launch the app. From then on, go to the venv/app/ directory and use the command "python3 main.py" to run the app in the virtual environment.
