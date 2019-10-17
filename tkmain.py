from web import Web
from tkrenderer import TkRender
from imgrenderer import ImageRender
import tkinter as tk

res = 1000
rules = {"draw_anchor": False, "draw_center": False, "aa": 2}



class Window:
    def __init__(self):
        #Setup UI
        self.main = tk.Tk()
        self.cnv = tk.Canvas(self.main, width=res, height=res, background="black")
        self.cnv.bind("<Button-1>", self.Click)
        self.cnv.pack(side="left")
        self.pnl = tk.Frame(self.main)
        self.pnl.pack(side="right")
        a = tk.Label(self.pnl, text="Detail")
        a.pack()
        self.db = tk.Entry(self.pnl)
        self.db.pack()
        self.db.insert(0, "10")
        a = tk.Label(self.pnl, text="Anchors")
        a.pack()
        self.ab = tk.Entry(self.pnl)
        self.ab.pack()
        self.ab.insert(0, "5")
        a = tk.Label(self.pnl, text="Anchor Deviancy")
        a.pack()
        self.devb = tk.Entry(self.pnl)
        self.devb.pack()
        self.devb.insert(0, "0.2")
        a = tk.Label(self.pnl, text="Radial Strings")
        a.pack()
        self.rb = tk.Entry(self.pnl)
        self.rb.pack()
        self.rb.insert(0, "5")
        a = tk.Label(self.pnl, text="Rings")
        a.pack()
        self.rib = tk.Entry(self.pnl)
        self.rib.pack()
        self.rib.insert(0, "40")
        a = tk.Label(self.pnl, text="Hang")
        a.pack()
        self.drb = tk.Entry(self.pnl)
        self.drb.pack()
        self.drb.insert(0, "0.7")
        a = tk.Label(self.pnl, text="AA")
        a.pack()
        self.aa = tk.Entry(self.pnl)
        self.aa.insert(0, "2")
        self.aa.pack()
        self.gen = tk.Button(self.pnl, command=self.Generate, text="Generate")
        self.gen.pack()
        self.lgen = tk.Button(self.pnl, command=self.LineGen, text="Regenerate Lines")
        self.lgen.pack()
        self.clr = tk.Button(self.pnl, command=self.Clear, text="Clear")
        self.clr.pack()
        self.rnd = tk.Button(self.pnl, command=self.Render, text="Render")
        self.rnd.pack()
        a = tk.Label(self.pnl, text="Filename")
        a.pack()
        self.name = tk.Entry(self.pnl)
        self.name.pack()
        self.name.insert(0, "web")
        self.sve = tk.Button(self.pnl, command=self.Save, text="Save")
        self.sve.pack()

        #setup web generator
        self.Eng = Web(res, TkRender(self.cnv))
        self.Eng.Generate(int(self.ab.get()), float(self.devb.get()), int(self.rb.get()), int(self.rib.get()), float(self.drb.get()), int(self.db.get()))
        self.Eng.Render(rules)


    #event on mouse click, sets adds anchor at position
    def Click(self, event):
        self.Eng.SetAnchor(event.x, event.y)
        self.LineGen()
    #called on button click, generates new web
    def Generate(self):
        self.Eng.Generate(int(self.ab.get()), float(self.devb.get()), int(self.rb.get()), int(self.rib.get()), float(self.drb.get()), int(self.db.get()))
        self.Eng.Render(rules)
    #clears web
    def Clear(self):
        self.Eng.ClearAnchors()
        self.Eng.GenerateLines(float(self.drb.get()), int(self.rb.get()), int(self.rib.get()), int(self.db.get()))
        self.Eng.Render(rules)
    #rerender web
    def Render(self):
        self.Eng.Render(rules, int(self.db.get()))
    #regenerate lines but keep anchors the same
    def LineGen(self):
        self.Eng.GenerateLines(float(self.drb.get()), int(self.rb.get()), int(self.rib.get()), int(self.db.get()))
        self.Eng.Render(rules)
    #save to file
    def Save(self):
        i = ImageRender()
        rules["name"] = self.name.get()
        rules["aa"] = int(self.aa.get())
        i.Render(self.Eng, rules, int(self.db.get()))

if(__name__ == "__main__"):
    w = Window()
    w.main.mainloop()