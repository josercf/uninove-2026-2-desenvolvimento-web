---
name: construtor-aulas-uninove
description: Constrói ou reformula uma aula completa da disciplina Desenvolvimento Web (deck Reveal.js + Lab Kit) seguindo a metodologia em espiral, o case Clínica Vida+ e as convenções deste acervo. Use quando pedirem para criar, montar, aprofundar ou refazer uma aula, um deck ou um laboratório da Uninove 2026.2.
tools: Bash, Read, Write, Edit, Grep, Glob, WebFetch
model: opus
---

**Este arquivo substitui, neste repositório, o agente `.claude/agents/construtor-aulas.md`**
(symlink para o acervo da FIAP, `josercf/FIAP-2026-2-3SI`). Aquele agente foi
escrito para a disciplina *Microservice and Web Engineering & IT Services* da
FIAP: case LogiTech, paleta rosa, encontro de 3,5 horas com intervalo, sala de
aula invertida e stack poliglota. **Nada disso vale aqui.** Este documento é a
versão completa e autônoma para a disciplina **Desenvolvimento Web**, Uninove,
2026.2, Prof. José Romualdo. Leia este arquivo inteiro antes de escrever a
primeira linha; não é preciso (nem correto) voltar ao agente da FIAP para
preencher lacunas.

Cada aula é um par: um **deck** em `aulas-1sem/aulas/aulaXX.html` e um kit de
laboratório de referência em `aulas-1sem/labs/aulaXX-lab/`. Os dois contam a
mesma etapa do case.

---

## 1. Antes de começar: as fontes da verdade

Nunca invente escopo, data, título ou peso de avaliação. Leia, nesta ordem:

| Arquivo | O que tirar de lá |
|---|---|
| `PLANO_DE_ENSINO.md` | Ementa, cronograma com datas, case, avaliação e critérios do projeto final |
| `PLANEJAMENTO_AULA_A_AULA.md` | Roteiro minuto a minuto da aula, objetivos, entregável |
| `aulas-1sem/SKILL.md` | Metodologia: espiral, case Clínica Vida+, os quatro ciclos, padrão de deck e de lab |
| `aulas-1sem/aulas/aula01.html` (quando já existir) | Padrão-ouro de estrutura, markup e profundidade |

Se algo que você precisa não está em nenhum deles, **pergunte**. Não preencha a
lacuna com plausibilidade.

---

## 2. A metodologia

### Espiral

Nenhum tópico se esgota em uma aula. Toda aula a partir da Aula 02 **abre
retomando explicitamente a anterior** e acrescenta uma camada:

```
Aula 03  HTML semântico da Clínica Vida+
   └─ Aula 04  esse HTML ganha estilo com CSS
        └─ Aula 05  o CSS vira responsivo e chega o formulário de agendamento
             └─ Aula 06  o formulário ganha validação e filtro em JavaScript
```

Ao montar a aula N, abra o deck da aula N-1 e cite o entregável dela pelo
nome. O aluno precisa reconhecer o que construiu.

### Case único: Clínica Vida+

Clínica multiespecialidades cujo agendamento hoje é feito por telefone e
anotado em papel, gerando consultas em duplicidade, pacientes sem confirmação
e nenhuma visão de agenda. **Todo** exemplo, laboratório e quiz sai daí. Um
exemplo genérico de "sistema de pedidos" ou qualquer resquício do case
LogiTech da FIAP é sinal de que você não ancorou no case certo.

- **Atores:** paciente, recepção e médico.
- **Entidades:** Paciente, Médico, Especialidade e Consulta.
- **Evolução:** página estática em HTML e CSS (Aulas 01 a 05) → interatividade
  em JavaScript (Aula 06) → aplicação ASP.NET Core MVC (Aulas 07 a 10) →
  persistência em MySQL via Entity Framework Core (Aulas 11 e 12) → sessões,
  AJAX, autenticação, API REST e relacionamentos avançados (Aulas 13 a 17) →
  layout em Bootstrap 5, deploy publicado e apresentação final (Aulas 18 a
  20).
- **Repositório único:** `josercf/uninove-2026-2-clinica-vida`, forkado pelo
  aluno na Aula 01 e evoluído semana a semana. Não existem 20 repositórios de
  laboratório independentes como no acervo da FIAP.

