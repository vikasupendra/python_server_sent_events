## 1. Convert JSON to CSV ##
## ==================================
import json
if __name__ == '__main__':
    try:
        with open('input.json', 'r') as f:
            data = json.loads(f.read())

        output = ','.join([*data[0]])
        for obj in data:
            output += f'\n{obj["Name"]},{obj["age"]},{obj["birthyear"]}'

        with open('output.csv', 'w') as f:
            f.write(output)
    except Exception as ex:
        print(f'Error: {str(ex)}')


## 2. Password Generator ##
## ==============================
import random
import string
total = string.ascii_letters + string.digits + string.punctuation
length = 16
password = "".join(random.sample(total, length))
print(password)

## 3. String search from multiple files ##
## ========================================
import os
text = input("input text : ")
path = input("path : ")
# os.chdir(path)
def getfiles(path):
    f = 0
    os.chdir(path)
    files = os.listdir()
    # print(files)
    for file_name in files:
        abs_path = os.path.abspath(file_name)
        if os.path.isdir(abs_path):
            getfiles(abs_path)
        if os.path.isfile(abs_path):
            f = open(file_name, "r")
            if text in f.read():
                f = 1
                print(text + " found in ")
                final_path = os.path.abspath(file_name)
                print(final_path)
                return True
    if f == 1:
        print(text + " not found! ")
        return False

#getfiles(path)


## 4. Fetch all links from a given webpage ##
## ==========================================
import requests as rq
from bs4 import BeautifulSoup

url = input("Enter Link: ")
if ("https" or "http") in url:
    data = rq.get(url)
else:
    data = rq.get("https://" + url)
soup = BeautifulSoup(data.text, "html.parser")
links = []
for link in soup.find_all("a"):
    links.append(link.get("href"))
# Writing the output to a file (myLinks.txt) instead of to stdout
# You can change 'a' to 'w' to overwrite the file each time
with open("myLinks.txt", 'a') as saved:
    print(links[:10], file=saved)


## 5. Image Watermarking ##
## ==================================
import os
from PIL import Image

def watermark_photo(input_image_path,watermark_image_path,output_image_path):
    base_image = Image.open(input_image_path)
    watermark = Image.open(watermark_image_path).convert("RGBA")
    # add watermark to your image
    position = base_image.size
    newsize = (int(position[0]*8/100),int(position[0]*8/100))
    # print(position)
    watermark = watermark.resize(newsize)
    # print(newsize)
    # return watermark

    new_position = position[0]-newsize[0]-20,position[1]-newsize[1]-20
    # create a new transparent image
    transparent = Image.new(mode='RGBA',size=position,color=(0,0,0,0))
    # paste the original image
    transparent.paste(base_image,(0,0))
    # paste the watermark image
    transparent.paste(watermark,new_position,watermark)
    image_mode = base_image.mode
    print(image_mode)
    if image_mode == 'RGB':
        transparent = transparent.convert(image_mode)
    else:
        transparent = transparent.convert('P')
    transparent.save(output_image_path,optimize=True,quality=100)
    print("Saving"+output_image_path+"...")

folder = input("Enter Folder Path:")
watermark = input("Enter Watermark Path:")
os.chdir(folder)
files = os.listdir(os.getcwd())
print(files)

if not os.path.isdir("output"):
    os.mkdir("output")

c = 1
for f in files:
    if os.path.isfile(os.path.abspath(f)):
        if f.endswith(".png") or f.endswith(".jpg"):
            watermark_photo(f,watermark,"output/"+f)


### 6. Scrap and Download all images from the WEB Page ###
## =======================================================
from selenium import webdriver
import requests as rq
import os
from bs4 import BeautifulSoup
import time

# path= E:\web scraping\chromedriver_win32\chromedriver.exe
path = input("Enter Path : ")
url = input("Enter URL : ")
output = "output"

def get_url(path, url):
    driver = webdriver.Chrome(executable_path=r"{}".format(path))
    driver.get(url)
    print("loading.....")
    res = driver.execute_script("return document.documentElement.outerHTML")
    return res

def get_img_links(res):
    soup = BeautifulSoup(res, "lxml")
    imglinks = soup.find_all("img", src=True)
    return imglinks

