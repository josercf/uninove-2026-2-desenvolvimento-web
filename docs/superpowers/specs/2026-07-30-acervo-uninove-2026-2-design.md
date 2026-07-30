# Design: acervo didático Uninove 2026.2, Desenvolvimento Web

**Data:** 30/07/2026
**Autor:** Prof. José Romualdo, com Claude Code
**Status:** aprovado pelo professor em 30/07/2026
**Repositório:** <https://github.com/josercf/uninove-2026-2-desenvolvimento-web>

---

## 1. Problema

A disciplina Desenvolvimento Web da Uninove será ministrada em 2026.2 para duas turmas,
uma às quartas-feiras e outra às quintas-feiras, com conteúdo idêntico. Existe material
de 2026.1 em <https://github.com/josercf/uninove-2026-1-desenvolvimento-web>, com 20 decks
de slides e um plano de aulas em Markdown, mas sem laboratórios, sem validação de layout,
sem plano de ensino formal e sobre um motor de slides próprio que não conversa com a
automação já construída para a FIAP.

O acervo da FIAP, em `josercf/FIAP-2026-2-3SI`, resolve exatamente esses pontos: decks
Reveal.js validados, kits de laboratório com código funcional, planejamento aula a aula,
agentes de construção e revisão e um hook que valida o layout a cada edição.

O objetivo é montar o acervo de 2026.2 com o conteúdo da Uninove e o formato da FIAP.

## 2. Escopo

Entra no escopo:

- Estrutura completa do repositório novo, publicada no GitHub Pages
- 20 decks Reveal.js com identidade visual da Uninove
- 20 kits de laboratório ancorados em um case integrador
- Repositório-esqueleto do projeto do semestre, para fork pelos alunos
- Plano de ensino e planejamento aula a aula, com as datas das duas turmas
- Resolução automática da turma no navegador, por dia da semana
- Compartilhamento de agentes, hooks e ferramentas com o acervo da FIAP, via symlink
- Testes automatizados do que é testável em um site estático

Fica fora do escopo:

- Configuração das turmas no Google Classroom, que depende dos identificadores
  ainda não divulgados pela instituição
- Correção de atividades e lançamento de notas
- Migração retroativa do repositório de 2026.1

## 3. Decisões

| Tema | Decisão |
|---|---|
| Conteúdo base | Grade de 20 aulas de 2026.1, de HTML/CSS/JS a ASP.NET Core MVC com EF Core e MySQL |
| Formato | Idêntico ao acervo da FIAP: Reveal.js em 1280x720, portal com cards, um lab por aula |
| Identidade visual | Azul `#00274D`, coral `#C84B31` e `uninove-logo.png`, vindos do repositório de 2026.1 |
| Turmas | Conteúdo único; o calendário é resolvido em tempo de execução pelo navegador |
| Encontro | 19h30 às 22h, 150 minutos, sem intervalo, teoria e prática intercaladas em proporção de 50/50 |
| Metodologia | Sem sala de aula invertida. Conteúdo, explicação e exercício em ciclos dentro da aula |
| Case integrador | Clínica Vida+, sistema de agendamento de consultas, evoluindo aula a aula |
| Calendário | 20 encontros por turma, de agosto a dezembro de 2026 |
| Avaliação | Mesma composição de 2026.1, detalhada na seção 9 |
| Entregas | Google Classroom, quando as turmas estiverem configuradas |

### 3.1 Por que sem sala de aula invertida

O plano de 2026.1 previa atividade pré-aula obrigatória. Na prática, a adesão do público da
Uninove à leitura prévia é baixa, e a aula perdia tempo recuperando base que deveria ter
chegado pronta. O encontro passa a ser autossuficiente: cada ciclo de aproximadamente 35
minutos apresenta um conceito, demonstra e coloca o aluno para praticar imediatamente.

### 3.2 Por que Reveal.js em vez do motor próprio de 2026.1

O motor de 2026.1 (`slides.css` e `slides.js`) funciona, mas nada da automação existente
opera sobre ele: o validador de layout, a exportação para PDF via `?print-pdf` e os agentes
de construção e revisão assumem Reveal.js com slides de 1280x720. Migrar custa reescrever
20 decks e devolve todo esse ferramental de uma vez. A identidade visual de 2026.1 é
preservada, portada para um tema Reveal próprio.

## 4. Arquitetura do repositório

