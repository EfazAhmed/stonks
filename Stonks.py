from tkinter import *
import tkinter.font as font
import yfinance as yf
import urllib.request
from bs4 import BeautifulSoup
from PIL import Image, ImageTk


def placing_Image(link):
    url = link
    html_code = '''
    <html>
        <body>
            <img src=''' + url + '''>
        </body>
    </html>
    '''
    file = open("logo.html", "w")
    file.write(html_code)
    file.close()
    with open('logo.html') as html_file:
        soup = BeautifulSoup(html_file, 'lxml')
    image_links = soup.select('img')
    for image in image_links:
        image_src = image["src"]

        urllib.request.urlretrieve(image_src, 'Company_Logo.png')
    photo = Image.open('Company_Logo.png')
    image1 = ImageTk.PhotoImage(photo)
    imagePanel.image = image1  # keep a reference
    imagePanel.config(bg='white', image=image1)


def placing_no_image():
    photo = Image.open('NoPreviewAvailable.png')
    image1 = ImageTk.PhotoImage(photo)
    imagePanel.image = image1  # keep a reference
    imagePanel.config(bg='white', image=image1)


def on_click(event):
    userInput.delete(0, 'end')


def off_click(event):
    userInput.insert(0, "Enter stock symbol")


def show_breaks():
    break1.config(fg='white')
    break2.config(fg='white')
    break3.config(fg='white')
    break4.config(fg='white')
    break5.config(fg='white')


def calc():
    if len(userInput.get()) <= 4:
        stock = yf.Ticker(userInput.get().upper())
        print(stock.info)
        try:
            placing_Image(stock.info['logo_url'])
        except urllib.error.HTTPError:
            placing_no_image()
        show_breaks()
        stockLabel.config(text=stock.info['shortName'] + " (" + userInput.get().upper() + ")")
        stockInfo.config(fg='white', text=" Currency in " + str(stock.info['currency']))
        stockPrice.config(text="$" + str(round(stock.info['previousClose'], 2)))
        prevClosingLabel.config(fg='white', text=" Previous Close:  $" + str(stock.info['previousClose']))
        openLabel.config(fg='white', text=" Open:  $" + str(stock.info['open']))
        bidLabel.config(fg='white', text=" Bid:  $" + str(stock.info['bid']) + " x " + str(stock.info['bidSize']))
        askLabel.config(fg='white', text=" Ask:  $" + str(stock.info['ask']) + " x " + str(stock.info['askSize']))
        dayRangeLabel.config(fg='white',
                             text=" Day's Range:  $" + str(stock.info['dayLow']) + " - $" + str(stock.info['dayHigh']))
        yearRangeLabel.config(fg='white', text=" 52 Year Range:  $" + str(stock.info['fiftyTwoWeekLow']) + " - $" + str(
            stock.info['fiftyTwoWeekHigh']))
        df = stock.recommendations

        print(df.columns)
        print(df[['Firm', 'To Grade', 'From Grade']])
        # print(df)

        print(df.loc[df['Date'].year])


root = Tk()
root.geometry('800x650')
root.title('Stonks')
root.resizable(width=False, height=False)
root.configure(bg='black')

tFont = font.Font(family="Helvetica Now", size=20, weight="bold")
lFont = font.Font(family="Helvetica Now", size=40, weight="bold")
bFont = font.Font(family="Helvetica Now", size=30, weight="bold")
pFont = font.Font(family="Helvetica Now", size=50, weight="bold")
gFont = font.Font(family="Helvetica Now", size=20, weight="bold")

top_bar = Canvas(root, bg='white', width=1600, height=80)
top_bar.place(x=0, y=0)

logo = Label(root, text="stonks.", bg='white', fg='black', font=lFont)
logo.place(relx=0.5, rely=0.065, anchor=CENTER)

variable = StringVar()
userInput = Entry(root, textvariable=variable, width=20, bg='white', fg='black', font=tFont, insertwidth=10, bd=1,
                  justify='left')
userInput.insert(0, "Enter stock symbol")
userInput.bind('<FocusIn>', on_click)
userInput.bind('<FocusOut>', off_click)
userInput.place(x=15, y=100)

button = Button(root, text="search", width=10, height=1, font=font.Font(family="Helvetica Now", size=10, weight="bold"),
                command=lambda: calc())
button.place(x=330, y=105)

stockLabel = Label(root, text="", bg='black', fg='white', font=bFont)
stockLabel.place(x=15, y=170)

stockInfo = Label(root, text="", bg='black', fg='white', font=font.Font(family="Helvetica Now", size=15))
stockInfo.place(x=15, y=215)

stockPrice = Label(root, text="", bg='black', fg='green', font=pFont)
stockPrice.place(x=15, y=240)

break1 = Label(root, text="-------------------------------------------------", fg='black', bg='black', font=gFont)
break1.place(x=15, y=360)
break2 = Label(root, text="-------------------------------------------------", fg='black', bg='black', font=gFont)
break2.place(x=15, y=410)
break3 = Label(root, text="-------------------------------------------------", fg='black', bg='black', font=gFont)
break3.place(x=15, y=460)
break4 = Label(root, text="-------------------------------------------------", fg='black', bg='black', font=gFont)
break4.place(x=15, y=510)
break5 = Label(root, text="-------------------------------------------------", fg='black', bg='black', font=gFont)
break5.place(x=15, y=560)

prevClosingLabel = Label(root, text=" Previous Close: ", bg='black', fg='black', font=gFont)
prevClosingLabel.place(x=15, y=340)

openLabel = Label(root, text=" Open: ", bg='black', fg='black', font=gFont)
openLabel.place(x=15, y=390)

bidLabel = Label(root, text=" Bid: ", bg='black', fg='black', font=gFont)
bidLabel.place(x=15, y=440)
askLabel = Label(root, text=" Ask: ", bg='black', fg='black', font=gFont)
askLabel.place(x=15, y=490)

dayRangeLabel = Label(root, text=" Day's Range: ", bg='black', fg='black', font=gFont)
dayRangeLabel.place(x=15, y=540)

yearRangeLabel = Label(root, text=" 52 Week Range: ", bg='black', fg='black', font=gFont)
yearRangeLabel.place(x=15, y=590)

imagePanel = Label(root, bg='black')
imagePanel.place(x=575, y=350)  # x=1445, y=105)

root.mainloop()
