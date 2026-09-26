import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt
from scipy.io import wavfile
SR=48000; D=36.5; N=int(SR*D)
t=np.arange(N)/SR
L=np.zeros(N); R=np.zeros(N)
rng=np.random.default_rng(3)
def hz(m): return 440*2**((m-69)/12)
def add(sig,start,gain=1.0,pan=0.0):
    i=int(start*SR); n=min(len(sig),N-i)
    if n<=0: return
    l=np.cos((pan+1)*np.pi/4); r=np.sin((pan+1)*np.pi/4)
    L[i:i+n]+=sig[:n]*gain*l*1.414; R[i:i+n]+=sig[:n]*gain*r*1.414
def lp(x,f,o=2): return sosfilt(butter(o,f,'low',fs=SR,output='sos'),x)
def hp(x,f,o=2): return sosfilt(butter(o,f,'high',fs=SR,output='sos'),x)
def bp(x,a,b,o=2): return sosfilt(butter(o,[a,b],'band',fs=SR,output='sos'),x)
def env(n,a,r):
    e=np.ones(n); ai=int(a*SR); ri=int(r*SR)
    if ai: e[:ai]=np.linspace(0,1,ai)**2
    if ri: e[-ri:]*=np.linspace(1,0,ri)**2
    return e

# ---- pads: warm detuned chords (D major colour) ----
chords=[ (0.0, [50,57,62,64,69]),      # D add9 (dark hook)
         (3.0, [50,57,62,66,69,76]),   # Dmaj9 (laptop rises)
         (7.0, [47,54,62,66,69,73]),   # Bm11 (into the brand)
         (10.0,[43,50,59,62,66,69]),   # Gmaj9 (apply)
         (13.0,[45,52,57,61,64,71]),   # A6/9
         (16.0,[50,57,62,66,69,73]),   # Dmaj9 (discover)
         (18.5,[47,54,62,66,69,74]),   # Bm
         (21.0,[43,50,59,62,67,71]),   # G (dashboard)
         (24.4,[40,47,55,59,62,67]),   # Em9 (trust)
         (28.3,[45,52,57,61,64,69]),   # A sus-ish (lift)
         (32.8,[50,57,62,66,69,74,78])]# D resolve
for k,(st,notes) in enumerate(chords):
    en=chords[k+1][0] if k+1<len(chords) else D
    dur=en-st+1.2; n=int(dur*SR); tt=np.arange(n)/SR
    sig=np.zeros(n)
    for m in notes:
        f=hz(m)
        for det in (-0.07,0.0,0.07):
            ff=f*2**(det/12)
            sig+=np.sin(2*np.pi*ff*tt+rng.uniform(0,6))*0.6+0.25*np.sin(4*np.pi*ff*tt)*0.5
    sig/=len(notes)*3
    cut=900 if st<3 else (1400 if st<24 else 1100)
    sig=lp(sig,cut,2)
    sig*=env(n,1.0 if st>0 else 1.6,1.2)
    trem=1+0.08*np.sin(2*np.pi*0.25*tt)
    g=0.30 if st<3 else 0.34
    if st>=32: g=0.40
    add(sig*trem,st,g,-0.25); add(np.roll(sig,480)*trem,st,g,0.25)

# ---- warm pulse: soft sub thump + filtered 8th pluck from 3.0s ----
bpm=96; beat=60/bpm
def thump():
    n=int(0.5*SR); tt=np.arange(n)/SR
    f=48+40*np.exp(-tt*28)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*9)
def pluck(m):
    n=int(0.35*SR); tt=np.arange(n)/SR; f=hz(m)
    s=(np.sin(2*np.pi*f*tt)+0.3*np.sin(4*np.pi*f*tt))*np.exp(-tt*14)
    return lp(s,1800)
bassroot={3:38,7:35,10:31,13:33,16:38,18.5:35,21:31,24:28}
def root_at(x):
    r=38
    for k in sorted(bassroot):
        if x>=k: r=bassroot[k]
    return r
x=3.0
while x<28.3:
    if not (15.0<=x<16.0):
        g=0.5 if x<24.4 else 0.32
        add(thump(),x,g)
        add(pluck(root_at(x)+24),x+beat/2,0.07,0.3)
        add(pluck(root_at(x)+31),x+beat*0.75,0.045,-0.3)
    x+=beat

