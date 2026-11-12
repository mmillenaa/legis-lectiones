# Legis Lectiones · Greve — Laboratório v3

## O que foi entregue

Uma reformulação completa do banco de **Greve**, baseada no capítulo estudado de Sergio Pinto Martins, inclusive nas 13 perguntas finais, e na legislação e nos precedentes expressamente citados.

**45 desafios** em cinco percursos: Fundamentos (8), Agentes (8), Prazos (10), Efeitos (10) e Prova do professor (9). Em vez das 40 questões de quatro alternativas, a versão traz **22 questões de três opções**, **7 veredictos**, **7 associações**, **3 sequências**, **3 relógios jurídicos de duas decisões** e **3 lacunas**.

O banco dá especial atenção a: datas e destinatários; 48 e 72 horas; publicação de sentença normativa em 15 dias (Lei 10.192/2001, art. 12, § 2º); trabalhadores, assembleia, sindicato e comissão; quórum estatutário; portos e compensação bancária; hipóteses de abusividade; greve de zelo; solidariedade; e lockout.

## Implantação no repositório

No repositório `mmillenaa/legis-lectiones`, pasta **`labour-law/`**:

1. Substituir `labour-law/greve.html` pelo arquivo `greve.html` fornecido.
2. Substituir `labour-law/greve.json` pelo arquivo `greve.json` fornecido.
3. Manter os arquivos compartilhados `p2-quiz.js`, `p2-quiz.css`, `result-celestial.js` e demais bancos **sem alterações**. O novo HTML de Greve usa motor próprio para não interferir nas outras páginas. A celebração celestial continua integrada, se presente no repositório.

Esta versão **não foi publicada nem commitada** no GitHub. As duas substituições só ocorrem quando você as aplicar.

## Uso

Abra `greve.html` para experimentar a versão embutida, mesmo sem servidor. Ao publicá-la no GitHub Pages junto ao `greve.json`, a aplicação lê o JSON externo; assim, é possível editar questões somente no JSON publicado.

O botão **Começar com 8 desafios** cria rodadas pequenas, priorizando assuntos ainda não respondidos. **Trilha completa** percorre 45 atividades. É possível escolher uma das cinco trilhas e revisar somente erros pendentes.

A primeira resposta de cada questão é conservada. Revisões atualizam o domínio atual daquela questão sem apagar se a resposta inicial estava errada. Os dados ficam apenas no navegador, sob a chave `legis-lectiones:labour:greve:lab-v3`, diferente do progresso da versão antiga (`...:v1`).

## Edição dos arquivos

`greve.html` já inclui CSS, JS e uma cópia do conteúdo para funcionar como arquivo único. O pacote também inclui `greve-lab.css`, `greve-lab.js` e `assemble.py` como fontes editoriais.

Se alterar o JSON, em **produção** basta republicar `greve.json`. Se também quiser atualizar a cópia embutida para abrir o HTML sem servidor, execute no mesmo diretório:

```bash
python assemble.py
```

O script reúne o JSON, o CSS e o JavaScript no `greve.html`. Não é preciso editar o motor compartilhado do site.

## Verificações realizadas

- Sintaxe JavaScript: `node --check`, sem erro.
- Estrutura JSON: 45 IDs únicos, tipos válidos e todos os gabaritos dentro das opções.
- Teste automatizado em navegador Chromium: fluxo de **45/45 respostas corretas** e resultado de 100%, sem exceções JavaScript.
- Teste de **erro → revisão → acerto**: mantém o erro original na primeira tentativa e remove a pendência após o acerto.
- Capturas de prévia para tela de computador, relógio e largura móvel (390px).

**Limite do teste:** a suíte usou uma página injetada no Chromium sem chamadas a fontes externas, analytics e efeitos visuais opcionais. O funcionamento em produção no GitHub Pages e a integração com scripts remotos não foram testados neste ambiente.

## Atenção jurídica

As questões sinalizadas como **posição doutrinária do autor** refletem a perspectiva de Martins, especialmente sobre greve política, solidariedade, greve de zelo e participação na assembleia. Não as apresente como consenso jurídico. Para assuntos normativos foram consultados o texto atualizado da Lei 7.783/1989, a Constituição e o STF (Temas 531 e 541).
