"""Sincroniza o HTML autocontido com estabilidade.json, estabilidade-lab.css e .js.
Executar em qualquer computador: python tests/assemble-estabilidade.py
O arquivo HTML original do pacote é a base; não depende do laboratório de Greve.
"""
from pathlib import Path
import json,re
r=Path(__file__).resolve().parent
html_path=r/'estabilidade.html'
html=html_path.read_text(encoding='utf-8')
css=(r/'estabilidade-lab.css').read_text(encoding='utf-8')
js=(r/'estabilidade-lab.js').read_text(encoding='utf-8')
bank=json.loads((r/'estabilidade.json').read_text(encoding='utf-8'))
embedded=json.dumps(bank,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
patterns=[
 (r'<style>.*?</style>', lambda _: '<style>\n'+css+'\n</style>'),
 (r'<script id="bankData" type="application/json">.*?</script>',lambda _: '<script id="bankData" type="application/json">'+embedded+'</script>'),
 (r'<script>\s*/\* Legis Lectiones \| Estabilidade, laboratório v4:.*?</script>',lambda _: '<script>\n'+js+'\n</script>')
]
for pattern,repl in patterns:
 html,count=re.subn(pattern,repl,html,count=1,flags=re.S)
 if count!=1:raise SystemExit('HTML não contém bloco esperado; arquivo preservado: '+pattern)
html_path.write_text(html,encoding='utf-8')
print('HTML remontado:',html_path,'—',len(bank['questions']),'questões')
