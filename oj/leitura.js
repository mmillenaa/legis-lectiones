(() => {
  "use strict";
  const root=document.documentElement;
  const slug=root.dataset.module||"";
  const $=id=>document.getElementById(id);
  const home="./";
  const stateKey="legis-lectiones:oj:leitura:"+slug+":last";
  let records=[],groups=[],meta={},current=0;
  function node(tag,className,textValue){
    const el=document.createElement(tag);
    if(className)el.className=className;
    if(textValue!==undefined)el.textContent=String(textValue);
    return el;
  }
  function add(parent,...children){parent.append(...children);return parent}
  function section(label){
    const out=node("section","section");
    add(out,node("h2","",label));
    return out;
  }
  function safeImage(path){
    return typeof path==="string"&&/^\.\/assets\/[a-z0-9-]+\.(png|webp|jpg|jpeg)$/i.test(path)?path:null;
  }
  function dataFromOriginal(){
    const articles=window.ARTICLES;
    const assets=window.ASSETS;
    if(!Array.isArray(articles)||articles.length!==30||!assets)throw Error("Dados da LINDB incompletos.");
    groups=[
      {title:"Arts. 1º–6º",start:0,end:6},
      {title:"Arts. 7º–10",start:6,end:10},
      {title:"Arts. 11–19",start:10,end:19},
      {title:"Arts. 20–30",start:19,end:30}
    ];
    meta={title:"LINDB — Lei comentada e ilustrada",subtitle:"Direito Civil",sourceLegal:"https://www.planalto.gov.br/ccivil_03/decreto-lei/del4657compilado.htm"};
    records=articles.map((x,i)=>({
      id:"LINDB"+String(x.n||i+1).padStart(2,"0"),
      title:"Art. "+x.n+"º · "+x.title,
      normLabel:"Art. "+x.n+"º",
      normKind:"trecho essencial do dispositivo",
      normText:x.legal||"",
      image:safeImage("./"+(assets[x.group]||"assets/lindb-"+x.group+".webp").replace(/^\.\//,"")),
      rule:x.rule||"",
      scene:x.scene||"",
      source:"LINDB · art. "+x.n
    }));
  }
  function dataFromBank(data){
    if(!data||!Array.isArray(data.cards)||!data.cards.length)throw Error("Banco de conteúdo indisponível.");
    records=data.cards;
    groups=Array.isArray(data.groups)?data.groups:[{title:"Tópicos",start:0,end:records.length}];
    meta=data.meta||{};
  }
  async function load(){
    if(slug==="lindb"){dataFromOriginal();return}
    if(!/^[a-z0-9-]+$/.test(slug))throw Error("Módulo inválido.");
    const res=await fetch("./"+slug+".json",{cache:"no-store"});
    if(!res.ok)throw Error("Não foi possível ler o módulo (HTTP "+res.status+").");
    dataFromBank(await res.json());
  }
  function buildNav(){
    $("navTitle").textContent=slug==="lindb"?"LINDB":slug==="cpc-normas"?"Normas Fundamentais":slug==="cpc-jurisdicao"?"Jurisdição":"Improbidade";
    const host=$("groupNav");
    host.replaceChildren();
    for(const group of groups){
      const sectionBlock=node("section","group");
      add(sectionBlock,node("div","group-heading",group.title));
      const from=Math.max(0,group.start||0),to=Math.min(records.length,group.end||records.length);
      for(let i=from;i<to;i++){
        const item=records[i],button=node("button","nav-item");
        button.type="button";button.dataset.index=String(i);
        const n=node("span","nav-num",String(i+1).padStart(2,"0"));
        add(button,n,document.createTextNode(item.title));
        button.addEventListener("click",()=>show(i,true));
        sectionBlock.append(button);
      }
      host.append(sectionBlock);
    }
  }
  function lawBlock(item){
    const block=section("Lei seca");
    const norm=(item.normText||"").trim();
    const kind=(item.normKind||"").toLowerCase();
    const isConcept=!norm;
    if(isConcept){
      const h=block.querySelector("h2");h.textContent="Base conceitual do PDF";
      add(block,node("div","law concept","Este tópico trata de um conceito doutrinário do material. Não há dispositivo legal transcrito neste cartão."));
    }else{
      add(block,node("div","law",norm));
      const label=(item.normLabel||"").trim();
      if(kind.includes("excerto")||kind.includes("trecho")||kind.includes("recorte")||slug==="lindb"){
        block.append(node("p","note",(label?label+" · ":"")+"Texto ou recorte conforme o material de estudo; confira o dispositivo completo na fonte oficial."));
      }
    }
    let legal=meta.sourceLegal||"";
    if(slug==="cpc-jurisdicao"&&/^CF[, ]/.test(item.normLabel||"")){
      legal="https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm";
    }
    if(/^https:\/\/(www\.)?(planalto\.gov\.br|www2\.camara\.leg\.br)\//i.test(legal)){
      const p=node("p","note");const link=node("a","",isConcept?"Consultar legislação de referência":"Conferir texto legal completo");
      link.href=legal;link.target="_blank";link.rel="noopener noreferrer";
      p.append(link);block.append(p);
    }
    return block;
  }
  function imageBlock(item){
    const path=safeImage(item.image);
    if(!path)return null;
    const block=section("Imagem");
    const d=node("details","illustration");d.open=true;
    const summary=node("summary","","Quadrinho ilustrativo");
    const figure=node("figure");
    const img=node("img");img.src=path;img.alt="Ilustração didática de "+item.title;img.loading="lazy";img.decoding="async";
    img.addEventListener("error",()=>{block.remove();console.warn("Ilustração indisponível:",path)});
    add(figure,img,node("figcaption","","Ilustração de estudo · toque no título acima para recolher"));
    add(d,summary,figure);
    block.append(d);
    return block;
  }
  function show(idx,resetScroll=false){
    current=Math.max(0,Math.min(records.length-1,idx));
    try{localStorage.setItem(stateKey,String(current))}catch(e){}
    const item=records[current];
    const subject=slug==="improbidade"?"Direito Administrativo":slug==="lindb"?"Direito Civil":"Direito Processual Civil";
    $("context").textContent=subject+" / "+(slug==="lindb"?"LINDB":meta.title||"");
    $("articleTitle").textContent=item.title;
    $("subhead").textContent=meta.subtitle||"Lei comentada e ilustrada";
    $("pageNum").textContent=(current+1)+" de "+records.length;
    const page=$("article");
    page.replaceChildren();
    page.append(lawBlock(item));
    const img=imageBlock(item);if(img)page.append(img);
    const comment=section("Comentário");comment.append(node("p","copy",(item.rule||"Não há comentário adicional neste recorte.")));
    page.append(comment);
    const example=section("Exemplo");const box=node("div","example");box.append(node("p","",item.scene||"Não há exemplo específico no material."));
    example.append(box);page.append(example);
    for(const button of $("groupNav").querySelectorAll("[data-index]")){
      if(Number(button.dataset.index)===current)button.setAttribute("aria-current","step");
      else button.removeAttribute("aria-current");
    }
    for(const side of ["prev","prevBottom"])$(side).disabled=current===0;
    for(const side of ["next","nextBottom"])$(side).disabled=current===records.length-1;
    if(resetScroll)window.scrollTo({top:0,behavior:"instant"});
  }
  async function init(){
    await load();
    buildNav();
    let last=0;
    try{last=Number.parseInt(localStorage.getItem(stateKey)||"0",10)||0}catch(e){}
    const url=new URL(location.href),item=Number.parseInt(url.searchParams.get("card")||"",10);
    if(Number.isInteger(item)&&item>=1&&item<=records.length)last=item-1;
    for(const id of ["prev","prevBottom"])$(id).addEventListener("click",()=>show(current-1,true));
    for(const id of ["next","nextBottom"])$(id).addEventListener("click",()=>show(current+1,true));
    show(last);
  }
  init().catch(e=>{
    console.error("Falha ao abrir leitura:",e);
    $("article").replaceChildren(node("p","",e.message));
  });
})();
