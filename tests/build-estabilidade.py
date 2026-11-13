from pathlib import Path
from collections import Counter
import json
root=Path(__file__).resolve().parent
book='https://app.minhabiblioteca.com.br/reader/books/9786553628977'
cf='https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm'
clt='https://www.planalto.gov.br/ccivil_03/decreto-lei/del5452.htm'
lei8213='https://www.planalto.gov.br/ccivil_03/leis/l8213cons.htm'
lei8036='https://www.planalto.gov.br/ccivil_03/leis/l8036consol.htm'
tst='https://www.tst.jus.br/jurisprudencia'
tema163='https://www.tst.jus.br/documents/d/guest/irr163'
questions=[]
def add(t,k,p,**kw):
 questions.append(dict(id=f'EST4-{len(questions)+1:03d}',track=t,kind=k,prompt=p,**kw))
def pick(t,p,opts,a,why,trap,source,url=clt,author=False):
 add(t,'pick',p,options=opts,answer=a,why=why,trap=trap,source=source,url=url,**({'authorView':True} if author else {}))
def truth(t,p,a,why,trap,source,url=clt,author=False):
 add(t,'truth',p,answer=a,why=why,trap=trap,source=source,url=url,**({'authorView':True} if author else {}))
def match(t,p,choices,rows,why,trap,source,url=clt):
 add(t,'match',p,choices=choices,rows=[{'text':a,'answer':b} for a,b in rows],why=why,trap=trap,source=source,url=url)
def order(t,p,steps,why,trap,source,url=clt):
 add(t,'order',p,items=steps,answer=list(range(len(steps))),why=why,trap=trap,source=source,url=url)
def clock(t,p,context,left,right,why,trap,source,url=clt,leftTitle='1 · Início da proteção',rightTitle='2 · Término da proteção'):
 add(t,'clock',p,scenario=context,whenOptions=[x[0] for x in left],whenAnswer=next(i for i,x in enumerate(left) if x[1]),toOptions=[x[0] for x in right],toAnswer=next(i for i,x in enumerate(right) if x[1]),labelWhen=leftTitle,labelTo=rightTitle,why=why,trap=trap,source=source,url=url)
def fill(t,p,answers,why,trap,source,url=clt):
 add(t,'fill',p,answers=answers,why=why,trap=trap,source=source,url=url)
