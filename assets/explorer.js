'use strict';
const names=['HP','LP','HV','LV'];
const contexts=['P','P','V','V'];
const activities=['H','L','H','L'];
const presets={original:[[100,4],[200,1],[50,4],[300,1]],independent:[[100,3],[200,1],[100,3],[200,1]],correlated:[[100,8],[200,.5],[50,2],[400,2]]};
const rows=document.getElementById('opportunity-rows');
const state={N:[],c:[],Q:[],M:[],F:[],lastError:null};
for(let i=0;i<4;i++){
 const tr=document.createElement('tr');
 tr.innerHTML=`<th scope="row">${names[i]}</th><td><input type="number" min="1" step="1" id="n-${i}" aria-label="${names[i]} population" value="${presets.original[i][0]}"></td><td><input type="number" min="0.01" step="0.1" id="c-${i}" aria-label="${names[i]} annual rate" value="${presets.original[i][1]}"></td><td id="q-${i}"></td><td id="share-${i}"></td>`;
 rows.appendChild(tr);
}
function goodNumber(x){return Number.isFinite(x)&&x>0;}
function balanceSymmetric(W,Q){
 const n=Q.length;let a=Array(n).fill(1);let converged=false;
 for(let iteration=0;iteration<30000;iteration++){
  const totals=a.map((ai,i)=>ai*W[i].reduce((sum,w,j)=>sum+w*a[j],0));
  const error=Math.max(...totals.map((x,i)=>Math.abs(x-Q[i])/Q[i]));
  if(error<1e-12){converged=true;break;}
  a=a.map((x,i)=>x*Math.sqrt(Q[i]/totals[i]));
 }
 if(!converged)throw new Error('Symmetric balancing did not converge; try less extreme inputs.');
 return W.map((row,i)=>row.map((w,j)=>a[i]*w*a[j]));
}
function calculate(){
 const N=names.map((_,i)=>Number(document.getElementById(`n-${i}`).value));
 const c=names.map((_,i)=>Number(document.getElementById(`c-${i}`).value));
 if(!N.every(goodNumber)||!c.every(goodNumber)){showError('All group sizes and rates must be strictly positive.');return;}
 const Q=N.map((n,i)=>n*c[i]);const T=Q.reduce((a,b)=>a+b,0);
 if(!goodNumber(T)){showError('Invalid opportunity totals.');return;}
 state.N=N;state.c=c;state.Q=Q;
 Q.forEach((q,i)=>{document.getElementById(`q-${i}`).textContent=q.toFixed(1);document.getElementById(`share-${i}`).textContent=(100*q/T).toFixed(1)+'%';});
 const hp=Q[0]/(Q[0]+Q[1]),hv=Q[2]/(Q[2]+Q[3]);
 const same=Math.abs(hp-hv)<1e-10;
 document.getElementById('joint-info').innerHTML=`High-activity share <strong>within physical</strong>: ${(hp*100).toFixed(1)}%; <strong>within virtual</strong>: ${(hv*100).toFixed(1)}%. ${same?'These two distributions match in this example.':'These distributions differ; a product of marginal shares will not recover the correct joint distribution.'}`;
 const e=Number(document.getElementById('epsilon').value),r=Number(document.getElementById('theta-r').value),m=Number(document.getElementById('theta-m').value);
 for(const [id,v] of [['epsilon',e],['theta-r',r],['theta-m',m]])document.getElementById(`${id}-value`).textContent=v.toFixed(2);
 const mode=document.getElementById('mix-mode').value;
 let M,F,note='';
 try {
 if(mode==='proportionate'){
  M=Q.map(()=>Q.map(q=>q/T));note='Every row equals the joint opportunity distribution. This construction is reciprocal for all strictly positive Q.';
 }else if(mode==='preferred'){
  M=Q.map((_,i)=>Q.map((q,j)=>(i===j?e:0)+(1-e)*q/T));note='Exact-match preferred mixing: one ε for matching both activity and context. Reciprocal for any positive Q.';
 }else if(mode==='twoaxis'){
  const W=Q.map((qi,i)=>Q.map((qj,j)=>qi*qj/T*Math.exp(r*(activities[i]===activities[j]?1:0)+m*(contexts[i]===contexts[j]?1:0))));
  F=balanceSymmetric(W,Q);M=F.map((row,i)=>row.map(value=>value/Q[i]));note='Symmetric affinity weights balanced to observed opportunity totals. θ is not ε; reciprocity and normalization follow from constrained balancing.';
 }else{
  const qH=Q[0]+Q[2],qL=Q[1]+Q[3],qP=Q[0]+Q[1],qV=Q[2]+Q[3];
  M=Q.map((_,i)=>Q.map((q,j)=>((activities[i]===activities[j]?e:0)+(1-e)*(activities[j]==='H'?qH:qL)/T)*((contexts[i]===contexts[j]?e:0)+(1-e)*(contexts[j]==='P'?qP:qV)/T)));
  note='Deliberately problematic example: two independently normalized marginal preference kernels are multiplied. Rows sum to one, but partnership flow reciprocity generally fails; when opportunity dimensions are correlated, even ε=0 is not joint proportionate.';
 }
 F=F||M.map((row,i)=>row.map(v=>v*Q[i]));
 state.M=M;state.F=F;state.lastError=null;
 const rowsum=Math.max(...M.map(row=>Math.abs(row.reduce((a,b)=>a+b,0)-1)));
 let mismatch=0;for(let i=0;i<4;i++)for(let j=0;j<4;j++)mismatch=Math.max(mismatch,Math.abs(F[i][j]-F[j][i]));
 const sameJoint=F.reduce((sum,row,i)=>sum+row[i],0)/T;
 const sameActivity=F.reduce((sum,row,i)=>sum+row.reduce((a,v,j)=>a+(activities[i]===activities[j]?v:0),0),0)/T;
 const sameContext=F.reduce((sum,row,i)=>sum+row.reduce((a,v,j)=>a+(contexts[i]===contexts[j]?v:0),0),0)/T;
 document.getElementById('same-group').textContent=(100*sameJoint).toFixed(1)+'%';
 document.getElementById('same-activity').textContent=(100*sameActivity).toFixed(1)+'%';
 document.getElementById('same-context').textContent=(100*sameContext).toFixed(1)+'%';
 const scale=Math.max(1,...Q);
 const nonneg=M.every(row=>row.every(v=>v>=0&&v<=1+1e-9));
 const good=rowsum<1e-9&&mismatch/scale<1e-8&&nonneg;
 document.getElementById('mix-explainer').textContent=note;
 document.getElementById('prob-matrix').innerHTML=tableHTML(M,true);
 document.getElementById('flow-matrix').innerHTML=tableHTML(F,false);
 const status=document.getElementById('matrix-diagnostics');status.classList.toggle('fail',!good);
 status.innerHTML=`<strong>${good?'✓ All mathematical checks passed':'⚠ One or more checks failed'}</strong><dl><dt>Largest row-sum error</dt><dd>${rowsum.toExponential(2)}</dd><dt>Largest flow imbalance</dt><dd>${mismatch.toFixed(5)} ends/year</dd><dt>Valid probabilities</dt><dd>${nonneg?'Yes':'No'}</dd><dt>Reciprocity</dt><dd>${mismatch/scale<1e-8?'Pass':'FAIL'}</dd></dl>`;
 const i=0,j=3;
 document.getElementById('pair-demo').innerHTML=`<div class="toolsplit"><div class="tool-panel"><strong>HP → LV</strong><p>${Q[i].toFixed(1)} × ${(M[i][j]*100).toFixed(2)}% = <strong>${F[i][j].toFixed(3)}</strong> ends/year</p></div><div class="tool-panel"><strong>LV → HP</strong><p>${Q[j].toFixed(1)} × ${(M[j][i]*100).toFixed(2)}% = <strong>${F[j][i].toFixed(3)}</strong> ends/year</p></div></div>`;
 }catch(err){showError(String(err.message||err));}
}
function tableHTML(A,pct){const max=Math.max(...A.flat());let out='<table aria-label="'+(pct?'Mixing probabilities':'Partnership flows')+'"><thead><tr><th>From ↓ / To →</th>'+names.map(x=>'<th>'+x+'</th>').join('')+'</tr></thead><tbody>';
 A.forEach((row,i)=>{out+='<tr><th>'+names[i]+'</th>';row.forEach(v=>{const intensity=max?Math.min(1,v/max):0;out+=`<td style="background:rgba(38,147,139,${(0.05+0.29*intensity).toFixed(3)})">${pct?(100*v).toFixed(1)+'%':v.toFixed(1)}</td>`;});out+='</tr>';});return out+'</tbody></table>';
}
function showError(msg){state.lastError=msg;let s=document.getElementById('matrix-diagnostics');s.classList.add('fail');s.textContent=msg;}
function usePreset(p){presets[p].forEach((x,i)=>{document.getElementById(`n-${i}`).value=x[0];document.getElementById(`c-${i}`).value=x[1];});calculate();}
document.querySelectorAll('input,select').forEach(el=>el.addEventListener('input',calculate));
document.querySelectorAll('[data-preset]').forEach(btn=>btn.addEventListener('click',()=>usePreset(btn.dataset.preset)));
document.getElementById('reset-matrix').addEventListener('click',()=>{document.getElementById('mix-mode').value='proportionate';document.getElementById('epsilon').value=.4;document.getElementById('theta-r').value=.8;document.getElementById('theta-m').value=1.2;usePreset('original');});
document.getElementById('copy-matrix').addEventListener('click',async()=>{
 if(state.lastError||!state.M.length)return;
 const csv=['from,'+names.join(','),...state.M.map((row,i)=>names[i]+','+row.map(x=>x.toFixed(10)).join(','))].join('\n');
 try{await navigator.clipboard.writeText(csv);document.getElementById('copy-matrix').textContent='Copied CSV';}catch(err){const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv'}));a.download='mixing-matrix.csv';a.click();URL.revokeObjectURL(a.href);}
});
calculate();