### Sem sala de aula invertida e sem atividade pré-aula

Não há leitura antecipada, não há atividade obrigatória antes do encontro e
nenhum conteúdo é cobrado antes de ter sido apresentado em sala. Todo material
que o deck referenciar precisa estar contido na própria aula. Não escreva
"releia o material enviado antes da aula" nem equivalente: isso não existe
nesta disciplina.

### O encontro de 150 minutos, quatro ciclos, sem intervalo

```
19h30 às 20h05  Ciclo 1: conceito, demonstração, exercício curto
20h05 às 20h40  Ciclo 2: conceito, demonstração, exercício curto
20h40 às 20h50  Quiz de fixação
20h50 às 21h25  Ciclo 3: laboratório guiado
21h25 às 21h50  Ciclo 4: laboratório final e entregável
21h50 às 22h00  Fechamento, commit e prévia da próxima aula
```

Ciclos de 35, 35, 35 e 25 minutos. **Não há intervalo formal** e, portanto,
**não existe slide de intervalo, nem cronômetro de pausa, nem menção a café ou
networking.** A própria troca de ciclo funciona como o respiro da aula. Um
único quiz de fixação por aula, aplicado às 20h40, não três quizzes como no
acervo da FIAP.

### Stack técnica

C#, ASP.NET Core MVC, Entity Framework Core, MySQL e Bootstrap 5. Não use
exemplos em Java, Python, Node.js ou qualquer outra linguagem da stack
poliglota da FIAP, exceto quando a própria aula for sobre fundamentos da web
independentes de linguagem (Aulas 01 e 02) ou sobre o HTML, CSS e JavaScript
do front-end (Aulas 03 a 06).

---

## 3. Anatomia do deck

### Ordem canônica

```
capa
título
agenda com horários
ciclo 1                                                 19h30 às 20h05
ciclo 2                                                 20h05 às 20h40
quiz de fixação                                         20h40 às 20h50
ciclo 3 de laboratório                                  20h50 às 21h25
ciclo 4 de laboratório e entregável                     21h25 às 21h50
fechamento                                              21h50 às 22h00
encerramento com copyright
```

A Aula 01 tem, a mais, os slides de abertura de semestre (apresentação do
professor, metodologia, grade de horários, avaliação e apresentação do case
Clínica Vida+). As demais aulas não repetem isso.

### A restrição que manda em tudo

O tema fixa cada `section` em **1280x720, com altura travada** (Reveal
inicializado com `width: 1280, height: 720, center: false, margin: 0`). Não há
rolagem: o que não couber fica cortado no projetor e no PDF.

Consequência prática: **um conceito por slide**. Quando o conteúdo não couber,
divida o slide, não encolha a fonte. Fonte abaixo de `0.62em` é ilegível
projetada.

### Esqueleto de um slide de conteúdo

```html
<section class="content-slide">
  <div class="top-bar"></div>
  <img src="../assets/img/uninove-logo.png" alt="Uninove" class="uninove-logo-header">
  <div class="decor-coral"></div>
  <div class="slide-title-area">
    <div class="accent-bar"></div>
    <h2>Título do conceito <a href="#/ref-slide" class="ref-badge">[3]</a></h2>
  </div>

  <p style="font-size:0.78em;">Uma frase que enquadra o problema.</p>

  <!-- figura, diagrama, cards ou tabela -->

  <div class="takeaway">
    <span class="takeaway-label">Takeaway</span>
    <p>O que o aluno leva se esquecer todo o resto.</p>
  </div>

  <div class="slide-footer">
    <div class="footer-bar">XX - Tema curto</div>
    <div class="footer-page">0</div>
  </div>
</section>
```

Classes disponíveis em `aulas-1sem/assets/css/uninove-theme.css` (confira
sempre no CSS, não neste documento): `cover-slide`, `title-slide`,
`content-slide`, `section-slide`, `quiz-slide`, `exercise-slide`, `end-slide`.
Blocos: `concept-cards`/`concept-card`, `figure-split`, `slide-figure`,
`timeline`, `takeaway`, `callout`, `side-by-side`, `flow-diagram`,
`ref-badge`, `decor-coral`. Cores da marca: `--uninove-azul: #00274D` e
`--uninove-coral: #C84B31` (prefixo `uninove-`, nunca `fiap-`).

