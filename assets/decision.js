'use strict';
const answers={};
document.querySelectorAll('.choice button').forEach(btn=>btn.addEventListener('click',()=>{
 const parent=btn.closest('[data-question]'),q=parent.dataset.question;
 answers[q]=btn.dataset.value;parent.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',b===btn?'true':'false'));
 const output=document.getElementById('decision-output');
 if(!answers.unit||!answers.evidence||!answers.axes){output.innerHTML='<h2>Keep going</h2><p>Complete all three questions to see a recommendation and its caveats.</p>';return;}
 let method,reason,caveat;
 if(answers.unit==='directed'){
  method='Begin with a directed flow or exposure model';reason='Your interaction is not an undirected partnership. Reciprocity of partnership ends cannot be imposed without a justified pairwise accounting model.';caveat='Define origin/destination units, population boundaries, and flow conservation constraints appropriate to movement or directed contact.';
 }else if(answers.unit==='network'){
  method='Begin with an explicit or temporal network representation';reason='Persistence and link-level structure matter to the research question. A group-level matrix can still be used to diagnose simulated edge patterns.';caveat='Specify formation and dissolution, degree distributions and concurrency; aggregate reciprocity alone will not identify topology.';
 }else if(answers.evidence==='matrix'){
  method='Begin with an empirical contact or partnership matrix';reason='You have partner-specific observations, so estimate the interactions directly before imposing a parametric preference model.';caveat='Assess sampling, weighting, unobserved partners, demographic transport, and reciprocal reconciliation.';
 }else if(answers.axes==='none'){
  method='Start with joint proportionate mixing';reason='With no strong evidence of assortative selection, Qᵢ=Nᵢcᵢ gives a transparent reciprocal baseline.';caveat='Preserve the joint subgroup distribution; do not replace it with a product of margins unless independence is supported.';
 }else if(answers.axes==='one'){
  method='Compare proportionate and standard preferred mixing';reason='A single exact-group mixture parameter ε offers a transparent partially assortative alternative with automatic reciprocity.';caveat='Exact-group matching is not the same as assortativity by one specific feature when groups combine multiple dimensions.';
 }else{
  method='Compare proportionate, preferred, and balanced two-axis affinities';reason='Separate preferences for activity and context require a joint reciprocal construction, particularly when the subgroup opportunity distribution is correlated.';caveat='The illustrative θ parameters are not ε. Explore range and interaction assumptions; qualitative evidence alone does not estimate numeric values.';
 }
 output.innerHTML='<div class="eyebrow">STARTING STRUCTURE</div><h2>'+method+'</h2><p>'+reason+'</p><p><strong>Check:</strong> '+caveat+'</p><a class="button" href="explorer.html">Compare the matrices →</a>';
}));