# ---- piano: additive with inharmonic partials ----
def piano(m,dur=2.8):
    n=int(dur*SR); tt=np.arange(n)/SR; f=hz(m); s=np.zeros(n)
    for h,a in [(1,1),(2,.45),(3,.22),(4,.12),(5,.06),(6,.03)]:
        fh=f*h*np.sqrt(1+0.0004*h*h)
        s+=a*np.sin(2*np.pi*fh*tt)*np.exp(-tt*(1.3+h*0.9))
    s*=np.minimum(1,tt/0.004)
    return lp(s,5000)
notes=[(1.5,74),(3.2,78),(7.0,78),(10.0,73),(16.0,81),(21.0,79),(24.5,76),(28.3,81),(32.85,74),(32.85,78),(32.87,81),(32.9,86)]
for st,m in notes: add(piano(m,3.2 if st<32 else 3.0),st,0.11,rng.uniform(-.4,.4))

# ---- glassy shimmer on card lifts ----
def shimmer():
    n=int(1.4*SR); tt=np.arange(n)/SR; s=np.zeros(n)
    for f,a,dc in [(2637,1,4),(3520,.7,5),(4699,.5,6),(5274,.35,7),(7040,.2,9)]:
        s+=a*np.sin(2*np.pi*f*tt+rng.uniform(0,6))*np.exp(-tt*dc)*np.minimum(1,tt/0.02)
    nz=hp(rng.standard_normal(n),6000)*np.exp(-tt*8)*np.minimum(1,tt/0.05)*0.25
    rise=np.linspace(0.6,1,n)
    return (s*0.3+nz)*rise
for st in [10.95,12.2,13.4,16.35,16.85,17.25,24.85,25.8,26.75]:
    add(shimmer(),st,0.10,rng.uniform(-.6,.6))

# ---- whoosh at the whip ----
n=int(1.2*SR); tt=np.arange(n)/SR
nz=rng.standard_normal(n)
fc=300+3500*np.sin(np.pi*np.clip(tt/1.0,0,1))**2
w=np.zeros(n); blk=1024
for i in range(0,n,blk):
    seg=nz[max(0,i-512):i+blk]
    f=fc[i]; y=bp(seg,max(80,f*0.6),min(20000,f*1.6))
    w[i:i+blk]=y[-len(nz[i:i+blk]):]
w*=np.sin(np.pi*np.clip(tt/1.0,0,1))**1.5
panl=np.linspace(-0.9,0.9,n)
i0=int(14.95*SR)
for j in range(n):
    pass
l=np.cos((panl+1)*np.pi/4); r=np.sin((panl+1)*np.pi/4)
L[i0:i0+n]+=w*l*0.9; R[i0:i0+n]+=w*r*0.9

# ---- low risers ----
def riser(dur,f0,f1):
    n=int(dur*SR); tt=np.arange(n)/SR
    f=f0*(f1/f0)**(tt/dur)
    s=np.sin(2*np.pi*np.cumsum(f)/SR)+0.4*np.sin(2*np.pi*np.cumsum(f*1.5)/SR)
    s+=lp(rng.standard_normal(n),600)*0.6*(tt/dur)
    return s*(tt/dur)**2*np.minimum(1,(dur-tt)/0.08)
add(riser(1.2,45,90),23.3,0.20)
add(riser(0.8,55,110),27.6,0.12)
add(riser(0.9,70,140),31.95,0.12)

# ---- warm resolved chime on the logo ----
n=int(3.2*SR); tt=np.arange(n)/SR; ch=np.zeros(n)
for m,a in [(74,1),(81,.7),(86,.6),(90,.35),(93,.25)]:
    f=hz(m)
    for h,ha in [(1,1),(2.76,.25),(5.4,.08)]:
        ch+=a*ha*np.sin(2*np.pi*f*h*tt)*np.exp(-tt*(1.6+h*0.8))