```
uninove-2026-2-desenvolvimento-web/
├── CLAUDE.md                        instruções do acervo para o Claude Code
├── PLANO_DE_ENSINO.md               ementa, case, cronograma das duas turmas, avaliação
├── PLANEJAMENTO_AULA_A_AULA.md      roteiro minuto a minuto das 20 aulas
├── index.html                       redireciona para o portal
├── package.json                     apenas para `npm test`, sem dependências
├── .gitignore                       artefatos de build .NET dos labs, node_modules
├── .github/workflows/static.yml     publicação no GitHub Pages
├── .claude/
│   ├── settings.json                symlink para o acervo da FIAP
│   ├── settings.local.json           ajustes exclusivos deste repositório
│   └── agents/
│       ├── construtor-aulas.md      symlink para o acervo da FIAP
│       ├── revisor-slides.md        symlink para o acervo da FIAP
│       └── construtor-aulas-uninove.md   override local
├── tools/
│   ├── check_slides.py              symlink para o acervo da FIAP
│   ├── scaffold_labs.py             symlink para o acervo da FIAP
│   └── check_portal.py              validação do portal e dos links dos cards
├── tests/
│   └── turmas.test.mjs              executado por `node --test`
├── docs/
│   ├── ANDAMENTO.md                 estado do trabalho entre sessões
│   ├── adrs/                        ADR-001 a ADR-004
│   ├── referencia/SKILL-fiap.md     symlink para `aulas-1sem/SKILL.md` da FIAP
│   └── superpowers/specs/           este documento
└── aulas-1sem/
    ├── index.html                   portal, cards com a data da turma ativa
    ├── SKILL.md                     metodologia da Uninove, arquivo local
    ├── aulas/aula01.html … aula20.html
    ├── labs/aula01-lab/ … aula20-lab/
    └── assets/
        ├── css/uninove-theme.css, uninove-print.css
        ├── js/uninove-quiz.js, turmas.js
        └── img/uninove-logo.png e figuras das aulas
```

### 4.1 Sobre o nome `aulas-1sem/`

O diretório mantém o mesmo nome do acervo da FIAP, ainda que a disciplina da Uninove ocupe
um semestre só. O motivo é prático: os agentes compartilhados por symlink citam esse caminho
literalmente nos prompts, e o glob do hook também. Divergir o nome obrigaria a manter uma
cópia local dos agentes, que é justamente o que o symlink existe para evitar.

## 5. Compartilhamento com o acervo da FIAP

Os symlinks são criados arquivo a arquivo, e não por diretório, para que arquivos locais
convivam com os espelhados no mesmo diretório:

| Caminho neste repositório | Alvo em `../../FIAP/FIAP-2026-2-3SI/` |
|---|---|
| `.claude/settings.json` | `.claude/settings.json` |
| `.claude/agents/construtor-aulas.md` | `.claude/agents/construtor-aulas.md` |
| `.claude/agents/revisor-slides.md` | `.claude/agents/revisor-slides.md` |
| `tools/check_slides.py` | `tools/check_slides.py` |
| `tools/scaffold_labs.py` | `tools/scaffold_labs.py` |
| `docs/referencia/SKILL-fiap.md` | `aulas-1sem/SKILL.md` |

Os symlinks são relativos, para continuarem válidos se a árvore `Projects/` for movida
inteira. Como o workflow do Pages publica o repositório todo e `actions/checkout` não
resolve symlinks para fora do repositório, os arquivos espelhados ficam sob `.claude/`,
`tools/` e `docs/`, que não são servidos como página. O `.gitignore` não os exclui: eles
são versionados como symlink, o que é o comportamento nativo do Git.

### 5.1 Ajustes necessários no acervo da FIAP

Dois ajustes pequenos, que também melhoram o acervo da FIAP:

1. O glob do hook em `.claude/settings.json` passa de `*aulas-1sem/aulas/aula*.html` para
   `*/aulas/aula*.html`. Continua pegando os decks da FIAP e passa a pegar os daqui.
2. Confirmar que `tools/check_slides.py` não carrega caminho absoluto embutido. Se carregar,
   parametrizar pela raiz do projeto antes de criar o symlink.

### 5.2 Override local

`construtor-aulas.md` é da FIAP e continuará evoluindo lá, com o case LogiTech, a paleta rosa,
o encontro de 3,5 horas com intervalo e a stack poliglota. `construtor-aulas-uninove.md`
é local e sobrescreve o que muda aqui:

