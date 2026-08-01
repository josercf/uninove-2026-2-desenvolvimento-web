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

### A paleta da Clínica Vida+

O case tem identidade visual própria, **distinta do azul e coral da Uninove**.
As cores da Uninove vestem o deck do professor; estas vestem o site que o aluno
constrói. Foram fixadas na Aula 04, quando o CSS entra, e valem daí em diante,
inclusive na customização do Bootstrap da Aula 18 e no projeto final:

```css
:root {
  --vida-primaria:   #0B6E75;   /* verde-azulado escuro, cabeçalho e destaques */
  --vida-secundaria: #2E9E7E;   /* verde médio, bordas e apoios               */
  --vida-destaque:   #E4572E;   /* laranja avermelhado, ações e alertas       */
  --vida-fundo:      #F4F7F6;   /* fundo das páginas                          */
  --vida-texto:      #1F2A30;   /* corpo de texto                             */
  --vida-borda:      #D6E2E0;   /* separadores e contornos suaves             */
}
```

Não reinvente cores por aula: o aluno carrega o mesmo `site.css` de agosto a
dezembro, e paleta trocada no meio do semestre quebra o que ele já escreveu.

### O contrato técnico da aplicação, Aulas 07 a 20

A partir da Aula 07 todas as aulas constroem **a mesma aplicação ASP.NET Core
MVC**. Estes nomes são fixos e valem até a Aula 20. Quem escrever uma aula nova
herda daqui, não inventa:

| O quê | Valor |
|---|---|
| SDK | .NET 10 LTS, `TargetFramework` `net10.0` |
| Projeto e namespace raiz | `ClinicaVida.Web` |
| `DbContext` | `ClinicaContext`, em `Data/ClinicaContext.cs` |
| Banco | `clinicavida`, no MySQL |
| Connection string | chave `"DefaultConnection"` em `appsettings.json` |
| Provedor EF Core | `Pomelo.EntityFrameworkCore.MySql` |
| Repositório em memória (Aulas 09 e 10) | `Models/ClinicaEmMemoria.cs` |
| Migration inicial | `InicialClinicaVida` |

Models, em `Models/`, com estas propriedades exatas:

- `Especialidade`: Id, Nome, Descricao
- `Medico`: Id, Nome, Crm, EspecialidadeId, Especialidade
- `Paciente`: Id, Nome, Cpf, DataNascimento, Telefone, Email
- `Consulta`: Id, PacienteId, MedicoId, Data, Horario, Observacoes

Convenções que valem para o código de todas as aulas:

- **Nomes de action em inglês**, seguindo o scaffold do ASP.NET Core: `Index`,
  `Details`, `Create`, `Edit`, `Delete`, mais `DeleteConfirmed` para o POST de
  exclusão. Isso é deliberado, apesar de a disciplina ser toda em pt-BR: é o que
  o aluno encontra na documentação e em qualquer tutorial quando trava sozinho.
  Textos, comentários e mensagens continuam em português.
- `Consulta.Data` é `DateTime` e `Consulta.Horario` é `TimeSpan`.
- `Cpf` é `string`, mascarado como `000.000.000-00`, conforme a Aula 05.
- **Nunca fixe porta de `localhost` como se fosse universal.** `dotnet new mvc`
  sorteia as portas em `Properties/launchSettings.json`, e a de cada aluno é
  diferente. Escreva "a porta que o seu terminal imprimiu" e use `7145` só como
  exemplo.

### Autenticação e API, a partir da Aula 15

- **Um contexto só.** Na Aula 15 o `ClinicaContext` **passa a herdar de
  `IdentityDbContext<IdentityUser>`**, em vez de nascer um segundo contexto.
  Uma cadeia de migrations, um banco coerente, e o aluno vê a própria classe
  que escreveu na Aula 11 evoluir. A Aula 15 precisa de um slide explicando a
  troca de herança e a migration que ela gera.
