# Introduction

This repository serves as a desktop app that allows you to track the price of Amazon products by inserting its URL. It will look for price reductions every time the program is started, and every hour while the program is running. When the price of a tracked product is found to be reduced, it will signify this in the "All Tracked Products" window where the "Reduced" column will contain the field "Yes".


# Getting Started

## Clone the repository
- Go to the terminal on Linux or the command prompt on Windows, and create a new folder.
- Ensure that git is installed for your system (for instructions, click here: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
- Type the command "git clone https://github.com/nagaokakid/AmazonPriceTracker.git" to download the repository onto your system.

## Build the app
You must have python3 installed on your system to run the app. For instructions on python3 installation, click here: https://www.geeksforgeeks.org/download-and-install-python-3-latest-version/
### Windows
In the command prompt, navigate to the folder containing the repository. Type the command "windows-version.bat" to run the app.
### Linux
In the terminal, navigate to the folder containing the repository. Type the command "make run" to run the app.

After building the app via the command line on Windows or Linux, navigate to the folder venv\app\ and use the command "python3 main.py" to run the app from then on.

**Happy Hunting!**


