import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { spawn } from 'child_process';
const mode=process.argv[2]||'preview';
const browser=await chromium.launch({args:['--allow-file-access-from-files','--font-render-hinting=none']});
const page=await browser.newPage({viewport:{width:1080,height:1920}});
page.on('console',m=>console.log('console:',m.text()));page.on('pageerror',e=>console.log('ERR',e.message));
await page.goto('file://'+process.cwd()+'/video/index.html');
await page.evaluate(()=>window.ready);
if(mode==='preview'){
 const ts=process.argv.slice(3).map(Number);
 for(const t of ts){await page.evaluate(t=>render(t),t);await page.screenshot({path:`prev_${t}.jpg`,type:'jpeg',quality:70});}
}else{
 const FPS=30,N=20*FPS;
 const ff=spawn(process.argv[3],['-y','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-','-i','music.wav',
  '-c:v','libx264','-pix_fmt','yuv420p','-preset','slow','-crf','18','-profile:v','high','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart','breakly_chicca.mp4'],{stdio:['pipe','inherit','inherit']});
 for(let i=0;i<N;i++){await page.evaluate(t=>render(t),i/FPS);const b=await page.screenshot({type:'jpeg',quality:95});
  if(!ff.stdin.write(b))await new Promise(r=>ff.stdin.once('drain',r));if(i%60===0)console.log('frame',i)}
 ff.stdin.end();await new Promise(r=>ff.on('close',r));
}
await browser.close();
