// Uso: node mpp_render.mjs preview <916|45> t1 t2 ... | node mpp_render.mjs full <916|45> <ffmpeg> <out.mp4>
import { chromium } from 'playwright';
import { spawn } from 'child_process';
const [mode,ar]=process.argv.slice(2);const F45=ar==='45';
const vp={width:1080,height:F45?1350:1920};
const browser=await chromium.launch({args:['--allow-file-access-from-files','--font-render-hinting=none']});
const page=await browser.newPage({viewport:vp});
page.on('pageerror',e=>console.log('ERR',e.message));
await page.goto('file://'+process.cwd()+'/b2/index.html'+(F45?'?f45':''));
await page.evaluate(()=>window.ready);
if(mode==='preview'){
 for(const t of process.argv.slice(4).map(Number)){await page.evaluate(t=>render(t),t);await page.screenshot({path:`bprev_${ar}_${t}.jpg`,type:'jpeg',quality:70});}
}else{
 const [ffmpeg,out]=process.argv.slice(4);const DUR=await page.evaluate(()=>window.DURATION);const FPS=30,N=Math.round(DUR*FPS);
 const ff=spawn(ffmpeg,['-y','-loglevel','error','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-','-i','b2_music.wav',
  '-c:v','libx264','-pix_fmt','yuv420p','-preset','slow','-crf','18','-profile:v','high','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',out],{stdio:['pipe','inherit','inherit']});
 for(let i=0;i<N;i++){await page.evaluate(t=>render(t),i/FPS);const b=await page.screenshot({type:'jpeg',quality:95});
  if(!ff.stdin.write(b))await new Promise(r=>ff.stdin.once('drain',r))}
 ff.stdin.end();await new Promise(r=>ff.on('close',r));
}
await browser.close();