def download_img(img_link, index):
    try:
        extensions = [".jpeg", ".jpg", ".png", ".gif"]
        extension = ".jpg"
        for exe in extensions:
            if img_link.find(exe) > 0:
                extension = exe
                break
        img_data = rq.get(img_link).content
        with open(output + "\\" + str(index + 1) + extension, "wb+") as f:
            f.write(img_data)
        f.close()
    except Exception:
        pass

result = get_url(path, url)
time.sleep(60)
img_links = get_img_links(result)
if not os.path.isdir(output):
    os.mkdir(output)
for index, img_link in enumerate(img_links):
    img_link = img_link["src"]
    print("Downloading...")
    if img_link:
        download_img(img_link, index)
print("Download Complete!!")

### 7. Organized download folder with different categories ###
## ============================================================
import os
import shutil
os.chdir("E:\downloads")
#print(os.getcwd())

#check number of files in  directory
files = os.listdir()
#list of extension (You can add more if you want)
extentions = {
    "images": [".jpg", ".png", ".jpeg", ".gif"],
    "videos": [".mp4", ".mkv"],
    "musics": [".mp3", ".wav"],
    "zip": [".zip", ".tgz", ".rar", ".tar"],
    "documents": [".pdf", ".docx", ".csv", ".xlsx", ".pptx", ".doc", ".ppt", ".xls"],
    "setup": [".msi", ".exe"],
    "programs": [".py", ".c", ".cpp", ".php", ".C", ".CPP"],
    "design": [".xd", ".psd"]

}

#sort to specific folder depend on extenstions
def sorting(file):
    keys = list(extentions.keys())
    for key in keys:
        for ext in extentions[key]:
            # print(ext)
            if file.endswith(ext):
                return key

#iterat through each file
for file in files:
    dist = sorting(file)
    if dist:
        try:
            shutil.move(file, "../download-sorting/" + dist)
        except:
            print(file + " is already exist")
    else:
        try:
            shutil.move(file, "../download-sorting/others")
        except:
            print(file + " is already exist")

### 8. Send Emails in Bulk From CSV File ###
## ==========================================
import csv
from email.message import EmailMessage
import smtplib

def get_credentials(filepath):
    with open("credentials.txt", "r") as f:
        email_address = f.readline()
        email_pass = f.readline()
    return (email_address, email_pass)

def login(email_address, email_pass, s):
    s.ehlo()
    # start TLS for security
    s.starttls()
    s.ehlo()
    # Authentication
    s.login(email_address, email_pass)
    print("login")

