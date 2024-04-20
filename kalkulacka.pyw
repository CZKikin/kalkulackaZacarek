import tkinter as tk
from PIL import ImageTk, Image

def updateValue(entry, value):
    entry.delete(0, tk.END)
    entry.insert(0, value)

def cenaZac():
    cena = entries["cena"]["entry"].get()
    if cena == "" or not cena.isnumeric():
        cena = 1
        updateValue(entries["cena"]["entry"], cena)

    zaklad = int(cena)*int(entries["zac"]["value"].get())
    Rprut = zaklad//400
    rprut = zaklad%400//50
    mprut = zaklad%400%50//5

    updateValue(entries["yang"]["entry"], zaklad)
    updateValue(entries["400"]["entry"], Rprut)
    updateValue(entries["50"]["entry"], rprut)
    updateValue(entries["5"]["entry"], mprut)

def yangZmena():
    yang = entries["yang"]["entry"].get()
    if yang == "" or not yang.isnumeric():
        yang = 0
    Rprut=int(yang)//400
    rprut=int(yang)%400//50
    mprut=int(yang)%400%50//5

    cena = int(entries["cena"]["value"].get())
    if cena == 0:   
        cena = 1
        updateValue(entries["cena"]["entry"], cena)
    zac=int(yang)//cena
    
    updateValue(entries["400"]["entry"], Rprut)
    updateValue(entries["50"]["entry"], rprut)
    updateValue(entries["5"]["entry"], mprut)
    updateValue(entries["zac"]["entry"], zac)

def prut400():
    pruty = entries["400"]["entry"].get()
    if pruty == "" or not pruty.isnumeric():
        pruty = 0

    yang = int(pruty)*400
    rprut= int(yang)%400//50
    mprut= int(yang)%400%50//5

    cena = int(entries["cena"]["value"].get())
    if cena == 0:   
        cena = 1
        updateValue(entries["cena"]["entry"], cena)
    zac=int(yang)//cena

    if (stack := int(pruty)//255) >= 1:
        Rprut = int(pruty)%255
        updateValue(entries["400"]["entry"], Rprut)

    labelStack["text"] = f"+ 255x{stack}"
    updateValue(entries["yang"]["entry"], yang)
    updateValue(entries["50"]["entry"], rprut)
    updateValue(entries["5"]["entry"], mprut)
    updateValue(entries["zac"]["entry"], zac)

def prut50or5(value):
    pruty = entries[value]["entry"].get()
    if pruty == "" or not pruty.isnumeric():
        pruty = 0
    yang =int(pruty)*int(value)
    Rprut=int(yang)//400
    rprut=int(yang)%400//50
    mprut=int(yang)%400%50//5

    cena = int(entries["cena"]["value"].get())
    if cena == 0:   
        cena = 1
        updateValue(entries["cena"]["entry"], cena)
    zac=int(yang)//cena

    updateValue(entries["yang"]["entry"], yang)
    updateValue(entries["400"]["entry"], Rprut)
    updateValue(entries["50"]["entry"], rprut)
    updateValue(entries["5"]["entry"], mprut)
    updateValue(entries["zac"]["entry"], zac)

def zacarka():
    zac = entries["zac"]["entry"].get() 
    if zac == "" or not zac.isnumeric():
        zac = 0 
    yang =int(zac)*int(entries["cena"]["value"].get())
    Rprut=int(yang)//400
    rprut=int(yang)%400//50
    mprut=int(yang)%400%50//5

    updateValue(entries["yang"]["entry"], yang)
    updateValue(entries["400"]["entry"], Rprut)
    updateValue(entries["50"]["entry"], rprut)
    updateValue(entries["5"]["entry"], mprut)

def callback(*args):
    global updateLock
    if updateLock:
        return
    updateLock = True

    match args[0]:
        case "PY_VAR0":
            cenaZac()

        case "PY_VAR1":
            yangZmena()

        case "PY_VAR2":
            prut400()

        case "PY_VAR3":
            prut50or5("50")

        case "PY_VAR4":
            prut50or5("5")

        case "PY_VAR5":
            zacarka()

        case _:
            print("Unknown variable")
    updateLock = False

root = tk.Tk()
root.title("Kalkulačka začarek")

imgNames=["400KK.jpg","50KK.jpg","5KK.jpg","zacarka.png"]
images=[]
for imgN in imgNames:
    images.append(ImageTk.PhotoImage(Image.open(imgN)))

labels = []
labels.append(tk.Label(root, text="Cena začarka v KK: "))
labels.append(tk.Label(root, text="Yang (KK): "))

for img in images:
    labels.append(tk.Label(root, image=img))

entries = {
        "cena": {},
        "yang": {},
        "400": {},
        "50": {},
        "5": {},
        "zac": {}
           }


for i, key in enumerate(entries):
    if key == "cena":
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

# Přidat column na rows 2 jako 255x[] +

updateLock = False
root.mainloop()
