import numpy as np, wave
SR=44100; D=20.0; N=int(SR*D)
L=np.zeros(N); R=np.zeros(N)
rs=np.random.RandomState(3)
def add(sig,t,g=1.0,pan=0.0):
    i=int(t*SR); n=min(len(sig),N-i)
    if n<=0: return
    L[i:i+n]+=sig[:n]*g*np.sqrt((1-pan)/2); R[i:i+n]+=sig[:n]*g*np.sqrt((1+pan)/2)
def env(n,a=.005,d=.2):
    t=np.arange(n)/SR; return np.minimum(1,t/a)*np.exp(-t/d)
def lp(x,k):  # one-pole lowpass, k in (0,1) or array
    y=np.zeros_like(x); s=0.0; kk=np.broadcast_to(k,x.shape)
    for i in range(len(x)): s+=kk[i]*(x[i]-s); y[i]=s
    return y
def nf(m): return 440*2**((m-69)/12)
def kick(g=1):
    n=int(.35*SR); t=np.arange(n)/SR; f=45+110*np.exp(-t*30)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)*g
def snare():
    n=int(.22*SR); t=np.arange(n)/SR; nz=rs.randn(n); nz=nz-lp(nz,.3)
    return (nz*.6*np.exp(-t*18)+np.sin(2*np.pi*190*t)*.5*np.exp(-t*25))
def hat(o=False):
    n=int((.18 if o else .05)*SR); nz=rs.randn(n); nz=np.diff(np.r_[0,np.diff(np.r_[0,nz])])
    return nz*.12*np.exp(-np.arange(n)/SR*(12 if o else 60))
def ep(m,dur=.35,g=.18):
    n=int(dur*SR*1.6); t=np.arange(n)/SR; f=nf(m)
    s=np.sin(2*np.pi*f*t)+.35*np.sin(2*np.pi*2*f*t)*np.exp(-t*8)+.12*np.sin(2*np.pi*3*f*t)*np.exp(-t*14)
    return s*env(n,.004,dur)*g
def bass(m,dur=.24,g=.32):
    n=int(dur*SR); t=np.arange(n)/SR; f=nf(m); ph=2*np.pi*f*t
    s=np.sin(ph)+.4*np.sin(2*ph)+.2*np.sin(3*ph)
    return np.tanh(1.5*s)*np.minimum(1,t/.004)*np.exp(-t*5)*g
def pluck(m,g=.16,d=.25):
    n=int(.6*SR); t=np.arange(n)/SR; f=nf(m)
    s=2*((f*t)%1)-1; s=lp(s,np.clip(.35*np.exp(-t*12)+.03,0,1))
    return s*env(n,.002,d)*g
def pop(f0=500,f1=1100,g=.35):
    n=int(.09*SR); t=np.arange(n)/SR; f=f0+(f1-f0)*np.minimum(1,t/.05)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*40)*np.minimum(1,t/.002)*g
def whoosh(dur=.5,up=True,g=.35):
    n=int(dur*SR); t=np.arange(n)/SR; x=t/dur; e=np.sin(np.pi*x)**2
    k=(.02+.25*(x if up else 1-x))
    return lp(rs.randn(n),k)*e*g*2.2
def boing(g=.3):
    n=int(.45*SR); t=np.arange(n)/SR; f=180+90*np.sin(2*np.pi*14*t)*np.exp(-t*5)+120*np.exp(-t*8)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*6)*g
def scratch(g=.35):
    n=int(.35*SR); t=np.arange(n)/SR; f=900*np.exp(-t*9)+80
    s=2*((np.cumsum(f)/SR)%1)-1; nz=lp(rs.randn(n),.2)
    return (s*.5+nz*.8)*np.exp(-t*4)*g
def boom(g=.9):
    n=int(1.2*SR); t=np.arange(n)/SR; f=30+90*np.exp(-t*18)
    return (np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*3)+lp(rs.randn(n),.08)*np.exp(-t*6)*1.5)*g
def tick(g=.25):
    n=int(.03*SR); t=np.arange(n)/SR
    return (np.sin(2*np.pi*2400*t)+.5*rs.randn(n))*np.exp(-t*160)*g
def chime(m,g=.12):
    n=int(1.2*SR); t=np.arange(n)/SR; f=nf(m)
    return (np.sin(2*np.pi*f*t)+.3*np.sin(2*np.pi*f*2.76*t)*np.exp(-t*6))*np.exp(-t*3)*np.minimum(1,t/.002)*g
def brass(ms,dur,g=.12):
    n=int(dur*SR); t=np.arange(n)/SR; s=np.zeros(n)
    for m in ms:
        f=nf(m)*(1+.003*np.sin(2*np.pi*5.5*t)); s+=2*((np.cumsum(f)/SR)%1)-1
    s=lp(s,np.clip(.03+.25*np.minimum(1,t/.08),0,1))
    return s*np.minimum(1,t/.02)*np.minimum(1,(dur-t)/.25)*g
def riser(dur,g=.25):
    n=int(dur*SR); t=np.arange(n)/SR; x=t/dur
    f=200+1400*x**2
    return (np.sin(2*np.pi*np.cumsum(f)/SR)*.3+lp(rs.randn(n),.02+.3*x))*x**2*g