# 01 — Fundamentos
T='fundamentos'
pick(T,'No sentido jurídico trabalhista, estabilidade significa:',[
 'Direito à permanência no emprego, ressalvadas hipóteses admitidas.',
 'Direito à indenização em qualquer encerramento de contrato.',
 'Proibição perpétua de toda e qualquer forma de desligamento.'
],0,'A estabilidade jurídica restringe a dispensa a causas admitidas pelo ordenamento.','Não equivale a vínculo vitalício.','Martins, itens 2 e 3 — Denominação e conceito',book,True)
pick(T,'Na distinção de Sérgio Pinto Martins, garantia de emprego é:',[
 'Uma modalidade exclusiva da estabilidade decenal.',
 'Um gênero que inclui medidas amplas de proteção ao emprego.',
 'Apenas a impossibilidade absoluta de despedida.'
],1,'O conceito mais amplo alcança obtenção, manutenção e colocação no emprego; estabilidade é proteção mais específica.','O autor também diferencia garantia de emprego de garantia no emprego.','Martins, itens 2 e 3',book,True)
pick(T,'Qual diploma foi marco da estabilidade no setor privado e da previdência ferroviária?',[
 'A Lei nº 8.036, de 1990.',
 'A Constituição de 1988.',
 'A Lei Eloy Chaves, de 1923.'
],2,'O Decreto nº 4.682/1923 instituiu proteção aos ferroviários, marco histórico do regime privado.','O instituto havia surgido antes no setor público.','Martins, item 1 — Histórico',book)
order(T,'Coloque os três marcos em ordem cronológica:',[
 'Lei Eloy Chaves: ferroviários e estabilidade (1923)',
 'FGTS inaugura regime de opção (1966)',
 'Constituição extingue a alternatividade para novos direitos (1988)'
],'A trajetória apresentada pelo autor vai do regime de estabilidade decenal à opção pelo FGTS e à sistemática constitucional de 1988.','A Constituição de 1988 preservou direitos adquiridos.','Martins, item 1 — Histórico',book)
pick(T,'Na disciplina clássica do art. 492 da CLT, a estabilidade decenal exigia, em regra:',[
 'Mais de dez anos de serviço na mesma empresa.',
 'Cinco anos consecutivos de serviço público.',
 'Três anos de exercício após concurso.'
],0,'O art. 492 se refere ao empregado com mais de dez anos de serviço na mesma empresa.','O prazo de três anos pertence à estabilidade constitucional do servidor efetivo.','CLT, art. 492; Martins, item 8',clt)
truth(T,'Quem completou dez anos de emprego após 1988 adquiriu automaticamente a antiga estabilidade decenal da CLT.',False,'A transição constitucional preserva direitos adquiridos do antigo regime, mas não cria estabilidade decenal nova de forma geral.','Dez anos atualmente não bastam para reviver o regime extinto.','Lei nº 8.036/1990, art. 14; Martins, item 8',lei8036)
pick(T,'O pedido de demissão do empregado estável, nos termos do art. 500 da CLT:',[
 'É válido apenas com duas testemunhas.',
 'Exige assistência sindical ou da autoridade indicada na falta de sindicato.',
 'Depende de sentença judicial em todos os casos.'
],1,'O art. 500 estabelece assistência pelo sindicato ou, inexistindo sindicato, por autoridade local do Ministério do Trabalho ou da Justiça do Trabalho.','Formalidade especial não se confunde com aceitação patronal.','CLT, art. 500')
truth(T,'A estabilidade jurídica necessariamente impede qualquer mudança de cargo ou local de trabalho.',False,'A proteção recai sobre a manutenção do vínculo, respeitadas as regras legais de alteração contratual e transferência.','Estabilidade não é inamovibilidade.','Martins, itens 3 e 8; CLT, arts. 468 e 469',book)
# 02 — Prazos
T='prazos'
clock(T,'Para o dirigente sindical eleito, inclusive suplente, identifique os limites da proteção.',
 'Direção sindical', [('Registro da candidatura',True),('Data da eleição',False),('Posse',False)],
 [('Fim do mandato',False),('Cinco meses após mandato',False),('Um ano após o mandato',True)],
 'A garantia começa no registro da candidatura e vai, para os eleitos, até um ano após o fim do mandato.',
 'A posse não inaugura o período protegido.','CF, art. 8º, VIII; CLT, art. 543',cf)
pick(T,'O mandato do dirigente sindical termina em 30/06/2026. Até quando vai a garantia, em regra?',[
 'Até 30/06/2027.',
 'Até 30/11/2026.',
 'Até 30/06/2028.'
],0,'O período final se projeta por um ano após o término do mandato.','Cinco meses é prazo ligado à gestante após o parto, não à garantia sindical.','CF, art. 8º, VIII',cf)
clock(T,'Qual o início e o término da proteção do empregado eleito para a CIPA?',
 'CIPA · empregado eleito', [('Posse no cargo',False),('Registro da candidatura',True),('Primeira reunião',False)],
 [('Mandato encerrado',False),('Um ano após o mandato',True),('Dois anos após o mandato',False)],
 'A proteção vai do registro de candidatura até um ano após o fim do mandato, abrangendo suplente eleito.','Não conte apenas os meses do mandato.','ADCT, art. 10, II, a; TST, Súmula 339',cf)
clock(T,'No regime constitucional da gestante, quais são os marcos de proteção?',
 'Gestação · ADCT', [('Início da licença',False),('Data do parto',False),('Confirmação da gravidez',True)],
 [('Cinco meses após o parto',True),('120 dias após a concepção',False),('Um ano após o parto',False)],
 'A garantia constitucional começa na confirmação da gravidez e termina cinco meses após o parto.','A licença-maternidade e a estabilidade possuem marcos e durações distintos.','ADCT, art. 10, II, b',cf)
