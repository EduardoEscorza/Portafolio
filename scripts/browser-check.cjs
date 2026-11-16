const fs = require('node:fs');
const assert = require('node:assert/strict');
const path = require('node:path');
process.chdir(path.resolve(__dirname, '..'));
(async () => {
  const tabs = await (await fetch('http://127.0.0.1:9223/json')).json();
  const ws = new WebSocket(tabs.find(t => t.type === 'page').webSocketDebuggerUrl);
  await new Promise(resolve => ws.addEventListener('open', resolve, { once: true }));
  let id = 0; const pending = new Map(); const errors = [];
  ws.addEventListener('message', event => {
    const m = JSON.parse(event.data);
    if (pending.has(m.id)) { const p = pending.get(m.id); pending.delete(m.id); m.error ? p.reject(m.error) : p.resolve(m.result); }
    if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.text);
  });
  const call = (method, params = {}) => new Promise((resolve, reject) => { const key = ++id; pending.set(key, { resolve, reject }); ws.send(JSON.stringify({ id: key, method, params })); });
  const evaluate = async expression => {
    const r = await call('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
    assert.ok(!r.exceptionDetails, JSON.stringify(r.exceptionDetails));
    return r.result.value;
  };
  const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
  const navigate = async path => { await call('Page.navigate', { url: 'http://127.0.0.1:8765/' + path }); await delay(250); };
  const images = () => evaluate(`Promise.all([...document.images].map(async im => { im.loading='eager'; try { await im.decode(); return null; } catch { return im.getAttribute('src'); } })).then(r => r.filter(Boolean))`);
  await call('Page.enable'); await call('Runtime.enable');
  for (const [name,width,height,cols,serviceCols] of [['desktop-1080p',1920,1080,3,4],['desktop',1440,1000,3,4],['tablet',820,1100,2,2],['mobile',390,844,1,1],['small-mobile',320,740,1,1]]) {
    await call('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: width < 700 });
    await navigate('');
    assert.deepEqual(await images(), []);
    const state = await evaluate(`(() => { const box=s=>document.querySelector(s).getBoundingClientRect();const text=box('.hero-in'),scene=box('.hero-visual');return {width:innerWidth,scroll:document.documentElement.scrollWidth,columns:getComputedStyle(document.querySelector('.grid')).gridTemplateColumns.split(' ').length,services:getComputedStyle(document.querySelector('.services-grid')).gridTemplateColumns.split(' ').length,photosInHero:document.querySelectorAll('.hero .contact-photo,.hero #foto,.hero .hero-bg').length,cards:document.querySelectorAll('.project').length,overlap:Math.min(text.right,scene.right)>Math.max(text.left,scene.left)&&Math.min(text.bottom,scene.bottom)>Math.max(text.top,scene.top),sceneHeight:box('.scene-stage').height,photoRatio:box('#foto').width/box('#foto').height}; })()`);
    console.log(name, state);
    assert.ok(state.scroll <= width); assert.equal(state.columns,cols); assert.equal(state.services,serviceCols); assert.equal(state.photosInHero,0); assert.equal(state.cards,9); assert.equal(state.overlap,false); assert.ok(Math.abs(state.photoRatio-.75)<.01);
    if (width < 1051) {
      await evaluate(`document.querySelector('.burger').click()`);
      assert.equal(await evaluate(`document.querySelector('.burger').getAttribute('aria-expanded')`), 'true');
      await call('Input.dispatchKeyEvent', { type:'keyDown', key:'Escape', code:'Escape', windowsVirtualKeyCode:27 });
      assert.equal(await evaluate(`document.querySelector('.burger').getAttribute('aria-expanded')`), 'false');
      assert.equal(await evaluate(`document.activeElement.className`), 'burger');
      await evaluate(`document.querySelector('.burger').click();document.querySelector('#menu a[href="#contacto"]').click()`);
      assert.equal(await evaluate(`document.querySelector('.burger').getAttribute('aria-expanded')`),'false');
    }
    assert.equal(await evaluate(`document.querySelectorAll('.cert').length`),6);
    assert.equal(await evaluate(`document.querySelectorAll('#toolkit .tool').length`),33);
    assert.equal(await evaluate(`document.querySelectorAll('.section-heading .eyebrow').length`),0);
    if(width===1920) {
      assert.ok(await evaluate(`document.querySelector('.hero').getBoundingClientRect().width`) >= 1400);
      assert.ok(await evaluate(`parseFloat(getComputedStyle(document.querySelector('.project-description')).fontSize)`) >= 15);
    }
    // Static entry text and the photo's relocation are independent of animations.
    assert.equal(await evaluate(`document.querySelector('#hero-title').textContent`), 'Eduardo Escorza');
    assert.equal(await evaluate(`document.querySelector('.hero-role').textContent`), 'Full Stack Developer');
    const trackBefore = await evaluate(`document.querySelector('#certificate-track').scrollLeft`);
    await evaluate(`document.querySelector('.nav-btn[data-dir="1"]').click()`);await delay(600);
    assert.ok(await evaluate(`document.querySelector('#certificate-track').scrollLeft`) > trackBefore);
    await evaluate(`document.querySelector('#certificate-track').focus();document.querySelector('#certificate-track').dispatchEvent(new KeyboardEvent('keydown',{key:'Home',bubbles:true}))`); await delay(600);
    assert.ok(await evaluate(`document.querySelector('#certificate-track').scrollLeft`) <= 2);
    await evaluate(`document.activeElement.blur();scrollTo({top:0,behavior:'instant'})`);await delay(300);
  }
  // A real touch gesture over the scene must scroll the page, never capture a drag.
  await call('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:1,mobile:true});
  await call('Emulation.setTouchEmulationEnabled',{enabled:true,maxTouchPoints:1});await navigate('');
  await evaluate(`document.querySelector('.scene-stage').scrollIntoView({block:'center',behavior:'instant'})`);await delay(200);
  const touchBox=await evaluate(`(()=>{const r=document.querySelector('.scene-stage').getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2,scroll:scrollY}})()`);
  await call('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:touchBox.x,y:touchBox.y}]});
  for(let i=1;i<=5;i++) { await call('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:touchBox.x,y:touchBox.y-i*24}]});await delay(25); }
  await call('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await delay(300);
  assert.ok(await evaluate(`scrollY`) > touchBox.scroll + 20);
  assert.equal(await evaluate(`document.querySelector('.scene-stage').classList.contains('dragging')`),false);
  await evaluate(`document.querySelector('#contacto').scrollIntoView({block:'start',behavior:'instant'})`);await delay(100);
  await call('Emulation.setTouchEmulationEnabled',{enabled:false});
  await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});await navigate('');
  await evaluate(`document.querySelector('.scene-stage').dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}))`);await delay(100);
  assert.equal(await evaluate(`document.querySelector('.scene-model').style.getPropertyValue('--yaw')`),'-11deg');
  await evaluate(`for(let i=0;i<30;i++)document.querySelector('.scene-stage').dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}))`);await delay(100);
  assert.ok(parseFloat(await evaluate(`document.querySelector('.scene-model').style.getPropertyValue('--yaw')`))<=3);
  await evaluate(`document.querySelector('.scene-stage').dispatchEvent(new KeyboardEvent('keydown',{key:'Home',bubbles:true}))`);await delay(100);
  assert.equal(await evaluate(`document.querySelector('.scene-model').style.getPropertyValue('--yaw')`),'-15deg');
  // Drag stays bounded, then returns to the neutral angle.
  const stage = await evaluate(`(()=>{const r=document.querySelector('.scene-stage').getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}})()`);
  await call('Input.dispatchMouseEvent',{type:'mousePressed',x:stage.x,y:stage.y,button:'left',clickCount:1});
  await call('Input.dispatchMouseEvent',{type:'mouseMoved',x:stage.x+160,y:stage.y+70,button:'left',buttons:1});await delay(80);
  let yaw=parseFloat(await evaluate(`document.querySelector('.scene-model').style.getPropertyValue('--yaw')`));assert.ok(yaw<=3&&yaw>=-33);
  await call('Input.dispatchMouseEvent',{type:'mouseReleased',x:stage.x+160,y:stage.y+70,button:'left',clickCount:1});await delay(100);
  assert.equal(await evaluate(`document.querySelector('.scene-model').style.getPropertyValue('--yaw')`),'-15deg');
  await call('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]});
  assert.equal(await evaluate(`getComputedStyle(document.documentElement).scrollBehavior`),'auto');
  assert.equal(await evaluate(`getComputedStyle(document.querySelector('.scene-float')).animationName`),'none');
  assert.equal(await evaluate(`document.querySelectorAll('canvas').length`),0);
  // Direct navigation and reload work for every published project, including mobile layout.
  const data=JSON.parse(fs.readFileSync('scripts/content.json','utf8'));
  for(const project of data.projects.filter(p=>p.published)) {
    await call('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:1,mobile:true});
    await navigate('');
    await evaluate(`document.querySelector('a.text-link[href="proyectos/${project.slug}.html"]').click()`);
    await delay(250);
    assert.ok(await evaluate(`location.pathname.endsWith('/proyectos/${project.slug}.html')`));
    await call('Page.reload');await delay(150);
    assert.equal(await evaluate(`document.querySelector('h1').textContent`),project.title);
    assert.equal(await evaluate(`document.querySelectorAll('.detail-panel').length`),3+(project.result?1:0)+(project.status?1:0));
    assert.ok(await evaluate(`document.documentElement.scrollWidth<=innerWidth`));
    assert.deepEqual(await images(),[]);
    assert.equal(await evaluate(`document.querySelector('.project-role').textContent`),project.role);
    await evaluate(`document.querySelector('.detail-back a').click()`);await delay(250);
    assert.ok(await evaluate(`location.hash==='#proyectos'`));
    assert.equal(await evaluate(`document.querySelectorAll('.project').length`),9);
    await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
    await navigate('proyectos/'+project.slug+'.html');
    assert.ok(await evaluate(`document.documentElement.scrollWidth<=innerWidth`));
  }
  // The portfolio remains navigable with JavaScript disabled.
  await call('Emulation.setScriptExecutionDisabled',{value:true});await navigate('');
  assert.equal(await evaluate(`document.querySelectorAll('.project').length`),9);
  await call('Emulation.setScriptExecutionDisabled',{value:false});
  assert.deepEqual(errors,[]);
  console.log('PASS: responsive layouts, no overlap/overflow, all images, menu/Escape, carousel controls/keyboard, bounded scene and reset, reduced motion, direct project reloads, static content without JS.');
  ws.close();
})().catch(error=>{console.error(error);process.exit(1)});
