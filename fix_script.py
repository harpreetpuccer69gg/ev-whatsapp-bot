import re, json, sys
sys.path.insert(0,'.')
from translations import HI, BN, KN

c = open('app/static/index.html', encoding='utf-8', errors='replace').read()
start = c.rfind('<script>')
html_only = c[:start]

def t(d):
    return '{' + ','.join(f"'{k}':'{v}'" for k,v in d.items()) + '}'

hi_js = t(HI)
bn_js = t(BN)
kn_js = t(KN)

new_script = """<script>
const T = {
  en:{heroTitle:'Find the Best <span>EV Rentals</span> for Delivery Riders',heroSub:'Affordable weekly plans | Instant booking | Vendor support',heroBadge:'For Delivery Riders',cityLabel:'1. Select City',cityHint:'Choose your delivery city.',budgetLabel:'2. Weekly Budget',b1:'Below Rs.1000',b2:'Per week',b3:'Per week',b4:'Above Rs.2000',findBtn:'Find EVs',sheetTitle:'Confirm Your Details',namePh:'Your Name',phonePh:'Mobile Number',confirmBtn:'Confirm & Request',successTitle:'Request Submitted!',successMsg:'Vendor will contact you within <strong>24 hours</strong>.',noRes:'No EVs found in {city}.',foundText:'{count} EVs found in {city}',cityDef:'-- Select city --'},
  hi:""" + hi_js + """,
  bn:""" + bn_js + """,
  kn:""" + kn_js + """
};

let lang='en', budget=null, vendors=[], selVendor=null;
const BR={'1':[0,1000],'2':[1000,1500],'3':[1500,2000],'4':[2000,99999]};
const IMGS={'hi-speed':'/static/images/ev_hi_speed.svg','low-speed':'/static/images/ev_low_speed.svg','e-cycle':'/static/images/ev_e_cycle.svg'};

fetch('/vendors').then(r=>r.json()).then(d=>{vendors=Array.isArray(d)?d:[];}).catch(()=>{vendors=[];});

const TOTAL_SLIDES=3;
let curSlide=0;
function goSlide(n){
  curSlide=(n+TOTAL_SLIDES)%TOTAL_SLIDES;
  document.getElementById('heroSlides').style.transform='translateX(-'+curSlide*100+'%)';
  document.querySelectorAll('.hero-dot').forEach((d,i)=>d.classList.toggle('active',i===curSlide));
}
setInterval(()=>goSlide(curSlide+1),10000);

// Manual swipe - iOS compatible
let touchStartX=0,touchStartY=0;
window.addEventListener('load',()=>{
  const heroEl=document.getElementById('heroSlides');
  if(!heroEl)return;
  heroEl.addEventListener('touchstart',e=>{touchStartX=e.touches[0].clientX;touchStartY=e.touches[0].clientY;},{passive:true});
  heroEl.addEventListener('touchmove',e=>{
    if(Math.abs(e.touches[0].clientX-touchStartX)>Math.abs(e.touches[0].clientY-touchStartY))e.preventDefault();
  },{passive:false});
  heroEl.addEventListener('touchend',e=>{
    const dx=touchStartX-e.changedTouches[0].clientX;
    const dy=Math.abs(touchStartY-e.changedTouches[0].clientY);
    if(Math.abs(dx)>30&&dy<80)goSlide(dx>0?curSlide+1:curSlide-1);
  },{passive:true});
});

function closeIntro(){
  const city=document.getElementById('introCity').value;
  if(!city){alert('Please select your city');return;}
  document.getElementById('introBox').classList.add('hide');
  setTimeout(()=>{
    document.getElementById('introOverlay').style.display='none';
    document.getElementById('citySelect').value=city;
    document.getElementById('langSel').value=lang;
    checkReady();
  },300);
}

function closeSuccess(){
  document.getElementById('successOverlay').classList.remove('show');
  window.scrollTo({top:0,behavior:'smooth'});
}

function setLang(l){
  lang=l;const t=T[l]||T.en;
  document.getElementById('heroBadge').innerText=t.heroBadge;
  document.getElementById('heroTitle').innerHTML=t.heroTitle;
  document.getElementById('heroSub').innerText=t.heroSub;
  document.getElementById('cityLabel').innerHTML='<span style="width:3px;height:16px;background:#ffd600;border-radius:2px;display:inline-block;margin-right:8px;"></span>'+t.cityLabel;
  document.getElementById('cityHint').innerText=t.cityHint;
  document.getElementById('budgetLabel').innerHTML='<span style="width:3px;height:16px;background:#ffd600;border-radius:2px;display:inline-block;margin-right:8px;"></span>'+t.budgetLabel;
  document.getElementById('b1').innerText=t.b1;
  document.getElementById('b2').innerText=t.b2;
  document.getElementById('b3').innerText=t.b3;
  document.getElementById('b4').innerText=t.b4;
  document.getElementById('findBtn').innerText=t.findBtn;
  document.getElementById('riderName').placeholder=t.namePh;
  document.getElementById('riderPhone').placeholder=t.phonePh;
  document.getElementById('confirmBtn').innerText=t.confirmBtn;
  document.getElementById('sheetTitle').innerText=t.sheetTitle;
  document.getElementById('citySelect').options[0].text=t.cityDef;
}

function setBudget(el,v){
  el.classList.toggle('active');
  const active=[...document.querySelectorAll('.bchip.active')].map(b=>b.dataset.budget);
  budget=active.length===0||active.length===4?null:active;
  checkReady();
}

function checkReady(){
  const city=document.getElementById('citySelect').value;
  document.getElementById('findBtn').disabled=!city;
}

function parseRent(s){
  if(!s)return null;
  const n=String(s).match(/[0-9]+/g);
  return n?parseInt(n[0]):null;
}

function findEVs(){
  const city=document.getElementById('citySelect').value;
  const live=['live','live from next week','minutes wip'];
  const budgetSelected = budget && budget.length > 0;
  let res=vendors.filter(v=>{
    if((v.City||'').toLowerCase()!==city.toLowerCase())return false;
    if(!live.includes((v.Status||'').toLowerCase()))return false;
    if(budgetSelected){
      const r=parseRent(v['Approx Rental/Week']);
      const match=budget.some(b=>{
        const [bMin,bMax]=BR[b];
        return r!==null&&r>=bMin&&r<=bMax;
      });
      if(!match)return false;
    }
    return true;
  });
  const box=document.getElementById('resultsArea');
  if(!res.length){
    if(budgetSelected){
      box.innerHTML='<div class="no-res"><div style="font-size:36px;margin-bottom:10px;">😔</div><div style="font-weight:800;color:#002d62;font-size:15px;margin-bottom:6px;">No EVs available in '+city+' for this budget</div><div style="font-size:13px;color:#9e9e9e;">Try a higher budget or check other cities.</div></div>';
    } else {
      box.innerHTML='<div class="no-res">No EVs found in '+city+'.</div>';
    }
    return;
  }
  renderResults(res,city);
}

function renderResults(list,city){
  const t=T[lang]||T.en;
  const box=document.getElementById('resultsArea');
  if(!list.length){box.innerHTML='<div class="no-res">'+t.noRes.replace('{city}',city)+'</div>';return;}
  let html='<div class="results-hdr">'+t.foundText.replace('{count}',list.length).replace('{city}',city)+'</div>';
  html+='<input class="search-bar" id="searchBar" placeholder="Search vendor or bike..." oninput="renderCards()" />';
  html+='<div class="results-toolbar">';
  html+='<button class="type-chip active" onclick="setType(this,\'all\')">All</button>';
  html+='<button class="type-chip" onclick="setType(this,\'hi-speed\')">Hi-Speed</button>';
  html+='<button class="type-chip" onclick="setType(this,\'low-speed\')">Low Speed</button>';
  html+='<button class="type-chip" onclick="setType(this,\'e-cycle\')">E-Cycle</button>';
  html+='<button class="sort-btn" id="sortBtn" onclick="toggleSort()">Price: Low to High</button>';
  html+='</div><div id="evList"></div>';
  box.innerHTML=html;
  box._list=list;
  box._sort='asc';
  box._type='all';
  renderCards();
  box.scrollIntoView({behavior:'smooth'});
}

function renderCards(){
  const box=document.getElementById('resultsArea');
  if(!box||!box._list)return;
  let list=[...box._list];
  const q=((document.getElementById('searchBar')||{}).value||'').toLowerCase();
  const type=box._type||'all';
  const sort=box._sort||'asc';
  if(q)list=list.filter(v=>(v.Make||'').toLowerCase().includes(q)||(v.Vendor||'').toLowerCase().includes(q));
  if(type!=='all')list=list.filter(v=>{
    const r=(v.Type||'').toLowerCase();
    if(type==='hi-speed')return r.includes('hi');
    if(type==='low-speed')return r.includes('low');
    return r.includes('cycle');
  });
  list.sort((a,b)=>{
    const ra=parseRent(a['Approx Rental/Week'])||0,rb=parseRent(b['Approx Rental/Week'])||0;
    return sort==='asc'?ra-rb:rb-ra;
  });
  const evList=document.getElementById('evList');
  if(!evList)return;
  if(!list.length){evList.innerHTML='<div class="no-res">No results found.</div>';return;}
  let html='';
  list.forEach((v)=>{
    const raw=(v.Type||'').toLowerCase();
    const tk=raw.includes('hi')?'hi-speed':raw.includes('low')?'low-speed':'e-cycle';
    const bc=tk==='hi-speed'?'badge-hi':tk==='low-speed'?'badge-lo':'badge-ec';
    const bl=tk==='hi-speed'?'Hi-Speed':tk==='low-speed'?'Low Speed':'E-Cycle';
    const img=v.Image&&!v.Image.includes('ev_hi')&&!v.Image.includes('ev_lo')&&!v.Image.includes('ev_e')?v.Image:IMGS[tk];
    const idx=box._list.indexOf(v);
    html+='<div class="ev-card">'
      +'<div class="ev-img-wrap"><img src="'+img+'" onerror="this.src=\\''+IMGS[tk]+'\\'"/></div>'
      +'<div class="ev-card-body"><span class="ev-badge '+bc+'">'+bl+'</span>'
      +'<div class="ev-name">'+(v.Make||'EV')+' - '+(v.Vendor||'')+'</div>'
      +'<div class="ev-meta">'
      +'<div class="ev-meta-item">Range <span>'+(v['Range (Km)']||'N/A')+' km</span></div>'
      +'<div class="ev-meta-item">Charge <span>'+(v['Charging/Swap']||'N/A')+'</span></div>'
      +'<div class="ev-meta-item">Deposit <span>'+(v['Security Deposit']||'NIL')+'</span></div>'
      +'</div></div>'
      +'<div class="ev-card-bot"><div class="ev-price"><small>Weekly rental</small>'+(v['Approx Rental/Week']||'N/A')+'</div>'
      +'<button class="book-btn" onclick="openSheet('+idx+')">Book Now</button></div></div>';
  });
  evList.innerHTML=html;
}

function setType(el,type){
  document.querySelectorAll('.type-chip').forEach(c=>c.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('resultsArea')._type=type;
  renderCards();
}

function toggleSort(){
  const box=document.getElementById('resultsArea');
  const btn=document.getElementById('sortBtn');
  if(box._sort==='asc'){box._sort='desc';btn.innerText='Price: High to Low';btn.classList.add('active');}
  else{box._sort='asc';btn.innerText='Price: Low to High';btn.classList.remove('active');}
  renderCards();
}

function openSheet(i){
  selVendor=document.getElementById('resultsArea')._list[i];
  openDetail(selVendor);
}

function openDetail(v){
  selVendor=v;
  const tk=(v.Type||'').toLowerCase().includes('hi')?'hi-speed':(v.Type||'').toLowerCase().includes('low')?'low-speed':'e-cycle';
  const bc=tk==='hi-speed'?'badge-hi':tk==='low-speed'?'badge-lo':'badge-ec';
  const bl=tk==='hi-speed'?'Hi-Speed':tk==='low-speed'?'Low Speed':'E-Cycle';
  const img=v.Image&&!v.Image.includes('ev_hi')&&!v.Image.includes('ev_lo')&&!v.Image.includes('ev_e')?v.Image:IMGS[tk];
  document.getElementById('detailImg').src=img;
  document.getElementById('detailHeaderTitle').innerText=(v.Make||'EV')+' - '+(v.Vendor||'');
  document.getElementById('detailName').innerText=(v.Make||'EV')+' - '+(v.Vendor||'');
  const badge=document.getElementById('detailBadge');
  badge.className='detail-badge ev-badge '+bc;
  badge.innerText=bl;
  document.getElementById('detailPrice').innerText=v['Approx Rental/Week']||'N/A';
  document.getElementById('detailCity').innerText=v.City||'';
  document.getElementById('detailRange').innerText=(v['Range (Km)']||'N/A')+' km';
  document.getElementById('detailCharge').innerText=v['Charging/Swap']||'N/A';
  document.getElementById('detailDeposit').innerText=v['Security Deposit']||'NIL';
  document.getElementById('detailRefund').innerText=v['Refundable Deposit']||'NIL';
  const page=document.getElementById('detailPage');
  page.style.display='block';
  page.style.transform='translateX(100%)';
  page.style.transition='transform 0.3s ease';
  setTimeout(()=>page.style.transform='translateX(0)',10);
  window.scrollTo(0,0);
}

function closeDetail(){
  const page=document.getElementById('detailPage');
  page.style.transform='translateX(100%)';
  setTimeout(()=>page.style.display='none',300);
}

function openDetailPopup(){
  const v=selVendor;
  const tk=(v.Type||'').toLowerCase().includes('hi')?'hi-speed':(v.Type||'').toLowerCase().includes('low')?'low-speed':'e-cycle';
  const img=v.Image&&!v.Image.includes('ev_hi')&&!v.Image.includes('ev_lo')&&!v.Image.includes('ev_e')?v.Image:IMGS[tk];
  document.getElementById('dpopImg').src=img;
  document.getElementById('dpopName').innerText=(v.Make||'EV')+' - '+(v.Vendor||'');
  document.getElementById('dpopPrice').innerText='Weekly: '+(v['Approx Rental/Week']||'N/A');
  document.getElementById('dpopOverlay').classList.add('show');
}

function closeDetailPopup(){
  document.getElementById('dpopOverlay').classList.remove('show');
}

function submitDetailLead(){
  const name=document.getElementById('dpopName2').value.trim();
  const phone=document.getElementById('dpopPhone').value.trim();
  if(!name||!phone){alert('Please enter name and phone.');return;}
  if(phone.length!==10){alert('Please enter a valid 10-digit mobile number.');return;}
  const btn=document.getElementById('dpopBtn');
  btn.innerText='Submitting...';
  btn.disabled=true;
  const v=selVendor;
  fetch('/submit-lead',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({
    name,phone,city:v.City||'',lang,budget,
    vendor:v.Vendor,make:v.Make,type:v.Type,
    rental:v['Approx Rental/Week'],security_deposit:v['Security Deposit'],
    refundable_deposit:v['Refundable Deposit'],
    spoc_name:v.SPOC,spoc_phone:v.Phone,image:v.Image||''
  })}).finally(()=>{
    btn.innerText='Confirm & Request';
    btn.disabled=false;
    closeDetailPopup();
    closeDetail();
    const t=T[lang]||T.en;
    document.getElementById('successTitle').innerText=t.successTitle;
    document.getElementById('successMsg').innerHTML=t.successMsg;
    document.getElementById('successOverlay').classList.add('show');
  });
}

function yuvwaaClick(){
  const yuvwaa=vendors.find(v=>v.Vendor==='YuvwaaSpeed');
  if(yuvwaa)openDetail(yuvwaa);
}
function bounceClick(){
  const bigo=vendors.find(v=>v.Vendor==='BiGO');
  if(bigo)openDetail(bigo);
}
function closeSheet(){
  document.getElementById('overlay').classList.remove('show');
  document.getElementById('sheet').classList.remove('show');
}

function submitLead(){
  const name=document.getElementById('riderName').value.trim();
  const phone=document.getElementById('riderPhone').value.trim();
  if(!name||!phone){alert('Please enter name and phone.');return;}
  if(phone.length!==10){alert('Please enter a valid 10-digit mobile number.');return;}
  const btn=document.getElementById('confirmBtn');
  btn.innerText='Submitting...';
  btn.disabled=true;
  fetch('/submit-lead',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({
    name,phone,city:document.getElementById('citySelect').value,lang,budget,
    vendor:selVendor&&selVendor.Vendor,make:selVendor&&selVendor.Make,type:selVendor&&selVendor.Type,
    rental:selVendor&&selVendor['Approx Rental/Week'],security_deposit:selVendor&&selVendor['Security Deposit'],
    refundable_deposit:selVendor&&selVendor['Refundable Deposit'],
    spoc_name:selVendor&&selVendor.SPOC,spoc_phone:selVendor&&selVendor.Phone,image:(selVendor&&selVendor.Image)||''
  })}).finally(()=>{
    btn.innerText='Confirm & Request';
    btn.disabled=false;
    closeSheet();
    document.getElementById('resultsArea').innerHTML='';
    const t=T[lang]||T.en;
    document.getElementById('successTitle').innerText=t.successTitle;
    document.getElementById('successMsg').innerHTML=t.successMsg;
    document.getElementById('successOverlay').classList.add('show');
  });
}

setLang('en');
document.querySelectorAll('.bchip').forEach(b=>b.classList.add('active'));
</script>
"""

final = html_only.rstrip()
# Remove closing </body></html> if present, we'll add them after script
if final.endswith('</html>'):
    final = final[:-7].rstrip()
if final.endswith('</body>'):
    final = final[:-7].rstrip()
final = final + '\n' + new_script + '\n</body>\n</html>\n'
open('app/static/index.html', 'w', encoding='utf-8').write(final)
print('Done')