pick(T,'O empregado sofre acidente de trabalho. Após a cessação do benefício acidentário, a garantia do art. 118 dura, em regra:',[
 'Seis meses.', 'Doze meses.', 'Vinte e quatro meses.'
],1,'A norma garante manutenção do contrato por, no mínimo, doze meses após a cessação do auxílio-doença acidentário.','O marco não é automaticamente a data do acidente.','Lei nº 8.213/1991, art. 118',lei8213)
match(T,'Indique a correspondência entre marcos e períodos previstos na legislação.',[
 '30 dias', '12 meses', '5 meses'
],[
 ('Prazo para ajuizar inquérito a partir da suspensão do empregado.',0),
 ('Garantia ordinária após cessação de auxílio-doença acidentário.',1),
 ('Intervalo constitucional após o parto.',2)
],'As durações têm fatos geradores diferentes: suspensão, cessação de benefício e parto.','A pergunta cobra simultaneamente prazo e marco inicial.','CLT, art. 853; Lei 8.213/1991, art. 118; ADCT, art. 10',clt)
clock(T,'Representante dos trabalhadores no Conselho Curador do FGTS: qual intervalo?',
 'Conselho Curador do FGTS', [('Registro de candidatura',False),('Nomeação',True),('Posse do conselho anterior',False)],
 [('Fim do mandato',False),('Um ano após o mandato',True),('Cinco meses após o mandato',False)],
 'Representantes dos trabalhadores, efetivos e suplentes, têm garantia da nomeação até um ano após o mandato.','A exigência de falta grave é por processo sindical no texto legal.','Lei nº 8.036/1990, art. 3º, §9º',lei8036)
clock(T,'Representante dos trabalhadores no CNPS: identifique o intervalo.',
 'Conselho Nacional de Previdência Social', [('Posse em sindicato',False),('Registro da candidatura',False),('Nomeação',True)],
 [('Um ano após o mandato',True),('Término do mandato',False),('Dois anos após o mandato',False)],
 'O CNPS também utiliza a nomeação como marco inicial, até um ano depois do mandato.','Ao contrário do Conselho Curador do FGTS, a lei menciona processo judicial para comprovação de falta grave.','Lei nº 8.213/1991, art. 3º, §7º',lei8213)
clock(T,'Empregado eleito para a Comissão de Conciliação Prévia: identifique os limites.',
 'Comissão de Conciliação Prévia', [('Registro da candidatura',False),('Eleição',True),('Primeira reunião',False)],
 [('Fim do mandato',False),('Cinco meses após o mandato',False),('Um ano após o mandato',True)],
 'A CLT atribui proteção aos representantes dos empregados, titulares e suplentes, desde a eleição até um ano após o término do mandato.','A data inicial não é o registro de candidatura nessa hipótese.','CLT, art. 625-B, §1º')
clock(T,'Comissão de representantes dos empregados na empresa: duração e proteção posterior.',
 'CLT · art. 510-D', [('Mandato de um ano',True),('Mandato de dois anos',False),('Mandato de três anos',False)],
 [('Seis meses após mandato',False),('Um ano após mandato',True),('Dois anos após mandato',False)],
 'O mandato é de um ano, e a proteção contra despedida arbitrária alcança um ano após seu término, iniciando-se no registro de candidatura.','Mandato e período protegido não são a mesma medida.','CLT, art. 510-D',clt,leftTitle='1 · Duração do mandato',rightTitle='2 · Proteção posterior')