- **As telas de login são MVC, escritas à mão.** `ContaController` com `Login`
  em GET e POST, `Logout` e `Registrar` em GET e POST, usando `SignInManager` e
  `UserManager`, com Views em `Views/Conta/`. **Não use o scaffold do
  Identity**, que gera Razor Pages em `Areas/Identity/`: a disciplina inteira
  ensina MVC, e um paradigma novo por uma aula só confunde mais do que economiza
  tempo. O aluno precisa ver o fluxo de autenticação, não recebê-lo pronto.
- **Perfis:** `Recepcao` e `Medico`, conforme o planejamento.
- **A API da Aula 16 é protegida** com `[Authorize]`, herdando a autenticação
  por cookie configurada na Aula 15. Diga em sala a limitação, com honestidade:
  cookie serve ao navegador, e integração real entre sistemas usaria token.
  **JWT não entra**, nem na Aula 16 nem em nenhuma outra: não está na ementa e
  não cabe num encontro que já traz REST, DTO, status HTTP e ferramenta de
  teste.
- **A rota da API é literal:** `[Route("api/consultas")]` em
  `ConsultasApiController`. A convenção `[Route("api/[controller]")]` daria
  `api/consultasapi`, porque o token resolve para o nome da classe sem o
  sufixo `Controller`, e o nome tem o `Api` para não colidir com o
  `ConsultasController` do MVC. A Aula 16 ensina a convenção, explica o
  conflito e usa a rota literal.
- **Com cookie, uma requisição não autenticada à API receberia 302 e a tela de
  login em HTML.** A Aula 16 configura `ConfigureApplicationCookie` para
  devolver **401** em caminhos sob `/api`, senão o 401 da tabela de status
  seria mentira dentro da própria aplicação do aluno.

### Deploy, Aula 19: Docker e GitHub Codespaces

Decisão do professor. A Clínica Vida+ é **containerizada com Docker** e roda no
**GitHub Codespaces**, com a porta encaminhada em modo público, o que dá a URL
acessível pela internet que a Aula 19 e a apresentação da Aula 20 exigem.

Artefatos que o aluno cria na Aula 19, todos na raiz do fork:

| Arquivo | Conteúdo |
|---|---|
| `Dockerfile` | Multi-stage: build em `mcr.microsoft.com/dotnet/sdk:10.0`, runtime em `mcr.microsoft.com/dotnet/aspnet:10.0` |
| `compose.yaml` | Dois serviços, `web` e `db`; o `db` é `mysql:8.4`, com volume nomeado para os dados sobreviverem ao `down` |
| `.dockerignore` | `bin/`, `obj/`, `.git/`, `.env` |
| `.env` | Senhas do MySQL e a connection string. **Vai para o `.gitignore`, nunca para o repositório** |
| `.devcontainer/devcontainer.json` | O que faz o Codespaces subir com .NET 10 e Docker disponíveis |

Convenções que valem no deck e no kit:

- **Configuração por variável de ambiente, com a convenção de duplo
  sublinhado:** `ConnectionStrings__DefaultConnection` sobrescreve o
  `appsettings.json` sem que o aluno precise editar arquivo nenhum. É o
  argumento concreto do quiz desta aula, cuja resposta correta é justamente
  "fora do repositório".
- `ASPNETCORE_ENVIRONMENT=Production` no serviço `web`, para o aluno ver a
  página de erro amigável no lugar da página de exceção detalhada.
- **Dentro do compose, o host do banco é `db`, não `localhost`.** É o nome do
  serviço que vira nome de host na rede do compose, e é o erro número um de
  quem containeriza pela primeira vez.
- As migrations são aplicadas contra o banco do contêiner. O `db` precisa estar
  saudável antes de o `web` tentar conectar: use `healthcheck` no `db` e
  `depends_on` com `condition: service_healthy`.

**Diga a limitação em voz alta, no deck e no kit.** A URL do Codespaces existe
enquanto o codespace está rodando: ele hiberna por inatividade e a URL para de
responder. Isso não é defeito do material, é como o Codespaces funciona, e o
aluno precisa saber para **iniciar o codespace antes da apresentação da Aula
20**. O material deve dizer isso com todas as letras, e o checklist de
publicação da Aula 19 deve incluir "a porta está marcada como pública, e não
privada", que é o esquecimento mais comum e faz a URL responder 401 para quem
não é o dono.

