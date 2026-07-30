---
name: uninove-course-design
description: Metodologia e padrão de construção das aulas de Desenvolvimento Web da Uninove 2026.2. Inclui a espiral de conteúdo, o case Clínica Vida+, a estrutura do encontro de 150 minutos em quatro ciclos, o padrão dos decks Reveal.js com tema Uninove e o padrão dos kits de laboratório.
---

# Uninove Course Design Skill: Metodologia e Construção das Aulas de Desenvolvimento Web

Este guia consolida a metodologia pedagógica e os padrões técnicos de construção
do acervo da disciplina **Desenvolvimento Web**, Uninove, 2026.2, Prof. José
Romualdo. Duas turmas com conteúdo idêntico, quarta e quinta-feira, 19h30 às
22h, 20 encontros de 150 minutos cada.

Este documento é a fonte da verdade de metodologia e padrão de construção. Para
datas, títulos e escopo aula a aula, a fonte é `PLANEJAMENTO_AULA_A_AULA.md`; para
ementa, cronograma e avaliação, `PLANO_DE_ENSINO.md`.

---

## 1. Pilares metodológicos

A construção das aulas se apoia em dois pilares integrados.

### 1.1 Aprendizagem em espiral

Nenhum tópico técnico se esgota em uma única aula. Toda aula a partir da Aula
02 **abre retomando explicitamente a aula anterior** e acrescenta uma camada
nova sobre o que já existe. Ao montar a aula N, cite pelo nome o entregável da
aula N-1: o aluno precisa reconhecer o que construiu antes de avançar.

```
Aula 03  HTML semântico da Clínica Vida+
   └─ Aula 04  esse HTML ganha estilo com CSS
        └─ Aula 05  o CSS vira responsivo e chega o formulário de agendamento
             └─ Aula 06  o formulário ganha validação e filtro em JavaScript
```

### 1.2 Aprendizagem por case: Clínica Vida+

Todo exemplo, laboratório e quiz do semestre orbita um único case, a **Clínica
Vida+**, um sistema de agendamento de consultas médicas. Não há exercícios de
tema genérico soltos ao longo do curso.

- **Mini mundo:** clínica multiespecialidades cujo agendamento hoje é feito por
  telefone e anotado em papel, gerando consultas em duplicidade, pacientes sem
  confirmação e nenhuma visão de agenda.
- **Atores:** paciente, recepção e médico.
- **Entidades:** Paciente, Médico, Especialidade e Consulta.
- **Evolução:** o case nasce como página estática em HTML e CSS (Aulas 01 a
  05), ganha interatividade no navegador com JavaScript (Aula 06), vira
  aplicação ASP.NET Core MVC (Aulas 07 a 10), passa a persistir em MySQL via
  Entity Framework Core (Aulas 11 e 12), acumula sessões, AJAX, autenticação,
  API REST e relacionamentos avançados (Aulas 13 a 17) e termina com layout em
  Bootstrap 5, deploy publicado e apresentação do projeto final (Aulas 18 a
  20).
- **Repositório único:** diferente de um lab por aula, existe um único
  repositório-esqueleto, `josercf/uninove-2026-2-clinica-vida`, que o aluno
  forka na Aula 01 e evolui semana a semana. Os diretórios em
  `aulas-1sem/labs/` são a referência e o gabarito do professor para cada
  etapa, não repositórios independentes.

### 1.3 Sem sala de aula invertida

A disciplina **não usa sala de aula invertida**. Não há atividade
pré-aula, não há leitura antecipada e nenhum conteúdo é cobrado antes de ter
sido apresentado em sala. Cada encontro é **autossuficiente**: tudo o que o
aluno precisa para acompanhar a aula chega dentro dela mesma. Esta é uma
diferença deliberada em relação a outros acervos que a mesma família de tema
serve, motivada pela baixa adesão de leitura prévia observada no semestre
anterior (ver ADR-004).

---

## 2. Estrutura do encontro de 150 minutos

Cada encontro tem 150 minutos corridos, das 19h30 às 22h, **sem intervalo
formal**, organizados em quatro ciclos de 35, 35, 35 e 25 minutos, mais quiz e
fechamento de 10 minutos cada:

```
19h30 às 20h05  Ciclo 1: conceito, demonstração, exercício curto
20h05 às 20h40  Ciclo 2: conceito, demonstração, exercício curto
20h40 às 20h50  Quiz de fixação
20h50 às 21h25  Ciclo 3: laboratório guiado
21h25 às 21h50  Ciclo 4: laboratório final e entregável
21h50 às 22h00  Fechamento, commit e prévia da próxima aula
```

