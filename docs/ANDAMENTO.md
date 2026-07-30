# Andamento

**Última atualização:** 30/07/2026

## Ordem de leitura ao abrir uma sessão

1. `CLAUDE.md`, na raiz do repositório.
2. O agente construtor da Uninove, `.claude/agents/construtor-aulas-uninove.md`.
   Este arquivo ainda não existe: é entregue pela Task 7 do plano de fundação,
   descrita em `docs/superpowers/plans/2026-07-30-fundacao-do-acervo.md`. Até lá,
   ler o symlink `.claude/agents/construtor-aulas.md`, que aponta para o agente
   construtor da FIAP, sabendo que a versão da Uninove ainda vai sobrescrever
   parte dele.
3. Este arquivo, `docs/ANDAMENTO.md`.

## Onde está cada coisa

| O quê | Onde |
|---|---|
| Acervo (este repositório) | `/Users/joseromualdocostafilho/Projects/Uninove/2026/uninove-2026-2-desenvolvimento-web`, GitHub `josercf/uninove-2026-2-desenvolvimento-web`, branch `main` |
| Portal publicado | <https://josercf.github.io/uninove-2026-2-desenvolvimento-web/>. O workflow do Pages está publicando com sucesso e `index.html` redireciona para `aulas-1sem/index.html`, mas esse arquivo ainda não existe: o portal em si é entregue pela Task 10. Até lá, o redirecionamento aponta para uma página que retorna 404 |
| Repositório-esqueleto do case | `josercf/uninove-2026-2-clinica-vida`. Ainda não criado; é entregue pela Task 9 |
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

**Task 3, ADRs e documentação de entrada (esta task):**

- Quatro ADRs em `docs/adrs/`: migração dos decks para Reveal.js (ADR-001),
  resolução de turma no cliente (ADR-002), compartilhamento com o acervo da
  FIAP (ADR-003) e case Clínica Vida+ com encontro de 150 minutos (ADR-004).
- `CLAUDE.md` como ponto de entrada de qualquer sessão futura.
- Este arquivo.

## Próximos passos

Ainda faltam as Tasks 4 a 11 do plano de fundação
(`docs/superpowers/plans/2026-07-30-fundacao-do-acervo.md`), nesta ordem:
módulo `turmas.js` com testes (4), tema visual da Uninove (5), plano de ensino
e planejamento aula a aula (6), `SKILL.md` e o agente
`construtor-aulas-uninove.md` (7), deck da Aula 01 como padrão-ouro (8),
laboratório da Aula 01 e o repositório-esqueleto `uninove-2026-2-clinica-vida`
(9), portal com os 20 cards (10) e publicação final (11).

Só depois da Aula 01 aprovada, com o padrão visual e pedagógico travado, é que
se escreve o plano das Aulas 02 a 20. Produzir os 19 decks restantes contra um
padrão ainda não validado seria retrabalho garantido; por isso esse plano fica
deliberadamente fora do plano de fundação, para ser escrito depois.
