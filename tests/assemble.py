from pathlib import Path
import json
r=Path(__file__).resolve().parent
css=(r/'greve-lab.css').read_text()
js=(r/'greve-lab.js').read_text()
bank=json.loads((r/'greve.json').read_text())
embedded=json.dumps(bank,ensure_ascii=False).replace('<','\\u003c')
html='''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<title>Greve · Legis Lectiones — Laboratório de revisão</title>
<meta name="description" content="Revisão interativa de direito de greve: prazos, agentes, quórum, serviços essenciais, classificação, abuso e lockout. Questões baseadas em Sérgio Pinto Martins e na legislação atualizada.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600&display=swap" rel="stylesheet">
<!-- Integração com a celebração de resultados do repositório, se disponível. -->
<link rel="stylesheet" href="./result-celestial.css">
<style>\n'''+css+'''\n</style>
<script src="./result-celestial.js" defer></script>
</head>
<body data-bank="greve">
<div class="shell">
<nav class="topbar" aria-label="Navegação">
  <a class="back-link" href="./">← Direito do Trabalho</a>
  <span class="brand">Legis Lectiones</span>
</nav>
<header class="hero">
  <div>
    <div class="eyebrow">Direito do Trabalho · Estudo por desafios</div>
    <h1>Greve<span style="color:var(--gold)">.</span></h1>
    <p class="lead">Menos decoreba de alternativas e mais decisões. Treine prazos e destinatários, identifique quem faz o quê e enfrente as pegadinhas do capítulo de Sérgio Pinto Martins.</p>
  </div>
  <div class="hero-art" role="img" aria-label="Ilustração geométrica com os prazos de 48 e 72 horas">
    <div class="dial"><strong>48h</strong><small>regra geral</small><span class="dial-divider"></span><strong class="dial-small">72h</strong><small>essenciais</small></div>
  </div>
</header>
<div class="memory-strip" aria-label="Três pontos para memorizar">
  <div class="memory-card"><span class="memory-number">48h</span><div><strong>Atividade não essencial</strong><p>Aviso à parte patronal.</p></div></div>
  <div class="memory-card"><span class="memory-number purple">72h</span><div><strong>Atividade essencial</strong><p>Aviso a empregadores e usuários.</p></div></div>
  <div class="memory-card"><span class="memory-number word">Estatuto</span><div><strong>Quórum sindical</strong><p>A lei não fixa porcentagem geral.</p></div></div>
</div>
<main>
  <section id="homeView" aria-labelledby="homeTitle">
    <div class="separator"></div>
    <div class="dashboard-heading"><h2 id="homeTitle">Escolha um percurso</h2><span id="globalMetric" class="metric">Progresso local</span></div>
    <div class="controls-home">
      <button type="button" class="btn primary large" id="quickBtn">Começar com 8 desafios</button>
      <button type="button" class="btn" id="allBtn">Trilha completa</button>
      <button type="button" class="btn quiet" id="reviewBtn" disabled>Sem erros pendentes</button>
      <button type="button" class="btn quiet" id="resumeBtn" hidden>Continuar sessão</button>
    </div>
    <div class="track-grid" id="trackGrid" aria-label="Percursos temáticos"></div>
    <details class="reference-drawer">
      <summary>Os 13 temas do professor estão contemplados?</summary>
      <p>Sim. As atividades cobrem o roteiro final do capítulo, distribuído pelas cinco trilhas:</p>
      <div class="topic-list">
        <span>01 Conceito</span><span>02 Constituição de 1937</span><span>03 Natureza jurídica</span><span>04 Classificações</span><span>05 Limitações</span><span>06 Titularidade e legitimidade</span><span>07 Interesses a defender</span><span>08 Quórum</span><span>09 Aviso-prévio</span><span>10 Efeitos contratuais</span><span>11 Lockout</span><span>12 Solidariedade</span><span>13 Greve de zelo</span>
      </div>
      <p>Nas questões doutrinárias, as interpretações do autor são sinalizadas. A legislação e as teses do STF aparecem em separado.</p>
    </details>
    <p class="footnote">As primeiras respostas alimentam o histórico; acertar depois corrige o ponto pendente, mas não apaga o primeiro resultado. Cada rodada é independente.</p>
    <button type="button" class="small-btn" id="resetAllBtn">Apagar apenas o progresso deste laboratório</button>
  </section>

  <section id="studyView" hidden aria-label="Sessão de estudo">
    <div class="quiz-toolbar">
      <div class="quiz-info">
        <div class="progress-meta"><strong id="sessionTitle">Sessão</strong><span id="counter">Desafio 1</span></div>
        <div class="progress" aria-label="Progresso da sessão"><span id="progressBar"></span></div>
        <div class="progress-meta" style="margin:8px 0 0"><span id="progressText">0 respondidos</span><span>1ª tentativa registrada</span></div>
      </div>
      <button class="small-btn" type="button" id="goHomeBtn">← Trilhas</button>
      <button class="small-btn" type="button" id="finishBtn">Resultado</button>
    </div>
    <article id="quizCard" class="question-card">
      <div class="qhead"><span id="sectionLabel" class="section"></span><span class="type" id="typeLabel"></span></div>
      <h2 class="prompt" id="prompt"></h2>
      <p id="qContext" class="context" hidden></p>
      <div id="interactive" class="interactive" aria-live="off"></div>
      <section id="feedback" class="feedback" aria-live="polite" role="status" hidden></section>
      <div class="controls">
        <button type="button" class="btn quiet" id="prevBtn">← Anterior</button>
        <div class="controls-right">
          <span class="answer-state" id="answerState"></span>
          <button type="button" class="btn primary" id="checkBtn">Conferir</button>
          <button type="button" class="btn" id="nextBtn">Próximo →</button>
        </div>
      </div>
    </article>
    <p class="footnote">Respostas comentadas com base legal, indicação de interpretação doutrinária e alerta sobre a pegadinha. Não há limite de tempo.</p>
  </section>

  <section id="result" class="result" hidden aria-labelledby="resultTitle">
    <div class="eyebrow" id="resultCaption">Resultado da sessão</div>
    <h2 id="resultTitle">Revisão da rodada</h2>
    <div id="score" class="score" aria-live="polite">0%</div>
    <p id="scoreDetail">0 acertos · 0 erros · 0 atividades</p>
    <p id="resultExtra" class="result-extra"></p>
    <div class="result-actions">
      <button type="button" class="btn primary" id="reviewWrongBtn">Treinar erros</button>
      <button type="button" class="btn" id="restartBtn">Repetir esta sessão</button>
      <button type="button" class="btn quiet" id="resultHomeBtn">Escolher trilha</button>
    </div>
  </section>
</main>
<footer class="site-footer">
  <strong>Referências e critérios editoriais</strong>
  <p>MARTINS, Sergio Pinto. <em>Manual de Direito do Trabalho</em>. 15. ed. São Paulo: Saraiva Jur, 2024. Capítulo “Greve”, inclusive as 13 questões finais. <a href="https://app.minhabiblioteca.com.br/reader/books/9786553628977" target="_blank" rel="noopener noreferrer">Minha Biblioteca</a>.</p>
  <p>BRASIL. <a href="https://www2.camara.leg.br/legin/fed/lei/1989/lei-7783-28-junho-1989-372139-normaatualizada-pl.html" target="_blank" rel="noopener noreferrer">Lei nº 7.783/1989, texto atualizado</a>; <a href="https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm" target="_blank" rel="noopener noreferrer">Constituição Federal</a>, arts. 9º, 37, VII, 142, § 3º, IV; STF, <a href="https://portal.stf.jus.br/jurisprudenciarepercussao/tema.asp?num=531" target="_blank" rel="noopener noreferrer">Tema 531</a> e <a href="https://portal.stf.jus.br/jurisprudenciaRepercussao/tema.asp?num=541" target="_blank" rel="noopener noreferrer">Tema 541</a>.</p>
  <p class="footnote">Banco versão 3.0. Não carrega nem modifica o armazenamento das antigas 56 atividades. O progresso novo fica neste navegador.</p>
</footer>
</div>
<audio id="sfxCorrect" preload="none" src="../civil-procedure/correct.mp3"></audio>
<audio id="sfxWrong" preload="none" src="../civil-procedure/wrong.mp3"></audio>
<!-- Analytics original preservado. -->
<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token":"51f24d9a0ec840c5bcb40df413a4bf46"}'></script>
<script id="bankData" type="application/json">'''+embedded+'''</script>
<script>\n'''+js+'''\n</script>
</body>
</html>
'''
(r/'greve.html').write_text(html,encoding='utf-8')
print('html kb',round(len(html.encode())/1024,1))