- Case Clínica Vida+ no lugar de LogiTech
- Paleta azul e coral no lugar do rosa
- Encontro de 150 minutos sem intervalo, em quatro ciclos
- Stack ASP.NET Core MVC, C#, EF Core, MySQL e Bootstrap
- Ausência de atividade pré-aula
- Pesos de avaliação podem aparecer nos slides, ao contrário da convenção da FIAP

## 6. Calendário dinâmico por turma

### 6.1 Datas

20 encontros por turma:

- **Quartas-feiras:** 05/08, 12/08, 19/08, 26/08, 02/09, 09/09, 16/09, 23/09, 30/09, 07/10,
  14/10, 21/10, 28/10, 04/11, 11/11, 18/11, 25/11, 02/12, 09/12, 16/12
- **Quintas-feiras:** 06/08, 13/08, 20/08, 27/08, 03/09, 10/09, 17/09, 24/09, 01/10, 08/10,
  15/10, 22/10, 29/10, 05/11, 12/11, 19/11, 26/11, 03/12, 10/12, 17/12

Nenhum feriado nacional de 2026 cai em quarta ou quinta dentro do período. O único ponto a
confirmar com a coordenação é 15/10, Dia do Professor, que cai numa quinta e pode ter as
aulas suspensas. Se for suspenso, restam 19 datas para a turma de quinta, terminando em
17/12. O plano B é fundir as Aulas 18 e 19 em um encontro só, porque Layout com Bootstrap e
Deploy são as duas mais compactas da grade, preservando a Aula 20 como fechamento e
apresentação do projeto.

### 6.2 Resolução da turma

`aulas-1sem/assets/js/turmas.js`, sem dependências, exporta os dados e uma função pura:

```js
export const TURMAS = {
  quarta: { rotulo: 'Quarta-feira', identificador: null, datas: ['2026-08-05', ...] },
  quinta: { rotulo: 'Quinta-feira', identificador: null, datas: ['2026-08-06', ...] },
};

export function resolverTurma({ hoje, salva }) { ... }
```

Ordem de resolução:

1. Se `salva` for `'quarta'` ou `'quinta'`, vence. Qualquer outro valor é ignorado.
2. Senão, o dia da semana de `hoje`: 3 resolve para quarta, 4 resolve para quinta.
3. Senão, retorna `null`, e cabe à camada de interface perguntar.

`resolverTurma` não toca em `localStorage` nem em `Date` por conta própria: recebe os dois
valores por parâmetro. É o que a torna testável sem navegador e sem mock de relógio.

A camada de interface, no portal, lê `localStorage.getItem('uninove-turma')` e
`new Date()`, chama `resolverTurma`, e se o resultado for `null` abre um modal com as duas
opções. A escolha é gravada em `localStorage`. Um seletor no cabeçalho do portal permite
trocar a qualquer momento, e a troca re-renderiza as datas dos cards sem recarregar a página.

O campo `identificador` fica `null` até a instituição divulgar os códigos das turmas.
Preencher esses dois valores é a única mudança necessária quando isso acontecer.

Os decks carregam o mesmo módulo e preenchem a data no slide de capa. Um deck aberto sem
turma resolvida mostra as duas datas, em vez de abrir modal, para não atrapalhar a projeção
em sala.

## 7. Grade das 20 aulas e a espiral do case

O case Clínica Vida+ é um sistema de agendamento de consultas. Ele começa como página
estática e termina como aplicação ASP.NET Core MVC com banco, autenticação, API e deploy.
Cada aula faz o case avançar um passo.

| # | Tema | O que o case ganha |
|---|---|---|
| 01 | Apresentação, panorama da web, Git e GitHub | Ambiente montado, fork do esqueleto, primeiro commit |
| 02 | Estrutura da web e redes TCP/IP | Análise das requisições da clínica no DevTools |
| 03 | Introdução ao HTML | Home semântica, primeira branch e primeiro Pull Request |
| 04 | Introdução ao CSS | Identidade visual da clínica |
| 05 | CSS avançado e formulários HTML | Página de agendamento, layout responsivo |
| 06 | Introdução ao JavaScript | Validação do agendamento no cliente |
| 07 | Ambiente de desenvolvimento .NET | Aplicação de console, tipos e sintaxe de C# |
| 08 | Primeiros passos com ASP.NET Core MVC | Projeto `ClinicaVida.Web`, primeiro Controller e View |
| 09 | Estruturas de controle e coleções em C# | Listagem de especialidades e médicos no Razor |
| 10 | Formulários e Models no MVC | Agendamento posta para o Controller, Data Annotations |
| 11 | Entity Framework Core e MySQL | `DbContext`, string de conexão, migration inicial |
| 12 | CRUD completo com EF Core | CRUD de médicos |
| 13 | Cookies e sessões | Sessão do paciente e consultas em andamento |
| 14 | Requisições HTTP assíncronas com AJAX | Busca de horários livres sem recarregar a página |
| 15 | Autenticação e autorização | Identity, papéis de paciente e de recepção |
| 16 | API REST com ASP.NET Core | Consultas expostas em JSON, Swagger |
| 17 | Relacionamentos e EF Core avançado | Médico e Especialidade, Paciente e Consulta, `Include` |
| 18 | Layout, Partial Views e Bootstrap | `_Layout`, partials, componentização visual |
| 19 | Publicação e deploy | Publish, Docker, configuração por ambiente |
| 20 | Revisão geral e projeto final | Apresentação da Clínica Vida+ completa |

