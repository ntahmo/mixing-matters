'use strict';
// No tracking, local storage, service workers, or external dependencies.
document.addEventListener('click',event=>{
  const btn=event.target.closest('[data-copy]');
  if(btn&&navigator.clipboard){navigator.clipboard.writeText(btn.dataset.copy).then(()=>{btn.textContent='Copied';}).catch(()=>{});}
});
