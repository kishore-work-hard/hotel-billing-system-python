#---------------------------------------------imports for mouse-------------------------------------------------------
from functools import partial
#---------------------------------------------imports for printer-------------------------------------------------------
import os, sys
import win32print
import tempfile
# --------------------------------imports for buttons gui---------------------------------------------------------------
import tkinter as tk
# ----------------------------------Connecting to internet -------------------------------------------------------------
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]


creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)


sheet = client.open("tutorial").sheet1  # Open the spreadhseet

data = sheet.get_all_records()

#pprint(data)

row = sheet.row_values(3)  # Get a specific row


# ----------------------FOOD LIST WITH COST-----------------------------------------------------------------------------
foodDic = {
    'Eggs': 20,
    'Bat': 70,
    'Chicken': 60,
    'Soup': 40,
    'Rice': 30,
    'Lamb': 60,
    'Pizza': 50,
    'Salad': 10,
    'Pasta': 55
}
numberOfTables = 18

#--------------------------function to go UP using arrow UP key---------------------------------------------------------
def goup(e):
    global loc
    if page0.grid_info(): #how up arrow works for page 0
        btns[loc]['bg'] = "white"
        loc = loc - 1 if loc != 0 else loc
        btns[loc]['bg'] = "#17559c"
    elif page1.grid_info(): #how up arrow works for page 1
        foodBtns[loc]['bg'] = "white"
        loc = loc - 1 if loc != 0 else loc
        foodBtns[loc]['bg'] = "#17559c"
    elif page2.grid_info(): #how up arrow works for page 2
        tableBtns[loc]['bg'] = "white"
        loc = loc - 5 if loc >= 5 else loc
        tableBtns[loc]['bg'] = "#17559c"
    elif lastpage.grid_info(): #how up arrow works for last page
        compBtn['bg'] = "#17559c"
        backBtn['bg'] = "white"
        loc = 0

#--------------------------function to go down using arrow down key-----------------------------------------------------
def godown(e):
    global loc
    if page0.grid_info(): #how down arrow works for page 0
        btns[loc]['bg'] = "white"
        loc = loc + 1 if loc != 1 else loc
        btns[loc]['bg'] = "#17559c"
    elif page1.grid_info(): #how down arrow works for page 1
        foodBtns[loc]['bg'] = "white"
        loc = loc + 1 if loc != len(foodBtns) - 1 else loc
        foodBtns[loc]['bg'] = "#17559c"
    elif page2.grid_info(): #how down arrow works for page 2
        tableBtns[loc]['bg'] = "white"
        loc = loc + 5 if loc <= len(tableBtns) - 6 else loc
        tableBtns[loc]['bg'] = "#17559c"
    elif lastpage.grid_info(): #how down arrow works for last page
        compBtn['bg'] = "white"
        backBtn['bg'] = "#17559c"
        loc = 1

#--------------------------function to go left using left arrow key-----------------------------------------------------
def goleft(e):
    global loc
    if page2.grid_info(): #how left arrow works for page 2, only oage 2 needs the use of left arrow (to select table)
        tableBtns[loc]['bg'] = "white"
        loc = loc - 1 if loc % 5 != 0 else loc
        tableBtns[loc]['bg'] = "#17559c"

#--------------------------function to go right using right arrow key---------------------------------------------------
def goright(e):
    global loc
    if page2.grid_info():  #how right arrow works for page 2, only oage 2 needs the use of right arrow (to select table)
        tableBtns[loc]['bg'] = "white"
        loc = loc + 1 if ((loc + 1) % 5 != 0 and loc != len(tableBtns) - 1) else loc
        tableBtns[loc]['bg'] = "#17559c"

#--------------------------function to select using enter key-----------------------------------------------------------
def select(e):
    global loc
    global rec
    if page0.grid_info(): #how enter works for page 0
        btns[loc].invoke() #invoke means to acess the particular function of a button
    elif page1.grid_info(): #how enter works for page 1
        foodBtns[loc].invoke() #invoke means to acess the particular function of a button
    elif page2.grid_info(): #how enter works for page 2
        tableBtns[loc].invoke() #invoke means to acess the particular function of a button
    elif lastpage.grid_info(): #how enter works for last page
        if loc == 0:
            compBtn.invoke() #invoke means to acess the particular function of a button
        if loc == 1:
            backBtn.invoke() #invoke means to acess the particular function of a button

#--------------------------function to de select using backspace key----------------------------------------------------
def deselect(e):
    global loc
    if page1.grid_info(): #how back space to works for page 1. we only need to use this button on page 1(food quantiity)
        if foodNums[loc]['text'] != 0:
            foodNums[loc]['text'] -= 1