### 7.1 Git e GitHub nas aulas iniciais

O material de versionamento vem do deck da Aula 01 da FIAP, adaptado ao tema. De lá são
aproveitados os slides de versionamento e trabalho colaborativo, evolução do Git, ecossistema
GitHub, o multiverso do Git (branches) e a anatomia de um commit, incluindo os diagramas SVG.

Distribuição:

- **Aula 01:** por que versionar, o que é um commit, o que é uma branch, o que é o GitHub.
  No laboratório, fork do repositório-esqueleto, clone, primeiro commit e push.
- **Aula 03:** branch por funcionalidade e Pull Request na prática, no momento em que existe
  código de verdade para versionar (a home da clínica).

Fica de fora o que é específico da FIAP e não cabe aqui: Git Worktrees para agentes de IA,
GitFlow completo e o rigor de Conventional Commits, que vira recomendação e não exigência.

## 8. Anatomia de um deck

Cada `aulaXX.html` é autocontido, carrega Reveal.js 5.1.0 do jsDelivr,
`../assets/css/uninove-theme.css`, `../assets/css/uninove-print.css` e as fontes do Google
Fonts. Reveal é inicializado inline com `width: 1280, height: 720, center: false, margin: 0`.
O tema fixa `section` em 1280x720 absoluto: o conteúdo não rola, e o que não couber quebra
o slide. Daí a existência do validador.

Ordem canônica, em quatro ciclos de aproximadamente 35 minutos:

```
capa
título
agenda com horários
ciclo 1: conceito, demonstração, exercício curto        19h30 às 20h05
ciclo 2: conceito, demonstração, exercício curto        20h05 às 20h40
quiz de fixação                                         20h40 às 20h50
ciclo 3: laboratório guiado, parte 1                    20h50 às 21h25
ciclo 4: laboratório, parte 2, e entregável             21h25 às 21h50
fechamento, commit e prévia da próxima aula             21h50 às 22h00
encerramento com copyright
```

A partir da Aula 02, o primeiro slide depois da agenda é a recapitulação da aula anterior,
como já previa o `melhorias_plano.md` de 2026.1.

Classes de slide, espelhando o tema da FIAP com nomes próprios: `cover-slide`, `title-slide`,
`content-slide`, `section-slide`, `quiz-slide`, `exercise-slide`, `end-slide`. Blocos
reutilizáveis: `concept-cards`, `side-by-side`, `slide-title-area` com `accent-bar`,
`top-bar`, `slide-footer` e `uninove-logo-header`.

Quizzes seguem o markup da FIAP: `.quiz-container` com `<ul class="quiz-options">`, opção
correta marcada com `data-correct="true"` e feedbacks em `data-correct-msg` e
`data-incorrect-msg`. O comportamento vive em `uninove-quiz.js`.

## 9. Avaliação

Reaproveitada de 2026.1 sem alteração.

**AV1:** checkpoints feitos em aula valem 40%, prova objetiva vale 60%.
**AV2:** avaliação institucional, com questões de todas as disciplinas do semestre.
**Média:** `(AV1 + AV2) / 2`. **Aprovação:** média maior ou igual a 6,0.

Critérios do projeto final, apresentados na Aula 20: funcionalidade 30%, código 25%, banco de
dados 20%, interface 15% e apresentação 10%. Entrega por repositório no GitHub mais deploy
funcional.

Ao contrário da convenção da FIAP, aqui os pesos aparecem nos slides, porque assim era em
2026.1 e o professor quer manter.

