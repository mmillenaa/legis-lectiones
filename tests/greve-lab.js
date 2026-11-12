/* Legis Lectiones | Greve, laboratório v3: motor exclusivo, sem interferir em p2-quiz.js. */
(() => {
  'use strict';
  const VERSION = '3.0';
  const KEY = 'legis-lectiones:labour:greve:lab-v3';
  const byId = (id) => document.getElementById(id);
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const norm = (s) => String(s ?? '').normalize('NFD').replace(/[\u0300-\u036f]/g,'').trim().toLowerCase().replace(/\s+/g,' ');
  const staticBank = JSON.parse(byId('bankData').textContent);
  let bank=staticBank, lookup=new Map(), state={version:VERSION, first:{}, latest:{}, session:null};
  let draft={};
  const $ = byId;
  const kinds={pick:'Escolha estratégica',truth:'Veredito',match:'Associar agentes',order:'Ordenar etapas',clock:'Relógio jurídico',fill:'Memória ativa'};
  const formatN = n => new Intl.NumberFormat('pt-BR').format(n);
  const shuffle = a => {const z=[...a];for(let i=z.length-1;i>0;i--){let j=Math.floor(Math.random()*(i+1));[z[i],z[j]]=[z[j],z[i]];}return z;};
  function has(obj,id) {return Object.prototype.hasOwnProperty.call(obj||{},id);}
  function readState(){try{
    const s=JSON.parse(localStorage.getItem(KEY));
    if(s?.version===VERSION && s.first && s.latest && (!s.session || Array.isArray(s.session.ids))) {
      state={version:VERSION,first:s.first,latest:s.latest,session:s.session};
      if(state.session && state.session.ids.some(id=>!lookup.has(id))) state.session=null;
    }
  }catch(e){/* navegação privada não deve quebrar o estudo */}}
  function save(){try{localStorage.setItem(KEY,JSON.stringify(state));}catch(e){/* mantém progresso na aba */}}
  function validate(b){
    if(!Array.isArray(b.questions)||b.questions.length===0||!Array.isArray(b.tracks))throw Error('Banco sem atividades.');
    const ids=new Set(),tracks=new Set(b.tracks.map(t=>t.id));
    for(const q of b.questions){
      if(!q.id||ids.has(q.id)||!tracks.has(q.track)||!q.prompt||!q.why||!q.source)throw Error('Atividade incompleta ou duplicada: '+q.id);
      ids.add(q.id);
      if(q.kind==='pick'&&(![2,3].includes(q.options?.length)||q.answer<0||q.answer>=q.options.length))throw Error('Opções inválidas: '+q.id);
      if(q.kind==='truth' && typeof q.answer!=='boolean')throw Error('V/F inválido: '+q.id);
      if(q.kind==='match'&&(!q.rows?.length || !q.choices?.length || q.rows.some(r=>r.answer<0||r.answer>=q.choices.length)))throw Error('Associação inválida: '+q.id);
      if(q.kind==='order'&&(!q.items ||q.items.length<3))throw Error('Sequência inválida: '+q.id);
      if(q.kind==='clock'&&(!q.whenOptions||!q.toOptions||!Number.isInteger(q.whenAnswer)||!Number.isInteger(q.toAnswer)))throw Error('Prazo inválido: '+q.id);
      if(q.kind==='fill'&&(!q.answers?.length||!q.prompt.includes('{{blank}}')))throw Error('Lacuna inválida: '+q.id);
      if(!kinds[q.kind])throw Error('Tipo desconhecido: '+q.id);
    }
    return true;
  }
  function show(name){
    $('homeView').hidden=name!=='home'; $('studyView').hidden=name!=='study'; $('result').hidden=name!=='result';
    $('result').classList.toggle('show',name==='result');
    window.scrollTo?.({top:0,behavior:'instant'});
  }
  function home(){
    const attempted=Object.keys(state.first).filter(id=>lookup.has(id)).length;
    const right=Object.entries(state.first).filter(([id,v])=>lookup.has(id)&&v===true).length;
    const outstanding=Object.entries(state.latest).filter(([id,v])=>lookup.has(id)&&v===false).length;
    $('globalMetric').innerHTML=`<b>${attempted}/${bank.questions.length}</b> experimentadas na primeira tentativa · <b>${right}</b> acertos iniciais`;
    $('reviewBtn').disabled=outstanding===0;
    $('reviewBtn').textContent=outstanding?`Revisar ${outstanding} ponto${outstanding===1?'':'s'} de atenção`:'Sem erros pendentes';
    $('resumeBtn').hidden=!state.session||Boolean(state.session.completed);
    $('trackGrid').innerHTML=bank.tracks.map(t=>{
      const list=bank.questions.filter(q=>q.track===t.id);
      const done=list.filter(q=>has(state.first,q.id)).length;
      return `<button class="track-card" type="button" data-track="${esc(t.id)}" aria-label="Estudar ${esc(t.short)}: ${done} de ${list.length} já respondidas">
        <span class="track-motif" aria-hidden="true">${esc(t.motif)}</span><strong>${esc(t.label)}</strong><small>${esc(t.subtitle)}</small>
        <span class="track-progress">${done}/${list.length}</span><span class="bar-mini"><span style="width:${Math.round(100*done/list.length)}%"></span></span></button>`;
    }).join('');
    $('trackGrid').querySelectorAll('[data-track]').forEach(btn=>btn.addEventListener('click',()=>start('track',bank.questions.filter(q=>q.track===btn.dataset.track).map(q=>q.id),btn.textContent.trim().split('\n')[0])));
    show('home');
  }
  function start(mode,ids,label){
    if(!ids.length)return;
    state.session={mode,label,ids,pos:0,records:{},completed:false};
    draft={};save();question();
  }
  function quick(){
    const unseen=shuffle(bank.questions.filter(q=>!has(state.first,q.id)));
    const pending=shuffle(bank.questions.filter(q=>state.latest[q.id]===false));
    const rest=shuffle(bank.questions.filter(q=>has(state.first,q.id)&&state.latest[q.id]!==false));
    const ids=[...unseen,...pending,...rest].slice(0,8).map(q=>q.id);
    start('quick',ids,'Sessão curta · 8 desafios');
  }
  function resume(){if(!state.session)return;draft={};question();}
  function answerStatus(q){return state.session.records[q.id] || null;}
  function pendingFor(q){if(!has(draft,q.id)){
    if(q.kind==='match')draft[q.id]=Array(q.rows.length).fill(null);
    else if(q.kind==='order')draft[q.id]=[];
    else if(q.kind==='clock')draft[q.id]={when:null,to:null};
    else if(q.kind==='fill')draft[q.id]='';
    else draft[q.id]=null;
  }return draft[q.id];}
  function complete(q,ans){
    if(q.kind==='pick')return Number.isInteger(ans);
    if(q.kind==='truth')return typeof ans==='boolean';
    if(q.kind==='match')return Array.isArray(ans)&&ans.length===q.rows.length&&ans.every(Number.isInteger);
    if(q.kind==='order')return Array.isArray(ans)&&ans.length===q.items.length;
    if(q.kind==='clock')return Number.isInteger(ans.when)&&Number.isInteger(ans.to);
    if(q.kind==='fill')return Boolean(String(ans).trim());
    return false;
  }
  function evaluate(q,a){
    if(q.kind==='pick'||q.kind==='truth')return a===q.answer;
    if(q.kind==='match')return a.every((v,i)=>v===q.rows[i].answer);
    if(q.kind==='order')return a.every((v,i)=>v===q.answer[i]);
    if(q.kind==='clock')return a.when===q.whenAnswer && a.to===q.toAnswer;
    if(q.kind==='fill')return q.answers.some(s=>norm(s)===norm(a));
    return false;
  }
  function correctText(q){
    if(q.kind==='pick')return q.options[q.answer];
    if(q.kind==='truth')return q.answer?'Procede.':'Não procede.';
    if(q.kind==='match')return q.rows.map(r=>`${r.text.trim()} → ${q.choices[r.answer]}`).join(' | ');
    if(q.kind==='order')return q.items.join(' → ');
    if(q.kind==='clock')return `${q.whenOptions[q.whenAnswer]} · ${q.toOptions[q.toAnswer]}`;
    if(q.kind==='fill')return q.answers[0];
  }
  function audio(ok){const x=$(ok?'sfxCorrect':'sfxWrong');try{x?.play().catch(()=>{});}catch(e){}}
  function submit(q,a){
    if(answerStatus(q)||!complete(q,a))return;
    const good=evaluate(q,a);
    state.session.records[q.id]={correct:good,response:a};
    if(!has(state.first,q.id))state.first[q.id]=good;
    state.latest[q.id]=good;save();audio(good);
    question();
  }
  function makeOption(text,i,answer,current,checked){
    let cls='choice';
    if(checked){if(i===answer)cls+=' correct';else if(i===current)cls+=' incorrect';}
    else if(i===current)cls+=' active';
    return `<button class="${cls}" type="button" data-choice="${i}" ${checked?'disabled':''}><span class="choice-no">${String.fromCharCode(65+i)}</span><span>${esc(text)}</span></button>`;
  }
  function renderPick(q,a,r,host){
    host.innerHTML=q.options.map((o,i)=>makeOption(o,i,q.answer,a,r!==null)).join('');
    if(!r)host.querySelectorAll('[data-choice]').forEach(btn=>btn.addEventListener('click',()=>submit(q,Number(btn.dataset.choice))));
  }
  function renderTruth(q,a,r,host){
    const options=['Procede','Não procede'];
    host.innerHTML='<p class="mini-note">Julgue a afirmação à luz da referência indicada.</p><div class="truth-grid">'+options.map((o,i)=>{
      const v=i===0;
      let cls='choice';if(r){if(v===q.answer)cls+=' correct';else if(v===a)cls+=' incorrect';}
      return `<button class="${cls}" type="button" data-truth="${v}" ${r?'disabled':''}>${o}</button>`;
    }).join('')+'</div>';
    if(!r)host.querySelectorAll('[data-truth]').forEach(btn=>btn.addEventListener('click',()=>submit(q,btn.dataset.truth==='true')));
  }
  function renderMatch(q,a,r,host){
    host.innerHTML='<p class="mini-note">Escolha uma categoria para cada situação. Não é necessário arrastar cartões.</p>'+q.rows.map((row,idx)=>{
      const selected=a[idx];
      const chips=q.choices.map((label,i)=>{
        const cls='chip'+(selected===i?' selected':'')+(r&&i===row.answer?' is-right':'')+(r&&selected===i&&i!==row.answer?' is-wrong':'');
        return `<button type="button" class="${cls}" data-row="${idx}" data-value="${i}" ${r?'disabled':''}>${esc(label)}</button>`;
      }).join('');
      return `<div class="match-row"><p class="row-label"><b>${String(idx+1).padStart(2,'0')}</b> &nbsp; ${esc(row.text)}</p><div class="chip-row">${chips}</div>${r&&selected!==row.answer?`<p class="correct-note">Correto: ${esc(q.choices[row.answer])}</p>`:''}</div>`;
    }).join('');
    if(!r)host.querySelectorAll('[data-row]').forEach(btn=>btn.addEventListener('click',()=>{
      const v=[...pendingFor(q)];v[Number(btn.dataset.row)]=Number(btn.dataset.value);draft[q.id]=v;question(false);
    }));
  }
  function renderOrder(q,a,r,host){
    const placed=a||[];
    const pool=q.items.map((label,i)=>({label,i})).sort((x,y)=>((x.i*3+1)%7)-((y.i*3+1)%7));
    host.innerHTML='<p class="mini-note">Toque nos cartões em ordem. Use “desfazer” para corrigir antes de conferir.</p><div class="order-wrap"><ol class="order-rail">'+
      q.items.map((_,i)=>`<li class="${i<placed.length?'filled':''}"><b>${i+1}.</b> ${i<placed.length?esc(q.items[placed[i]]):'Escolha a etapa'}</li>`).join('')+'</ol><div class="order-tiles">'+
      pool.map(x=>`<button type="button" class="chip ${placed.includes(x.i)?'used':''}" data-order="${x.i}" ${r||placed.includes(x.i)?'disabled':''}>${esc(x.label)}</button>`).join('')+`</div><div class="order-actions"><button type="button" class="small-btn" id="undoOrder" ${r||!placed.length?'disabled':''}>Desfazer última</button><button type="button" class="small-btn" id="clearOrder" ${r||!placed.length?'disabled':''}>Limpar</button></div></div>`;
    if(!r){host.querySelectorAll('[data-order]').forEach(btn=>btn.addEventListener('click',()=>{draft[q.id]=[...pendingFor(q),Number(btn.dataset.order)];question(false);}));
      $('undoOrder').addEventListener('click',()=>{draft[q.id]=pendingFor(q).slice(0,-1);question(false)});
      $('clearOrder').addEventListener('click',()=>{draft[q.id]=[];question(false)});
    }
  }
  function renderClock(q,a,r,host){
    function block(title,prop,opts,answer){return `<div class="task-block"><strong>${esc(title)}</strong><div class="chip-row">${opts.map((o,i)=>{
      const cls='chip'+(a[prop]===i?' selected':'')+(r&&i===answer?' is-right':'')+(r&&a[prop]===i&&i!==answer?' is-wrong':'');
      return `<button type="button" class="${cls}" data-clock="${prop}" data-value="${i}" ${r?'disabled':''}>${esc(o)}</button>`;
    }).join('')}</div></div>`;}
    host.innerHTML=`<div class="clock-scene"><small>Marco da paralisação</small><strong>${esc(q.scenario)}</strong><div class="clock-rail"></div><div class="clock-labels"><span>Aviso</span><span>Início da greve</span></div></div>`+
      block('1 · Até quando avisar?', 'when',q.whenOptions,q.whenAnswer)+block('2 · A quem comunicar?','to',q.toOptions,q.toAnswer);
    if(!r)host.querySelectorAll('[data-clock]').forEach(btn=>btn.addEventListener('click',()=>{
      const v={...pendingFor(q)};v[btn.dataset.clock]=Number(btn.dataset.value);draft[q.id]=v;question(false);
    }));
  }
  function renderFill(q,a,r,host){
    const parts=q.prompt.split('{{blank}}');
    host.innerHTML=`<p class="mini-note">Responda sem alternativas. Acentos e maiúsculas não fazem diferença.</p><div class="fill-line"><span>${esc(parts[0])}</span><input class="fill-input" id="fillInput" type="text" autocomplete="off" spellcheck="false" aria-label="Palavra da lacuna" ${r?'disabled':''} value="${esc(a)}"><span>${esc(parts.slice(1).join(' '))}</span></div>`;
    if(!r){$('fillInput').addEventListener('input',e=>{draft[q.id]=e.target.value;$('checkBtn').disabled=!complete(q,draft[q.id])});
      $('fillInput').addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();const v=$('fillInput').value;draft[q.id]=v;submit(q,v);}});
    }
  }
  function renderFeedback(q,r){
    if(!r){$('feedback').hidden=true;$('feedback').innerHTML='';return;}
    const c=r.correct?'good':'bad';
    const link=q.url&&/^https:\/\//i.test(q.url)?`<a href="${esc(q.url)}" target="_blank" rel="noopener noreferrer">Consultar fonte</a>`:'';
    $('feedback').hidden=false;$('feedback').className=`feedback ${c}`;
    $('feedback').innerHTML=`<h3>${r.correct?'Acerto registrado.':'Pegadinha identificada.'}</h3>`+
     (!r.correct?`<p><b>Resposta esperada:</b> ${esc(correctText(q))}</p>`:'')+`<p>${esc(q.why)}</p>`+
     (q.trap?`<p class="trap"><b>Atenção à prova:</b> ${esc(q.trap)}</p>`:'')+
     `<div class="source">${q.authorView?'<b>Posição doutrinária do autor.</b> ':''}${esc(q.source)} ${link}</div>`;
  }
  function question(scroll=true){
    const s=state.session;if(!s){home();return;}
    const q=lookup.get(s.ids[s.pos]);if(!q){home();return;}
    const r=answerStatus(q),a=r?r.response:pendingFor(q);
    $('sessionTitle').textContent=s.label;
    $('counter').textContent=`Desafio ${s.pos+1} de ${s.ids.length}`;
    const done=s.ids.filter(id=>has(s.records,id)).length;
    $('progressText').textContent=`${done}/${s.ids.length} respondidos`;
    $('progressBar').style.width=`${(done/s.ids.length)*100}%`;
    $('sectionLabel').textContent=bank.tracks.find(t=>t.id===q.track)?.label||'';
    $('typeLabel').textContent=kinds[q.kind];
    $('prompt').textContent=q.kind==='fill'?'Complete a lacuna.':q.prompt;
    $('qContext').hidden=!q.context;
    $('qContext').textContent=q.context||'';
    const host=$('interactive');host.innerHTML='';
    if(q.kind==='pick')renderPick(q,a,r,host);
    if(q.kind==='truth')renderTruth(q,a,r,host);
    if(q.kind==='match')renderMatch(q,a,r,host);
    if(q.kind==='order')renderOrder(q,a,r,host);
    if(q.kind==='clock')renderClock(q,a,r,host);
    if(q.kind==='fill')renderFill(q,a,r,host);
    renderFeedback(q,r);
    $('answerState').textContent=r?(r.correct?'✓ Registrado':'↻ Para revisar'):'Primeira escolha vale para a estatística';
    $('checkBtn').hidden=Boolean(r)||['pick','truth'].includes(q.kind);
    $('checkBtn').disabled=Boolean(r)||!complete(q,a);
    $('prevBtn').disabled=s.pos===0;
    $('nextBtn').textContent=s.pos===s.ids.length-1?'Ver resultado →':'Próximo →';
    $('quizCard').dataset.questionId=q.id;
    $('quizCard').dataset.questionType=q.kind;
    $('quizCard').dataset.questionSection=q.track;
    $('quizCard').dataset.questionPrompt=q.prompt;
    showStudy(scroll);
    if(scroll && s.pos>0)document.querySelector('.quiz-toolbar')?.scrollIntoView({behavior:'smooth',block:'start'});
  }
  function showStudy(scroll){
    if($('studyView').hidden){show('study');} // não recomeça navegação quando apenas escolhe chips
  }
  function result(){
    const s=state.session;if(!s)return;
    s.completed=s.ids.every(id=>has(s.records,id));save();
    const all=Object.values(s.records);const answered=all.length;const right=all.filter(v=>v.correct).length;
    const wrong=answered-right;const total=s.ids.length;const ratio=Math.round((right/total)*100);
    $('score').textContent=`${ratio}%`;
    $('scoreDetail').textContent=`${right} acertos · ${wrong} erros · ${total-answered} não respondidas · ${total} atividades`;
    $('resultCaption').textContent=s.label;
    $('resultExtra').textContent=total-answered>0?
      'A pontuação considera o total desta sessão, incluindo desafios não respondidos. Você pode continuar quando voltar à trilha.':
      (wrong?'A primeira resposta ficou registrada. Os erros podem ser refeitos numa rodada própria, sem apagar o histórico.':'Todos os desafios desta sessão foram resolvidos.');
    const toReview=s.ids.filter(id=>state.latest[id]===false);
    $('reviewWrongBtn').disabled=!toReview.length;
    $('reviewWrongBtn').textContent=toReview.length?`Treinar ${toReview.length} erro${toReview.length===1?'':'s'}`:'Sem erros nesta sessão';
    show('result');
    window.dispatchEvent(new CustomEvent('law-bank-result',{detail:{answered,total,complete:answered===total}}));
  }
  function review(){
    const ids=bank.questions.filter(q=>state.latest[q.id]===false).map(q=>q.id);
    if(!ids.length)return;
    start('review',shuffle(ids),'Revisão inteligente · erros pendentes');
  }
  function bind(){
    $('quickBtn').addEventListener('click',quick);
    $('allBtn').addEventListener('click',()=>start('all',bank.questions.map(q=>q.id),'Trilha completa · 45 desafios'));
    $('reviewBtn').addEventListener('click',review);
    $('resumeBtn').addEventListener('click',resume);
    $('goHomeBtn').addEventListener('click',home);
    $('resultHomeBtn').addEventListener('click',home);
    $('finishBtn').addEventListener('click',result);
    $('reviewWrongBtn').addEventListener('click',review);
    $('restartBtn').addEventListener('click',()=>{if(confirm('Reiniciar esta sessão? O histórico de primeiras tentativas permanecerá salvo.')){
      const s=state.session;start(s.mode,s.ids,s.label);
    }});
    $('resetAllBtn').addEventListener('click',()=>{if(confirm('Apagar as tentativas e o progresso deste novo laboratório de Greve? O banco antigo permanecerá intacto.')){
      state={version:VERSION,first:{},latest:{},session:null};draft={};save();home();
    }});
    $('checkBtn').addEventListener('click',()=>{
      const q=lookup.get(state.session?.ids[state.session.pos]);if(q)submit(q,pendingFor(q));
    });
    $('prevBtn').addEventListener('click',()=>{const s=state.session;if(s.pos>0){s.pos--;save();question();}});
    $('nextBtn').addEventListener('click',()=>{const s=state.session;if(!s)return;if(s.pos<s.ids.length-1){s.pos++;save();question();}else{result();}});
  }
  async function boot(){
    // No GitHub Pages o JSON externo tem precedência. Em file://, o conteúdo embutido mantém a prévia funcional.
    if(location.protocol!=='file:'){
      try{const res=await fetch(new URL('greve.json',document.baseURI),{cache:'no-store'});
        if(res.ok){const live=await res.json();validate(live);bank=live;}
      }catch(e){console.warn('Usando cópia incorporada de Greve:',e);}
    }
    validate(bank);lookup=new Map(bank.questions.map(q=>[q.id,q]));readState();bind();home();
  }
  boot().catch(e=>{console.error(e);$('homeView').innerHTML=`<p role="alert">Não foi possível carregar o laboratório: ${esc(e.message)}</p>`;});
})();
