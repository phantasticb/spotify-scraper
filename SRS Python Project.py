from bs4 import BeautifulSoup
import requests
from tkinter import *
import io
import base64
import urllib
from io import BytesIO
from PIL import Image, ImageTk

#This color variable is used for the OK! indicator.

global color
color = "lightgrey"

#Define scraping function. THIS IS THE BRUNT OF THE PROGRAMMING
def scrape():

    #First we get our url.
    
    global url
    print("Scraping! \n")
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    streams = []

    chartStreams = soup.find_all("td", {"class" : "chart-table-streams"})

    for entries in chartStreams:
        streams.append(entries.text)

    #Alright here we go.
    #First we make a list called streams. It contains the number of streams for all the songs
    #Next we have to find the greatest number of streams, so we have to convert all the strings to int
    #But there are commas in the way so we have to remove them, creating the list noCommas
    #Then we can convert noCommas into an int list, called convertedStreams
    #Then we find the greatest entry in convertedStreams and assign it to a variable
    #called indexPosition and use it to find the corresponding element in the original streams list
    #This seems convoluted but is useful in case the songs are not ordered by views to begin with.

    noCommas = [i.replace(',', '') for i in streams]
    convertedStreams = [int(i) for i in noCommas]

    greatestStreams = max(convertedStreams)
    indexPosition = convertedStreams.index(greatestStreams)

    #global because we are going to use it later in the GUI

    global finalStreams
    finalStreams = str(streams[indexPosition])

    #now that we have found the string that we are looking for we return to scraping the entry
    #with greatest streams.
    #We will display album cover, name, artist, and number of streams.

    target = soup.find_all(text=re.compile(finalStreams))
    targetTag = target[0]
    tdtag = targetTag.parent
    trtag = tdtag.parent

    #excellent! Now we've found the TABLE ROW THAT OUR MOST STREAMED SONG IS FOUND IN
    #NOW ALL WE HAVE TO DO IS TAKE APART THIS TAG!

    #FIND THE NAME OF THE SONG

    nameTag = trtag.findChild("td", {"class" : "chart-table-track"})

    global finalName
    finalName = nameTag.findChild("strong").text
    print(finalName)

    #FIND THE ARTIST

    global finalArtist
    artist = nameTag.findChild("span").text
    finalArtist = artist.strip('by ')
    print(finalArtist)

    #FIND THE ALBUM COVER
    
    imageLink = trtag.findChild("td", {"class" : "chart-table-image"})
    link = imageLink.findChild("a")
    insideLink = link.findChild('img')
    finalLink = insideLink['src']
    print(finalLink)

    #DISPLAY THE FINDINGS
    
    global im
    fd = urllib.request.urlopen(finalLink)
    imgFile = io.BytesIO(fd.read())
    im = ImageTk.PhotoImage(Image.open(imgFile))
    image = Label(root, image = im)
    image.grid(row = 1, column = 2, padx = 5, pady = 5, sticky = W, rowspan = 2)

    global name
    name.configure(text = finalName)
    name.grid(row = 1, column = 3, padx = 5, pady = 6, sticky = SW)

    global artistLabel
    artistLabel.configure(text = finalArtist)
    artistLabel.grid(row = 2, column = 3, padx = 5, pady = 0, sticky = NW)


# This testurl function tests if there is a url in the entry field.
# It does not test if the url is valid or not. Oopsie.

def testurl():
    global color
    if url != "":
        color = "green2"
    else:
        color = "lightgrey"

    global statusLabel
    statusLabel.configure(fg = color)
    print("Switching to " + color + "\n")

# The seturl function is bound to the Enter button. It sets the url in
# the entry box to a variable called "url" (go figure!)

def seturl():
    global url
    url = entry.get()
    print("URL received: \n" + url + "\n")
    testurl()

# We set up the GUI object

root = Tk()
root.title("Most Streamed Spotify Track")
root.configure(bg = 'gray')

# this entry variable is necessary to make the entry box work

entry = StringVar()
global url
url = ""

#creating all the GUI elements

urlLabel = Label(root, text = "Enter Spotify Chart URL: ", bg = "gray")
urlField = Entry(root, width = 100, textvariable = entry)
enterButton = Button(root, text = "Enter", command = seturl, bg = 'grey')
bigButton = Button(root, text = "SCRAPE", command = scrape, width = 8, height = 1, font = "SegoeUI, 30", bg = "grey")
name = Label(root, text = "Song Title", bg = "gray")
artistLabel = Label(root, text = "Artist", bg = "gray")

#Status Indicator is a little more complicated

global statusLabel
statusLabel = Label(root, text="OK!", fg=color, font="SegoeUI, 30", bg = "grey")
statusLabel.grid(row=1, column=0, padx=5, pady=5, rowspan = 2)


urlLabel.grid(row = 0, column = 0, sticky = W, pady = 5, padx = 5)
urlField.grid(row = 0, column = 1, sticky = E, pady = 5, padx = 5, columnspan = 3)
enterButton.grid(row = 0, column = 4, sticky = E, pady = 5, padx = 5)
bigButton.grid(row = 1, column = 1, pady = 5, padx = 5, sticky = W, rowspan = 2)
name.grid(row=1, column=3, padx=5, pady=6, sticky=SW)
artistLabel.grid(row=2, column=3, padx=5, pady=0, sticky=NW)

# Ignition sequence start!
root.mainloop()

# We have liftoff!
