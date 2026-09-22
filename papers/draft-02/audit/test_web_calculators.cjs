const fs=require('node:fs');const vm=require('node:vm');const assert=require('node:assert/strict');
const html=fs.readFileSync(require('node:path').join(__dirname,'..','calculators.html'),'utf8');
const code=html.match(/<script id="calculator-core">([\s\S]*?)<\/script>/)[1];
const c=vm.createContext({});vm.runInContext(code,c);let count=0;
function test(name,f){f();count++;}
test('Gaussian cap is below rational certificate',()=>assert(c.gaussian(35/1664,4)<626/1629));
test('Gaussian envelope coefficient is capped at one',()=>assert.equal(c.gaussian(0,.1),1));
test('Triangle exact cap agrees',()=>assert(Math.abs(c.triangular(.001)-2072/2997)<1e-15));
test('Both endpoints start at one',()=>{const w=c.wilson(0);assert(Math.abs(w.x-1)<1e-15);assert(Math.abs(w.re-1)<1e-15);assert.equal(w.im,0);});
test('Stable small endpoint deficits',()=>{const a=c.wilson(1e-6);assert(a.dx>0&&a.dx<2e-16);assert(a.dp>0&&a.dp<3e-16);assert(a.im>1e-8&&a.im<1.2e-8);});
test('Numerical allowance is separately charged',()=>assert(c.heat(1e-8)>c.heat(0)&&c.heat(1e-8)<.000037));
for(const call of [()=>c.gaussian(-.1,4),()=>c.gaussian(.1,4),()=>c.gaussian(0,0),()=>c.gaussian(0,Infinity),()=>c.triangular(.002),()=>c.wilson(NaN),()=>c.wilson(-1e-6),()=>c.wilson(.2),()=>c.heat(-1)])test('Reject invalid input',()=>assert.throws(call));
console.log(JSON.stringify({status:'passed',count,scope:'Standalone web calculator formula and invalid-input tests; not new theorem proofs'},null,2));