pick(T,'A restrição eleitoral do art. 73, V, da Lei nº 9.504/1997 vai, em regra:',[
 'Somente da votação à diplomação.',
 'Dois meses antes do pleito ao término da apuração.',
 'Dos três meses anteriores ao pleito até a posse dos eleitos.'
],2,'A lei eleitoral estabelece esse intervalo, sujeito às hipóteses e exceções específicas do dispositivo.','Não confunda com a estabilidade do art. 41 da Constituição.','Lei nº 9.504/1997, art. 73, V', 'https://www.planalto.gov.br/ccivil_03/leis/l9504.htm')
pick(T,'Servidor nomeado após concurso para cargo efetivo: o art. 41 da Constituição prevê estabilidade, em regra, após:',[
 'Três anos de efetivo exercício e avaliação especial de desempenho.',
 'Cinco anos de exercício sem concurso.',
 'Dois anos em cargo exclusivamente comissionado.'
],0,'A regra exige três anos de efetivo exercício para cargo efetivo, mediante concurso, e avaliação especial de desempenho.','O art. 19 do ADCT possui hipótese transitória distinta.','CF, art. 41',cf)
# 03 — Agentes
T='agentes'
match(T,'Relacione cada representante ou colegiado ao procedimento expressamente previsto.',[
 'Processo sindical', 'Processo judicial', 'Assistência do sindicato'
],[
 ('Falta grave de representante dos trabalhadores no Conselho Curador do FGTS.',0),
 ('Falta grave de representante dos trabalhadores no CNPS.',1),
 ('Pedido de demissão de empregado estável, como regra.',2)
],'Os dois conselhos usam processos distintos no texto legal, enquanto o pedido de demissão tem exigência específica de assistência.','É uma pegadinha de agente e procedimento, não apenas de duração.','Lei nº 8.036/1990, art. 3º, §9º; Lei nº 8.213/1991, art. 3º, §7º; CLT, art. 500',lei8036)
pick(T,'Quem NÃO tem garantia sindical apenas por sua função fiscalizadora?',[
 'Suplente eleito para a direção.',
 'Membro do conselho fiscal sindical.',
 'Diretor sindical regularmente eleito.'
],1,'Segundo a OJ 365, quem integra o conselho fiscal fiscaliza contas e não exerce a direção sindical tutelada pela norma.','Suplência de direção e conselho fiscal não são funções equivalentes.','TST, OJ 365 da SBDI-1',tst)
pick(T,'O dirigente de categoria profissional diferenciada precisa, segundo a Súmula 369, III, que:',[
 'Trabalhe em qualquer atividade, mesmo alheia à categoria.',
 'Seja eleito por votação de todos os empregados da empresa.',
 'Exerça na empresa atividade correspondente à categoria representada.'
],2,'O nexo entre a atividade efetiva e a categoria representada é requisito importante para essa garantia.','A eleição sindical isolada não resolve a situação da categoria diferenciada.','TST, Súmula 369, III',tst)
pick(T,'Quanto ao suplente eleito para representação dos empregados na CIPA:',[
 'É abrangido pela garantia reconhecida na jurisprudência.',
 'Só tem garantia se substituir definitivamente o titular.',
 'Não tem garantia porque não ocupa a presidência.'
],0,'Súmula 339, I, do TST e Súmula 676 do STF reconhecem a garantia ao suplente.','A literalidade isolada do art. 165 da CLT é insuficiente.','TST, Súmula 339, I; STF, Súmula 676',tst)
truth(T,'A mera indicação de representante patronal para a CIPA, sem eleição pelos empregados, gera automaticamente a garantia prevista no ADCT.',False,'A proteção constitucional ordinária estudada refere-se ao empregado eleito como representante dos trabalhadores.','O autor discute cenário peculiar de representante patronal eleito; isso não transforma indicação em eleição.','ADCT, art. 10, II, a; Martins, item 11.2',cf)
pick(T,'Segundo a OJ 253 da SBDI-1, o suplente de dirigente de sociedade cooperativa:',[
 'Tem a mesma garantia do dirigente, em qualquer circunstância.',
 'Não recebe essa garantia apenas por ser suplente.',
 'Possui garantia por exatamente cinco meses após a eleição.'
],1,'A OJ 253 restringe a garantia ao diretor de sociedade cooperativa nas condições legais.','Não transfira a regra do suplente da CIPA ou do sindicato para o suplente cooperativo.','TST, OJ 253 da SBDI-1',tst)
match(T,'Associe as proteções a seus beneficiários.',[
 'Conselho Curador FGTS', 'Comissão de Conciliação Prévia', 'CIPA'
],[
 ('Representantes dos trabalhadores nomeados, titulares e suplentes.',0),
 ('Representantes dos empregados eleitos, titulares e suplentes.',1),
 ('Representantes dos empregados eleitos para prevenção de acidentes e assédio.',2)
],'A titularidade dos cargos e a forma de investidura diferenciam os institutos.','Não memorize apenas um prazo de doze meses: memorize o agente e o marco.','Leis nº 8.036/1990 e 8.213/1991; CLT',clt)
pick(T,'O art. 19 do ADCT considerou estáveis determinados servidores públicos civis sem concurso, desde que contassem, na promulgação da Constituição, com:',[
 'Três anos intercalados.', 'Dez anos de serviço no mesmo cargo.', 'Cinco anos continuados de exercício.'
],2,'É uma regra transitória para servidores civis nas condições e órgãos previstos no dispositivo.','Não se trata da mesma hipótese do art. 41, aplicável a titulares de cargos efetivos.','ADCT, art. 19',cf)
fill(T,'O prazo do art. 853 da CLT para ajuizar inquérito após a suspensão é de {{blank}} dias.',
 ['30','trinta'],'O empregador conta trinta dias a partir da suspensão do empregado para a propositura do inquérito.','A pergunta não trata da duração de estabilidade.','CLT, art. 853',clt)
