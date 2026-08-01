# Andamento

**Última atualização:** 31/07/2026 (Task 14, lote do Módulo 3)

## Ordem de leitura ao abrir uma sessão

1. `CLAUDE.md`, na raiz do repositório.
2. O agente construtor da Uninove, `.claude/agents/construtor-aulas-uninove.md`.
3. Este arquivo, `docs/ANDAMENTO.md`.

## Onde está cada coisa

| O quê | Onde |
|---|---|
| Acervo (este repositório) | `/Users/joseromualdocostafilho/Projects/Uninove/2026/uninove-2026-2-desenvolvimento-web`, GitHub `josercf/uninove-2026-2-desenvolvimento-web`, branch `main` |
| Portal publicado | <https://josercf.github.io/uninove-2026-2-desenvolvimento-web/aulas-1sem/index.html>, com a raiz `https://josercf.github.io/uninove-2026-2-desenvolvimento-web/` redirecionando para lá. Publicado com sucesso, com os 20 cards e o seletor de turma |
| Repositório-esqueleto do case | [`josercf/uninove-2026-2-clinica-vida`](https://github.com/josercf/uninove-2026-2-clinica-vida) |
| Acervo da FIAP | `/Users/joseromualdocostafilho/Projects/FIAP/FIAP-2026-2-3SI`, GitHub `josercf/FIAP-2026-2-3SI`. Symlinks deste repositório apontam para lá; ver a seção de compartilhamento do `CLAUDE.md` e o ADR-003 |

## Concluído

**Task 1, esqueleto do repositório e publicação:**

- `.gitignore`, `package.json` (com `"type": "module"` e script `test` rodando
  `node --test tests/`), `index.html` na raiz redirecionando para
  `aulas-1sem/index.html`, `README.md` e `.github/workflows/static.yml`.
- GitHub Pages habilitado e publicando com sucesso a partir da `main`.

**Task 2, symlinks com o acervo da FIAP:**

- No acervo da FIAP, o seletor de exclusão do validador `check_slides.py` passou
  a `[class*="logo-header"]` e o glob do hook em `.claude/settings.json` passou a
  `*/aulas/aula*.html`, tornando os dois arquivos reutilizáveis por outros
  acervos.
- Seis symlinks relativos criados neste repositório: `tools/check_slides.py`,
  `tools/scaffold_labs.py`, `.claude/settings.json`,
  `.claude/agents/construtor-aulas.md`, `.claude/agents/revisor-slides.md` e
  `docs/referencia/SKILL-fiap.md`.
- Confirmado empiricamente que `check_slides.py` detecta a raiz do projeto
  corretamente através do symlink, porque `os.path.abspath` não resolve
  symlink.
- `.claude/settings.local.json` criado localmente, com as permissões de uso
  frequente. Não é versionado, por um gitignore global do usuário.

**Task 3, ADRs e documentação de entrada:**

- Seis ADRs em `docs/adrs/`: migração dos decks para Reveal.js (ADR-001),
  resolução de turma no cliente (ADR-002), compartilhamento com o acervo da
  FIAP (ADR-003), case Clínica Vida+ com encontro de 150 minutos (ADR-004),
  legibilidade do código projetado e integridade das decorações do tema
  (ADR-005) e artefato de publicação sem as ferramentas (ADR-006, Task 11).
- `CLAUDE.md` como ponto de entrada de qualquer sessão futura.

**Task 4, módulo de turmas:**

- `aulas-1sem/assets/js/turmas.js`, resolução de turma (quarta ou quinta) no
  cliente, com precedência de valor salvo sobre dia da semana e cálculo de
  data por aula sem deslocamento de fuso.
- `tests/turmas.test.mjs`, 14 testes cobrindo golden path, edge cases e
  regressão de fuso horário. `npm test` roda com `node --test`.

**Task 5, tema visual:**

- `aulas-1sem/assets/css/uninove-theme.css` e `uninove-print.css`, paleta azul
  e coral, classes de slide e blocos reutilizáveis descritos no `CLAUDE.md`.
- Logo com canal alfa e ligaduras de código desligadas, conforme ADR-005.

**Task 6, planos:**

- `PLANO_DE_ENSINO.md` e `PLANEJAMENTO_AULA_A_AULA.md`, na raiz.

**Task 7, metodologia e agente:**

- `aulas-1sem/SKILL.md` e `.claude/agents/construtor-aulas-uninove.md`,
  override local do agente construtor da FIAP para o case Clínica Vida+.

**Task 8, Aula 01 como padrão-ouro:**

- `aulas-1sem/aulas/aula01.html`, deck completo, validado por
  `tools/check_slides.py` e `tools/check_canto_coral.py`.

**Task 9, laboratório da Aula 01 e repositório-esqueleto:**

- `aulas-1sem/labs/aula01-lab/`, com `index.html` e `README.md`.
- Repositório-esqueleto do case,
  [`josercf/uninove-2026-2-clinica-vida`](https://github.com/josercf/uninove-2026-2-clinica-vida).

**Task 10, portal:**

- `aulas-1sem/index.html`, portal com os 20 cards e seletor de turma.

**Task 11, publicação e fechamento (esta task):**

- `.github/workflows/static.yml` passou a montar `_site` com `rsync`,
  publicando só o material didático (`aulas-1sem/`, planos, ADRs, `README.md`
  e `index.html` da raiz) e excluindo ferramentas, testes, agentes de IA e
  documentação de processo interno. Um passo de `find _site -type l` falha o
  build se sobrar symlink no artefato. Ver ADR-006 para o raciocínio completo:
  a causa raiz do bloqueio anterior era `actions/upload-pages-artifact@v3`
  empacotando com `tar --dereference`, que seguia os seis symlinks
  compartilhados com a FIAP até um alvo inexistente no runner e abortava.
- Publicação confirmada com sucesso, com as seis URLs de aceite (portal, deck
  da Aula 01, lab, tema, `turmas.js`, logo) respondendo 200, e
  `tools/check_portal.py` e `.claude/settings.json` respondendo 404 no site
  publicado, confirmando que as ferramentas não foram ao ar.

**Revisão final do conjunto, 31/07/2026:**

- A metodologia documentada (`aulas-1sem/SKILL.md` e
  `.claude/agents/construtor-aulas-uninove.md`) passou a descrever o deck que
  a Aula 01 realmente é: esqueleto fiel com o `<link>` do Google Fonts e o
  `Reveal.initialize` completo, o mecanismo `data-data-da-aula`, a ordem
  canônica com o slide de referências, o formato do `<title>` e do
  `footer-bar`, e a lista completa de blocos do tema.
- **`data-data-da-aula` está documentado.** É o único ponto do deck que muda
  por aula, e não aparecia em nenhum documento do repositório.
- O ciclo do artefato fechou: `SKILL.md` e agente agora mandam criar
  `labs/aulaXX-lab/index.html` e habilitar o card da aula no portal.
- Novo validador estático `tools/check_decks.py`, com sete checagens (hoje
  oito, ver Task 12), cada uma
  provada por defeito induzido numa cópia do padrão-ouro.
- `.claude/agents/revisor-slides-uninove.md` criado, override do revisor da
  FIAP, que proibia os pesos de avaliação obrigatórios aqui.
- Carga horária corrigida para 60 horas-aula; e-mail do professor confirmado
  em 31/07/2026 e registrado no `PLANO_DE_ENSINO.md`.
- Resíduos de intervalo removidos do tema (`.break-slide` nos dois CSS e o
  comentário do `startTimer`).
- **Decisão sobre critérios de aceitação:** a regra do `SKILL.md` fica, e o kit
  da Aula 01 ganhou a tabela que faltava. O checkpoint vale nota, e uma lista
  em prosa deixa margem para aluno e professor lerem coisas diferentes.

**Task 12, lote do Módulo 1, Aulas 02 a 06 (31/07/2026):**

- Cinco decks e cinco kits produzidos em paralelo, um agente
  `construtor-aulas-uninove` por aula: `aula02.html` (22 slides, TCP/IP e DNS),
  `aula03.html` (32, HTML semântico e o fluxo branch/PR), `aula04.html` (26,
  CSS, box model e Flexbox), `aula05.html` (24, Grid, responsivo e
  formulários) e `aula06.html` (29, JavaScript, DOM e eventos), cada um com
  `labs/aulaXX-lab/README.md` e `index.html`.
- Os cinco cards do portal habilitados em uma edição única, feita fora dos
  agentes: cinco escritas concorrentes no mesmo `index.html` se atropelariam.
  `check_portal.py` confirma os 12 links das seis aulas respondendo 200.
- **Módulo 1 completo.** O front-end da Clínica Vida+ vai da página semântica
  ao formulário com validação em JavaScript.

**Reconciliação entre aulas produzidas em paralelo, 31/07/2026:**

Produzir cinco aulas ao mesmo tempo cobra um preço específico: cada agente
supõe o que as vizinhas vão entregar. O que foi encontrado e corrigido depois:

- **Seletor do filtro de especialidades.** A Aula 04 faz o aluno escrever
  `.lista-especialidades li`, com os cards como `<li>` sem classe; a Aula 06
  filtrava por `.card-especialidade`, que não existiria no arquivo dele. A
  Aula 06 passou a usar o seletor que a Aula 04 de fato produz, no deck e no
  kit. Corrigido na aula dependente, não na que já entregou.
- **IP de exemplo.** A Aula 02 usava `200.160.2.3`, endereço real do
  registro.br. Trocado por `203.0.113.42`, do bloco de documentação da
  RFC 5737, nas quatro ocorrências.
- **Referência não verificada.** A Aula 02 citava Kurose e Ross e afirmava
  estar "na biblioteca digital", o que ninguém conferiu, e o livro não consta
  da bibliografia do `PLANO_DE_ENSINO.md`, que é toda documentação. Trocado
  pelo glossário da MDN. Varredura nas seis aulas não achou outra citação fora
  da lista oficial.
- **Falso alarme registrado para não ser reinvestigado:** a divergência
  aparente de CPF entre a Aula 05 (campo mascarado) e a Aula 06 (11 dígitos)
  **não existe**. A Aula 06 faz `replace(/\D/g, '')` antes de contar.
- **Paleta da Clínica Vida+.** Não existia em documento nenhum, e a Aula 04
  precisou inventá-la. O professor decidiu mantê-la, e ela está registrada na
  seção 3 do `SKILL.md` para as aulas seguintes herdarem.

**Dois defeitos de tema, ADR-007 e a oitava checagem (31/07/2026):**

Três dos cinco construtores, isolados um do outro, relataram o **mesmo par de
defeitos**. Coincidência tripla em agentes independentes é defeito de tema, não
de autoria, e cada aula nova pagaria o mesmo pedágio. Os dois passam nos quatro
validadores e só aparecem na tela.

- **Código cortado silenciosamente.** O `reveal.css` da CDN traz
  `pre code { max-height: 400px; overflow: auto }`. Medido no laboratório da
  Aula 03: bloco de 433px exibido com 410px, 23px de código fora da tela, com
  o validador imprimindo OK, porque quem estoura é o `<code>` e não a caixa do
  `<pre>`. O tema agora zera esse limite, o que troca falha silenciosa por
  falha ruidosa: bloco alto passa a estourar a `section` e o `check_slides.py`
  acusa. Os três contornos inline que a Aula 03 tinha criado foram removidos.
- **Alternativa de quiz partida pelo flex**, descrito nas pendências abaixo.
  Corrigido no tema com `.option-text` e transformado na oitava checagem do
  `check_decks.py`.

Os seis decks, incluindo a Aula 01, foram revalidados depois das mudanças de
tema. `npm test` continua com 14 testes passando.

**Task 13, lote do Módulo 2, Aulas 07 a 12 (31/07/2026):**

- Seis decks e seis kits produzidos em paralelo: `aula07.html` (30 slides,
  ambiente .NET), `aula08.html` (27, MVC e roteamento), `aula09.html` (31, C# e
  LINQ), `aula10.html` (27, Models e validação), `aula11.html` (30, EF Core e
  MySQL) e `aula12.html` (26, CRUD completo). Cards 07 a 12 habilitados na
  edição única de sempre.
- **Doze aulas no ar.** O case sai da página estática e chega à aplicação que
  persiste em MySQL.
- **O contrato técnico foi fixado antes de despachar**, e não depois. Foi a
  lição direta do Módulo 1, e funcionou: os agentes se reconciliaram sozinhos
  em vários pontos (a Aula 09 corrigiu os ids das especialidades para bater com
  a 08; a 10 e a 09 convergiram no caminho de `ClinicaEmMemoria`). O contrato
  está registrado na seção 3 do `SKILL.md` e vale até a Aula 20.
- Decisões do professor neste lote: **.NET 10 LTS** e **Pomelo** como provedor.

**Reconciliação do Módulo 2:**

- **Nomes de action uniformizados em inglês.** O `PLANEJAMENTO_AULA_A_AULA.md`,
  que é a fonte da verdade, misturava `Detalhes` (Aulas 08 e 09) e `Details`
  (Aula 12) para a mesma operação. Não era erro de agente: os dois seguiram
  fielmente o que leram. Por decisão do professor, o planejamento, os decks e
  os kits das Aulas 08 e 09 passaram a `Details`, incluindo a alternativa
  correta do quiz da Aula 08. Atenção ao repetir isso: a substituição em massa
  quebrou uma prosa em português (`ViewData["Title"] = "Detalhes da
  especialidade"`), que foi restaurada. `Detalhes` maiúsculo era action; em
  minúsculo, prosa.
- **Tipo de horário.** A Aula 09 usava `TimeOnly` num exemplo de sobrecarga
  enquanto as Aulas 10 e 11 fixaram `TimeSpan` para `Consulta.Horario`. Se o
  aluno passasse o `Horario` do Model para aquele método, não compilaria.
  Alinhado em `TimeSpan`.
- **Porta de `localhost`.** Três aulas citavam três portas diferentes (5001,
  5145, 7145), e nenhuma é confiável, porque `dotnet new mvc` sorteia as portas
  em `launchSettings.json`. A Aula 08 passou a mandar o aluno usar a porta que o
  próprio terminal imprimiu. Virou regra no `SKILL.md`.
- **Rótulo errado na Aula 07.** O construtor "corrigiu" a pasta `Models/` de
  "Aulas 09 e 10" para "Aula 10", mas a Aula 09 cria `Especialidade` e `Medico`
  em `Models`. Corrigido para "Aulas 09 a 11".
- **Corte horizontal de código.** A correção do ADR-007 zerou o `max-height`,
  que é vertical; o `overflow-x` continua cortando linha longa em silêncio.
  Medi `scrollWidth` contra `clientWidth` em todo `pre code` dos **doze** decks:
  um único caso, de 2px, na connection string da Aula 11, resolvido encurtando
  a senha de exemplo. **Esta medição não é feita por nenhum validador** e vale
  repetir a cada lote.

**Task 14, lote do Módulo 3, Aulas 13 a 17 (31/07/2026):**

- Cinco decks e cinco kits: `aula13.html` (27 slides, cookies e sessões),
  `aula14.html` (26, AJAX), `aula15.html` (29, autenticação e autorização),
  `aula16.html` (28, API REST) e `aula17.html` (27, relacionamentos e EF Core
  avançado). Cards 13 a 17 habilitados na edição única de sempre.
- **Dezessete aulas no ar.** Falta só o Módulo 4.
- Decisões do professor, registradas na seção 3 do `SKILL.md`: o
  `ClinicaContext` **passa a herdar de `IdentityDbContext<IdentityUser>`** na
  Aula 15, em vez de nascer um segundo contexto; as telas de login são MVC
  escritas à mão em `ContaController`, **sem o scaffold em Razor Pages**; e a
  API da Aula 16 é protegida com `[Authorize]` pelo cookie do Identity, sem
  JWT.
- **Instrução nova que funcionou:** cada agente mediu o corte horizontal de
  código no próprio deck, em vez de eu descobrir na reconciliação. Um deles
  chegou a validar o próprio medidor injetando uma linha de 200 caracteres
  para confirmar que ele acusava. Zero cortes chegaram até mim.

**Reconciliação do Módulo 3:**

- **Expediente da clínica.** As Aulas 06, 09 e 10 fixam 07h às 19h, e o aluno
  escreveu essa regra em JavaScript e em C#. A Aula 14 inventou uma grade de
  horários das 08:00 às 17:30. Não era contradição lógica, porque a grade cabe
  dentro do expediente, mas o aluno estranharia. Grade alinhada para 07:00 às
  18:30.
- **Rota da API, e este erro foi meu.** O contrato que passei aos agentes
  mandava `[Route("api/[controller]")]` numa classe `ConsultasApiController`,
  o que resolve para `api/consultasapi` e não para o `api/consultas` usado na
  aula inteira. Copiei do planejamento, que traz as duas coisas e se
  contradiz. O construtor da Aula 16 percebeu, manteve a rota do recurso e
  transformou o conflito em conteúdo de slide. O planejamento ganhou uma nota
  explícita mandando **não** "corrigir" o deck de volta.
- **401 contra 302 na API.** Consequência da decisão do cookie que eu não
  antecipei: sem configuração, uma requisição não autenticada à API receberia
  302 e a tela de login em HTML, e o 401 da tabela de status seria mentira
  dentro da própria aplicação. A Aula 16 configura
  `ConfigureApplicationCookie` para devolver 401 sob `/api`.
- **Perfil no registro**, decisão do professor: a conta criada pela tela de
  registro nasce **sem perfil**. Assim o laboratório exercita os dois lados da
  autorização, e a proteção deixa de ser decorativa no exemplo que a ensina. A
  tabela de teste, no kit e no fechamento do deck, ganhou a coluna "logado,
  sem perfil", que é a linha mais importante da aula.
- Conferidos e **sem conflito**: migrations (`MedicosIniciais`,
  `IdentityClinicaVida`, `RelacionamentosClinicaVida`, distintas e
  sequenciais); só a Aula 13 semeia médicos; numeração de Fase nos kits (12 a
  16); e o acoplamento entre as Aulas 13 e 14, que se reconciliaram sozinhas
  em nomes de action, chave de sessão e `ViewBag`.

**Terceiro defeito de tema, ADR-007 atualizado (31/07/2026):**

`.exercise-container h3` também era `display: flex` com `gap`, a mesma
armadilha da alternativa de quiz, em outro seletor. **Estava vivo em
produção:** a Aula 09, já publicada, trazia `Em <code>ClinicaVida.Web/Models</code>`
com 8px de buraco no lugar do espaço. A oitava checagem não pegava, porque só
olha `li` de `.quiz-options`.

Corrigido no tema, voltando o `h3` a bloco. **A correção aqui foi de natureza
diferente da do quiz, de propósito:** no quiz o flex serve para alinhar o
círculo da letra, então a saída foi dar ao texto um elemento próprio, ao custo
de uma convenção; no título do exercício não havia nada a alinhar, e deu para
remover a armadilha na origem, sem convenção nova e sem checagem nova. Preferir
sempre a correção que não cria regra para alguém lembrar.

## Próximos passos

Produzir o **Módulo 4, Aulas 18 a 20** (layout com Partial Views e Bootstrap,
publicação e deploy, revisão geral e projeto final), fechando as 20 aulas.

Antes de despachar, decidir com o professor o que o planejamento não fixa:
onde a aplicação será publicada na Aula 19 (o planejamento fala em variável de
ambiente e `appsettings.Production.json`, mas não nomeia provedor), e como o
banco MySQL de produção será provido. Sem isso, cinco agentes inventariam cinco
provedores diferentes, que é exatamente o erro que os Módulos 2 e 3 ensinaram a
não cometer.

O que os três lotes ensinaram, e que o próximo deve repetir:

1. **Fixar o contrato técnico antes de despachar.** Está na seção 3 do
   `SKILL.md` e já cobre até a Aula 20.
2. **Manter o portal fora dos agentes**, habilitando os cards numa edição única.
3. **Reconciliar contratos ao fim do lote** é etapa, não detalhe. Inclui
   confrontar números inventados (expediente, grade de horários) contra o que
   aulas anteriores já fixaram.
4. **Medir o corte horizontal de código**, que nenhum validador cobre. Desde a
   Task 14 a instrução vai no prompt de cada agente.

## Pendências conhecidas

- **Cada laboratório precisa do próprio `index.html`**, porque o GitHub Pages
  não faz listagem de diretório. O padrão está em
  `aulas-1sem/labs/aula01-lab/index.html`; laboratórios futuros devem seguir o
  mesmo formato.
- **`tools/check_slides.py` não detecta sobreposição envolvendo
  `.decor-coral`**, porque o elemento tem caixa zerada e quem desenha o
  triângulo é o `::after` (ver ADR-005). Para esse caso específico existe
  `tools/check_canto_coral.py`, que precisa rodar em conjunto com o
  `check_slides.py`, não no lugar dele.
- **Alternativa de quiz com `<code>` precisa de `<span class="option-text">`**
  em volta do texto, senão a `li`, que é `display: flex` com `gap: 12px`,
  parte a frase com 12px de buraco em volta do trecho de código (ADR-007).
  Escapou três vezes, por três autores diferentes, porque nenhum validador
  pegava. **Deixou de ser pendência na Task 12:** virou a oitava checagem do
  `check_decks.py`, provada por defeito induzido em três variantes (`<code>`,
  `<strong>` e `<br>` soltos) mais um controle negativo com o `<code>` dentro
  do `option-text`.
- **15/10/2026 cai numa quinta-feira e é o Dia do Professor.** Se a
  coordenação suspender a aula nessa data, a turma de quinta perde a Aula 11;
  o plano B já registrado no `PLANO_DE_ENSINO.md` é fundir as Aulas 18 e 19.