- **Ciclos 1 e 2** seguem sempre o mesmo ritmo interno: o professor apresenta o
  conceito, demonstra ao vivo no projetor e o aluno reproduz num exercício
  curto, ainda dentro do ciclo.
- **O quiz de fixação**, às 20h40, quebra o ritmo entre a teoria dos dois
  primeiros ciclos e o laboratório dos dois últimos.
- **Ciclos 3 e 4** são laboratório: o aluno constrói uma etapa concreta do case
  com o professor circulando pela sala. O entregável nasce dentro do Ciclo 4,
  não fora da aula.
- **O fechamento** inclui o commit e o push do trabalho do dia no fork do
  aluno, mais a prévia da aula seguinte.

Não há intervalo: a própria troca de ciclo, a cada 35 minutos aproximadamente,
funciona como o respiro da aula.

---

## 3. Eixos de conteúdo da disciplina

Toda aula se encaixa em um destes sete eixos, que avançam em espiral ao longo
do semestre:

1. **Fundamentos da web e redes:** arquitetura cliente-servidor, TCP/IP, DNS,
   HTTP e HTTPS.
2. **HTML e CSS:** marcação semântica, estilização, Flexbox, Grid, layout
   responsivo e formulários com validação nativa.
3. **JavaScript e DOM:** tipos, funções, manipulação do DOM, eventos e
   requisições assíncronas com `fetch`.
4. **C# e ASP.NET Core MVC:** a linguagem C#, o padrão MVC, rotas,
   Controllers, Views Razor, Models e Data Annotations.
5. **Entity Framework Core e MySQL:** migrations, CRUD e relacionamentos entre
   entidades.
6. **Segurança e autenticação:** cookies, sessões, autenticação e autorização.
7. **API REST e deploy:** serviços web no estilo REST e publicação da
   aplicação em ambiente acessível pela internet.

---

## 4. Anatomia do deck Reveal.js

Cada aula tem uma apresentação HTML autocontida em
`aulas-1sem/aulas/aulaXX.html`, publicada por CDN, sem build e sem bundler.

### 4.1 Esqueleto do arquivo

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Aula XX: Título da aula | Desenvolvimento Web Uninove</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/white.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/highlight/monokai.css">
  <link rel="stylesheet" href="../assets/css/uninove-theme.css">
  <link rel="stylesheet" href="../assets/css/uninove-print.css">
</head>
<body>
  <div class="reveal">
    <div class="slides">
      <!-- Capa -->
      <section class="cover-slide">...</section>
      <!-- Título da aula -->
      <section class="title-slide">...</section>
      <!-- Agenda com os horários dos quatro ciclos -->
      <section class="content-slide">...</section>
      <!-- Ciclo 1: conceito, demonstração, exercício curto -->
      <section class="content-slide">...</section>
      <!-- Ciclo 2: conceito, demonstração, exercício curto -->
      <section class="content-slide">...</section>
      <!-- Quiz de fixação -->
      <section class="quiz-slide content-slide">...</section>
      <!-- Ciclo 3: laboratório guiado -->
      <section class="content-slide">...</section>
      <!-- Ciclo 4: laboratório final e entregável -->
      <section class="content-slide">...</section>
      <!-- Fechamento: commit, push e prévia da próxima aula -->
      <section class="content-slide">...</section>
      <!-- Encerramento com copyright -->
      <section class="end-slide">...</section>
    </div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/highlight/highlight.js"></script>
  <script src="../assets/js/uninove-quiz.js"></script>
  <script>
    Reveal.initialize({
      width: 1280,
      height: 720,
      center: false,
      margin: 0,
      plugins: [ RevealHighlight ]
    });
  </script>