# 04 — Casos
T='casos'
pick(T,'A empresa é encerrada e deixa de existir a base de representação do dirigente sindical. A garantia, segundo a Súmula 369, IV:',[
 'Prossegue por dez anos na nova empresa.',
 'Não subsiste após a extinção da atividade empresarial pertinente.',
 'Converte-se necessariamente em vitaliciedade.'
],1,'A garantia protege a representação sindical na atividade empresarial.','Não é a mesma lógica aplicada à gestante diante do encerramento da empresa.','TST, Súmula 369, IV',tst)
pick(T,'O estabelecimento é extinto, não subsistindo a CIPA. Segundo a Súmula 339, II:',[
 'Não há reintegração nem indenização do período remanescente por esse fato.',
 'É sempre devida indenização em dobro até o fim do mandato.',
 'O trabalhador deve ser transferido automaticamente para outro estabelecimento.'
],0,'A garantia da CIPA não é vantagem pessoal: está ligada à existência de suas atividades no estabelecimento.','A extinção do local de trabalho deve ser diferenciada de uma dispensa arbitrária isolada.','TST, Súmula 339, II',tst)
pick(T,'A empregada estava grávida, mas o empregador não sabia ao dispensá-la. Segundo a Súmula 244, I:',[
 'A proteção depende de comunicação formal anterior à dispensa.',
 'O desconhecimento impede a reintegração e a indenização.',
 'O desconhecimento não afasta o direito à indenização decorrente da estabilidade.'
],2,'O TST adotou proteção objetiva quanto ao desconhecimento patronal da gravidez.','O livro também apresenta posição subjetiva do autor, contrária à tese predominante.','TST, Súmula 244, I; Martins, item 11.3',tst)
truth(T,'A confirmação da gravidez durante o aviso-prévio indenizado é irrelevante para a garantia gestacional.',False,'A CLT expressamente protege a confirmação ocorrida durante o contrato, inclusive aviso-prévio trabalhado ou indenizado.','A projeção do aviso-prévio pode ser determinante.','CLT, art. 391-A',clt)
pick(T,'No contrato de experiência, a gestante tem proteção conforme a tese firmada no Tema 163 do TST?',[
 'Não, a experiência sempre exclui a garantia.',
 'Sim, a garantia também alcança essa modalidade de prazo determinado.',
 'Somente mediante renovação para prazo indeterminado.'
],1,'O TST firmou em 27/06/2025 a tese de que a garantia do ADCT cabe no contrato de experiência.','Martins apresenta posição restritiva no capítulo; não a confunda com a tese repetitiva do TST.','TST, Tema 163 (2025)',tema163)
pick(T,'Após terminar o período de garantia da gestante, ela ajuíza ação dentro do prazo prescricional. Conforme a OJ 399:',[
 'O ajuizamento tardio não é por si só abuso, e pode ser devida indenização.',
 'A indenização é impossível após o fim da garantia.',
 'O prazo da garantia reinicia com a distribuição da ação.'
],0,'A OJ 399 distingue o exercício do direito de ação, sujeito à prescrição, do fim da garantia para reintegração.','A posição pessoal do autor é mais restritiva; a jurisprudência segue outra orientação.','TST, OJ 399 da SBDI-1',tst)
pick(T,'Doença profissional relacionada ao trabalho constatada após a dispensa, sem benefício acidentário prévio:',[
 'Nunca permite reconhecimento da garantia.',
 'Garante estabilidade decenal em qualquer hipótese.',
 'Pode atrair a exceção jurisprudencial se demonstrado nexo causal.'
],2,'Súmula 378, II, prevê exceção quando constatada após a dispensa doença profissional relacionada ao contrato.','A ausência do benefício não é sempre fatal, mas o nexo causal é essencial.','TST, Súmula 378, II',tst)
pick(T,'O empregado sofre acidente de trabalho durante contrato por prazo determinado. Segundo a Súmula 378, III:',[
 'O prazo determinado afasta toda garantia.',
 'Há garantia provisória também no contrato a termo.',
 'A garantia depende de contratação subsequente por prazo indeterminado.'
],1,'A jurisprudência do TST reconhece a garantia acidentária também em contrato por prazo determinado.','O livro registra orientação pessoal mais restritiva.','TST, Súmula 378, III',tst)
pick(T,'A gestante dispensada irregularmente procura o Judiciário depois de finalizado o período estabilitário. A Súmula 244, II, prevê:',[
 'Salários e direitos do período de garantia, sem reintegração após o término.',
 'Reintegração obrigatória por mais cinco anos.',
 'Extinção automática de toda pretensão indenizatória.'
],0,'Quando já não cabe reintegração no período protegido, a tutela restringe-se à indenização correspondente.','Término da garantia não apaga necessariamente direitos da dispensa anterior.','TST, Súmula 244, II',tst)
# 05 — Pontos específicos e prova
T='prova'
match(T,'Qual é a escala legal de reserva de cargos para PcD/reabilitados?',[ '2%', '3%', '4%', '5%' ],[
 ('Empresas com 100 a 200 empregados.',0),('201 a 500 empregados.',1),('501 a 1.000 empregados.',2),('1.001 ou mais empregados.',3)
],'O art. 93 apresenta progressão de 2%, 3%, 4% e 5%, conforme o porte da empresa.','A faixa intermediária de 201 a 500 corresponde a 3%, não 4%.','Lei nº 8.213/1991, art. 93',lei8213)
pick(T,'Na hipótese do art. 93, §1º, a dispensa imotivada de trabalhador reabilitado em contrato indeterminado condiciona-se:',[
 'À autorização judicial coletiva em toda e qualquer dispensa.',
 'Ao simples pagamento integral das verbas rescisórias.',
 'À contratação de substituto com deficiência ou reabilitado em condição semelhante.'
],2,'A norma exige contratação de substituto na hipótese especificada, além das demais condições legais.','É regra diferente de estabilidade por prazo fixo.','Lei nº 8.213/1991, art. 93, §1º',lei8213)
pick(T,'A dispensa de trabalhador com HIV ou doença grave que suscite estigma ou preconceito, segundo a Súmula 443:',[
 'Presume-se discriminatória e pode gerar reintegração.',
 'É livre desde que haja indenização de quarenta por cento do FGTS.',
 'Só será discriminatória se houver confissão formal do empregador.'
],0,'A Súmula 443 presume discriminatória a dispensa e considera inválido o ato, assegurando reintegração; entendimento reafirmado no Tema 254.','Presunção não é sinônimo de prova exclusivamente direta da intenção discriminatória.','TST, Súmula 443 e Tema 254','https://jurisprudencia-backend.tst.jus.br/rest/documentos/24')
clock(T,'Diretor de cooperativa criada pelos empregados: identifique o intervalo de garantia indicado na lei.',
 'Direção de sociedade cooperativa', [('Posse',False),('Registro da candidatura',True),('Primeiro ano de mandato',False)],
 [('Um ano após o mandato',True),('Fim do mandato',False),('Cinco meses após o mandato',False)],
 'O art. 55 da Lei 5.764/1971 remete às garantias do art. 543 da CLT para empregados eleitos diretores.','Não se estende automaticamente ao suplente (OJ 253).','Lei nº 5.764/1971, art. 55; CLT, art. 543','https://www.planalto.gov.br/ccivil_03/leis/l5764.htm')