def send_mail():
    s = smtplib.SMTP("smtp.gmail.com", 587)
    email_address, email_pass = get_credentials("./credentials.txt")
    login(email_address, email_pass, s)
    # message to be sent
    subject = "Welcome to Python"
    body = """Python is an interpreted, high-level,
    general-purpose programming language.\n
    Created by Guido van Rossum and first released in 1991,
    Python's design philosophy emphasizes code readability\n
    with its notable use of significant whitespace"""
    message = EmailMessage()
    message.set_content(body)
    message['Subject'] = subject
    with open("emails.csv", newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        for email in spamreader:
            s.send_message(email_address, email[0], message)
            print("Send To " + email[0])
    # terminating the session
    s.quit()
    print("sent")

if __name__ == "__main__":
    send_mail()

### 9. Get the IP Address and Hostname of A Website ###
## =====================================================
# Get Ipaddress and Hostname of Website
# importing socket library
import socket

def get_hostname_IP():
    hostname = input("Please enter website address(URL):")
    try:
        print (f'Hostname: {hostname}')
        print (f'IP: {socket.gethostbyname(hostname)}')
    except socket.gaierror as error:
        print (f'Invalid Hostname, error raised is {error}')
get_hostname_IP()

### 10. Terminal Progress Bar ###
## ==================================

from tqdm import tqdm
from PIL import Image
import os
from time import sleep

def Resize_image(size, image):
    if os.path.isfile(image):
        try:
            im = Image.open(image)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save("resize/" + str(image) + ".jpg")
        except Exception as ex:
            print(f"Error: {str(ex)} to {image}")

path = input("Enter Path to images : ")
size = input("Size Height , Width : ")
size = tuple(map(int, size.split(",")))
os.chdir(path)
list_images = os.listdir(path)
if "resize" not in list_images:
    os.mkdir("resize")
for image in tqdm(list_images, desc="Resizing Images"):
    Resize_image(size, image)
    sleep(0.1)
print("Resizing Completed!")

### 11. I Todo App ###
## ==================================
import click

@click.group()
@click.pass_context
def todo(ctx):
    '''Simple CLI Todo App'''
    ctx.ensure_object(dict)
    #Open todo.txt – first line contains latest ID, rest contain tasks and IDs
    with open('./todo.txt') as f:
        content = f.readlines()
    #Transfer data from todo.txt to the context
    ctx.obj['LATEST'] = int(content[:1][0])
    ctx.obj['TASKS'] = {en.split('```')[0]:en.split('```')[1][:-1] for en in content[1:]}

@todo.command()
@click.pass_context
def tasks(ctx):
    '''Display tasks'''
    if ctx.obj['TASKS']:
        click.echo('YOUR TASKS\n**********')
        #Iterate through all the tasks stored in the context
        for i, task in ctx.obj['TASKS'].items():
            click.echo('• ' + task + ' (ID: ' + i + ')')
        click.echo('')
    else:
        click.echo('No tasks yet! Use ADD to add one.\n')
@todo.command()
@click.pass_context
@click.option('-add', '--add_task', prompt='Enter task to add')
def add(ctx, add_task):
    '''Add a task'''
    if add_task:
        #Add task to list in context 
        ctx.obj['TASKS'][ctx.obj['LATEST']] = add_task
        click.echo('Added task "' + add_task + '" with ID ' + str(ctx.obj['LATEST']))
        #Open todo.txt and write current index and tasks with IDs (separated by " ```
{% endraw %}
 ")
        curr_ind = [str(ctx.obj['LATEST'] + 1)] 
        tasks = [str(i) + '
{% raw %}
```' + t for (i, t) in ctx.obj['TASKS'].items()]
        with open('./todo.txt', 'w') as f:
            f.writelines(['%s\n' % en for en in curr_ind + tasks])
@todo.command()
@click.pass_context
@click.option('-fin', '--fin_taskid', prompt='Enter ID of task to finish', type=int)
def done(ctx, fin_taskid):
    '''Delete a task by ID'''
    #Find task with associated ID
    if str(fin_taskid) in ctx.obj['TASKS'].keys():
        task = ctx.obj['TASKS'][str(fin_taskid)]
        #Delete task from task list in context
        del ctx.obj['TASKS'][str(fin_taskid)]
        click.echo('Finished and removed task "' + task + '" with id ' + str(fin_taskid))
        #Open todo.txt and write current index and tasks with IDs (separated by " ```
{% endraw %}
 ")
        if ctx.obj['TASKS']:
            curr_ind = [str(ctx.obj['LATEST'] + 1)] 
            tasks = [str(i) + '
{% raw %}
```' + t for (i, t) in ctx.obj['TASKS'].items()]
            with open('./todo.txt', 'w') as f:
                f.writelines(['%s\n' % en for en in curr_ind + tasks])
        else:
            #Resets ID tracker to 0 if list is empty
            with open('./todo.txt', 'w') as f:
                f.writelines([str(0) + '\n'])
    else:
        click.echo('Error: no task with id ' + str(fin_taskid))
if __name__ == '__main__':
    todo()


### 12. Encrypt and Decrypt Texts ###
## ==================================
from Crypto.Cipher import AES
from Crypto import Random
from binascii import b2a_hex
import sys

# get the plaintext
plain_text = sys.argv[1]
# The key length must be 16 (AES-128), 24 (AES-192), or 32 (AES-256) Bytes.
key = b'this is a 16 key'
# Generate a non-repeatable key vector with a length
# equal to the size of the AES block
iv = Random.new().read(AES.block_size)
# Use key and iv to initialize AES object, use MODE_CFB mode
mycipher = AES.new(key, AES.MODE_CFB, iv)
# Add iv (key vector) to the beginning of the encrypted ciphertext
# and transmit it together
ciphertext = iv + mycipher.encrypt(plain_text.encode())

# To decrypt, use key and iv to generate a new AES object
mydecrypt = AES.new(key, AES.MODE_CFB, ciphertext[:16])
# Use the newly generated AES object to decrypt the encrypted ciphertext
decrypttext = mydecrypt.decrypt(ciphertext[16:])
# output
file_out = open("encrypted.bin", "wb")
file_out.write(ciphertext[16:])
file_out.close()
print("The key k is: ", key)
print("iv is: ", b2a_hex(ciphertext)[:16])
print("The encrypted data is: ", b2a_hex(ciphertext)[16:])
print("The decrypted data is: ", decrypttext.decode())