---

## 4. Anatomia do deck Reveal.js

Cada aula tem uma apresentação HTML autocontida em
`aulas-1sem/aulas/aulaXX.html`, publicada por CDN, sem build e sem bundler.

### 4.1 Esqueleto do arquivo

O trecho abaixo é extraído do padrão-ouro, `aulas-1sem/aulas/aula01.html`. Copie
daqui, ou do próprio deck da Aula 01, e não reescreva de memória: cada linha do
`<head>` e do `Reveal.initialize` está aqui por um motivo registrado.

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aula XX, Título da aula | Uninove</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/white.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/highlight/monokai.css">
  <link rel="stylesheet" href="../assets/css/uninove-theme.css">
  <link rel="stylesheet" href="../assets/css/uninove-print.css">
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
</head>
<body>
  <div class="reveal">
    <div class="slides">
      <!-- Capa -->
      <section class="cover-slide">...</section>
      <!-- Título da aula, com a data resolvida por turma -->
      <section class="title-slide">...</section>
      <!-- Agenda com os horários dos quatro ciclos -->
      <section class="content-slide">...</section>
      <!-- Ciclo 1: conceito, demonstração, exercício curto -->
      <section class="content-slide">...</section>
      <!-- Ciclo 2: conceito, demonstração, exercício curto -->
      <section class="content-slide">...</section>
      <!-- Quiz de fixação -->
      <section class="quiz-slide content-slide">...</section>
      <!-- Ciclo 3: laboratório guiado, um slide por passo -->
      <section class="exercise-slide content-slide">...</section>
      <!-- Ciclo 4: laboratório final e entregável -->
      <section class="exercise-slide content-slide">...</section>
      <!-- Fechamento: entregável, commit, push e prévia da próxima aula -->
      <section class="content-slide">...</section>
      <!-- Referências da aula, alvo das citações [N] -->
      <section id="ref-slide" class="content-slide">...</section>
      <!-- Encerramento com copyright -->
      <section class="end-slide">...</section>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/highlight/highlight.js"></script>
  <script src="../assets/js/uninove-quiz.js"></script>
  <script type="module">
    import { TURMAS, resolverTurma, dataDaAula, formatarData } from '../assets/js/turmas.js';
    const turma = resolverTurma({
      hoje: new Date(),
      salva: localStorage.getItem('uninove-turma'),
    });
    const alvo = document.querySelector('[data-data-da-aula]');
    if (alvo) {
      const n = Number(alvo.getAttribute('data-data-da-aula'));
      alvo.textContent = turma
        ? `${TURMAS[turma].rotulo}, ${formatarData(dataDaAula(turma, n))}`
        : `Quarta ${formatarData(dataDaAula('quarta', n))} ou quinta ${formatarData(dataDaAula('quinta', n))}`;
    }
  </script>
  <script>
    Reveal.initialize({
      width: 1280, height: 720, center: false, margin: 0,
      hash: true, slideNumber: false,
      // Os chevrons de navegação caem sobre a footer-bar e sobre o triângulo
      // azul do canto inferior direito; a barra de progresso encosta no rodapé
      // e parece um segundo rodapé. Nenhum dos dois é usado na projeção.
      controls: false, progress: false,
      // Um slide por página no ?print-pdf, para o PDF bater com o deck.
      pdfMaxPagesPerSlide: 1,
      plugins: [RevealHighlight],
    });
  </script>