ch*=np.minimum(1,tt/0.003)
add(ch,32.85,0.16)
# soft low bloom under the chime
n=int(2.0*SR); tt=np.arange(n)/SR
add(np.sin(2*np.pi*hz(38)*tt)*np.exp(-tt*1.4)*np.minimum(1,tt/0.02),32.85,0.35)
# soft impact as the laptop settles
add(thump()*1.0,3.0,0.5); add(lp(rng.standard_normal(int(1.5*SR)),400)*np.exp(-np.arange(int(1.5*SR))/SR*3)*0.3,3.0,0.5)

# ---- reverb ----
irn=int(2.6*SR); it=np.arange(irn)/SR
irL=rng.standard_normal(irn)*np.exp(-it*2.4); irR=rng.standard_normal(irn)*np.exp(-it*2.4)
irL=lp(irL,6000); irR=lp(irR,6000)
irL/=np.sqrt((irL**2).sum()); irR/=np.sqrt((irR**2).sum())
wetL=fftconvolve(L,irL)[:N]; wetR=fftconvolve(R,irR)[:N]
oL=L*0.8+wetL*0.45; oR=R*0.8+wetR*0.45
music=np.stack([oL,oR],1)

# ---- voiceover: each phrase placed on its caption (source sped up 1.08x) ----
import os
from scipy.io import wavfile as wf
TEMPO=1.08
_,vo=wf.read(os.environ.get('VO_FAST','vo_fast.wav')); vo=vo.astype(np.float64)/32768.0
PHRASES=[(0.00,1.19,0.35),(1.64,3.11,1.60),(3.56,4.48,4.80),(4.96,5.74,5.80),(6.21,6.93,7.75),(7.35,9.14,8.50),
 (9.62,10.14,11.10),(10.58,11.21,12.35),(11.66,12.42,13.55),(12.86,14.81,16.50),(15.24,16.36,18.45),(16.82,17.88,19.65),
 (18.36,18.93,21.35),(19.39,19.81,21.98),(20.27,20.99,22.50),(21.47,22.63,23.30),(23.11,24.18,25.15),(24.63,25.55,26.15),
 (25.97,27.44,27.10),(27.90,30.38,29.15),(30.74,31.94,31.55),(32.42,32.93,32.90),(33.37,34.73,33.45),(35.17,35.85,34.80)]
V=np.zeros((N,2)); PRE,POST=0.04,0.10
for a,b,dst in PHRASES:
    i0=int(max(0,a/TEMPO-PRE)*SR); i1=min(len(vo),int((b/TEMPO+POST)*SR))
    seg=vo[i0:i1].copy(); n=len(seg); f=int(0.012*SR); g=int(0.06*SR)
    seg[:f]*=np.linspace(0,1,f)[:,None]; seg[-g:]*=np.linspace(1,0,g)[:,None]
    j=int((dst-PRE)*SR); m=min(n,N-j); V[j:j+m]+=seg[:m]
# gentle room on the voice so it sits in the score
vr=np.stack([fftconvolve(V[:,0],irL)[:N],fftconvolve(V[:,1],irR)[:N]],1)
V=V+vr*0.08
V=V/np.max(np.abs(V))*0.80
# duck the music under the voice
envv=np.abs(V).max(1); win=int(0.03*SR)
envv=np.convolve(envv,np.ones(win)/win,'same')
act=(envv>0.02).astype(float)
duck=np.zeros(N); a_c=np.exp(-1/(0.06*SR)); r_c=np.exp(-1/(0.35*SR)); y=0.0
for k in range(0,N,48):
    x=act[k]; c=a_c if x>y else r_c; y=c*y+(1-c)*x; duck[k:k+48]=y
music=music/np.max(np.abs(music))*0.55
music=music*(1-0.55*duck)[:,None]
# master: fades, soft clip, normalize
fade=np.ones(N); fi=int(0.9*SR); fade[-fi:]=np.linspace(1,0,fi)**1.5
fin=int(0.05*SR); fade[:fin]=np.linspace(0,1,fin)
st=(music+V)*fade[:,None]
st=np.tanh(st*1.05)
st=st/np.max(np.abs(st))*0.92
out=os.environ.get('OUT','score.wav')
wavfile.write(out,SR,(st*32767).astype(np.int16))
print('ok', np.sqrt((st**2).mean()))