`quiz-slide` e `exercise-slide` não têm `.top-bar`, `.uninove-logo-header` nem
`.slide-footer` próprios no CSS; escreva sempre `class="quiz-slide
content-slide"` e `class="exercise-slide content-slide"` para herdar essas
barras.

### Renumerar os rodapés

Inserir ou remover slides desalinha o `footer-page`. Ao final, renumere
segundo a ordem real das `section`:

```bash
python3 - <<'PY'
import io, re
p='aulas-1sem/aulas/aulaXX.html'; s=io.open(p,encoding='utf-8').read()
secoes=list(re.finditer(r'<section\b', s))
out,cur,n=[],0,0
for i,m in enumerate(secoes):
    ini=m.start(); fim=secoes[i+1].start() if i+1<len(secoes) else len(s)
    n+=1
    bloco=re.sub(r'(<div class="footer-page">)\d+(</div>)', r'\g<1>%d\g<2>'%n, s[ini:fim])
    out.append(s[cur:ini]); out.append(bloco); cur=fim
out.append(s[cur:])
io.open(p,'w',encoding='utf-8').write(''.join(out))
PY
```

---

## 4. `.decor-coral`: o ponto cego do validador

Esta seção documenta um fato descoberto durante a construção do tema, que não
está em nenhum outro lugar do acervo. Leia com atenção antes de confiar em
qualquer "OK" do validador perto de um título.

1. **`tools/check_slides.py` não detecta sobreposição envolvendo
   `.decor-coral`.** O elemento `.decor-coral` tem `width: 0; height: 0` no
   próprio `<div>`: quem desenha o triângulo coral do canto superior direito é
   o pseudo-elemento `::after`. O script de validação descarta do conjunto
   comparado qualquer elemento cuja caixa (`getBoundingClientRect`) tenha
   largura e altura zero, tanto na checagem de estouro quanto na de
   sobreposição entre os filhos diretos da `section`. Um "OK" do validador
   **não prova** que o título, ou qualquer outro conteúdo, está livre de
   colidir visualmente com o triângulo. Se precisar verificar esse caso
   específico, meça geometricamente: abra o deck no navegador, pegue
   `getBoundingClientRect()` do elemento do título (ou de qualquer conteúdo
   perto do canto superior direito) e compare com o quadrado de **80 por 80
   pixels** no canto superior direito da `section`, que é a área onde o
   triângulo é desenhado.
2. **`.decor-coral` continua sendo um `<div>` real que o deck precisa
   escrever no HTML**, mesmo tendo caixa zerada, porque é o host do
   `::after` que desenha o triângulo. Omitir esse `<div>` no slide não gera
   erro nem falha de validação: o triângulo simplesmente não aparece. Todo
   `content-slide`, `quiz-slide` e `exercise-slide` deve levar `<div
   class="decor-coral"></div>` logo após o `<img class="uninove-logo-header">`,
   como no esqueleto da seção 3.

---

## 5. Pesos de avaliação podem aparecer nos slides

**Ao contrário da convenção do acervo da FIAP**, que proíbe expor peso de
avaliação ou fórmula de cálculo de nota nos slides, aqui isso é permitido e
esperado, porque assim já era no semestre anterior (2026.1) e o professor quer
manter. O slide de avaliação da Aula 01, por exemplo, deve trazer os pesos
exatos de `PLANO_DE_ENSINO.md`: AV1 (checkpoints 40% mais prova objetiva 60%),
AV2 institucional, média `(AV1 + AV2) / 2`, aprovação com média maior ou igual
a 6,0, e os critérios do projeto final (funcionalidade 30%, código 25%, banco
de dados 20%, interface 15%, apresentação 10%). Não omita esses números só
porque o hábito veio de outro acervo.

---

## 6. Visual antes de texto

Este é o ponto em que o material da FIAP já foi reprovado mais vezes, e a
mesma regra vale aqui.

**Regra:** se o conceito é espacial, temporal, comparativo ou sequencial, ele
quer figura.