</body>
</html>
```

Pontos do esqueleto que não são opcionais:

- **O `<link>` do Google Fonts.** O tema usa Montserrat no texto e JetBrains
  Mono no código, mas **não importa nenhuma das duas**: quem importa é o deck.
  Sem essa linha, o deck cai na fonte padrão do sistema e não é o mesmo
  material.
- **O formato do `<title>`:** `Aula XX, Título da aula | Uninove`, com vírgula
  depois do número e sem o nome da disciplina. É o formato do padrão-ouro.
- **As cinco folhas de estilo, nesta ordem:** Reveal, tema `white`, `monokai`
  do plugin de destaque, `uninove-theme.css` e `uninove-print.css`. O tema da
  Uninove precisa vir depois do `white.css` para sobrescrevê-lo.
- **`hash: true`** dá URL própria a cada slide, o que permite linkar um slide
  específico e faz `href="#/ref-slide"` funcionar.
- **`controls: false, progress: false`** e **`slideNumber: false`** existem pelo
  motivo registrado no comentário: os controles do Reveal caem em cima do
  rodapé do tema.
- **`pdfMaxPagesPerSlide: 1`** garante que a exportação com `?print-pdf` gere
  uma página por slide.

O tema fixa cada `section` em **1280x720, com altura travada**. O conteúdo não
rola: o que não couber quebra o slide visualmente, sem lançar nenhum erro no
console. Consequência prática: um conceito por slide. Quando o conteúdo não
couber, divida em dois slides, não encolha a fonte.

### 4.1.1 A data da aula: o único ponto do deck que muda por aula

O slide de título **não traz data escrita**. Ele traz um `<span>` vazio com o
atributo `data-data-da-aula`, e o módulo do fim do arquivo resolve a turma
(quarta ou quinta) e escreve a data correspondente. É assim no padrão-ouro:

```html
<h3>Prof. José Romualdo<br><span data-data-da-aula="1"></span></h3>
```

**O número do atributo é o número da aula.** `data-data-da-aula="1"` na Aula 01,
`"5"` na Aula 05, `"20"` na Aula 20. O módulo passa esse número para
`dataDaAula(turma, n)` em `assets/js/turmas.js`, que devolve a data daquele
encontro na turma resolvida. Quando não dá para resolver a turma, o deck mostra
as duas datas, quarta e quinta.

> **Este é o defeito mais caro que a produção em lote pode cometer.** Um deck
> copiado da Aula 01 sem trocar o número do atributo projeta **05/08/2026 na
> Aula 05**, na frente da turma, e passa em `check_slides.py`,
> `check_canto_coral.py` e `check_portal.py` sem uma única reclamação: nenhum
> dos três olha o conteúdo do arquivo. Quem pega isso é
> `tools/check_decks.py`, que compara o valor do atributo com o número no nome
> do arquivo. Trocar esse número é o **primeiro** passo depois de copiar o
> esqueleto, não o último.

Regras do atributo:

- Existe **exatamente um** `data-data-da-aula` por deck, no slide de título.
- O valor é o número da aula, sem zero à esquerda (`5`, não `05`).
- Nenhuma data é escrita à mão em nenhum lugar do deck. Data escrita à mão vira
  data errada para uma das duas turmas.

### 4.2 Ordem canônica dos slides

Segue exatamente os quatro ciclos do encontro, na ordem em que acontecem em
sala:

```
capa
título com a data resolvida por turma
agenda com os horários dos quatro ciclos
ciclo 1                                                 19h30 às 20h05
ciclo 2                                                 20h05 às 20h40
quiz de fixação                                         20h40 às 20h50
ciclo 3 de laboratório                                  20h50 às 21h25
ciclo 4 de laboratório e entregável                     21h25 às 21h50
fechamento                                              21h50 às 22h00
referências da aula, com id="ref-slide"
encerramento com copyright
```

O **slide de referências é canônico**, não opcional: é o alvo das citações
`[N]` que aparecem nos títulos dos slides de conteúdo, e por isso leva
`id="ref-slide"`. Ele vem entre o fechamento e o encerramento, como no
padrão-ouro.

A **agenda com horários também é canônica de todas as aulas**: todo deck abre
mostrando os quatro ciclos do encontro. O que a Aula 01 tem a mais são os
slides de abertura de semestre (apresentação do professor, metodologia,
avaliação com os pesos e apresentação do case Clínica Vida+). As demais aulas
não repetem esses.

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
`uninove-logo-header`, `uninove-logo-full` (a logo grande da capa e do
encerramento), `title-card` e `lesson-bar` (exclusivos do `title-slide`),
`slide-footer` com `footer-bar` e `footer-page`, `concept-cards` com
`concept-card`, `side-by-side` com `side`, `figure-split`, `slide-figure`,
`timeline` com `tl-item`, `tl-dot`, `tl-year`, `tl-tool`, `tl-desc` e o
modificador `is-past` no `tl-item` já percorrido, `takeaway` com
`takeaway-label`, `callout`, `flow-diagram` com `flow-item` e `flow-arrow`,
`exercise-container` com `exercise-steps` (a lista numerada dos passos de
laboratório), `code-compact` (modificador de `<pre>` para bloco de código curto
que precisa ocupar menos altura), `ref-badge` e `decor-coral`.

O `title-slide` tem markup próprio, que não é o do `content-slide`:

```html
<section class="title-slide">
  <div class="top-bar"></div>
  <img src="../assets/img/uninove-logo.png" alt="Uninove" class="uninove-logo-header">
  <div class="title-card">
    <div class="accent-bar"></div>
    <h1>Desenvolvimento Web</h1>
    <h2>Título da aula</h2>
    <h3>Prof. José Romualdo<br><span data-data-da-aula="XX"></span></h3>
  </div>
  <div class="lesson-bar">AULA XX &nbsp;|&nbsp; Módulo N, Nome do módulo</div>
