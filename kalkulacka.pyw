import tkinter as tk
from PIL import ImageTk, Image

def updateValue(entry, value):
    entry.delete(0, tk.END)
    entry.insert(0, value)

def updateCertainValues(values, value):
    value=int(value)
    for v in values:
        match v:
            case "400":
                updateStackLabel(value//400)
                updateValue(entries["400"]["entry"], value//400%255)
            case "50":
                updateValue(entries["50"]["entry"], value%400//50)
            case "5":
                updateValue(entries["5"]["entry"], value%400%50//5)
            case "yang":
                updateValue(entries["yang"]["entry"], value)
            case "price":
                updateValue(entries["price"]["entry"], value)
            case "enchantedItems":
                if (price := int(entries["price"]["entry"].get())) == 0:
                    price = 1
                updateValue(entries["enchantedItems"]["entry"], value//price)


def updateStackLabel(redBrickStack):
    if (stack := redBrickStack//255) >= 1:
        redBrickStack = redBrickStack%255

    labelStack["text"] = f"+ 255x{stack}"

def enchantedItemPriceChange():
    price = entries["price"]["entry"].get()
    if price == "" or not price.isnumeric():
        price = 1

    yang = int(price)*int(entries["enchantedItems"]["value"].get())

    updateCertainValues(["yang", "400", "50", "5"], yang)

def yangChange():
    yang = entries["yang"]["entry"].get()
    if yang == "" or not yang.isnumeric():
        yang = 0

    updateCertainValues(["400","50","5", "enchantedItems"], yang)

def redBrickStackChange():
    bricky = entries["400"]["entry"].get()
    if bricky == "" or not bricky.isnumeric():
        bricky = 0

    yang = int(bricky)*400

    if (stack := int(bricky)//255) >= 1:
        bricky = int(bricky)%255
        updateValue(entries["400"]["entry"], bricky)

    labelStack["text"] = f"+ 255x{stack}"
    updateCertainValues(["yang","50","5", "enchantedItems"], yang)

def brickChange(value):
    bricky = entries[value]["entry"].get()
    if bricky == "" or not bricky.isnumeric():
        bricky = 0

    yang = int(bricky)*int(value)
    
    if value == "50":
        updateCertainValues(["yang","400","5", "enchantedItems"], yang)
    else:
        updateCertainValues(["yang","400","50", "enchantedItems"], yang)

def enchatedItemsChange():
    enchantedItems = entries["enchantedItems"]["entry"].get() 
    if enchantedItems == "" or not enchantedItems.isnumeric():
        enchantedItems = 0 

    yang =int(enchantedItems)*int(entries["price"]["value"].get())

    updateCertainValues(["yang","400","50", "5"], yang)

def callback(*args):
    global updateLock
    if updateLock:
        return
    updateLock = True

    match args[0]:
        case "PY_VAR0": enchantedItemPriceChange()

        case "PY_VAR1": yangChange()

        case "PY_VAR2": redBrickStackChange()

        case "PY_VAR3": brickChange("50")

        case "PY_VAR4": brickChange("5")

        case "PY_VAR5": enchatedItemsChange()

        case _: print("Unknown variable")

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
        "enchantedItems": {} }

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
