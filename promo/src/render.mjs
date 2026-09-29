// Uso: node render.mjs preview <v|h> t1 t2 ...   |   node render.mjs full <v|h> <ffmpeg> <out.mp4>
import { chromium } from 'playwright';
import { spawn } from 'child_process';
const [mode,ar]=process.argv.slice(2);const H=ar==='h';
const vp=H?{width:1920,height:1080}:{width:1080,height:1920};
const browser=await chromium.launch({args:['--allow-file-access-from-files','--font-render-hinting=none']});
const page=await browser.newPage({viewport:vp});
page.on('pageerror',e=>console.log('ERR',e.message));
await page.goto('file://'+process.cwd()+'/video/index.html'+(H?'?h':''));
await page.evaluate(()=>window.ready);
if(mode==='preview'){
 for(const t of process.argv.slice(4).map(Number)){await page.evaluate(t=>render(t),t);await page.screenshot({path:`prev_${ar}_${t}.jpg`,type:'jpeg',quality:70});}
}else{
 const [ffmpeg,out]=process.argv.slice(4);const FPS=30,N=20*FPS;
 const ff=spawn(ffmpeg,['-y','-loglevel','error','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-','-i','music.wav',
  '-c:v','libx264','-pix_fmt','yuv420p','-preset','slow','-crf','18','-profile:v','high','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',out],{stdio:['pipe','inherit','inherit']});
 for(let i=0;i<N;i++){await page.evaluate(t=>render(t),i/FPS);const b=await page.screenshot({type:'jpeg',quality:95});
  if(!ff.stdin.write(b))await new Promise(r=>ff.stdin.once('drain',r))}
 ff.stdin.end();await new Promise(r=>ff.on('close',r));
}
await browser.close();