## 10. Laboratórios

Cada aula tem um kit em `aulas-1sem/labs/aulaXX-lab/`, com `README.md` contendo a missão
dentro do case, os pré-requisitos, o passo a passo, o entregável e o commit esperado, mais
código funcional e completo, sem trecho pela metade.

Diferença deliberada em relação à FIAP: lá são 13 repositórios independentes que o aluno
forka, um por aula, porque cada lab é autocontido. Aqui o case é um projeto contínuo, então
existe **um único repositório-esqueleto**, `josercf/uninove-2026-2-clinica-vida`, que o aluno
forka na Aula 01 e evolui semana a semana. Os diretórios em `labs/` são a referência do
professor e o gabarito de cada etapa.

O repositório-esqueleto entrega, na Aula 01, apenas o mínimo: `README.md` com a descrição do
case, `.gitignore` para .NET e uma pasta `docs/` com o enunciado. Ele cresce junto com a turma.

## 11. Testes e validação

| O que | Como | Cobre |
|---|---|---|
| `resolverTurma` | `node --test tests/turmas.test.mjs` | Quarta, quinta, outro dia, valor salvo válido, valor salvo inválido, precedência do valor salvo sobre o dia |
| Layout dos decks | `python3 tools/check_slides.py` | Qualquer elemento que ultrapasse a área útil de 1280x720. Dispara pelo hook a cada edição de deck |
| Portal | `python3 tools/check_portal.py` | Turma resolvida em três datas simuladas (quarta, quinta, domingo), presença dos 20 cards, e nenhum link quebrado |

`node --test` é nativo do Node desde a versão 18, então não há dependência a instalar. O
`package.json` na raiz existe só para expor `npm test`; não há bundler nem framework.

## 12. ADRs a registrar

1. **ADR-001** Migração dos decks para Reveal.js com tema Uninove
2. **ADR-002** Resolução de turma no cliente por dia da semana, com fallback por modal
3. **ADR-003** Compartilhamento de agentes, hooks e ferramentas com a FIAP via symlink e override local
4. **ADR-004** Case integrador Clínica Vida+ e encontro de 150 minutos sem intervalo

## 13. Ordem de execução

1. Esqueleto do repositório, symlinks, workflow do Pages, `CLAUDE.md`, os quatro ADRs
2. `PLANO_DE_ENSINO.md` e `PLANEJAMENTO_AULA_A_AULA.md`, com as duas colunas de datas
3. Tema visual (`uninove-theme.css`, `uninove-print.css`, logo) e `turmas.js` com seus testes
4. Aula 01 como padrão-ouro, deck mais lab, validada em 1280x720
5. Repositório-esqueleto `uninove-2026-2-clinica-vida`
6. Portal `index.html` com os 20 cards e o seletor de turma
7. Aulas 02 a 20, por módulo, deck mais lab, com o revisor rodando depois de cada uma

## 14. Riscos

| Risco | Mitigação |
|---|---|
| Symlink para fora do repositório quebra em outra máquina ou no CI | Os arquivos espelhados ficam fora do que o Pages serve, e o workflow não os executa. Em máquina nova, basta clonar os dois repositórios lado a lado |
| Evolução do `construtor-aulas.md` da FIAP conflita com o contexto da Uninove | O override local existe justamente para isso, e é o arquivo que o agente lê por último |
| 15/10, Dia do Professor, pode suspender a aula da turma de quinta | Confirmar com a coordenação. O plano B, de 19 encontros na quinta, está descrito na seção 6.1 |
| 20 decks reescritos mais 20 labs é volume alto | Execução por módulo, com a Aula 01 consolidando o padrão antes de escalar |
| Identificadores das turmas ainda desconhecidos | Modelados como campo `identificador: null`; preencher os dois valores é a única mudança |

## 15. Convenções editoriais

Herdadas do acervo da FIAP, com uma exceção explícita:

- Sem emojis em slides, títulos ou textos. O tom é profissional
- Português do Brasil com acentuação completa. Nunca usar travessão em dash
- **Exceção à convenção da FIAP:** pesos de avaliação aparecem nos slides, conforme 2026.1
- Preferir diagramas e imagens didáticas a paredes de texto
- Referências numeradas ao longo dos slides e consolidadas em um slide final
- Todo deck termina com o slide de copyright do Prof. José Romualdo
- Commits em Conventional Commits, com escopo pela aula: `feat(aula01): ...`, `fix(portal): ...`
