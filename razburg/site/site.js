(function(){
  var btn=document.querySelector('.menu-btn'),nav=document.getElementById('nav');
  if(btn&&nav){btn.addEventListener('click',function(){var o=nav.classList.toggle('open');btn.setAttribute('aria-expanded',o)});}
  var grid=document.getElementById('grid');
  if(grid){
    var items=[].slice.call(grid.children),chips=[].slice.call(document.querySelectorAll('.chip')),q=document.getElementById('q'),count=document.getElementById('count'),f='all';
    function apply(){var t=(q.value||'').trim().toLowerCase(),n=0;items.forEach(function(li){var ok=(f==='all'||li.dataset.kind===f)&&(!t||li.dataset.s.indexOf(t)>-1);li.hidden=!ok;if(ok)n++});count.textContent=n+' of '+items.length+' releases';}
    chips.forEach(function(c){c.addEventListener('click',function(){f=c.dataset.f;chips.forEach(function(x){x.setAttribute('aria-pressed',x===c)});apply()})});
    q.addEventListener('input',apply);apply();
  }
  var form=document.getElementById('contact-form');
  if(form){
    form.addEventListener('submit',function(e){
      var key=form.querySelector('[name=access_key]'),st=form.querySelector('.form-status'),d=new FormData(form);
      if(d.get('botcheck')){e.preventDefault();return;}
      if(!key){
        e.preventDefault();
        var to=form.dataset.email;
        var body='Name: '+d.get('name')+'\nEmail: '+d.get('email')+'\nPhone: '+(d.get('phone')||'')+'\nService: '+d.get('service')+'\n\n'+d.get('message');
        if(to){location.href='mailto:'+to+'?subject='+encodeURIComponent('Project inquiry: '+d.get('service'))+'&body='+encodeURIComponent(body);st.textContent='Opening your email app…';}
        else{st.textContent='The form is not connected yet in this preview.';}
        return;
      }
      e.preventDefault();st.textContent='Sending…';
      fetch(form.action,{method:'POST',body:d,headers:{Accept:'application/json'}}).then(function(r){return r.json()}).then(function(j){st.textContent=j.success?'Thanks, your message was sent. I will get back to you soon.':'Something went wrong. Please call or email instead.';if(j.success)form.reset();}).catch(function(){st.textContent='Something went wrong. Please call or email instead.';});
    });
  }
})();
