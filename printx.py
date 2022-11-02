import tkinter as tk
# ----------------------------------------------------------------------------------------------------------------------
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


# ----------------------------------------------------------------------------------------------------------------------
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


def goup(e):
    global loc
    if page0.grid_info():
        btns[loc]['bg'] = "white"
        loc = loc - 1 if loc != 0 else loc
        btns[loc]['bg'] = "#17559c"
    elif page1.grid_info():
        foodBtns[loc]['bg'] = "white"
        loc = loc - 1 if loc != 0 else loc
        foodBtns[loc]['bg'] = "#17559c"
    elif page2.grid_info():
        tableBtns[loc]['bg'] = "white"
        loc = loc - 5 if loc >= 5 else loc
        tableBtns[loc]['bg'] = "#17559c"
    elif lastpage.grid_info():
        compBtn['bg'] = "#17559c"
        backBtn['bg'] = "white"
        loc = 0


def godown(e):
    global loc
    if page0.grid_info():
        btns[loc]['bg'] = "white"
        loc = loc + 1 if loc != 1 else loc
        btns[loc]['bg'] = "#17559c"
    elif page1.grid_info():
        foodBtns[loc]['bg'] = "white"
        loc = loc + 1 if loc != len(foodBtns) - 1 else loc
        foodBtns[loc]['bg'] = "#17559c"
    elif page2.grid_info():
        tableBtns[loc]['bg'] = "white"
        loc = loc + 5 if loc <= len(tableBtns) - 6 else loc
        tableBtns[loc]['bg'] = "#17559c"
    elif lastpage.grid_info():
        compBtn['bg'] = "white"
        backBtn['bg'] = "#17559c"
        loc = 1


def goleft(e):
    global loc
    if page2.grid_info():
        tableBtns[loc]['bg'] = "white"
        loc = loc - 1 if loc % 5 != 0 else loc
        tableBtns[loc]['bg'] = "#17559c"


def goright(e):
    global loc
    if page2.grid_info():
        tableBtns[loc]['bg'] = "white"
        loc = loc + 1 if ((loc + 1) % 5 != 0 and loc != len(tableBtns) - 1) else loc
        tableBtns[loc]['bg'] = "#17559c"


def select(e):
    global loc
    global rec
    if page0.grid_info():
        btns[loc].invoke()
    elif page1.grid_info():
        foodBtns[loc].invoke()
    elif page2.grid_info():
        tableBtns[loc].invoke()
    elif lastpage.grid_info():
        if loc == 0:
            compBtn.invoke()
        if loc == 1:
            backBtn.invoke()


def deselect(e):
    global loc
    if page1.grid_info():
        if foodNums[loc]['text'] != 0:
            foodNums[loc]['text'] -= 1


def take():
    global loc
    global rec
    rec['dt'] = 'take'
    page1.grid(row=0, column=0)
    page0.grid_forget()
    btns[loc]['bg'] = "white"
    loc = 0
    btns[loc]['bg'] = "#17559c"


def dine():
    global loc
    global rec
    rec['dt'] = 'dine'
    page2.grid(row=0, column=0)
    page0.grid_forget()
    btns[loc]['bg'] = "white"
    loc = 0
    btns[loc]['bg'] = "#17559c"


def foodsel():
    global loc
    foodNums[loc]['text'] += 1


def tablesel():
    global loc
    global rec
    rec['tableNum'] = loc + 1
    page1.grid(row=0, column=0)
    page2.grid_forget()
    tableBtns[loc]['bg'] = "white"
    loc = 0
    tableBtns[loc]['bg'] = "#17559c"


def done():
    global prettyFoodStr
    global rec
    global loc
    global lastpage
    global compBtn
    global backBtn
    lastpage = tk.Frame()
    foodBtns[loc]['bg'] = "white"
    loc = 0
    foodBtns[loc]['bg'] = "#17559c"
    for i in range(len(foodNums)):
        if foodNums[i]['text'] != 0:
            rec['food'][foodBtns[i]['text']] = foodNums[i]['text']
            foodNums[i]['text'] = 0
    prettyFoodStr = ''
    total = 0
    for food, num in rec['food'].items():
        food = food.rsplit(' (', 1)[0]
        prettyFoodStr = prettyFoodStr + str(num) + ' X ' + food + ' : ' + f'{num * foodDic[food]} ₹' + '\n'
        total = total + num * foodDic[food]
    prettyFoodStr = prettyFoodStr + '\n' + f'Total : {total} ₹'
    if rec['dt'] == 'take' and len(prettyFoodStr) != 0:
        l = tk.Label(lastpage, text='Your orders to take out\n\n\n' + prettyFoodStr)
    elif rec['dt'] == 'dine' and len(prettyFoodStr) != 0:
        l = tk.Label(lastpage, text=f'Your orders for table {rec["tableNum"]}\n\n\n' + prettyFoodStr)
    compBtn = tk.Button(
        master=lastpage,
        text="Complete order",
        width=14,
        height=1,
        bg="#17559c",
        command=CO)
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
    lastpage.grid(row=0, column=0)
    page1.grid_forget()


def CO():
    global prettyFoodStr
    global rec
    global loc
    page0.grid(row=0, column=0)
    lastpage.grid_forget()

    #-------------------------------------------------------------------------------------------------------------------
    sheet.insert_row([prettyFoodStr], 2)
    #-------------------------------------------------------------------------------------------------------------------
    rec = {'dt': None,
           'tableNum': None,
           'food': {}
           }
    loc = 0


def BA():
    global rec
    global loc
    page0.grid(row=0, column=0)
    lastpage.grid_forget()
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
window = tk.Tk()
window.title("Alien's Hotel")
page0 = tk.Frame()
page1 = tk.Frame()
page2 = tk.Frame()
btns = [
    tk.Button(
        master=page0,
        text="Dine in",
        width=25,
        height=5,
        bg="#17559c",
        command=dine
    ),
    tk.Button(
        master=page0,
        text="Take Out",
        width=25,
        height=5,
        bg="white",
        command=take

    )]
foodBtns = []
foodNums = []
q = 0
for food in foodList:
    foodBtns.append(
        tk.Button(
            master=page1,
            text=f'{food} ({foodDic[food]}' + '₹)',
            width=25,
            height=1,
            bg="white",
            command=foodsel)
    )
    foodNums.append(tk.Label(master=page1, width=4, text=0))
    foodBtns[-1].grid(row=q, column=0)
    foodNums[-1].grid(row=q, column=1)
    q += 1
foodBtns[0]['bg'] = "#17559c"
foodBtns.append(
    tk.Button(
        master=page1,
        text='Comfirm',
        width=25,
        height=2,
        bg="white",
        command=done)
)
foodBtns[-1].grid(row=q + 1, column=0)
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

window.bind("<Up>", goup)
window.bind("<Down>", godown)
window.bind("<Left>", goleft)
window.bind("<Right>", goright)
window.bind("<Return>", select)
window.bind("<BackSpace>", deselect)

window.mainloop()
