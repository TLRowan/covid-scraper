import tkinter

from bs4 import BeautifulSoup  # Allows data pulling from html
import requests
import tkinter as tk

# Utilized for searching by abbreviation
state_abbreviations = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
}


# Search for the state and retrieve and display the data.
def buttonClick():
    index = 0;
    state_input = entry.get().strip().upper()  # Convert input to uppercase
    state = state_abbreviations.get(state_input, state_input)  # Get full state name or use input if not an abbreviation
    for x in states:
        if x.lower() == state.lower():
            stats["text"] = states[index] + "\nTotal cases: " + totalCases[index] + "\nActive cases: " + totalActive[
                index] + "\nTotal deaths: " + totalDeaths[index]
        index += 1
    entry.delete(0, len(state))


USA_content = requests.get("https://www.worldometers.info/coronavirus/").text
state_content = requests.get("https://www.worldometers.info/coronavirus/country/us/").text
USAsoup = BeautifulSoup(USA_content, "html.parser")
stateSoup = BeautifulSoup(state_content, "html.parser")

# Track each div with class "maincounter-wrap"
USAcovidSoup = USAsoup.find_all("div", attrs={"class": "maincounter-number"})

# Track each states statistics ( class_ used to search for classes since class is a reserved word in python)

# Get whole table body than the rows
stateTable = stateSoup.tbody
stateRows = stateTable.contents  # tag objects

states = []
totalCases = []
totalDeaths = []
totalActive = []

# Loop through each row of the table and take in data (.contents gives all html tags)
tableRowIndex = 0
tagIndex = 0
for tablerow in stateRows:
    tableRowIndex += 1
    tagIndex = 0
    for tag in tablerow:
        if tagIndex == 3:
            stateName = tag.a
            states.append((tag.get_text()).strip())  # Strips /n and white space from state names
        elif tagIndex == 5:
            totalCases.append(tag.string.strip())
        elif tagIndex == 9:
            totalDeaths.append(tag.string.strip())
        elif tagIndex == 15:
            totalActive.append(tag.string.strip())
        tagIndex += 1

# Function to handle Enter key press
def onEnter(event):
    buttonClick()


# Create GUI
root = tk.Tk()
root.title("USA Covid Statistics")
info = tk.Label(root, text="Enter in a state name or 'USA Total' for statistics")
info.pack()
stats = tk.Label(root, font=('Aerial 16'))
stats.pack()
entry = tk.Entry(fg="black", bg="white", width=50)
entry.pack()
button = tk.Button(root, text="Submit", command=buttonClick)
button.pack()

# Bind the Enter key press to call buttonClick function
entry.bind('<Return>', onEnter)

# Get user choice and display data
# def displayStats(name):
#     name = tk.Entry(window).get()
#     print(choiceString)
#     name_Tf.bind('<Return>',welMsg)

root.mainloop()
