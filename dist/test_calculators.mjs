import fs from 'node:fs'; import vm from 'node:vm'; import assert from 'node:assert/strict';
const code=fs.readFileSync(new URL('./calculators.js',import.meta.url),'utf8'); const ctx={console}; vm.createContext(ctx); vm.runInContext(code,ctx); const T=ctx.PhysicsTools;
assert.equal(T.catalogue.length,24); assert.equal(Object.keys(T.constants).length,13);
for(const c of T.catalogue){ const x=T.compute(c.id,{}); assert(x.results.length>0,c.id); for(const z of x.results) assert(Number.isFinite(z.value),`${c.id} ${z.label}`); if(x.plot){assert(x.plot.series.length);for(const q of x.plot.series)for(const [a,b] of q.points)assert(Number.isFinite(a)&&Number.isFinite(b),c.id)} }
const get=(id,vals,label)=>T.compute(id,vals).results.find(x=>x.label===label).value;
assert(Math.abs(get('kinematics',{u:0,a:10,t:2},'Displacement')-20)<1e-12);
assert(Math.abs(get('projectile',{v:10,theta:45,h:0,g:10},'Range')-10)<1e-12);
assert(Math.abs(get('gravity',{M:1,m:1,r:1},'Force')-T.constants.G)<1e-20);
assert(Math.abs(get('circuit',{V:-12,R:3},'Current')+4)<1e-12);
assert(Math.abs(get('coulomb',{q1:1,q2:-1,r:1},'Force (signed)')+T.constants.ke)<1e-8*T.constants.ke);
assert(Math.abs(get('decay',{N0:100,halfLife:2,t:2},'Remaining count')-50)<1e-10);
const q=T.compute('quantum_well',{massMultiplier:1,L:10,n:2});const pts=q.plot.series[0].points;let area=0;for(let i=1;i<pts.length;i++)area+=(pts[i][1]+pts[i-1][1])*(pts[i][0]-pts[i-1][0])/2;assert(Math.abs(area-1)<0.002);
assert.throws(()=>T.compute('circuit',{V:'',R:1}),/finite/);assert.throws(()=>T.compute('circuit',{V:1,R:0}),/greater than 0/);assert.throws(()=>T.compute('projectile',{v:1,theta:91}),/between/);assert.throws(()=>T.compute('lens',{f:1,do:1}),/singular/);assert.throws(()=>T.compute('lorentz',{v:T.constants.c}),/below c/);assert.throws(()=>T.compute('de_broglie',{m:1,v:Infinity}),/finite/);assert.throws(()=>T.compute('schwarzschild',{M:1.989e30,r:1e3}),/Schwarzschild/);
// Regression checks for numerical stability, validation, and interpretation notes.
assert(Math.abs(get('rlc',{R:2,L:8,C:2,f:1,Vrms:1},'Quality factor')-1)<1e-12);
const low=T.compute('relativity',{beta:1e-8,m:1,properTime:1,properLength:1}).results.find(x=>x.label==='Kinetic energy').value;
assert(Math.abs(low-(0.5*T.constants.c*T.constants.c*1e-16)) < 1e-8*T.constants.c*T.constants.c*1e-16);
const vertical=T.compute('projectile',{v:10,theta:90,h:0,g:10}); assert(vertical.plot.series[0].points.length>1);
assert(Math.abs(get('rc',{R:1,C:1,V:1,t:1e-10},'Capacitor voltage')-(-Math.expm1(-1e-10)))<1e-20);
assert.throws(()=>T.compute('circuit',{V:null,R:1}),/finite/);
assert.throws(()=>T.compute('circuit',{V:true,R:1}),/finite/);
assert.throws(()=>T.compute('toString',{}),/Unknown calculator/);
const signed=T.compute('coulomb',{q1:1,q2:-1,r:1}); assert(signed.warnings.some(x=>/attractive/.test(x)));
const zeroDecay=T.compute('decay',{N0:0,halfLife:2,t:1}); assert(!zeroDecay.results.some(x=>x.label==='Fraction remaining')); assert(zeroDecay.warnings.some(x=>/undefined/.test(x)));
const noMin=T.compute('diffraction',{wavelength:20000,slit:1,L:1}); assert.equal(noMin.results.length,0); assert(noMin.warnings.some(x=>/no first minimum/.test(x)));
for(const c of T.catalogue){const x=T.compute(c.id,{});assert(x.steps.length>=3,c.id);}
// Independent geometry and weak-field limits prevent plausible-looking wrong plots.
const wide=T.compute('diffraction',{wavelength:500,slit:1,L:1});
const point=wide.plot.series[0].points.at(-1);const sine=point[0]/Math.hypot(1,point[0]);const alpha=2*Math.PI*sine;
assert(Math.abs(point[1]-(Math.sin(alpha)/alpha)**2)<1e-13);
const dropped=T.compute('projectile',{v:0,theta:90,h:10,g:10});assert.equal(dropped.plot.series[0].points.length,81);
assert(Math.abs(dropped.plot.series[0].points.at(-1)[1])<1e-12);
const highDensity=T.compute('quantum_well',{n:50}).plot.series[0].points;let norm=0;for(let i=1;i<highDensity.length;i++)norm+=(highDensity[i][1]+highDensity[i-1][1])*(highDensity[i][0]-highDensity[i-1][0])/2;assert(Math.abs(norm-1)<1e-10);
const weak=T.compute('schwarzschild',{M:1,r:1});assert(weak.results.find(x=>x.label==='Gravitational redshift').value>0);
assert(Math.abs(get('quantum_well',{n:2},'Energy')/get('quantum_well',{n:1},'Energy')-4)<1e-12);
console.log(`PASS: ${T.catalogue.length} calculators; analytic values, physical limits, normalization, unit conversions, and input/plot edge cases.`);
