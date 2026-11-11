(() => {
  "use strict";
  const mods=[
    ["lindb","Direito Civil · LINDB"],
    ["cpc-normas","DPC · Normas Fundamentais"],
    ["cpc-jurisdicao","DPC · Jurisdição"],
    ["improbidade","Direito Administrativo · Improbidade"]
  ];
  const $=id=>document.getElementById(id);
  let catalogs={};
  let currentModule="lindb", topic="todos", queue=[],currentIndex=0,selected=null,attempts={};
  let wrongOnly=false;
  function element(tag,text,cls){
    const el=document.createElement(tag);
    if(text!==undefined&&text!==null)el.textContent=String(text);
    if(cls)el.className=cls;
    return el;
  }
  function updateSelects(){
    const sel=$("moduleSelect");
    currentModule=sel.value;
    const prevTopic=topic;
    const tsel=$("topicSelect");
    tsel.replaceChildren(new Option("Todos os assuntos","todos"));
    const possible=currentModule==="todos"?mods:mods.filter(x=>x[0]===currentModule);
    possible.forEach(([slug])=>{
      const cat=catalogs[slug];
      const titles=[...new Set(cat.questions.map(q=>q.title))];
      for(const title of titles){
        const label=currentModule==="todos"?cat.title+" · "+title:title;
        tsel.add(new Option(label,slug+"|"+title));
      }
    });
    tsel.value=[...tsel.options].some(x=>x.value===prevTopic)?prevTopic:"todos";
    topic=tsel.value;
    refreshQueue();
  }
  function makeQueue(){
    const ids=currentModule==="todos"?mods.map(x=>x[0]):[currentModule];
    let result=ids.flatMap(slug=>catalogs[slug].questions.map(q=>({...q,module:slug})));
    if(topic!=="todos"){
      const pipe=topic.indexOf("|"),m=topic.slice(0,pipe),t=topic.slice(pipe+1);
      result=result.filter(q=>q.module===m&&q.title===t);
    }
    if(wrongOnly)result=result.filter(q=>attempts[q.id]&&!attempts[q.id].correct);
    return result;
  }
  function refreshQueue(){
    queue=makeQueue();
    currentIndex=0;selected=null;render();
  }
  function counts(){
    const solved=queue.filter(q=>Boolean(attempts[q.id])).length;
    const right=queue.filter(q=>attempts[q.id]?.correct).length;
    return {solved,right};
  }
  function render(){
    const box=$("questionBox");box.replaceChildren();
    const {solved,right}=counts();
    $("scoreLabel").textContent=solved+" respondidas · "+right+" acertos";
    $("progressLabel").textContent=queue.length+" questões neste filtro";
    $("progressBar").style.width=queue.length?(100*solved/queue.length)+"%":"0%";
    $("questionCounter").textContent=queue.length?(currentIndex+1)+" de "+queue.length:"";
    $("retryWrong").hidden=!Object.values(attempts).some(x=>!x.correct);
    $("retryWrong").textContent=wrongOnly?"Voltar a todas":"Refazer erradas";
    $("prevQuestion").disabled=currentIndex===0||queue.length===0;
    $("nextQuestion").disabled=currentIndex>=queue.length-1||queue.length===0;
    const backModule=currentModule==="todos"?"lindb":currentModule;
    $("backToRead").href="./"+backModule+".html";
    if(!queue.length){
      box.append(element("p",wrongOnly?"Nenhuma questão errada neste filtro.":"Nenhuma questão disponível neste filtro.","quiz-empty"));
      return;
    }
    const q=queue[currentIndex],attempt=attempts[q.id];
    box.append(element("div",catalogs[q.module].title+" · "+q.legalLabel,"quiz-overline"));
    box.append(element("h2",q.title));
    box.append(element("p",q.question,"quiz-prompt"));
    const choices=element("div",null,"quiz-choices");
    const order="ABCD";
    q.options.forEach((choice,i)=>{
      const b=element("button",null,"quiz-option");
      b.type="button";b.disabled=Boolean(attempt);
      if(!attempt&&selected===i)b.classList.add("selected");
      if(attempt&&i===q.answer)b.classList.add("correct");
      else if(attempt&&i===attempt.chosen)b.classList.add("incorrect");
      const letter=element("span",order[i],"quiz-letter");
      b.append(letter,element("span",choice));
      b.onclick=()=>{if(!attempt){selected=i;render()}};
      choices.append(b);
    });
    box.append(choices);
    if(attempt){
      const feedback=element("div",null,"quiz-feedback"+(attempt.correct?"":" incorrect"));
      feedback.append(element("strong",attempt.correct?"Resposta correta":"Resposta incorreta"));
      feedback.append(element("p",q.explanation));
      const details=element("details",null,"quiz-details");
      const summary=element("summary","Ver o trecho legal utilizado");
      details.append(summary,element("pre",q.legalText));
      feedback.append(details);
      const reading=element("a","Abrir o cartão na leitura");
      reading.href="./"+q.module+".html?card="+q.card;
      feedback.append(reading);
      box.append(feedback);
    }else{
      const action=element("button","Conferir resposta","quiz-action primary");
      action.disabled=selected===null;
      action.onclick=()=>{
        if(selected===null)return;
        attempts[q.id]={chosen:selected,correct:selected===q.answer};
        render();
      };
      box.append(action);
    }
  }
  function navigate(delta){
    currentIndex=Math.max(0,Math.min(queue.length-1,currentIndex+delta));selected=null;render();
    window.scrollTo({top:0,behavior:"instant"});
  }
  async function init(){
    const files=await Promise.all(mods.map(async ([slug])=>{
      const r=await fetch("./questoes-"+slug+".json",{cache:"no-store"});
      if(!r.ok)throw Error("Falha ao carregar "+slug+" (HTTP "+r.status+")");
      const data=await r.json();
      if(!Array.isArray(data.questions)||!data.questions.length||data.module!==slug)throw Error("Banco incompleto: "+slug);
      for(const q of data.questions){
        if(!q.legalText||!q.question||!Array.isArray(q.options)||q.options.length!==4||
          !Number.isInteger(q.answer)||q.answer<0||q.answer>3||!q.id)throw Error("Questão inválida: "+q.id);
      }
      return [slug,data];
    }));
    catalogs=Object.fromEntries(files);
    const requested=new URL(location.href).searchParams.get("modulo");
    currentModule=mods.some(x=>x[0]===requested)?requested:"lindb";
    $("moduleSelect").value=currentModule;
    $("moduleSelect").onchange=()=>{wrongOnly=false;updateSelects()};
    $("topicSelect").onchange=()=>{topic=$("topicSelect").value;wrongOnly=false;refreshQueue()};
    $("nextQuestion").onclick=()=>navigate(1);
    $("prevQuestion").onclick=()=>navigate(-1);
    $("retryWrong").onclick=()=>{wrongOnly=!wrongOnly;refreshQueue()};
    $("reset").onclick=()=>{
      if(Object.keys(attempts).length&&!confirm("Reiniciar as respostas deste treino?"))return;
      attempts={};wrongOnly=false;selected=null;refreshQueue();
    };
    updateSelects();
  }
  init().catch(e=>{$("questionBox").textContent="Erro ao carregar o banco de questões: "+e.message;console.error(e)});
})();