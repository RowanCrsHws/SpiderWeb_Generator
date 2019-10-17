from web import Web
from imgrenderer import ImageRender
#get settings
res = int(input("resolution:"))
det = int(input("detail:"))
anc = int(input("anchor points:"))
dev = float(input("anchor deviancy:"))
rad = int(input("radial strings:"))
ri = int(input("ring count:"))
dr = float(input("droop amount:"))
aa = int(input("aa amount:"))
name = input("name:")
#create web
w = Web(res, ImageRender())
w.Generate(anc, dev, rad, ri, dr, det)
w.Render({"draw_anchor": False, "draw_center": False, "aa": aa, "name": name}).show()