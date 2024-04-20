import tkinter as tk
from PIL import ImageTk, Image

def updateValue(entry, value):
    entry.delete(0, tk.END)
    entry.insert(0, value)

def updateStackLabel(redBrickStack):
    if (stack := redBrickStack//255) >= 1:
        redBrickStack = redBrickStack%255

    labelStack["text"] = f"+ 255x{stack}"

def enchantedItemPriceChange():
    price = entries["price"]["entry"].get()
    if price == "" or not price.isnumeric():
        price = 1
        updateValue(entries["price"]["entry"], 0)

    yang = int(price)*int(entries["enchantedItems"]["value"].get())

    updateStackLabel(yang//400)

    updateValue(entries["yang"]["entry"], yang)
    updateValue(entries["400"]["entry"], yang//400%255)
    updateValue(entries["50"]["entry"], yang%400//50)
    updateValue(entries["5"]["entry"], yang%400%50//5)

def yangChange():
    yang = entries["yang"]["entry"].get()
    if yang == "" or not yang.isnumeric():
        yang = 0

    price = int(entries["price"]["value"].get())
    if price == 0:   
        price = 1
        updateValue(entries["price"]["entry"], 0)
    enchantedItems=int(yang)//price

    updateStackLabel(int(yang)//400)

    updateValue(entries["50"]["entry"], int(yang)%400//50)
    updateValue(entries["400"]["entry"], int(yang)//400%255)
    updateValue(entries["5"]["entry"], int(yang)%400%50//5)
    updateValue(entries["enchantedItems"]["entry"], enchantedItems)

def redBrickStackChange():
    bricky = entries["400"]["entry"].get()
    if bricky == "" or not bricky.isnumeric():
        bricky = 0

    yang = int(bricky)*400

    price = int(entries["price"]["value"].get())
    if price == 0:   
        price = 1
        updateValue(entries["price"]["entry"], price)
    enchantedItems=yang//price

    if (stack := int(bricky)//255) >= 1:
        bricky = int(bricky)%255
        updateValue(entries["400"]["entry"], bricky)

    labelStack["text"] = f"+ 255x{stack}"
    updateValue(entries["yang"]["entry"], yang)
    updateValue(entries["50"]["entry"], yang%400//50)
    updateValue(entries["5"]["entry"], yang%400%50//5)
    updateValue(entries["enchantedItems"]["entry"], enchantedItems)

def brickChange(value):
    bricky = entries[value]["entry"].get()
    if bricky == "" or not bricky.isnumeric():
        bricky = 0

    yang = int(bricky)*int(value)
    price = int(entries["price"]["value"].get())

    if price == 0:   
        price = 1
        updateValue(entries["price"]["entry"], price)
    enchantedItems=int(yang)//price

    updateStackLabel(yang//400)
    
    if value == "50":
        updateValue(entries["5"]["entry"], yang%400%50//5)
    else:
        updateValue(entries["50"]["entry"], yang%400//50)

    updateValue(entries["yang"]["entry"], yang)
    updateValue(entries["400"]["entry"], yang//400%255)
    updateValue(entries["enchantedItems"]["entry"], enchantedItems)

def enchatedItemsChange():
    enchantedItems = entries["enchantedItems"]["entry"].get() 
    if enchantedItems == "" or not enchantedItems.isnumeric():
        enchantedItems = 0 

    yang =int(enchantedItems)*int(entries["price"]["value"].get())

    updateStackLabel(yang//400)

    updateValue(entries["yang"]["entry"], yang)
    updateValue(entries["400"]["entry"], yang//400%255)
    updateValue(entries["50"]["entry"], yang%400//50)
    updateValue(entries["5"]["entry"], yang%400%50//5)

def callback(*args):
    global updateLock
    if updateLock:
        return
    updateLock = True

    match args[0]:
        case "PY_VAR0":
            enchantedItemPriceChange()

        case "PY_VAR1":
            yangChange()

        case "PY_VAR2":
            redBrickStackChange()

        case "PY_VAR3":
            brickChange("50")

        case "PY_VAR4":
            brickChange("5")

        case "PY_VAR5":
            enchatedItemsChange()

        case _:
            print("Unknown variable")
    updateLock = False

root = tk.Tk()
root.title("Kalkulačka začarek")

imgNames=["400KK.jpg","50KK.jpg","5KK.jpg","zacarka.png"]
images=[ImageTk.PhotoImage(Image.open(imgN)) for imgN in imgNames]

labels = []
labels.append(tk.Label(root, text="cena začarka v KK: "))
labels.append(tk.Label(root, text="Yang (KK): "))

for img in images:
    labels.append(tk.Label(root, image=img))

entries = {
        "price": {},
        "yang": {},
        "400": {},
        "50": {},
        "5": {},
        "enchantedItems": {}
           }

for i, key in enumerate(entries):
    if key == "price":
        entries[key]["value"]=tk.IntVar(value=25)
    else:
        entries[key]["value"]=tk.IntVar()
    inp = tk.Entry(root, textvariable=entries[key]["value"])
    inp.grid(row=i, column = 1)
    entries[key]["value"].trace("w", callback)
    entries[key]["entry"] = inp

for i,l in enumerate(labels):
    l.grid(row=i, column=0)

labelStack = tk.Label(root, text="+ 255x0")
labelStack.grid(row=2, column=3)

updateLock = False
root.mainloop()