#--------------------------function if user choose take out-------------------------------------------------------------
def take():
    global loc
    global rec
    rec['dt'] = 'take'
    page1.grid(row=0, column=0) #may look confusing but all it dose is displa the page1 or window 1
    page0.grid_forget()  #hides or closes page 0
    btns[loc]['bg'] = "white" #button background colour white
    loc = 0
    btns[loc]['bg'] = "#17559c" #button background colour blue

#--------------------------function if user selects "dine in" button----------------------------------------------------
def dine():
    global loc
    global rec
    rec['dt'] = 'dine'
    page2.grid(row=0, column=0) #may look confusing but all it dose is display the page2 or window 2
    page0.grid_forget() #hides or closes page 0
    btns[loc]['bg'] = "white" #button background colour white
    loc = 0
    btns[loc]['bg'] = "#17559c" #button background colour white

#--------------------------function to select food and its quantity-----------------------------------------------------
def foodsel(w):
    global loc
    foodNums[w]['text'] += 1

#--------------------------function to select table number--------------------------------------------------------------
def tablesel():
    global loc
    global rec
    rec['tableNum'] = loc + 1
    page1.grid(row=0, column=0) #display page 1
    page2.grid_forget() #hides or closes page 2
    tableBtns[loc]['bg'] = "white"
    loc = 0
    tableBtns[loc]['bg'] = "#17559c"

#--------------------------function when "done" is called---------------------------------------------------------------
def done():
    global prettyFoodStr
    global rec
    global loc
    global lastpage
    global compBtn
    global backBtn
    #-------------------------creates last page(window) which is the 4th page-------------------------------------------
    lastpage = tk.Frame()
    foodBtns[loc]['bg'] = "white"
    loc = 0
    foodBtns[loc]['bg'] = "#17559c" #blue
    for i in range(len(foodNums)):
        if foodNums[i]['text'] != 0:
            rec['food'][foodBtns[i]['text']] = foodNums[i]['text']
            foodNums[i]['text'] = 0
    # -------------------------PrettyFoodStr contains all the data selected by the user so far--------------------------
    prettyFoodStr = ''
    total = 0
    for food, num in rec['food'].items():
        food = food.rsplit(' (', 1)[0]
        prettyFoodStr = prettyFoodStr + str(num) + ' X ' + food + ' : ' + f'{num * foodDic[food]} Rs' + '\n'
        # -------------------------calculates the total cost of food selected-------------------------------------------
        total = total + num * foodDic[food]
    prettyFoodStr = prettyFoodStr + '\n' + f'Total : {total} Rs'
    if rec['dt'] == 'take' and len(prettyFoodStr) != 0:
        l = tk.Label(lastpage, text='Your orders to take out\n\n\n' + prettyFoodStr)
    elif rec['dt'] == 'dine' and len(prettyFoodStr) != 0:
        l = tk.Label(lastpage, text=f'Your orders for table {rec["tableNum"]}\n\n\n' + prettyFoodStr)
        # -------------------------creates complete order button and calls the function "CO" when pressed---------------
    compBtn = tk.Button(
        master=lastpage,
        text="Complete order",
        width=14,
        height=1,
        bg="#17559c",
        command=CO)
    # -------------------------creates back button and calls the function "BA" when pressed-----------------------------
    backBtn = tk.Button(
        master=lastpage,
        text="Back",
        width=14,
        height=1,
        bg="white",
        command=BA)
    l.pack()
    compBtn.pack()
    backBtn.pack()
    lastpage.grid(row=0, column=0) #display last page
    page1.grid_forget() #closes page 1

#--------------------------function when user completes the order-------------------------------------------------------
def CO():

    global prettyFoodStr
    global rec
    global loc
    page0.grid(row=0, column=0) #display page 0
    lastpage.grid_forget() #closes last page

    #---------------------------------------code printing online--------------------------------------------------------
    if rec['tableNum']:
        prettyFoodStr=prettyFoodStr+f'\nTable{rec["tableNum"]}'
    sheet.insert_row([prettyFoodStr], 2)
    # -----------------------------Code For Printing using win32print---------------------------------------------------
    #p = win32print.OpenPrinter("RP 203")
    #job = win32print.StartDocPrinter(p, 1, ("test of raw data", None, "RAW"))
    #win32print.StartPagePrinter(p)
    #s = [prettyFoodStr]
    #listToStr = ' '.join(map(str, s))
    #print(listToStr)
    #win32print.WritePrinter(p, listToStr)
    #win32print.EndPagePrinter(p)
    # -----------------------------Code For Printing without win32print-------------------------------------------------
    filename = tempfile.mktemp(".txt") #creating a temperory file with .txt extension
    s = [prettyFoodStr] #storing the variable prettyFoodStr instide s inorder to convert prettyfoodstr into a string as of now its a list
    listToStr = ' '.join(map(str, s)) #the way we convert list to string and stores it inside listtostr
    print(listToStr)
    open(filename, "w").write(listToStr) #writing the contents of string variable into a temperory file .txt (printing hard copy)
    os.startfile(filename, "print") #prints the temp file
    #--------------------------code to clear the PrettyFoodVariable-----------------------------------------------------
    rec = {'dt': None,
           'tableNum': None,
           'food': {}
           }
    loc = 0

    #--------------------------code to go back--------------------------------------------------------------------------