</body>
</html>
```

O tema fixa cada `section` em **1280x720, com altura travada**. O conteúdo não
rola: o que não couber quebra o slide visualmente, sem lançar nenhum erro no
console. Consequência prática: um conceito por slide. Quando o conteúdo não
couber, divida em dois slides, não encolha a fonte.

### 4.2 Ordem canônica dos slides

Segue exatamente os quatro ciclos do encontro, na ordem em que acontecem em
sala:

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

### 4.3 Classes do tema Uninove

Conferidas em `aulas-1sem/assets/css/uninove-theme.css`. Não confie neste
documento nem em nenhum outro: confira sempre no CSS.

**Classes de `section`:** `cover-slide`, `title-slide`, `content-slide`,
`section-slide`, `quiz-slide`, `exercise-slide`, `end-slide`.

**Atenção:** `quiz-slide` e `exercise-slide` **não têm regras próprias** de
`.top-bar`, `.uninove-logo-header` nem `.slide-footer` no CSS. Essas barras só
aparecem se o slide também levar a classe `content-slide`, por isso o padrão é
sempre escrever `class="quiz-slide content-slide"` (e o mesmo vale para
`exercise-slide content-slide`).

**Blocos reutilizáveis:** `slide-title-area` com `accent-bar`, `top-bar`,
`uninove-logo-header`, `slide-footer` com `footer-bar` e `footer-page`,
`concept-cards` com `concept-card`, `side-by-side` com `side`, `figure-split`,
`slide-figure`, `timeline` com `tl-item`, `tl-dot`, `tl-year`, `tl-tool` e
`tl-desc`, `takeaway` com `takeaway-label`, `callout`, `flow-diagram` com
`flow-item` e `flow-arrow`, `ref-badge`, `decor-coral`.

Cores da marca: `--uninove-azul: #00274D` e `--uninove-coral: #C84B31`,
definidas em `:root` no próprio tema.

### 4.4 Esqueleto de um slide de conteúdo

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

`.decor-coral` é o triângulo coral do canto superior direito. É um `<div>`
real com caixa zerada no próprio elemento: quem desenha o triângulo é o
pseudo-elemento `::after`. Precisa ser escrito no HTML de cada slide de
conteúdo, quiz ou exercício; ele não aparece sozinho.

---

## 5. Quizzes de fixação

Um quiz por aula, aplicado às 20h40, entre o Ciclo 2 e o Ciclo 3. O markup que
funciona com `assets/js/uninove-quiz.js` é o padrão de lista:

```html
<section class="quiz-slide content-slide">
  <div class="top-bar"></div>
  <img src="../assets/img/uninove-logo.png" alt="Uninove" class="uninove-logo-header">
  <div class="decor-coral"></div>
  <div class="slide-title-area">
    <div class="accent-bar"></div>
    <h2>Quiz de Fixação</h2>
  </div>

  <div class="quiz-container">
    <div class="quiz-question">Pergunta direta, sem rodeio.</div>
    <ul class="quiz-options">
      <li data-correct="false"><span class="option-letter">A</span> Opção A</li>
      <li data-correct="true"><span class="option-letter">B</span> Opção B</li>
      <li data-correct="false"><span class="option-letter">C</span> Opção C</li>
      <li data-correct="false"><span class="option-letter">D</span> Opção D</li>
    </ul>
    <div class="quiz-feedback"
         data-correct-msg="Correto. Explica por que."
         data-incorrect-msg="Incorreto. Aponta o que revisar."></div>
  </div>
</section>
```

Regras de markup:

- `.quiz-container` envolve todo o quiz.
- `<div class="quiz-question">` traz o enunciado, direto, sem rodeio.
- `<ul class="quiz-options">` contém um `<li data-correct="true">` ou
  `data-correct="false">` por alternativa, cada um com
  `<span class="option-letter">` para a letra.
- Exatamente uma alternativa leva `data-correct="true"`.
- `<div class="quiz-feedback">` carrega os atributos `data-correct-msg` e
  `data-incorrect-msg`, com o texto completo exibido em cada caso. O script
  lê esses atributos: não é preciso registrar a resposta certa em nenhum outro
  lugar.

---

## 6. Padrão dos kits de laboratório

Cada aula tem um diretório de referência em `aulas-1sem/labs/aulaXX-lab/`,
contendo o roteiro e o gabarito daquela etapa do case, com:

1. **`README.md`:**
   - O passo do case Clínica Vida+ que a aula resolve, ligado ao entregável da
     aula anterior.
   - Pré-requisitos e comandos de execução passo a passo.
   - O entregável esperado, especificado com quantidade e critério, nunca de
     forma vaga.
   - Critérios de aceitação em tabela.
   - Instrução do commit e push esperados no fork do aluno.
2. **Código de referência** que resolve o passo da aula, servindo de gabarito
   para o professor durante a correção.

Diferente de um acervo com um repositório de laboratório por aula, aqui existe
um único repositório-esqueleto do case,
`josercf/uninove-2026-2-clinica-vida`, que o aluno forka na Aula 01 e evolui
a cada encontro. Os diretórios em `aulas-1sem/labs/` nunca substituem esse
repositório: são a referência do professor, não o material que o aluno clona
ou forka.

Os slides do laboratório, dentro do deck, seguem um slide por passo: o aluno
acompanha a tela enquanto executa, sem precisar dividir atenção entre o slide
e um roteiro à parte.
