# Parking Spot Monitoring App

This tutorial demonstrates how to deploy a Groundlight application on a Raspberry Pi Zero 2W to monitor vehicles entering and leaving a parking spot. The code can easily be adapted to any other monitoring task that you would like to deploy on a Raspberry Pi. 

## Table of Contents

1. [Required Hardware](#requiredhardware)
2. [Instructions](#instructions)

## Required Hardware
1. rpi
1. camera...

## Instructions

1. Flash Raspberry Pi OS
    1. Go to https://www.raspberrypi.com/software/. Download and install the Raspberry Pi Imager for your operating system.
    1. Open the Raspberry Pi Imager application.
    1. Choose the OS for your Raspberry Pi. Under 'Raspberry Pi OS (other)' select 'Raspberry Pi OS Lite (32-bit)'. This will give you a lightweight, headless OS. 
    1. Insert your micro SD card into your computer. Select 'Choose Storage' and select your micro SD card. 
    1. Configure some settings for your OS image:
        1. Click on the Settings button (gear icon). 
        1. On the Settings windows, choose a hostname that is relevant to your project. We chose 'parkmon' for our parking spot monitoring application.
        1. Enable SSH so that you can access your Raspberry Pi remotely from your computer. 
        1. Choose 'Allow pulic-key authentication only' to keep your Raspberry Pi secure.
        1. Choose a username and password for your Raspberry Pi in case you ever need to plug it into a monitor and keyboard to debug it.
        1. Configure wireless LAN. Enter your network's SSID and password. 
        1. Click 'Save'.
    1. Click 'Write' to write the OS to your SD card.
1. Boot up Raspberry Pi
    1. Remove the micro SD card from your laptop.
    1. Insert micro SD card into the Raspberry Pi.
    1. Connect Raspberry Pi to power and wait for it to boot.
1. On your computer, run `ssh parkmon` to network into your Raspberry Pi. It takes a bit of time for the Raspberry Pi to come online, especially the first time it boots, so be patient and try it a few times before assuming there are any issues. If it doesn't work after waiting 5-10 minutes and after multiple attempts, you can connect the Raspberry Pi to a monitor and keyboard to debug.     
1. Once you have successfully connected to your Raspberry Pi, unplug it and deploy on site. We connected a USB webcam and attached our Raspberry Pi to the wall with adhesive tape.
1. Ssh back into your Raspberry Pi: `ssh parkmon`
1. Create a folder for your project: `mkdir parkmon`
1. Enter project folder: `cd parkmon`
1. Set up a virtual Python environment for your dependencies: `python3 -m venv pm_env`
1. Activate the virtual environment by running `source pm_env/bin/activate`
1. Update your system packages: `sudo apt update && sudo apt upgrade`
1. Install the system dependencies for OpenCV.
    ```
    sudo apt install -y build-essential cmake git pkg-config libjpeg-dev libtiff-dev libpng-dev \
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev \
    libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev \
    libgtk-3-dev libatlas-base-dev gfortran python3-dev python3-numpy \
    libopenblas-dev
    sudo apt-get install libxml2-dev libxslt1-dev
    ```
1. Install OpenCV. OpenCV can be difficult to install on a Raspberry Pi Zero 2W due to the size of OpenCV and the resource constraints of the Raspberry Pi. To make it easy to install, we recommend installing from a prebuilt wheel.
    1. Download the wheel: `wget https://www.piwheels.org/simple/opencv-python/opencv_python-4.7.0.72-cp311-cp311-linux_armv7l.whl`
    1. Install the wheel: `pip install opencv_python-4.7.0.72-cp311-cp311-linux_armv7l.whl --no-cache-dir`
1. Install the other Python dependencies for this project: `pip install groundlight framegrab`
1. Ensure that you have a compatible version of numpy. We recommend version 1.26.4. 
    1. Check your version of numpy: `pip show numpy`
    1. If necessary, uninstall numpy: `pip uninstall numpy`
    1. Install numpy: `pip install numpy==1.26.4`
1. Authenticate your Raspberry Pi with Groundlight.
    1. Find your Groundlight API token in your password manager. If you need to generate a new API token, you can log into your Groundlight account at https://login.groundlight.ai and go to 'Api tokens'.
    1. Put your Groundlight API token into a file: `echo 'GROUNDLIGHT_API_TOKEN="<YOUR API TOKEN>"' >> .env_secrets`
    1. Source this file in your `.bashrc` so that you are always authenticated with Groundlight: `echo 'source /home/pi/parkmon/.env_secrets' >> ~/.bashrc && source ~/.bashrc`
1. Connect to your Raspberry Pi with your favorite code editor. The following instructions are for VSCode.
    1. Open VSCode on your computer.
    1. Open the Command Palette, press Ctrl + Shift + P on Windows or Cmd + Shift + P on macOS.
    1. From the Command Palette, select "Remote-SSH: Connect to Host..."
    1. In the Command Palette, write `ssh pi@parkmon`. Press enter.
    1. It will ask which SSH configuration file you want to use. Typically the first one listed is correct. 
    1. After you do this the first time, you may need to attempt the previous steps again to actually get connected. You'll know that you are connected if it says 'SSH: parkmon' in the bottom left corner.
1. Create a detector for your application:
    1. On your computer, log into your account on groundlight.ai.
    1. Go to the 'Detectors' tab and click 'Create New'.
    1. Choose a name and a query for your detector. 
    1. Click 'Create'
    1. We recommend turning off cloud labeling for now. This will give you a chance to review image queries on your own before allowing queries to be escalated to humans in the cloud. 
    1. Look in the address bar and notice the detector ID (starts with det_). Save this detector ID; you will need it when writing your application.
1. Go to the Explorer tab in VSCode an open the parkmon folder.
1. In the parkmon folder, create a file called `app.py`.
1. Write your application. Check out the `app.py` file in this repo to see the code we used in the tutorial.
1. Set up your application to run at boot.
    1. Write a shell script that runs the application and reruns it if it crashes. The script we used is available as `run_parkmon.sh` in this repo.
    1. Create a cronjob to start the application at boot. Run: `crontab -e`
    1. At the bottom of this file, write: `@reboot /home/pi/parkmon/run_parkmon.sh`.
    1. Save the file. Press Ctrl + O to save and Ctrl + X to exit.
    1. Reboot your Raspberry Pi: `sudo reboot`. Your application should start shortly after it reboots. 
    1. Check the log file to see what the application is doing: `tail /home/pi/parkmon/run_parkmon.log -f`
1. Collect some data. 
    1. Leave your detector running for a while (usually a day or so) to collect data.
    1. Log into groundlight.ai and label image queries on your detector. You will see either a "Label Image Queries" or "Keep Labeling" button on the detector detail page.
    1. Once you have labeled at least a few dozen image queries and your Projected ML Accuracy seems reasonable, activate Cloud Labeling. 
1. Set up SMS alerts.
    1. Log in to groundlight.ai.
    1. Go to Outputs and click on "Create New Groundlight Action".
    1. Give your action a name. Something like "Car arrives, send me a text".
    1. Select a condition. In this example, we choose "Changes to" and "Yes".
    1. Enter your phone number.
    1. Save.
    1. Sit back and wait for SMS alerts from your Groundlight detector. To debug, look at the logs `tail /home/pi/parkmon/run_parkmon.log -f` or view the detector detail page on groundlight.ai.