def BA():
    global rec
    global loc
    page0.grid(row=0, column=0)
    lastpage.grid_forget()
    # --------------------------code to clear the PrettyFoodVariable----------------------------------------------------
    rec = {'dt': None,
           'tableNum': None,
           'food': {}
           }
    loc = 0


foodList = list(foodDic.keys())
rec = {'dt': None,
       'tableNum': None,
       'food': {}
       }
#--------------------------creates a blank window where we have to put buttons------------------------------------------
window = tk.Tk()
#--------------------------title of the window--------------------------------------------------------------------------
window.title("Alien's Hotel")
#--------------------------here three pages are created(or windows) in total 4 pages, last page is defined else where---
page0 = tk.Frame() #dine in dine out
page1 = tk.Frame() #table no
page2 = tk.Frame() #food list

#--------------------------button for page0(dine in) are created--------------------------------------------------------
btns = [
    tk.Button(
        master=page0, #for page 0 button dine in
        text="Dine in",
        width=25,
        height=5,
        bg="#17559c", #blue colour
        command=dine #calling the function named dine which is defined on top. when the user presses this "dine in" the function "dine" gets called
    ),
#--------------------------button for page0(take out) are created-------------------------------------------------------
    tk.Button(
        master=page0,
        text="Take Out",
        width=25,
        height=5,
        bg="white",
        command=take

    )]
#--------------------------button for page1(food list) are created------------------------------------------------------
foodBtns = []
foodNums = []
q = 0

for index, food in enumerate(foodList):
    foodBtns.append(
                    tk.Button(
                    master = page1,
                    text=f'{food} ({foodDic[food]}'+'Rs)',
                    width=25,
                    height=1,
                    bg="white",
                    command = partial(foodsel, index))
                    )
    foodNums.append(tk.Label(master = page1,width=4, text=0))
    foodBtns[-1].grid(row=q,column=0)
    foodNums[-1].grid(row=q,column=1)
    q+=1

#for food in foodList:
#    foodBtns.append(
#        tk.Button(
#            master=page1,
#            text=f'{food} ({foodDic[food]}' + 'Rs)',#food list written in line 30
#            width=25,
#            height=1,
#            bg="white",
#            command=foodsel)
#    )
#    foodNums.append(tk.Label(master=page1, width=4, text=0))
#    foodBtns[-1].grid(row=q, column=0)
#    foodNums[-1].grid(row=q, column=1)
#    q += 1

foodBtns[0]['bg'] = "#17559c"
#--------------------------button for page1(confirm) are created--------------------------------------------------------
foodBtns.append(
    tk.Button(
        master=page1,
        text='Comfirm',
        width=25,
        height=2,
        bg="white",
        command=done) #calls function "done"
)
foodBtns[-1].grid(row=q + 1, column=0)
#--------------------------button for page2(table button) are created---------------------------------------------------
tableBtns = []
for i in range(numberOfTables):
    tableBtns.append(
        tk.Button(
            master=page2,
            text=f'Table {i + 1}',
            width=7,
            height=1,
            bg="white",
            command=tablesel)
    )
    tableBtns[-1].grid(row=int(i / 5), column=i % 5)
tableBtns[0]['bg'] = "#17559c"
btns[0].pack()
btns[1].pack()
page0.grid(row=0, column=0)
loc = 0
#--------------------------code to bind the keybord key to function-----------------------------------------------------
window.bind("<Up>", goup)
window.bind("<Down>", godown)
window.bind("<Left>", goleft)
window.bind("<Right>", goright)
window.bind("<Return>", select)
window.bind("<BackSpace>", deselect)
#--------------------------the programme will coonstantly look for values or inputs to recieve--------------------------
window.mainloop()