import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
im=np.asarray(Image.open('../images/1.webp').convert('RGB')).astype(np.float32)
mx=im.max(2); mn=im.min(2)
bgish=(mn>215)&((mx-mn)<18)
lab,n=ndimage.label(bgish)
sz=ndimage.sum(bgish,lab,range(1,n+1))
cm=ndimage.center_of_mass(bgish,lab,range(1,n+1))
edge=[i+1 for i,v in enumerate(sz) if v>150 and not (380<cm[i][1]<560 and 560<cm[i][0]<740)]
bg=np.isin(lab,list(edge))
# close small holes in bg (checker edges)
bg=ndimage.binary_opening(bg,iterations=1,border_value=1)
fg=~bg
# remove tiny specks
lab2,n2=ndimage.label(fg); sizes=ndimage.sum(fg,lab2,range(1,n2+1))
keep=np.isin(lab2,[i+1 for i,s in enumerate(sizes) if s>2000])
fg=ndimage.binary_erosion(keep,iterations=1)
a=Image.fromarray((fg*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
rgb=Image.fromarray(im.astype(np.uint8))
rgb.putalpha(a)
bb=rgb.getbbox(); rgb=rgb.crop(bb); print(bb,rgb.size)
rgb.save('chicca.png')
# preview on dark bg
bgc=Image.new('RGBA',rgb.size,(20,16,33,255)); bgc.alpha_composite(rgb); bgc.convert('RGB').save('preview.jpg')
