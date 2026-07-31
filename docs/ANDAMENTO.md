# Andamento

**Última atualização:** 31/07/2026

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
- Novo validador estático `tools/check_decks.py`, com sete checagens, cada uma
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

## Próximos passos

A fundação do acervo está concluída (Tasks 1 a 11). O próximo passo é escrever
o plano das Aulas 02 a 20, usando a Aula 01 como padrão-ouro (deck, lab e
portal já validados) e o agente `construtor-aulas-uninove.md` para produção.
A recomendação é produzir os 19 decks restantes em quatro lotes por módulo do
`PLANO_DE_ENSINO.md`, com revisão entre um lote e o seguinte, em vez de
produzir tudo de uma vez: cada lote incorpora o que for aprendido na revisão
do lote anterior, e um defeito sistêmico (como os do ADR-005) é pego cedo, sem
se multiplicar pelas 20 aulas.

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
- **15/10/2026 cai numa quinta-feira e é o Dia do Professor.** Se a
  coordenação suspender a aula nessa data, a turma de quinta perde a Aula 11;
  o plano B já registrado no `PLANO_DE_ENSINO.md` é fundir as Aulas 18 e 19.