B=.5  # 120 bpm
prog=[(48,[60,64,67,71]),(45,[60,64,67,69]),(50,[62,65,69,72]),(43,[62,65,67,71])]  # Cmaj7 Am7 Dm7 G7
def groove(t0,t1,full=True):
    b=int(np.ceil(t0/B-1e-6))
    while b*B<t1-1e-6:
        t=b*B; bar=int(t//2)%4; root,ch=prog[bar]; beat=b%4
        add(kick(.9),t)
        if full and beat in (1,3): add(snare(),t,.55)
        add(hat(),t+B/2,1,.3); add(hat(),t,.6,-.3)
        if beat==3 and full: add(hat(True),t+B*.75,.8,.3)
        add(bass(root),t,1); add(bass(root+ (12 if beat%2 else 7)),t+B/2,.8)
        if beat in (0,2):
            for m in ch: add(ep(m,.28),t+B/2+.0,.9,-.2)
        if full:
            mel=[72,76,79,76,74,72,71,74]
            add(pluck(mel[(b*2)%8]+(0 if bar!=2 else 2)),t+B*.25,.8,.35); add(pluck(mel[(b*2+1)%8]),t+B*.75,.6,-.35)
        b+=1

# --- intro 0-1.45: clock ticks + pad
for i in range(3): add(tick(.35),.1+i*.5,1,.2*(-1)**i)
for m in [60,64,67,71]: add(ep(m,1.2,.12),.2)
add(whoosh(.55,True,.45),.9)
add(boing(.45),1.45); add(boom(.7),1.45)
for m in [84,88,91]: add(chime(m,.1),1.5+(m-84)*.02)
# word pops
for i in range(4): add(pop(600+i*80,1200+i*80,.18),.25+i*.12)
for i in range(3): add(pop(500,1000,.2),1.7+i*.14)
groove(1.5,6.2)
# friends pop in + bubbles
for i in range(4): add(pop(400+i*120,900+i*150,.3),3.35+i*.1,1,[-.6,.6,-.6,.6][i])
for i,bt in enumerate([3.75,4.35,4.95,5.55]): add(pop(700,1500,.28),bt,1,[-.5,.5,-.5,.5][i])
# BASTA
add(scratch(.5),6.18); add(whoosh(.55,True,.4),6.2)
add(boom(1.0),6.72); add(snare(),6.72,.9)
for i,(ms) in enumerate([[48,55,60]]): add(brass([60,63,67],0.9,.1),6.72)
add(whoosh(.5,False,.35),6.75)
# decide breakly
add(riser(1.4,.18),6.9)
for i in range(2): add(pop(600,1300,.22),7.55+i*.12)
# wheel ticks + drum roll
def wheel(t):
    k=min(1,max(0,(t-8)/3.2)); s=min(1,max(0,(t-7.7)/.3))
    return -20*np.sin(np.pi*s)+1935*(1-(1-k)**4)
prev=np.floor(wheel(7.99)/45); tt=8.0
while tt<11.25:
    c=np.floor(wheel(tt)/45)
    if c!=prev: add(tick(.3),tt,1,.1); prev=c
    tt+=1/2000
for i in range(80):
    t=8+i*(3.2/80); add(snare(),t,.05+.25*(i/80),((-1)**i)*.2)
for i in range(4): add(kick(.4),8+i*.8)
# TA-DA
add(boom(.8),11.2); add(snare(),11.2,.8)
add(brass([60,64,67],.18,.14),11.2); add(brass([62,65,69],.18,.14),11.38); add(brass([64,67,72,76],1.0,.14),11.56)
for i in range(12): add(chime(84+[0,4,7,12,16,19][i%6],.07),11.2+i*.05,1,rs.uniform(-.8,.8))
for i in range(30): add(pop(rs.uniform(1500,3000),rs.uniform(2000,4000),.04),11.2+rs.uniform(0,1.4),1,rs.uniform(-1,1))
groove(12.0,16.45)
# feature cards swooshes
for i in range(4): add(whoosh(.35,True,.22),13.05+i*.55,1,.5); add(pop(500+i*100,1100+i*100,.2),13.4+i*.55)
for i in range(3): add(pop(600,1200,.18),12.75+i*.12)
# transition
add(riser(.8,.2),15.7); add(whoosh(.6,True,.5),16.35)
add(boom(.9),17.25); add(boing(.3),17.3)
for i in range(16): add(chime(84+[0,4,7,11,12,16,19,23][i%8],.08),17.3+i*.07,1,rs.uniform(-.8,.8))
groove(17.5,19.5)
for i in range(6): add(pop(600,1200,.16),17.6+i*.1)
add(pop(400,1600,.35),18.4); add(pop(700,1400,.22),18.8,1,-.4); add(pop(800,1600,.22),18.9,1,.4)
# final chord
add(kick(1),19.5); add(snare(),19.5,.6)
for m in [48,55,60,64,67,71,76]: add(ep(m,1.5,.16),19.5)
add(chime(96,.1),19.5)

mix=np.stack([L,R],1)
# fade & master
fade=np.ones(N); fi=int(.15*SR); fade[-fi:]=np.linspace(1,0,fi); mix*=fade[:,None]
mix/=np.abs(mix).max(); mix=np.tanh(mix*1.6)/np.tanh(1.6)*.92
with wave.open('music.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype('<i2').tobytes())
print('ok')