truth(T,'De acordo com a jurisprudência indicada no capítulo, o mero fim do período estabilitário impede qualquer indenização pela dispensa ocorrida durante a proteção.',False,'O término do período pode afastar a reintegração, mas não necessariamente a indenização relativa ao intervalo protegido.','Distinguir reintegração da indenização substitutiva é central para a prova.','TST, Súmulas 244, II, e 396, I',tst)
fill(T,'A garantia acidentária ordinária do art. 118 da Lei 8.213/1991 dura, no mínimo, {{blank}} meses após a cessação do auxílio-doença acidentário.',
 ['12','doze'],'O prazo é de doze meses e o termo inicial é a cessação do benefício indicado.','Não conta automaticamente desde o acidente.','Lei 8.213/1991, art. 118',lei8213)
# finalize
tracks=[
 {'id':'fundamentos','label':'Fundamentos e história','short':'Fundamentos','subtitle':'Evolução da estabilidade, conceito e regime decenal','motif':'§'},
 {'id':'prazos','label':'Prazos e marcos','short':'Prazos','subtitle':'Candidatura, mandato, parto, auxílio e inquérito','motif':'12'},
 {'id':'agentes','label':'Agentes e procedimentos','short':'Agentes','subtitle':'Quem está protegido e quem apura a falta grave','motif':'◎'},
 {'id':'casos','label':'Casos e jurisprudência','short':'Casos','subtitle':'Gestante, acidentado, CIPA e reintegração','motif':'⚖'},
 {'id':'prova','label':'Miudezas de prova','short':'Prova','subtitle':'Percentuais, exceções e distinções finas','motif':'✦'},
]
questions=questions[:-2]  # preserva as 42 atividades do laboratório conversacional; elimina 2 repetições finais
# Revisão editorial: distratores próximos e comprimento da resposta correta não previsível.
# As alterações abaixo só ampliam alternativas ERRADAS; preservam os gabaritos.
distratores_equilibrados={
 'EST4-001':{2:'A proibição de dispensa imotivada que permanece mesmo depois do período protegido.'},
 'EST4-002':{0:'Uma modalidade exclusiva de estabilidade decenal que alcança todos os contratos de trabalho.'},
 'EST4-003':{0:'A Lei nº 8.036, de 1990, que reorganizou o Fundo de Garantia do Tempo de Serviço.'},
 'EST4-005':{1:'Cinco anos continuados de trabalho público, independentemente de concurso.'},
 'EST4-007':{2:'Depende de prévia sentença trabalhista, dispensada a assistência de qualquer sindicato.'},
 'EST4-019':{0:'Trabalhe em qualquer atividade, ainda que não corresponda à categoria representada.'},
 'EST4-020':{1:'Só tem garantia se substituir definitivamente o titular afastado durante o mandato.'},
 'EST4-023':{0:'Tem garantia igual à do diretor eleito, ainda que a lei não trate expressamente da suplência.'},
 'EST4-028':{1:'Dez anos de serviço no mesmo cargo, independentemente do órgão público de origem.'},
 'EST4-030':{0:'Prossegue por dez anos na nova empresa para a qual o empregado eventualmente seja transferido.'},
 'EST4-032':{0:'A proteção depende de comunicação formal anterior à dispensa, inclusive se a gestação começou antes.'},
 'EST4-034':{0:'Não, a experiência sempre exclui a garantia, mesmo quando a gravidez ocorre durante o contrato.'},
 'EST4-035':{1:'A indenização é impossível depois do fim da garantia, ainda que a ação esteja dentro do prazo prescricional.'},
 'EST4-036':{0:'Nunca há garantia se não tiver sido concedido auxílio-doença acidentário antes da dispensa.'},
 'EST4-038':{2:'Extinção de qualquer pretensão indenizatória, ainda que o pedido ocorra dentro do prazo prescricional.'},
 'EST4-040':{0:'À autorização judicial coletiva sempre que houver dispensa imotivada do empregado com deficiência.'},
}
for q in questions:
 if q['kind']=='pick' and q['id'] in distratores_equilibrados:
  for i,label in distratores_equilibrados[q['id']].items():
   assert i!=q['answer']
   q['options'][i]=label

assert len(questions)==42,len(questions)
for q in questions:
 assert q['why'] and q['source']
 if q['kind']=='pick': assert len(q['options'])==3 and 0<=q['answer']<3
 if q['kind']=='clock': assert 0<=q['whenAnswer']<3 and 0<=q['toAnswer']<3
 if q['kind']=='order': assert len(q['items'])==len(q['answer'])
obj={'meta':{'title':'Garantias de Emprego e Estabilidade — Laboratório','language':'pt-BR','version':'4.0','totalActivities':len(questions),'typeCounts':dict(Counter(q['kind'] for q in questions)),'sourceNote':'Fonte principal: capítulo enviado de Sérgio Pinto Martins. Jurisprudência e legislação discriminadas em cada atividade. Orientações divergentes do autor identificadas.'},'tracks':tracks,'questions':questions}
(root/'estabilidade.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Generated',len(questions),'tracks',Counter(q['track'] for q in questions),'types',Counter(q['kind'] for q in questions),'answers by position',Counter(q['answer'] for q in questions if q['kind']=='pick'))
