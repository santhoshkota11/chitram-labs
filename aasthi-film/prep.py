from PIL import Image, ImageFilter
import numpy as np, cv2
A='hf/aasthi/assets/'
im=Image.open('work/src_1.png').convert('RGB')
hero=im.crop((327,127,1130,596))
hero=hero.resize((1606,938),Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.6,percent=70,threshold=2))
hero.save(A+'hero_screen.png')
nav=im.crop((327,127,1130,171)).resize((1606,88),Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.4,percent=60,threshold=2))
nav.save(A+'nav.png')
# logo
L=cv2.imread('work/src_4.png').astype(np.float32)
d=np.sqrt(((255-L)**2).sum(2))
mask=(d>60).astype(np.uint8)
ys,xs=np.where(mask); print('logo bbox',xs.min(),xs.max(),ys.min(),ys.max())
# fill edge colors from eroded interior
er=cv2.erode(mask,np.ones((5,5),np.uint8))
col=L.copy().astype(np.uint8)
inp=cv2.inpaint(col,(1-er).astype(np.uint8)*255,5,cv2.INPAINT_TELEA)
alpha=np.clip((d-20)/140,0,1)
alpha=cv2.GaussianBlur(alpha,(0,0),0.6)
rgba=np.dstack([inp[:,:,::-1],(alpha*255).astype(np.uint8)])
x0,x1,y0,y1=xs.min()-6,xs.max()+7,ys.min()-6,ys.max()+7
Image.fromarray(rgba[y0:y1,x0:x1]).save(A+'logo.png')
print(Image.open(A+'logo.png').size)