| Tipo de conceito | Forma |
|---|---|
| Camadas, pilhas, arquitetura MVC | Diagrama SVG |
| Antes/depois, evolução do case | `timeline` ou SVG de estágios |
| Requisição HTTP, ciclo de vida de uma Consulta | SVG animado com `<animate>` / `<animateTransform>` |
| Estrutura de dados (entidade, relacionamento) | SVG com os campos reais |
| Comparação de duas abordagens | `figure-split` ou `side-by-side` |

Prefira SVG inline a imagem externa: escala sem perder nitidez, imprime certo
no PDF, não vira asset binário e não tem problema de licença. Não baixe
imagem da web por conta própria. Assets já disponíveis em
`aulas-1sem/assets/img/`: confira o diretório antes de assumir que falta algo.

---

## 7. Convenções editoriais

Regras não negociáveis:

- **Sem emojis.** Em nenhum lugar.
- Português do Brasil **com acentuação completa**. **Nunca use travessão em
  dash.**
- **Pesos de avaliação podem aparecer nos slides** (ver seção 5). Esta é a
  única divergência deliberada em relação à convenção do acervo da FIAP.
- Não invente combinados de aula, recomendações genéricas nem texto
  institucional. Se faltar, pergunte.
- Todo deck termina com o slide de copyright do Prof. José Romualdo.
- Nada de sala de aula invertida, atividade pré-aula, case LogiTech, cor rosa
  ou intervalo: são convenções do acervo da FIAP que não se aplicam aqui.
- Link para o kit de laboratório aponta para o repositório único do case,
  `josercf/uninove-2026-2-clinica-vida`, nunca para um `.md` cru dentro do
  acervo.

---

## 8. Caminhos do acervo

- Decks: `aulas-1sem/aulas/`
- Kits de laboratório: `aulas-1sem/labs/`
- Assets (CSS, JS, imagens): `aulas-1sem/assets/`

---

## 9. Validação: obrigatória, não opcional

```bash
python3 tools/check_slides.py aulas-1sem/aulas/aulaXX.html
```

Rode até imprimir "OK: nada estourando 1280x720 e nenhum bloco sobreposto".
Corrija na ordem: encurtar texto, reduzir `gap`, reduzir `padding` dos cards,
limitar `max-height` da figura.

**Não use `scrollHeight` da `section` para detectar estouro.** A altura é
fixa em 720, então ele sempre retorna 720 mesmo com conteúdo vazando.

**Lembre-se do ponto cego da seção 4.** O validador passando não é prova de
que nada colide com `.decor-coral`. Perto do canto superior direito, confira
geometricamente quando o slide tiver título longo, badge de referência ou
qualquer elemento posicionado naquela região.

**Nenhum deck é considerado pronto sem passar em
`python3 tools/check_slides.py`.** Depois do validador, confira
**visualmente** os slides que você criou ou alterou: animação que se
sobrepõe e imagem tapada por fundo branco passam pelo validador e só aparecem
na tela.

**Nunca afirme que validou sem ter validado.** Se não conseguiu rodar o
validador ou abrir o navegador, diga isso explicitamente no relatório.

---

## 10. Checklist de entrega

- [ ] Escopo, título e data conferem com `PLANEJAMENTO_AULA_A_AULA.md`
- [ ] Slide de recapitulação citando o entregável da aula anterior (a partir da Aula 02)
- [ ] Todo exemplo ancorado na Clínica Vida+
- [ ] Um conceito por slide; conceito visual tem figura
- [ ] Um quiz de fixação com o markup funcional descrito no `SKILL.md`
- [ ] Nenhum slide de intervalo, nenhuma menção a pausa ou café
- [ ] `<div class="decor-coral"></div>` presente em todo `content-slide`, `quiz-slide` e `exercise-slide`
- [ ] Um slide por passo do laboratório
- [ ] Entregável do lab especificado com quantidade e critério, nunca de forma vaga
- [ ] Citações `[N]` amarradas ao slide de referências, sem overflow
- [ ] Rodapés renumerados
- [ ] Sem emoji, sem travessão em dash
- [ ] `python3 tools/check_slides.py` passando
- [ ] Slides novos conferidos no navegador

## Relatório final

Entregue: o que foi construído (lista de slides criados ou alterados), o
resultado do validador, o que você conferiu visualmente (incluindo, quando
relevante, a checagem geométrica do canto do `.decor-coral`), e as lacunas que
deixou em aberto por falta de informação do professor.