</section>
```

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
    <div class="footer-bar">XX Tema curto</div>
    <div class="footer-page">3</div>
  </div>
</section>
```

O `footer-bar` é **o número da aula com dois dígitos, um espaço e o tema curto
do slide**, sem hífen e sem travessão: `01 Agenda do encontro`,
`01 Laboratório, passo 2, clone`. O `footer-page` é a posição do slide no deck,
contada a partir de 1, com a capa como 1: por isso o primeiro slide que tem
rodapé, a agenda, já começa em 3. A sequência precisa ser crescente, sem pular
nem repetir, e `tools/check_decks.py` confere isso.

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
- **Alternativa com qualquer elemento inline, como `<code>` ou `<strong>`,
  precisa ter o texto envolvido em `<span class="option-text">`.** A `li` é
  `display: flex` com `gap: 12px`, então cada trecho de texto solto e cada
  elemento inline viram itens de flex separados: a alternativa ganha 12px de
  buraco de cada lado do `<code>`, no lugar onde deveria haver um espaço
  normal, e a frase se parte na projeção. Alternativa de texto puro dispensa o
  `span` e continua valendo como nas Aulas 01, 02 e 04. **Nenhum dos quatro
  validadores pega isso**, porque nada estoura nem se sobrepõe; foi encontrado
  três vezes, por três autores diferentes, olhando a tela. Ver ADR-007.

  ```html
  <li data-correct="false"><span class="option-letter">D</span><span class="option-text">Formata o conteúdo conforme o <code>type</code> declarado.</span></li>
  ```
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
   - **Critérios de aceitação em tabela**, com uma linha por critério e a
     evidência que o professor confere na correção. A tabela é obrigatória: o
     checkpoint vale nota, e uma lista em prosa deixa margem para o aluno e o
     professor lerem coisas diferentes. O kit da Aula 01 é o modelo.
   - Instrução do commit e push esperados no fork do aluno.
2. **`index.html`**, uma página de redirecionamento para o `README.md` exibido
   pelo GitHub. Ver a seção 7.
3. **Código de referência** que resolve o passo da aula, servindo de gabarito
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

---

## 7. O ciclo do artefato: deck, kit, `index.html` do lab e portal

Uma aula só está pronta quando os **quatro** artefatos existem. Deck e kit sem
os dois últimos passos dão 404 no portal publicado, e o aluno não chega ao
material.

### 7.1 `aulas-1sem/labs/aulaXX-lab/index.html`, obrigatório

