# Colonna sonora Breakly "Sala giochi" (20 s, 120 bpm): riusa i sintetizzatori di music.py
import numpy as np, wave
exec(open('music.py').read().split('B=.5')[0])
def sq(m,dur,g=.08,duty=.5):
    n=int(dur*SR); t=np.arange(n)/SR; ph=(nf(m)*t)%1
    return np.where(ph<duty,1.,-1.)*np.minimum(1,t/.003)*np.exp(-t*4)*np.minimum(1,(dur-t)/.01)*g
def coin(g=.12): return np.r_[sq(83,.07,g,.25),sq(88,.35,g,.25)]
def neon(g=.08):
    n=int(.5*SR); t=np.arange(n)/SR; s=np.sign(np.sin(2*np.pi*120*t))*(rs.rand(n)<.6)
    return lp(s,.2)*np.exp(-t*4)*g
def jingle(t0,g=.1):
    for i,m in enumerate([72,76,79,84]): add(sq(m,.12,g,.25),t0+i*.08)
    add(sq(88,.5,g,.25),t0+.32); add(sq(84,.5,g*.7,.5),t0+.32)

B=.5
prog=[(48,[60,64,67,72]),(53,[60,65,69,72]),(45,[60,64,69,72]),(43,[59,62,67,71])]  # C F Am G
def groove(t0,t1,full=True,lead=True):
    b=int(np.ceil(t0/B-1e-6))
    while b*B<t1-1e-6:
        t=b*B; bar=int(t//2)%4; root,ch=prog[bar]; beat=b%4
        add(kick(.85),t)
        if full and beat in (1,3): add(snare(),t,.5)
        add(hat(),t+B/2,1,.3); add(hat(),t+B*.25,.4,-.3); add(hat(),t+B*.75,.4,-.3)
        add(bass(root),t,1); add(bass(root+12),t+B/2,.7)
        if full and beat in (0,2):
            for m in ch: add(ep(m,.25,.12),t+B/2,1,-.2)
        if lead:
            arp=[ch[0]+12,ch[1]+12,ch[2]+12,ch[3]+12]
            add(sq(arp[beat],.12,.045,.25),t,1,.3); add(sq(arp[(beat+2)%4],.12,.035,.25),t+B/2,1,-.3)
        b+=1

# 1) hook: riflettore + caduta
add(boom(.5),.2)
for m in [48,55,60,64]: add(ep(m,1.2,.1),.25)
add(whoosh(.45,True,.45),.85); add(boing(.4),1.3); add(boom(.6),1.3)
for i in range(4): add(chime(84+[0,4,7,12][i],.08),1.35+i*.06)
for i in range(5): add(pop(700,1300,.12),.4+i*.06)
for i in range(7): add(pop(500,1100,.2),1.5+i*.1)
groove(1.5,3.8,full=False,lead=False)
# 2) sala giochi
add(neon(.18),3.85); add(coin(.12),4.0)
for i in range(8): add(whoosh(.18,True,.18),4.1+i*.15,1,(-1)**i*.5); add(pop(500+i*60,1100+i*80,.2),4.35+i*.15)
groove(4.0,6.4,True,True)
for i in range(6): add(pop(600,1300,.14),6.3+i*.07)
# roulette di luci: un tic per ogni passo (stessa curva di index.html)
CH0,CH1,STEPS=6.4,7.9,27
prev=0; tt=CH0
while tt<CH1:
    k=(tt-CH0)/(CH1-CH0); c=int(np.floor(STEPS*(1-(1-k)**3)+1e-6))
    if c!=prev: add(sq(84+(c%4)*2,.05,.06,.25),tt,1,.2*(-1)**c); add(tick(.15),tt); prev=c
    tt+=1/2000
add(riser(1.5,.12),6.4)
add(boom(.7),CH1); jingle(CH1+.02,.11)
for i in range(25): add(pop(rs.uniform(1500,3000),rs.uniform(2000,4000),.035),CH1+rs.uniform(0,1.2),1,rs.uniform(-1,1))
groove(8.0,9.2,True,False)
# 3) telefono
add(whoosh(.5,True,.35),9.1)
groove(9.5,15.5,True,True)
for tt in (10.8,12.4,14.0): add(whoosh(.3,True,.25),tt)
for tt in (9.9,11.5,13.1,14.7): add(pop(500,1300,.3),tt); add(chime(91,.07),tt+.05,1,.4)
for tt in (9.4,11.0,12.6,14.2):
    for i in range(3): add(pop(600,1200,.1),tt+i*.08)
# 4) finale
add(riser(.8,.15),14.8); add(whoosh(.6,True,.45),15.4)
add(boom(.9),16.05); add(boing(.3),16.1); jingle(16.1,.09)
for i in range(30): add(pop(rs.uniform(1500,3000),rs.uniform(2000,4000),.035),16.05+rs.uniform(0,1.2),1,rs.uniform(-1,1))
for i in range(4): add(pop(500,1100,.16),16.7+i*.12)
groove(16.5,19.5,True,True)
add(pop(400,1600,.35),17.6); add(coin(.1),17.65); add(pop(700,1400,.2),18.0,1,-.4); add(pop(800,1600,.2),18.1,1,.4)
add(kick(1),19.5); add(snare(),19.5,.6)
for m in [48,55,60,64,67,72,76]: add(ep(m,1.5,.15),19.5)
add(sq(84,.4,.06,.25),19.5)

mix=np.stack([L,R],1)
fade=np.ones(N); fi=int(.15*SR); fade[-fi:]=np.linspace(1,0,fi); mix*=fade[:,None]
mix/=np.abs(mix).max(); mix=np.tanh(mix*1.6)/np.tanh(1.6)*.92
with wave.open('b2_music.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype('<i2').tobytes())
print('ok')