O GitHub Pages **não faz listagem de diretório**: um diretório sem
`index.html` devolve 404. O botão "Lab" do portal aponta para
`labs/aulaXX-lab/`, então sem esse arquivo o botão quebra em produção, mesmo
com o `README.md` no lugar. O template é o da Aula 01, e só **dois tokens**
mudam, o número da aula nos caminhos e o número no título:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=https://github.com/josercf/uninove-2026-2-desenvolvimento-web/blob/main/aulas-1sem/labs/aulaXX-lab/README.md">
  <title>Laboratório da Aula XX, Desenvolvimento Web, Uninove</title>
  <script>window.location.href = "https://github.com/josercf/uninove-2026-2-desenvolvimento-web/blob/main/aulas-1sem/labs/aulaXX-lab/README.md";</script>
</head>
<body style="font-family: sans-serif; text-align: center; padding-top: 50px; background-color: #00274D; color: #fff;">
  <h2>Redirecionando para o roteiro do laboratório da Aula XX</h2>
  <p>O roteiro completo vive no <code>README.md</code> deste diretório, exibido pelo GitHub. Caso o redirecionamento não ocorra, <a href="https://github.com/josercf/uninove-2026-2-desenvolvimento-web/blob/main/aulas-1sem/labs/aulaXX-lab/README.md" style="color: #C84B31;">clique aqui</a>.</p>
</body>
</html>
```

`tools/check_portal.py` pega a ausência desse arquivo, porque o servidor dele
recusa listagem de diretório de propósito, exatamente como o GitHub Pages.

### 7.2 Habilitar o card da aula em `aulas-1sem/index.html`

O portal já tem os 20 cards escritos. O card de uma aula ainda não produzida
está desabilitado. Ao terminar a aula XX, **edite o card correspondente**:

Antes, aula ainda em produção:

```html
<article class="card" data-aula="2">
  ...
  <div class="card-acoes">
    <a class="btn disabled" aria-disabled="true">Slides</a>
    <a class="btn disabled" aria-disabled="true">Lab</a>
  </div>
  <span class="badge-producao">Em produção</span>
</article>
```

Depois, aula publicada:

```html
<article class="card" data-aula="2">
  ...
  <div class="card-acoes">
    <a class="btn" href="aulas/aula02.html">Slides</a>
    <a class="btn" href="labs/aula02-lab/">Lab</a>
  </div>
</article>
```

Ou seja: tirar `disabled` da classe dos dois botões, tirar o `aria-disabled`,
tirar o `<span class="badge-producao">` e pôr os dois `href`. Sem isso, a aula
fica pronta em disco e invisível para a turma.

---

## 8. Validação: os quatro validadores

Nenhuma aula é considerada pronta sem os quatro passando. Eles conferem coisas
diferentes e nenhum substitui o outro.

```bash
python3 tools/check_slides.py aulas-1sem/aulas/aulaXX.html   # estouro de 1280x720 e sobreposição
python3 tools/check_decks.py aulas-1sem/aulas/aulaXX.html    # estrutura do HTML, estático
python3 tools/check_canto_coral.py aulas-1sem/aulas/aulaXX.html  # triângulo coral, pixel a pixel
python3 tools/check_portal.py                                # portal, cards e links dos botões
npm test                                                     # lógica de resolução de turma
```

- **`check_slides.py`** mede geometria no navegador. Não olha o conteúdo do
  arquivo e não enxerga o `.decor-coral`, que tem caixa zerada.
- **`check_decks.py`** é estático e cobre justamente o que a produção em lote
  quebra: `data-data-da-aula` com o número da aula errado, `decor-coral`
  faltando, `quiz-slide` sem `content-slide`, quiz com zero ou duas respostas
  certas, âncora `#/...` sem `id` correspondente, `footer-page` fora de
  sequência e caminho relativo que não existe no disco.
- **`check_canto_coral.py`** confere pixel a pixel se o triângulo coral chegou
  inteiro à tela. É o único que pega elemento opaco cobrindo a decoração.
  Ele só confere slides que **têm** o `.decor-coral`; quem cobra a presença do
  elemento é o `check_decks.py`.
- **`check_portal.py`** abre o portal, confere os 20 cards, a resolução de
  turma e faz um GET real em cada botão habilitado.

Os três validadores de deck reportam o slide em **base 0**: o primeiro slide do
deck é o slide 0, a mesma base de `Reveal.slide(i)`.
