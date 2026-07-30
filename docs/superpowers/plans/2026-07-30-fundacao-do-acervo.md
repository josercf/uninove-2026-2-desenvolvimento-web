# Fundação do acervo Uninove 2026.2, plano de implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deixar o repositório `uninove-2026-2-desenvolvimento-web` publicado no GitHub Pages com toda a infraestrutura pronta e a Aula 01 completa como padrão-ouro, para que as Aulas 02 a 20 possam ser produzidas em série.

**Architecture:** Site estático, sem build e sem bundler. Decks Reveal.js 5.1.0 carregados por CDN, tema próprio em CSS puro, um módulo ES sem dependências para resolver a turma no cliente. Agentes, hooks e ferramentas Python são compartilhados com o acervo da FIAP por symlink relativo; o que é específico da Uninove vive em arquivos locais.

**Tech Stack:** HTML5, CSS3, JavaScript ES modules, Reveal.js 5.1.0, Node.js `node --test` (nativo), Python 3 com Playwright, GitHub Actions, GitHub Pages.

## Escopo deste plano

Cobre os passos 1 a 6 da seção 13 da spec: esqueleto, symlinks, ADRs, planos de ensino, tema, `turmas.js`, Aula 01 (deck e lab), repositório-esqueleto do case e portal.

**Fora deste plano:** as Aulas 02 a 20. Elas viram um segundo plano, escrito depois que a Aula 01 estiver aprovada e o padrão visual e pedagógico estiver travado. Produzir 19 decks contra um padrão ainda não validado seria retrabalho garantido.

## Global Constraints

- Diretório de trabalho: `/Users/joseromualdocostafilho/Projects/Uninove/2026/uninove-2026-2-desenvolvimento-web`
- Acervo da FIAP, alvo dos symlinks: `/Users/joseromualdocostafilho/Projects/FIAP/FIAP-2026-2-3SI`
- Push exige a chave do josercf. O remote já foi clonado por `git@github.com-josercf:`, então `git push` normal funciona. Se falhar, usar `GIT_SSH_COMMAND='ssh -i ~/.ssh/id_ed25519_josercf -o IdentitiesOnly=yes' git push`
- Texto em português do Brasil com acentuação completa
- **Nunca usar travessão em dash (—) em nenhum arquivo.** Usar vírgula, dois pontos ou parênteses
- Sem emojis em slides, títulos ou textos
- Paleta oficial: azul `#00274D`, coral `#C84B31`, branco `#FFFFFF`, cinza de texto `#333333`
- Slides medem exatamente 1280x720. Conteúdo que vaza quebra o slide, não rola
- Commits em Conventional Commits, escopo pela aula ou pelo componente: `feat(aula01): ...`, `chore(infra): ...`
- Toda mensagem de commit termina com `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`
- Os 20 encontros por turma, em ISO:
  - quarta: `2026-08-05, 2026-08-12, 2026-08-19, 2026-08-26, 2026-09-02, 2026-09-09, 2026-09-16, 2026-09-23, 2026-09-30, 2026-10-07, 2026-10-14, 2026-10-21, 2026-10-28, 2026-11-04, 2026-11-11, 2026-11-18, 2026-11-25, 2026-12-02, 2026-12-09, 2026-12-16`
  - quinta: `2026-08-06, 2026-08-13, 2026-08-20, 2026-08-27, 2026-09-03, 2026-09-10, 2026-09-17, 2026-09-24, 2026-10-01, 2026-10-08, 2026-10-15, 2026-10-22, 2026-10-29, 2026-11-05, 2026-11-12, 2026-11-19, 2026-11-26, 2026-12-03, 2026-12-10, 2026-12-17`

---

## Estrutura de arquivos

| Arquivo | Responsabilidade | Task |
|---|---|---|
| `.gitignore` | Ignorar artefatos .NET dos labs e `node_modules` | 1 |
| `package.json` | Expor `npm test`. Sem dependências | 1 |
| `index.html` | Redirecionar a raiz para o portal | 1 |
| `README.md` | Apresentação pública do acervo | 1 |
| `.github/workflows/static.yml` | Publicar o repositório no Pages | 1 |
| `.claude/settings.json` | Symlink. Hook do validador | 2 |
| `.claude/agents/construtor-aulas.md` | Symlink. Construtor da FIAP | 2 |
| `.claude/agents/revisor-slides.md` | Symlink. Revisor da FIAP | 2 |
| `tools/check_slides.py` | Symlink. Validador de layout | 2 |
| `tools/scaffold_labs.py` | Symlink. Scaffolder de labs | 2 |
| `docs/referencia/SKILL-fiap.md` | Symlink. Metodologia da FIAP, para consulta | 2 |
| `.claude/agents/construtor-aulas-uninove.md` | Override local do construtor | 7 |
| `aulas-1sem/SKILL.md` | Metodologia da Uninove | 7 |
| `docs/adrs/ADR-00{1..4}-*.md` | Decisões arquiteturais | 3 |
| `CLAUDE.md` | Instruções do acervo | 3 |
| `docs/ANDAMENTO.md` | Estado do trabalho entre sessões | 3 |
| `aulas-1sem/assets/js/turmas.js` | Dados das turmas e `resolverTurma` | 4 |
| `tests/turmas.test.mjs` | Testes de `resolverTurma` e `formatarData` | 4 |
| `aulas-1sem/assets/css/uninove-theme.css` | Tema Reveal da Uninove | 5 |
| `aulas-1sem/assets/css/uninove-print.css` | Estilos de exportação em PDF | 5 |
| `aulas-1sem/assets/js/uninove-quiz.js` | Quizzes interativos | 5 |
| `aulas-1sem/assets/img/uninove-logo.png` | Logo institucional | 5 |
| `PLANO_DE_ENSINO.md` | Ementa, case, cronograma, avaliação | 6 |
| `PLANEJAMENTO_AULA_A_AULA.md` | Roteiro minuto a minuto | 6 |
| `aulas-1sem/aulas/aula01.html` | Deck da Aula 01 | 8 |
| `aulas-1sem/labs/aula01-lab/README.md` | Kit de laboratório da Aula 01 | 9 |
| `aulas-1sem/index.html` | Portal com os 20 cards e seletor de turma | 10 |
| `tools/check_portal.py` | Validação do portal | 10 |

---

## Task 1: Esqueleto do repositório e publicação

**Files:**
- Create: `.gitignore`, `package.json`, `index.html`, `README.md`, `.github/workflows/static.yml`

**Interfaces:**
- Consumes: nada
- Produces: `npm test` executando `node --test tests/`, que a Task 4 vai usar. Diretório servido pelo Pages a partir da raiz do repositório.

- [ ] **Step 1: Criar `.gitignore`**

```gitignore
# Sistema
.DS_Store
Thumbs.db

# Node
node_modules/

# .NET, gerado pelos labs
bin/
obj/
*.user
appsettings.Development.json

# Python
__pycache__/
*.pyc
.venv/

# Saída de validação
shots/
```

- [ ] **Step 2: Criar `package.json`**

Sem dependências. `node --test` é nativo do Node 18 em diante.

```json
{
  "name": "uninove-2026-2-desenvolvimento-web",
  "version": "1.0.0",
  "private": true,
  "description": "Acervo didatico da disciplina Desenvolvimento Web, Uninove 2026.2",
  "type": "module",
  "scripts": {
    "test": "node --test tests/"
  },
  "engines": {
    "node": ">=18"
  }
}
```

- [ ] **Step 3: Verificar que o runner de testes existe**

Run: `node --version && npm test`
Expected: versão 18 ou maior, e o `npm test` termina sem erro reclamando que não há arquivo de teste (ainda não existe `tests/`). Se acusar erro de "no test files found", está correto neste momento.

- [ ] **Step 4: Criar `index.html` na raiz**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=aulas-1sem/index.html">
  <title>Desenvolvimento Web | Uninove 2026.2</title>
  <script>window.location.href = "aulas-1sem/index.html";</script>
</head>
<body style="font-family: sans-serif; text-align: center; padding-top: 50px; background-color: #00274D; color: #fff;">
  <h2>Redirecionando para o portal da disciplina</h2>
  <p>Caso o redirecionamento não ocorra, <a href="aulas-1sem/index.html" style="color: #C84B31;">clique aqui</a>.</p>
</body>
</html>
```

- [ ] **Step 5: Criar `README.md`**

```markdown
# Desenvolvimento Web, Uninove 2026.2

Acervo didático da disciplina **Desenvolvimento Web** da Uninove, segundo semestre de 2026.

Portal: <https://josercf.github.io/uninove-2026-2-desenvolvimento-web/>

## Turmas

Duas turmas com conteúdo idêntico, uma às quartas-feiras e outra às quintas-feiras.
O portal detecta o dia da semana e mostra o calendário da turma correspondente; em
qualquer outro dia, pergunta qual turma exibir.

## Case integrador

Todas as aulas e laboratórios constroem a **Clínica Vida+**, um sistema de agendamento
de consultas que começa como página estática e termina como aplicação ASP.NET Core MVC
com Entity Framework Core, MySQL, autenticação, API REST e deploy.

## Estrutura

```
PLANO_DE_ENSINO.md            ementa, cronograma das duas turmas e avaliação
PLANEJAMENTO_AULA_A_AULA.md   roteiro minuto a minuto das 20 aulas
aulas-1sem/
  index.html                  portal
  aulas/aulaXX.html           decks Reveal.js
  labs/aulaXX-lab/            kits de laboratório
  assets/                     tema, scripts e imagens
tools/                        validadores
docs/adrs/                    decisões arquiteturais
```

## Preview local

Os decks usam caminhos relativos, então é obrigatório servir por HTTP.

```bash
python3 -m http.server 8000
# http://localhost:8000/
```

## Validação

```bash
npm test                                    # lógica de turmas
python3 tools/check_slides.py               # layout de todos os decks
python3 tools/check_portal.py               # portal e links
```

## Professor

José Romualdo, <jose.romualdo@uni9.pro.br>
```

- [ ] **Step 6: Criar `.github/workflows/static.yml`**

```yaml
name: Deploy static content to Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Pages
        uses: actions/configure-pages@v5
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v5
```

- [ ] **Step 7: Verificar que nenhum arquivo tem travessão em dash**

Run: `grep -rn '—' --include='*.md' --include='*.html' --include='*.yml' --include='*.json' . | grep -v node_modules`
Expected: nenhuma linha de saída.

- [ ] **Step 8: Commit e primeiro push**

```bash
git add -A
git commit -m "chore(infra): esqueleto do repositorio e publicacao no Pages

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
git branch -M main
git push -u origin main
```

- [ ] **Step 9: Habilitar o Pages**

Run: `gh api -X POST repos/josercf/uninove-2026-2-desenvolvimento-web/pages -f build_type=workflow`
Expected: JSON de resposta com `"status": null` ou `"built"`. Se retornar 409, o Pages já está habilitado, o que também está correto.

Run: `gh run list --repo josercf/uninove-2026-2-desenvolvimento-web --limit 1`
Expected: um workflow `Deploy static content to Pages` com conclusão `success`.

---

## Task 2: Ajustar o acervo da FIAP e criar os symlinks

O validador da FIAP ignora o cabeçalho com logo pelo seletor `.fiap-logo-header`, que não vai existir aqui. Dois ajustes pequenos no acervo da FIAP tornam os dois arquivos compartilháveis.

**Files:**
- Modify: `../../FIAP/FIAP-2026-2-3SI/tools/check_slides.py` (linha do `el.closest`)
- Modify: `../../FIAP/FIAP-2026-2-3SI/.claude/settings.json` (glob do matcher)
- Create: `.claude/settings.json`, `.claude/agents/construtor-aulas.md`, `.claude/agents/revisor-slides.md`, `tools/check_slides.py`, `tools/scaffold_labs.py`, `docs/referencia/SKILL-fiap.md` (todos como symlink relativo)

**Interfaces:**
- Consumes: nada
- Produces: `python3 tools/check_slides.py [deck]` funcionando neste repositório, e o hook `PostToolUse` disparando ao editar `aulas-1sem/aulas/aula*.html`.

- [ ] **Step 1: Generalizar o seletor de exclusão no validador da FIAP**

Em `/Users/joseromualdocostafilho/Projects/FIAP/FIAP-2026-2-3SI/tools/check_slides.py`, dentro de `JS_MEDIR`, trocar:

```javascript
      if (el.closest('.slide-footer, .top-bar, .fiap-logo-header')) continue;
```

por:

```javascript
      if (el.closest('.slide-footer, .top-bar, [class*="logo-header"]')) continue;
```

`[class*="logo-header"]` casa com `.fiap-logo-header` e com `.uninove-logo-header`.

- [ ] **Step 2: Generalizar o glob do hook da FIAP**

Em `/Users/joseromualdocostafilho/Projects/FIAP/FIAP-2026-2-3SI/.claude/settings.json`, dentro do comando do hook, trocar o padrão do `case`:

```
case "$f" in *aulas-1sem/aulas/aula*.html) ;; *) exit 0 ;; esac;
```

por:

```
case "$f" in */aulas/aula*.html) ;; *) exit 0 ;; esac;
```

- [ ] **Step 3: Verificar que o validador da FIAP continua passando**

Run: `cd /Users/joseromualdocostafilho/Projects/FIAP/FIAP-2026-2-3SI && python3 tools/check_slides.py aulas-1sem/aulas/aula01.html`
Expected: `OK: nenhum conteudo estourando 1280x720`. Se acusar estouro, os ajustes quebraram algo; reverter e investigar antes de seguir.

- [ ] **Step 4: Commitar os ajustes no acervo da FIAP**

```bash
cd /Users/joseromualdocostafilho/Projects/FIAP/FIAP-2026-2-3SI
git add tools/check_slides.py .claude/settings.json
git commit -m "chore(tools): tornar validador e hook reutilizaveis por outros acervos

O seletor de exclusao passa a casar qualquer *-logo-header e o glob do hook
qualquer */aulas/aula*.html, para que o acervo da Uninove 2026.2 possa
compartilhar os dois arquivos por symlink.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
git push
```

- [ ] **Step 5: Criar os symlinks relativos**

Os caminhos são relativos para sobreviverem a uma mudança da árvore `Projects/` inteira.

O alvo de um symlink relativo é resolvido a partir do **diretório que contém o link**, não da
raiz do repositório. Como a raiz está em `Projects/Uninove/2026/uninove-2026-2-desenvolvimento-web`,
são quatro níveis de `..` para chegar em `Projects/` a partir de um subdiretório de primeiro
nível, e cinco a partir de um de segundo nível.

| Link | Diretório do link | Níveis até `Projects/` |
|---|---|---|
| `tools/check_slides.py` | `<raiz>/tools/` | 4 |
| `tools/scaffold_labs.py` | `<raiz>/tools/` | 4 |
| `.claude/settings.json` | `<raiz>/.claude/` | 4 |
| `.claude/agents/construtor-aulas.md` | `<raiz>/.claude/agents/` | 5 |
| `.claude/agents/revisor-slides.md` | `<raiz>/.claude/agents/` | 5 |
| `docs/referencia/SKILL-fiap.md` | `<raiz>/docs/referencia/` | 5 |

```bash
cd /Users/joseromualdocostafilho/Projects/Uninove/2026/uninove-2026-2-desenvolvimento-web
mkdir -p .claude/agents tools docs/referencia

ln -sfn ../../../../FIAP/FIAP-2026-2-3SI/tools/check_slides.py  tools/check_slides.py
ln -sfn ../../../../FIAP/FIAP-2026-2-3SI/tools/scaffold_labs.py tools/scaffold_labs.py
ln -sfn ../../../../FIAP/FIAP-2026-2-3SI/.claude/settings.json  .claude/settings.json
ln -sfn ../../../../../FIAP/FIAP-2026-2-3SI/.claude/agents/construtor-aulas.md .claude/agents/construtor-aulas.md
ln -sfn ../../../../../FIAP/FIAP-2026-2-3SI/.claude/agents/revisor-slides.md   .claude/agents/revisor-slides.md
ln -sfn ../../../../../FIAP/FIAP-2026-2-3SI/aulas-1sem/SKILL.md docs/referencia/SKILL-fiap.md
```

- [ ] **Step 6: Verificar que todo symlink resolve**

Run:
```bash
for f in tools/check_slides.py tools/scaffold_labs.py .claude/settings.json \
         .claude/agents/construtor-aulas.md .claude/agents/revisor-slides.md \
         docs/referencia/SKILL-fiap.md; do
  test -e "$f" && echo "OK   $f" || echo "QUEBRADO $f"
done
```
Expected: seis linhas começando com `OK`. Qualquer `QUEBRADO` significa contagem errada de `../`; contar de novo a partir do diretório que contém o link, não da raiz do repositório.

- [ ] **Step 7: Verificar que o validador roda a partir daqui**

Cria um deck mínimo temporário só para provar que a raiz é detectada corretamente, já que `os.path.abspath` não resolve symlink e portanto `RAIZ` aponta para este repositório.

Run:
```bash
mkdir -p aulas-1sem/aulas
printf '%s\n' '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><title>t</title>' \
  '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css"></head>' \
  '<body><div class="reveal"><div class="slides"><section><h2>Teste</h2></section></div></div>' \
  '<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>' \
  '<script>Reveal.initialize({width:1280,height:720,center:false,margin:0});</script></body></html>' \
  > aulas-1sem/aulas/aula00-temp.html
python3 tools/check_slides.py aulas-1sem/aulas/aula00-temp.html
rm aulas-1sem/aulas/aula00-temp.html
```
Expected: `aula00-temp.html  (1 slides)` seguido de `OK: nenhum conteudo estourando 1280x720`. Se der `FileNotFoundError` ou 404, a raiz foi detectada errada; nesse caso, parametrizar `RAIZ` no arquivo da FIAP por `CLAUDE_PROJECT_DIR` com fallback para o comportamento atual.

- [ ] **Step 8: Criar `.claude/settings.local.json`**

Arquivo local, para ajustes que não devem voltar para a FIAP. Começa vazio de hooks e só declara permissões usadas com frequência aqui.

```json
{
  "permissions": {
    "allow": [
      "Bash(npm test)",
      "Bash(python3 tools/check_slides.py:*)",
      "Bash(python3 tools/check_portal.py:*)",
      "Bash(python3 -m http.server:*)"
    ]
  }
}
```

- [ ] **Step 9: Commit**

```bash
git add -A
git commit -m "chore(infra): compartilhar agentes, hooks e ferramentas da FIAP via symlink

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 3: ADRs, CLAUDE.md e ANDAMENTO.md

**Files:**
- Create: `docs/adrs/ADR-001-migracao-dos-decks-para-revealjs.md`, `docs/adrs/ADR-002-resolucao-de-turma-no-cliente.md`, `docs/adrs/ADR-003-compartilhamento-com-o-acervo-da-fiap.md`, `docs/adrs/ADR-004-case-clinica-vida-e-encontro-de-150-minutos.md`, `CLAUDE.md`, `docs/ANDAMENTO.md`

**Interfaces:**
- Consumes: os symlinks da Task 2, citados no `CLAUDE.md`
- Produces: `CLAUDE.md` como ponto de entrada de qualquer sessão futura

- [ ] **Step 1: Criar os quatro ADRs**

Cada arquivo segue a estrutura mínima definida nas diretivas globais: Data, Status, Decisores, Contexto, Decisão, Motivações, Riscos conhecidos com mitigações, Consequências positivas e negativas, ADRs relacionadas. Todos com **Data:** 30/07/2026, **Status:** Aceita, **Decisores:** Prof. José Romualdo.

`ADR-001-migracao-dos-decks-para-revealjs.md`:
- **Contexto:** o acervo de 2026.1 usa motor próprio (`slides.css`, `slides.js`); nenhuma automação existente opera sobre ele.
- **Decisão:** reescrever os 20 decks em Reveal.js 5.1.0 a 1280x720, com tema Uninove próprio derivado do tema da FIAP.
- **Motivações:** habilita `check_slides.py`, o hook de validação, a exportação `?print-pdf` e os agentes construtor e revisor.
- **Riscos:** custo de reescrever 20 decks. Mitigação: Aula 01 primeiro como padrão-ouro, e o restante em série contra um padrão travado.
- **Consequências negativas:** o conteúdo de 2026.1 precisa ser transposto slide a slide, não copiado.
- **Relacionadas:** ADR-003.

`ADR-002-resolucao-de-turma-no-cliente.md`:
- **Contexto:** duas turmas, conteúdo idêntico, calendários diferentes, identificadores institucionais ainda desconhecidos.
- **Decisão:** um único conjunto de materiais; a turma é resolvida em tempo de execução por `resolverTurma({hoje, salva})`, com precedência para a escolha salva, depois o dia da semana, e modal como último recurso.
- **Motivações:** zero duplicação de conteúdo, e o professor abre o portal em sala sem escolher nada.
- **Riscos:** aluno que abre num sábado precisa escolher. Mitigação: a escolha fica em `localStorage` e há seletor no cabeçalho.
- **Consequências negativas:** a data deixa de ser conteúdo estático do HTML, o que exige JavaScript habilitado.
- **Relacionadas:** ADR-004.

`ADR-003-compartilhamento-com-o-acervo-da-fiap.md`:
- **Contexto:** os agentes, o hook e os validadores da FIAP servem aqui, mas parte do conteúdo é específico daquela disciplina.
- **Decisão:** symlink relativo arquivo a arquivo para o que é genérico, mais `construtor-aulas-uninove.md` local sobrescrevendo o que muda.
- **Motivações:** melhorias feitas na FIAP refletem aqui sem cópia manual.
- **Riscos:** symlink para fora do repositório quebra em máquina que não tenha os dois clones lado a lado. Mitigação: os arquivos espelhados ficam fora do que o Pages serve, e o workflow não os executa.
- **Consequências negativas:** um clone isolado deste repositório fica sem os validadores até que o acervo da FIAP também seja clonado.
- **Relacionadas:** ADR-001.

`ADR-004-case-clinica-vida-e-encontro-de-150-minutos.md`:
- **Contexto:** aulas de 19h30 às 22h, 150 minutos, sem intervalo; a sala de aula invertida de 2026.1 não teve adesão.
- **Decisão:** case integrador Clínica Vida+ evoluindo aula a aula, e encontro em quatro ciclos de aproximadamente 35 minutos, alternando conceito, demonstração e prática, sem atividade pré-aula.
- **Motivações:** o encontro fica autossuficiente e o entregável de cada aula acumula rumo ao projeto final.
- **Riscos:** sem intervalo formal, 150 minutos corridos cansam. Mitigação: a troca de ciclo funciona como respiro, e o quiz das 20h40 quebra o ritmo.
- **Consequências negativas:** o professor perde a folga de 30 minutos que a FIAP tem para atender aluno individualmente.
- **Relacionadas:** ADR-002.

- [ ] **Step 2: Criar `CLAUDE.md`**

Deve conter, nesta ordem: aviso para ler `docs/ANDAMENTO.md` primeiro; o que é o repositório (acervo didático, site estático, sem build); bloco de comandos com preview local por `python3 -m http.server 8000`, exportação em PDF por `?print-pdf`, `npm test`, `python3 tools/check_slides.py` e `python3 tools/check_portal.py`; as três camadas de conteúdo (planejamento na raiz, metodologia em `aulas-1sem/SKILL.md`, materiais em `aulas-1sem/`); o case Clínica Vida+; a anatomia do deck com a ordem canônica de slides e as classes do tema; a seção de compartilhamento com a FIAP explicando os symlinks e o override; as armadilhas conhecidas; e as convenções editoriais da seção 15 da spec, incluindo a exceção sobre pesos de avaliação.

Armadilhas conhecidas a registrar:
- Slide que estoura 720px não é detectável por `scrollHeight`, porque a `section` tem altura fixa. Usar `tools/check_slides.py`.
- `tools/check_slides.py` e `.claude/settings.json` são symlinks para o acervo da FIAP. Editá-los altera o acervo da FIAP também.
- `new Date('2026-08-05')` é interpretado como UTC e vira 04/08 no fuso de São Paulo. Datas em `turmas.js` são montadas componente a componente, nunca pelo construtor de string ISO.
- O workflow publica o repositório inteiro. Qualquer arquivo commitado fica público.

- [ ] **Step 3: Criar `docs/ANDAMENTO.md`**

Com: data da última atualização (30/07/2026); ordem de leitura ao abrir sessão (`CLAUDE.md`, o agente construtor da Uninove, este arquivo); tabela "onde está cada coisa" com acervo, portal publicado, repositório-esqueleto do case e acervo da FIAP; seção "Concluído" listando o que as tasks anteriores entregaram; e seção "Próximos passos" apontando para o plano das Aulas 02 a 20.

- [ ] **Step 4: Verificar ausência de travessão em dash**

Run: `grep -rn '—' CLAUDE.md docs/`
Expected: nenhuma linha de saída.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "docs(adr): registrar as quatro decisoes arquiteturais do acervo

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 4: Módulo de turmas com testes

Esta é a única lógica de verdade do repositório, então é a única que ganha TDD completo.

**Files:**
- Create: `aulas-1sem/assets/js/turmas.js`
- Test: `tests/turmas.test.mjs`

**Interfaces:**
- Consumes: `npm test` da Task 1
- Produces:
  - `export const TURMAS` com chaves `quarta` e `quinta`, cada uma `{ rotulo: string, identificador: string|null, datas: string[] }`
  - `export function resolverTurma({ hoje, salva })` retornando `'quarta' | 'quinta' | null`
  - `export function dataDaAula(turma, numeroDaAula)` retornando `Date`, com `numeroDaAula` de 1 a 20
  - `export function formatarData(data)` retornando `'DD/MM/AAAA'`
  - As Tasks 8 e 10 importam esses quatro símbolos.

- [ ] **Step 1: Escrever os testes que falham**

Criar `tests/turmas.test.mjs`:

```javascript
import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  TURMAS,
  resolverTurma,
  dataDaAula,
  formatarData,
} from '../aulas-1sem/assets/js/turmas.js';

test('cada turma tem 20 encontros', () => {
  assert.equal(TURMAS.quarta.datas.length, 20);
  assert.equal(TURMAS.quinta.datas.length, 20);
});

test('as datas de quarta caem todas numa quarta-feira', () => {
  for (const iso of TURMAS.quarta.datas) {
    const [a, m, d] = iso.split('-').map(Number);
    assert.equal(new Date(a, m - 1, d).getDay(), 3, `${iso} nao e quarta`);
  }
});

test('as datas de quinta caem todas numa quinta-feira', () => {
  for (const iso of TURMAS.quinta.datas) {
    const [a, m, d] = iso.split('-').map(Number);
    assert.equal(new Date(a, m - 1, d).getDay(), 4, `${iso} nao e quinta`);
  }
});

test('quarta-feira resolve para a turma de quarta', () => {
  assert.equal(resolverTurma({ hoje: new Date(2026, 7, 5), salva: null }), 'quarta');
});

test('quinta-feira resolve para a turma de quinta', () => {
  assert.equal(resolverTurma({ hoje: new Date(2026, 7, 6), salva: null }), 'quinta');
});

test('outro dia da semana nao resolve turma nenhuma', () => {
  assert.equal(resolverTurma({ hoje: new Date(2026, 7, 8), salva: null }), null);
});

test('a turma salva tem precedencia sobre o dia da semana', () => {
  assert.equal(resolverTurma({ hoje: new Date(2026, 7, 5), salva: 'quinta' }), 'quinta');
});

test('valor salvo invalido e ignorado e cai no dia da semana', () => {
  assert.equal(resolverTurma({ hoje: new Date(2026, 7, 6), salva: 'sexta' }), 'quinta');
});

test('valor salvo invalido num dia sem aula devolve null', () => {
  assert.equal(resolverTurma({ hoje: new Date(2026, 7, 8), salva: 'sexta' }), null);
});

test('dataDaAula devolve a data local correta, sem deslocamento de fuso', () => {
  const d = dataDaAula('quarta', 1);
  assert.equal(d.getDate(), 5);
  assert.equal(d.getMonth(), 7);
  assert.equal(d.getFullYear(), 2026);
});

test('dataDaAula cobre da aula 1 a aula 20', () => {
  assert.equal(formatarData(dataDaAula('quarta', 20)), '16/12/2026');
  assert.equal(formatarData(dataDaAula('quinta', 20)), '17/12/2026');
});

test('dataDaAula rejeita numero fora da faixa', () => {
  assert.throws(() => dataDaAula('quarta', 0), /fora da faixa/);
  assert.throws(() => dataDaAula('quarta', 21), /fora da faixa/);
});

test('dataDaAula rejeita turma desconhecida', () => {
  assert.throws(() => dataDaAula('sexta', 1), /turma desconhecida/);
});

test('formatarData usa o padrao brasileiro com dois digitos', () => {
  assert.equal(formatarData(new Date(2026, 7, 5)), '05/08/2026');
  assert.equal(formatarData(new Date(2026, 11, 16)), '16/12/2026');
});
```

- [ ] **Step 2: Rodar os testes para confirmar que falham**

Run: `npm test`
Expected: FAIL, com erro de módulo não encontrado apontando para `aulas-1sem/assets/js/turmas.js`.

- [ ] **Step 3: Implementar `turmas.js`**

Criar `aulas-1sem/assets/js/turmas.js`. Preencher os dois arrays `datas` com as listas ISO da seção Global Constraints, na ordem.

```javascript
/**
 * Turmas de Desenvolvimento Web, Uninove 2026.2.
 *
 * O conteudo das duas turmas e identico; o que muda e o calendario. Este modulo
 * concentra as datas e a regra de qual turma exibir.
 *
 * Datas sao sempre montadas componente a componente. `new Date('2026-08-05')`
 * seria interpretado como meia-noite UTC e viraria 04/08 no fuso de Sao Paulo.
 */

export const TURMAS = {
  quarta: {
    rotulo: 'Quarta-feira',
    identificador: null, // preencher quando a instituicao divulgar
    datas: [
      '2026-08-05', '2026-08-12', '2026-08-19', '2026-08-26', '2026-09-02',
      '2026-09-09', '2026-09-16', '2026-09-23', '2026-09-30', '2026-10-07',
      '2026-10-14', '2026-10-21', '2026-10-28', '2026-11-04', '2026-11-11',
      '2026-11-18', '2026-11-25', '2026-12-02', '2026-12-09', '2026-12-16',
    ],
  },
  quinta: {
    rotulo: 'Quinta-feira',
    identificador: null,
    datas: [
      '2026-08-06', '2026-08-13', '2026-08-20', '2026-08-27', '2026-09-03',
      '2026-09-10', '2026-09-17', '2026-09-24', '2026-10-01', '2026-10-08',
      '2026-10-15', '2026-10-22', '2026-10-29', '2026-11-05', '2026-11-12',
      '2026-11-19', '2026-11-26', '2026-12-03', '2026-12-10', '2026-12-17',
    ],
  },
};

const DIA_DA_SEMANA = { 3: 'quarta', 4: 'quinta' };

/**
 * Decide qual turma exibir.
 *
 * @param {{ hoje: Date, salva: string|null }} entrada
 * @returns {'quarta'|'quinta'|null} null quando nao ha como decidir sozinho
 */
export function resolverTurma({ hoje, salva }) {
  if (salva === 'quarta' || salva === 'quinta') return salva;
  return DIA_DA_SEMANA[hoje.getDay()] || null;
}

/**
 * Data do enesimo encontro de uma turma.
 *
 * @param {'quarta'|'quinta'} turma
 * @param {number} numeroDaAula de 1 a 20
 * @returns {Date} data local, sem deslocamento de fuso
 */
export function dataDaAula(turma, numeroDaAula) {
  const dados = TURMAS[turma];
  if (!dados) throw new Error(`turma desconhecida: ${turma}`);
  if (!Number.isInteger(numeroDaAula) || numeroDaAula < 1 || numeroDaAula > dados.datas.length) {
    throw new Error(`numero de aula fora da faixa: ${numeroDaAula}`);
  }
  const [ano, mes, dia] = dados.datas[numeroDaAula - 1].split('-').map(Number);
  return new Date(ano, mes - 1, dia);
}

/**
 * @param {Date} data
 * @returns {string} no formato DD/MM/AAAA
 */
export function formatarData(data) {
  const dd = String(data.getDate()).padStart(2, '0');
  const mm = String(data.getMonth() + 1).padStart(2, '0');
  return `${dd}/${mm}/${data.getFullYear()}`;
}
```

- [ ] **Step 4: Rodar os testes para confirmar que passam**

Run: `npm test`
Expected: PASS nos 14 testes. `# fail 0`.

Se os testes de dia da semana falharem, a lista de datas foi transcrita errada; conferir contra a seção Global Constraints, e não corrigir o teste.

- [ ] **Step 5: Commit**

```bash
git add aulas-1sem/assets/js/turmas.js tests/turmas.test.mjs
git commit -m "feat(turmas): resolucao de turma por dia da semana com calendario das duas turmas

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 5: Tema visual da Uninove

O tema nasce do tema da FIAP, que é o que o validador e os agentes esperam, com a paleta trocada e as decorações de 2026.1 incorporadas.

**Files:**
- Create: `aulas-1sem/assets/css/uninove-theme.css`, `aulas-1sem/assets/css/uninove-print.css`, `aulas-1sem/assets/js/uninove-quiz.js`, `aulas-1sem/assets/img/uninove-logo.png`

**Interfaces:**
- Consumes: nada
- Produces: as classes que a Task 8 vai usar no deck: `cover-slide`, `title-slide`, `content-slide`, `section-slide`, `quiz-slide`, `exercise-slide`, `end-slide`, mais `concept-cards`, `concept-card`, `side-by-side`, `slide-title-area`, `accent-bar`, `top-bar`, `slide-footer` com `footer-bar` e `footer-page`, `uninove-logo-header` e `uninove-logo-full`. Variáveis CSS `--uninove-azul`, `--uninove-coral`, `--uninove-branco`, `--uninove-cinza`, `--uninove-cinza-claro`, `--uninove-code-bg`, `--uninove-fonte`.

- [ ] **Step 1: Copiar o logo do acervo de 2026.1**

```bash
curl -fsSL -o aulas-1sem/assets/img/uninove-logo.png \
  https://raw.githubusercontent.com/josercf/uninove-2026-1-desenvolvimento-web/main/aulas/img/uninove-logo.png
file aulas-1sem/assets/img/uninove-logo.png
```
Expected: `PNG image data, 195 x 195`.

- [ ] **Step 2: Derivar o tema a partir do tema da FIAP**

```bash
FIAP=/Users/joseromualdocostafilho/Projects/FIAP/FIAP-2026-2-3SI/aulas-1sem/assets
sed -e 's/--fiap-pink/--uninove-coral/g' \
    -e 's/--fiap-dark/--uninove-azul/g' \
    -e 's/--fiap-black/--uninove-preto/g' \
    -e 's/--fiap-white/--uninove-branco/g' \
    -e 's/--fiap-light-gray/--uninove-cinza-claro/g' \
    -e 's/--fiap-gray/--uninove-cinza/g' \
    -e 's/--fiap-code-bg/--uninove-code-bg/g' \
    -e 's/--fiap-font/--uninove-fonte/g' \
    -e 's/fiap-logo-header/uninove-logo-header/g' \
    -e 's/fiap-logo-full/uninove-logo-full/g' \
    "$FIAP/css/fiap-theme.css" > aulas-1sem/assets/css/uninove-theme.css
sed -e 's/fiap-/uninove-/g' "$FIAP/css/fiap-print.css" > aulas-1sem/assets/css/uninove-print.css
cp "$FIAP/js/fiap-quiz.js" aulas-1sem/assets/js/uninove-quiz.js
grep -c fiap aulas-1sem/assets/css/uninove-theme.css aulas-1sem/assets/css/uninove-print.css aulas-1sem/assets/js/uninove-quiz.js
```
Expected: `0` para os três arquivos. `fiap-quiz.js` já é neutro de marca, por isso vai como cópia direta.

- [ ] **Step 3: Trocar o bloco de variáveis pela paleta da Uninove**

Substituir o `:root` no topo de `uninove-theme.css` por:

```css
/* ============================================
   Tema Uninove para Reveal.js
   Paleta e decoracoes herdadas do acervo 2026.1
   ============================================ */

:root {
  --uninove-azul: #00274D;
  --uninove-coral: #C84B31;
  --uninove-preto: #12121A;
  --uninove-branco: #FFFFFF;
  --uninove-cinza: #333333;
  --uninove-cinza-claro: #F5F5F5;
  --uninove-code-bg: #1E1E1E;
  --uninove-fonte: 'Montserrat', 'Segoe UI', Arial, sans-serif;
}
```

Também trocar o comentário de cabeçalho do arquivo, que ainda diz "FIAP Theme".

- [ ] **Step 4: Incorporar as decorações de 2026.1**

Acrescentar ao final de `uninove-theme.css`. São os dois triângulos azuis e o coral do canto, que caracterizam o template institucional.

```css
/* --- Decoracoes do template institucional --- */

.reveal .slides section.content-slide::before,
.reveal .slides section.section-slide::before,
.reveal .slides section.quiz-slide::before,
.reveal .slides section.exercise-slide::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 90px 90px 0 0;
  border-color: var(--uninove-azul) transparent transparent transparent;
  z-index: 0;
  pointer-events: none;
}

.reveal .slides section.content-slide::after,
.reveal .slides section.section-slide::after,
.reveal .slides section.quiz-slide::after,
.reveal .slides section.exercise-slide::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 0 0 60px 60px;
  border-color: transparent transparent var(--uninove-azul) transparent;
  z-index: 0;
  pointer-events: none;
}

.reveal .slides section .decor-coral {
  position: absolute;
  top: 0;
  right: 0;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 0 80px 80px 0;
  border-color: transparent var(--uninove-coral) transparent transparent;
  opacity: 0.75;
  z-index: 0;
  pointer-events: none;
}

/* O conteudo precisa ficar acima das decoracoes */
.reveal .slides section > * {
  position: relative;
  z-index: 1;
}
```

- [ ] **Step 5: Validar o tema com um deck de prova**

Cria um deck temporário que exercita as classes principais e roda o validador.

Run:
```bash
cat > aulas-1sem/aulas/aula00-temp.html <<'HTML'
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Prova de tema | Uninove</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/white.css">
  <link rel="stylesheet" href="../assets/css/uninove-theme.css">
  <link rel="stylesheet" href="../assets/css/uninove-print.css">
</head>
<body>
  <div class="reveal"><div class="slides">
    <section class="cover-slide">
      <img class="uninove-logo-full" src="../assets/img/uninove-logo.png" alt="Uninove">
    </section>
    <section class="content-slide">
      <div class="decor-coral"></div>
      <div class="top-bar"></div>
      <div class="slide-title-area"><div class="accent-bar"></div><h2>Prova de tema</h2></div>
      <div class="concept-cards">
        <div class="concept-card"><h4>Um</h4><p>Texto de prova.</p></div>
        <div class="concept-card"><h4>Dois</h4><p>Texto de prova.</p></div>
      </div>
      <div class="slide-footer"><div class="footer-bar">00 Prova</div><div class="footer-page">1</div></div>
    </section>
  </div></div>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
  <script src="../assets/js/uninove-quiz.js"></script>
  <script>Reveal.initialize({width:1280,height:720,center:false,margin:0,hash:true});</script>
</body>
</html>
HTML
python3 tools/check_slides.py aulas-1sem/aulas/aula00-temp.html
```
Expected: `OK: nenhum conteudo estourando 1280x720`.

- [ ] **Step 6: Conferir visualmente e remover o deck de prova**

Run: `python3 -m http.server 8000` e abrir `http://localhost:8000/aulas-1sem/aulas/aula00-temp.html`.
Expected: capa com o logo centralizado sobre fundo escuro; segundo slide com triângulo azul no canto superior esquerdo, coral no superior direito, azul no inferior direito, barra de destaque coral ao lado do título e rodapé legível. Nenhum triângulo por cima do texto.

Depois: `rm aulas-1sem/aulas/aula00-temp.html`

- [ ] **Step 7: Commit**

```bash
git add aulas-1sem/assets
git commit -m "feat(tema): tema Reveal da Uninove com paleta azul e coral

Derivado do tema da FIAP, que e o formato que o validador e os agentes
esperam, com a paleta institucional e as decoracoes do acervo 2026.1.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 6: Plano de ensino e planejamento aula a aula

Estes dois arquivos são a fonte da verdade de datas, títulos e escopo. Slides e portal seguem o que estiver aqui.

**Files:**
- Create: `PLANO_DE_ENSINO.md`, `PLANEJAMENTO_AULA_A_AULA.md`

**Interfaces:**
- Consumes: as datas da seção Global Constraints
- Produces: a grade de 20 aulas com títulos exatos, que as Tasks 8 e 10 devem reproduzir sem divergir

- [ ] **Step 1: Criar `PLANO_DE_ENSINO.md`**

Seções, nesta ordem:

1. **Identificação:** disciplina Desenvolvimento Web, Uninove, 2026.2, Prof. José Romualdo, duas turmas (quarta e quinta), 19h30 às 22h, 20 encontros de 150 minutos.
2. **Ementa:** fundamentos da web, HTML, CSS, JavaScript, C#, ASP.NET Core MVC, Entity Framework Core, MySQL, Bootstrap, API REST e deploy.
3. **Metodologia:** encontro autossuficiente em quatro ciclos de conceito, demonstração e prática; sem atividade pré-aula; espiral, em que cada aula retoma a anterior e acrescenta uma camada.
4. **O case integrador Clínica Vida+:** descrição do mini mundo, as entidades principais (Paciente, Médico, Especialidade, Consulta) e como ele evolui de página estática a aplicação completa.
5. **Cronograma:** tabela com as colunas Aula, Data quarta, Data quinta, Módulo, Tema, Entregável. 20 linhas, usando as datas da seção Global Constraints e os títulos da tabela abaixo.
6. **Avaliação:** AV1 com checkpoints em aula valendo 40% e prova objetiva valendo 60%; AV2 institucional com questões de todas as disciplinas; média igual a `(AV1 + AV2) / 2`; aprovação com média maior ou igual a 6,0. Critérios do projeto final: funcionalidade 30%, código 25%, banco de dados 20%, interface 15%, apresentação 10%. Entrega por repositório no GitHub mais deploy funcional.
7. **Observação sobre 15/10:** cai numa quinta e é o Dia do Professor. Confirmar com a coordenação. Se suspenso, fundir as Aulas 18 e 19 na turma de quinta.
8. **Bibliografia:** documentação oficial da Microsoft para ASP.NET Core e EF Core, MDN Web Docs para HTML, CSS e JavaScript, e documentação do MySQL e do Bootstrap 5.

Módulos e títulos, exatos:

| # | Módulo | Tema |
|---|---|---|
| 01 | 1 Fundamentos da Web e Front-End | Apresentação, panorama da web, Git e GitHub |
| 02 | 1 | Estrutura da web e redes TCP/IP |
| 03 | 1 | Introdução ao HTML |
| 04 | 1 | Introdução ao CSS |
| 05 | 1 | CSS avançado e formulários HTML |
| 06 | 1 | Introdução ao JavaScript |
| 07 | 2 Backend com C# e ASP.NET Core MVC | Ambiente de desenvolvimento .NET |
| 08 | 2 | Primeiros passos com ASP.NET Core MVC |
| 09 | 2 | Estruturas de controle e coleções em C# |
| 10 | 2 | Formulários e Models no MVC |
| 11 | 2 | Entity Framework Core e MySQL |
| 12 | 2 | CRUD completo com EF Core |
| 13 | 3 Acesso a Dados e Funcionalidades Avançadas | Cookies e sessões |
| 14 | 3 | Requisições HTTP assíncronas com AJAX |
| 15 | 3 | Autenticação e autorização |
| 16 | 3 | API REST com ASP.NET Core |
| 17 | 3 | Relacionamentos e EF Core avançado |
| 18 | 4 Tópicos Avançados e Projeto Final | Layout, Partial Views e Bootstrap |
| 19 | 4 | Publicação e deploy |
| 20 | 4 | Revisão geral e projeto final |

- [ ] **Step 2: Criar `PLANEJAMENTO_AULA_A_AULA.md`**

Abre com a estrutura padrão do encontro:

```
19h30 às 20h05  Ciclo 1: conceito, demonstração, exercício curto
20h05 às 20h40  Ciclo 2: conceito, demonstração, exercício curto
20h40 às 20h50  Quiz de fixação
20h50 às 21h25  Ciclo 3: laboratório guiado, parte 1
21h25 às 21h50  Ciclo 4: laboratório, parte 2, e entregável
21h50 às 22h00  Fechamento, commit e prévia da próxima aula
```

Depois, uma seção por aula, agrupadas por módulo, cada uma com: número, título, as duas datas, objetivos de aprendizagem, recapitulação da aula anterior (a partir da Aula 02), conteúdo de cada ciclo com o tempo, o enunciado do quiz com alternativas e resposta, a missão do laboratório dentro do case e o entregável esperado.

Preencher as 20 aulas. A Aula 01 deve detalhar o que a Task 8 vai transformar em slides:

- Ciclo 1: apresentação do professor e da disciplina, metodologia, avaliação (AV1, AV2, média e aprovação), panorama do desenvolvimento web, arquitetura cliente-servidor, apresentação do case Clínica Vida+.
- Ciclo 2: por que versionar, evolução do controle de versão até o Git, o que é um commit (objeto imutável endereçado por hash), o que é uma branch, o ecossistema GitHub.
- Quiz: "O que um commit representa no Git?" com alternativas (a) apenas as linhas alteradas, (b) uma fotografia completa e imutável do projeto, ligada ao commit anterior, (c) um backup do arquivo aberto, (d) uma cópia do repositório remoto. Correta: (b).
- Ciclos 3 e 4: fork do repositório-esqueleto, clone, configuração de `user.name` e `user.email`, edição do README com nome e RA, primeiro commit e push.
- Entregável: link do fork com pelo menos um commit do aluno.

- [ ] **Step 3: Conferir que as datas batem com o módulo de turmas**

Run:
```bash
node -e "
import('./aulas-1sem/assets/js/turmas.js').then(m => {
  for (const t of ['quarta','quinta'])
    for (let i = 1; i <= 20; i++)
      console.log(t, String(i).padStart(2,'0'), m.formatarData(m.dataDaAula(t, i)));
});
"
```
Expected: 40 linhas. Conferir por amostragem contra a tabela de cronograma do `PLANO_DE_ENSINO.md`: aula 01 quarta é 05/08/2026, aula 01 quinta é 06/08/2026, aula 20 quarta é 16/12/2026, aula 20 quinta é 17/12/2026.

- [ ] **Step 4: Verificar ausência de travessão em dash**

Run: `grep -n '—' PLANO_DE_ENSINO.md PLANEJAMENTO_AULA_A_AULA.md`
Expected: nenhuma linha de saída.

- [ ] **Step 5: Commit**

```bash
git add PLANO_DE_ENSINO.md PLANEJAMENTO_AULA_A_AULA.md
git commit -m "docs(plano): plano de ensino e planejamento aula a aula das 20 aulas

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 7: Metodologia e agente de construção

**Files:**
- Create: `aulas-1sem/SKILL.md`, `.claude/agents/construtor-aulas-uninove.md`

**Interfaces:**
- Consumes: `docs/referencia/SKILL-fiap.md` (symlink) e `.claude/agents/construtor-aulas.md` (symlink), que servem de base
- Produces: o agente que as Tasks 8 e o plano das Aulas 02 a 20 vão invocar

- [ ] **Step 1: Criar `aulas-1sem/SKILL.md`**

Com frontmatter:

```yaml
---
name: uninove-course-design
description: Metodologia e padrão de construção das aulas de Desenvolvimento Web da Uninove 2026.2. Inclui a espiral de conteúdo, o case Clínica Vida+, a estrutura do encontro de 150 minutos em quatro ciclos, o padrão dos decks Reveal.js com tema Uninove e o padrão dos kits de laboratório.
---
```

Corpo com as seções: pilares metodológicos (espiral e aprendizagem por case, sem sala invertida); estrutura do encontro de 150 minutos com o diagrama de horários da Task 6; os eixos de conteúdo da disciplina (fundamentos da web e redes, HTML e CSS, JavaScript e DOM, C# e ASP.NET Core MVC, EF Core e MySQL, segurança e autenticação, API REST e deploy); o padrão do deck com o esqueleto HTML completo apontando para `../assets/css/uninove-theme.css`, `../assets/css/uninove-print.css` e `../assets/js/uninove-quiz.js`; as regras de markup dos quizzes (`.quiz-container`, `<ul class="quiz-options">`, `data-correct="true"`, `data-correct-msg` e `data-incorrect-msg`); e o padrão dos kits de laboratório.

- [ ] **Step 2: Criar `.claude/agents/construtor-aulas-uninove.md`**

Ler primeiro `.claude/agents/construtor-aulas.md` (o symlink da FIAP) e escrever o override local, que deve declarar explicitamente que substitui aquele arquivo neste repositório. Precisa cobrir:

- Case Clínica Vida+ no lugar de LogiTech, com as entidades e a evolução por aula
- Paleta `--uninove-azul` e `--uninove-coral` no lugar do rosa da FIAP
- Encontro de 150 minutos em quatro ciclos, sem intervalo, com os horários exatos
- Stack ASP.NET Core MVC, C#, Entity Framework Core, MySQL, Bootstrap 5
- Ausência de atividade pré-aula
- Nomes das classes do tema com prefixo `uninove-` e não `fiap-`
- Caminhos: decks em `aulas-1sem/aulas/`, labs em `aulas-1sem/labs/`, assets em `aulas-1sem/assets/`
- Pesos de avaliação **podem** aparecer nos slides, ao contrário da convenção da FIAP
- Regra de que todo deck deve passar em `python3 tools/check_slides.py` antes de ser considerado pronto

- [ ] **Step 3: Verificar que o agente é reconhecido**

Run: `ls -la .claude/agents/`
Expected: três entradas, sendo duas symlinks resolvendo e `construtor-aulas-uninove.md` como arquivo comum.

- [ ] **Step 4: Commit**

```bash
git add aulas-1sem/SKILL.md .claude/agents/construtor-aulas-uninove.md
git commit -m "docs(metodologia): skill de design das aulas e agente construtor da Uninove

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 8: Deck da Aula 01

**Files:**
- Create: `aulas-1sem/aulas/aula01.html`
- Read: `/Users/joseromualdocostafilho/Projects/FIAP/FIAP-2026-2-3SI/aulas-1sem/aulas/aula01.html` (origem do material de Git)
- Read: `PLANEJAMENTO_AULA_A_AULA.md` (roteiro da Aula 01, da Task 6)

**Interfaces:**
- Consumes: as classes do tema da Task 5 e `dataDaAula`/`formatarData` da Task 4
- Produces: o padrão-ouro que as Aulas 02 a 20 vão seguir

- [ ] **Step 1: Montar o esqueleto do deck**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Aula 01, Apresentação, panorama da web, Git e GitHub | Uninove</title>
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
      <!-- slides aqui -->
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
      plugins: [RevealHighlight],
    });
  </script>
</body>
</html>
```

Sem turma resolvida, o deck mostra as duas datas em vez de abrir modal, para não atrapalhar a projeção em sala.

- [ ] **Step 2: Escrever os slides na ordem canônica**

Seguir o roteiro da Aula 01 registrado no `PLANEJAMENTO_AULA_A_AULA.md`. Ordem:

1. Capa: `cover-slide` com `uninove-logo-full`
2. Título: `title-slide`, com o elemento `<span data-data-da-aula="1"></span>` no lugar da data
3. Agenda com os horários dos quatro ciclos
4. Apresentação do professor e da disciplina
5. Metodologia da disciplina, sem sala invertida, e o que se espera do aluno
6. Avaliação: AV1 40% checkpoints e 60% prova, AV2 institucional, média e aprovação
7. Panorama do desenvolvimento web e arquitetura cliente-servidor, com diagrama
8. O case Clínica Vida+: o problema, as entidades e o que existirá ao fim do semestre
9. Por que versionar: o problema aparece quando a segunda pessoa toca no mesmo arquivo
10. Evolução do controle de versão até o Git, distribuído e assíncrono
11. O que é, de fato, um commit: fotografia completa e imutável, endereçada por hash
12. O que é uma branch, com a analogia de linhas do tempo paralelas
13. O ecossistema GitHub: repositório remoto, fork, Pull Request, Actions
14. `quiz-slide` com o quiz do commit definido na Task 6
15. a 19. Laboratório em cinco slides: fork, clone, configuração do Git, edição do README, commit e push
20. Entregável e prévia da Aula 02
21. `end-slide` com o copyright do Prof. José Romualdo

Aproveitar de `FIAP-2026-2-3SI/aulas-1sem/aulas/aula01.html` os diagramas SVG dos slides de versionamento, evolução do Git, ecossistema GitHub, multiverso do Git e anatomia do commit. Trocar as cores `#ED145B` por `var(--uninove-coral)` e adaptar exemplos que citem a LogiTech para a Clínica Vida+. Não trazer Git Worktrees nem GitFlow.

Markup do quiz:

```html
<section class="quiz-slide content-slide">
  <div class="decor-coral"></div>
  <div class="slide-title-area"><div class="accent-bar"></div><h2>Quiz de fixação</h2></div>
  <div class="quiz-container">
    <div class="quiz-question">O que um commit representa no Git?</div>
    <ul class="quiz-options">
      <li data-correct="false"><span class="option-letter">A</span> Apenas as linhas alteradas desde a última vez.</li>
      <li data-correct="true"><span class="option-letter">B</span> Uma fotografia completa e imutável do projeto, ligada ao commit anterior.</li>
      <li data-correct="false"><span class="option-letter">C</span> Um backup do arquivo que está aberto no editor.</li>
      <li data-correct="false"><span class="option-letter">D</span> Uma cópia do repositório remoto na sua máquina.</li>
    </ul>
    <div class="quiz-feedback"
         data-correct-msg="Isso. Cada commit guarda o estado inteiro do projeto e aponta para o commit anterior, formando a história."
         data-incorrect-msg="Não é bem isso. O commit guarda o estado inteiro do projeto, não só o que mudou, e aponta para o commit anterior."></div>
  </div>
  <div class="slide-footer"><div class="footer-bar">01 Quiz de fixação</div><div class="footer-page">14</div></div>
</section>
```

- [ ] **Step 3: Validar o layout**

Run: `python3 tools/check_slides.py aulas-1sem/aulas/aula01.html`
Expected: `OK: nenhum conteudo estourando 1280x720`.

Se acusar estouro, rodar com `--shots /tmp/shots` e olhar o PNG do slide apontado. A correção é reduzir conteúdo ou dividir em dois slides, nunca diminuir a fonte a ponto de ficar ilegível na projeção.

- [ ] **Step 4: Conferir o comportamento do quiz e da data**

Run: `python3 -m http.server 8000` e abrir `http://localhost:8000/aulas-1sem/aulas/aula01.html`.
Expected: navegar até o slide de quiz, clicar numa alternativa errada e ver a correta destacada em verde, a escolhida em vermelho e a mensagem de `data-incorrect-msg`. Sair do slide e voltar deve permitir responder de novo. No slide de título, a data deve aparecer preenchida.

- [ ] **Step 5: Conferir a numeração de rodapé**

Run: `grep -c 'footer-page' aulas-1sem/aulas/aula01.html`
Expected: um por slide de conteúdo. Conferir que a sequência de números não pula nem repete.

- [ ] **Step 6: Commit**

```bash
git add aulas-1sem/aulas/aula01.html
git commit -m "feat(aula01): deck de apresentacao, panorama da web, Git e GitHub

Padrao-ouro do acervo. Material de versionamento adaptado do deck da Aula 01
da FIAP, ancorado no case Clinica Vida+.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 9: Laboratório da Aula 01 e repositório-esqueleto do case

**Files:**
- Create: `aulas-1sem/labs/aula01-lab/README.md`
- Create: repositório `josercf/uninove-2026-2-clinica-vida` no GitHub, com `README.md`, `.gitignore` e `docs/CASE.md`

**Interfaces:**
- Consumes: o roteiro da Aula 01 da Task 6
- Produces: o repositório que o aluno forka na Aula 01 e evolui até a Aula 20

- [ ] **Step 1: Escrever `aulas-1sem/labs/aula01-lab/README.md`**

Estrutura, seguindo o padrão do acervo da FIAP:

- Título: `# Laboratório da Aula 01`
- Subtítulo com disciplina, professor e instituição
- `### Case: Clínica Vida+ (Fase 0, ambiente e versionamento)`, explicando que hoje o entregável não é código do sistema, é o ambiente montado e o primeiro commit
- Duração: 60 minutos, individual
- Pré-requisitos: conta no GitHub, Git instalado, VS Code
- Passo 1 (15 min): criar conta no GitHub se não tiver, e fazer fork de `https://github.com/josercf/uninove-2026-2-clinica-vida`
- Passo 2 (10 min): clonar o fork, com o comando exato e o lembrete de trocar `SEU-USUARIO`
- Passo 3 (10 min): configurar `git config user.name` e `git config user.email`
- Passo 4 (15 min): editar o `README.md` do fork, preenchendo nome completo, RA e turma
- Passo 5 (10 min): `git add`, `git commit -m "docs: identificacao do aluno"` e `git push`
- Seção de entregável: link do fork, com pelo menos um commit de autoria do aluno
- Seção "Se algo der errado", com os erros mais comuns: `Permission denied (publickey)`, `Author identity unknown` e `fatal: not a git repository`, cada um com a causa e o comando que resolve

- [ ] **Step 2: Criar o repositório-esqueleto**

```bash
gh repo create josercf/uninove-2026-2-clinica-vida --public \
  --description "Projeto do semestre da disciplina Desenvolvimento Web, Uninove 2026.2"
```
Expected: URL do repositório criado.

- [ ] **Step 3: Popular o repositório-esqueleto**

Clonar em `/tmp`, criar os três arquivos e empurrar.

`README.md` do esqueleto: título Clínica Vida+, uma linha sobre o que o sistema será, e um bloco de identificação para o aluno preencher:

```markdown
## Identificação

- **Nome completo:**
- **RA:**
- **Turma:** (quarta ou quinta)
```

`docs/CASE.md`: o enunciado do mini mundo, com o contexto da clínica, os atores (paciente, recepção, médico), as entidades (Paciente, Médico, Especialidade, Consulta) e a lista do que o sistema deve fazer ao fim do semestre.

`.gitignore`: o padrão do .NET (`bin/`, `obj/`, `*.user`, `appsettings.Development.json`) mais `.DS_Store`.

- [ ] **Step 4: Verificar que o fork funciona de ponta a ponta**

Run: `gh repo view josercf/uninove-2026-2-clinica-vida --json url,isPrivate,description`
Expected: `isPrivate: false`. Abrir a URL e confirmar que o botão Fork está disponível e que o `README.md` mostra o bloco de identificação.

- [ ] **Step 5: Commit no acervo**

```bash
git add aulas-1sem/labs/aula01-lab/README.md
git commit -m "feat(aula01): kit de laboratorio de ambiente e primeiro commit

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 10: Portal e validador do portal

**Files:**
- Create: `aulas-1sem/index.html`, `tools/check_portal.py`

**Interfaces:**
- Consumes: `TURMAS`, `resolverTurma`, `dataDaAula` e `formatarData` da Task 4; os títulos das 20 aulas da Task 6
- Produces: o portal publicado, ponto de entrada da disciplina

- [ ] **Step 1: Escrever o portal**

Requisitos do `aulas-1sem/index.html`:

- Cabeçalho com o nome da disciplina, o semestre, o professor e o logo
- Um seletor de turma no cabeçalho, com as duas opções, refletindo a turma ativa
- Quatro seções, uma por módulo, com os títulos da tabela da Task 6
- 20 cards, um por aula, cada um com número, título, data da turma ativa e dois botões: "Slides", apontando para `aulas/aulaXX.html`, e "Lab", apontando para `labs/aulaXX-lab/`
- Cards de aulas ainda não produzidas ficam com os botões desabilitados e o rótulo "Em produção"
- Um modal que aparece somente quando `resolverTurma` devolve `null`, com as duas opções e sem opção de fechar sem escolher
- A escolha grava em `localStorage` sob a chave `uninove-turma`, e trocar no seletor re-renderiza as datas dos cards sem recarregar a página
- Paleta: fundo `#00274D`, destaque `#C84B31`, texto claro. Fonte Montserrat
- Um atributo `data-aula="N"` em cada card, e `data-total-cards` no contêiner, para o validador conseguir contar

O script do portal é um `<script type="module">` inline que importa de `assets/js/turmas.js`.

- [ ] **Step 2: Escrever `tools/check_portal.py`**

Arquivo local, não symlink. Usa Playwright, servindo o repositório igual ao `check_slides.py`.

Verifica, em ordem:

1. Com o relógio do navegador fixado numa quarta (05/08/2026), `localStorage` limpo: o modal **não** aparece e os cards mostram datas de quarta. Fixar o relógio com `page.add_init_script` sobrescrevendo `Date`, ou mais simples, gravando `localStorage` antes de navegar e testando os três casos por `localStorage`.
2. Com `localStorage` gravado como `quinta`: os cards mostram datas de quinta, e a data do card da aula 01 é `06/08/2026`.
3. Com `localStorage` gravado com valor inválido e o dia real não sendo quarta nem quinta: o modal aparece.
4. Existem exatamente 20 cards.
5. Todo `href` de botão habilitado aponta para um arquivo que existe no disco.

Sai com código 1 se qualquer verificação falhar, imprimindo o que falhou.

- [ ] **Step 3: Rodar o validador do portal**

Run: `python3 tools/check_portal.py`
Expected: todas as verificações passando, e código de saída 0.

Neste momento só a Aula 01 tem deck e lab, então a verificação 5 deve encontrar apenas os links da Aula 01 habilitados. Se acusar link quebrado para outras aulas, é porque os cards não foram marcados como "Em produção".

- [ ] **Step 4: Conferir visualmente**

Run: `python3 -m http.server 8000` e abrir `http://localhost:8000/`.
Expected: redireciona para o portal; os 20 cards aparecem agrupados em quatro módulos; o card da Aula 01 tem os dois botões ativos; trocar a turma no seletor muda todas as datas na hora.

- [ ] **Step 5: Commit**

```bash
git add aulas-1sem/index.html tools/check_portal.py
git commit -m "feat(portal): portal com os 20 cards e selecao de turma

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 11: Publicação e fechamento

**Files:**
- Modify: `docs/ANDAMENTO.md`

**Interfaces:**
- Consumes: tudo o que as Tasks anteriores produziram
- Produces: acervo publicado e estado registrado para a próxima sessão

- [ ] **Step 1: Rodar a bateria completa de validação**

Run:
```bash
npm test
python3 tools/check_slides.py
python3 tools/check_portal.py
grep -rn '—' --include='*.md' --include='*.html' . | grep -v node_modules
```
Expected: testes passando, nenhum slide estourando, portal válido e nenhuma ocorrência de travessão em dash.

- [ ] **Step 2: Push**

```bash
git push
```

Se o push falhar por autenticação, usar:
```bash
GIT_SSH_COMMAND='ssh -i ~/.ssh/id_ed25519_josercf -o IdentitiesOnly=yes' git push
```

- [ ] **Step 3: Confirmar a publicação**

Run: `gh run list --repo josercf/uninove-2026-2-desenvolvimento-web --limit 1`
Expected: conclusão `success`.

Run: `curl -sI https://josercf.github.io/uninove-2026-2-desenvolvimento-web/aulas-1sem/aulas/aula01.html | head -1`
Expected: `HTTP/2 200`.

Abrir <https://josercf.github.io/uninove-2026-2-desenvolvimento-web/> e confirmar que o portal carrega, o seletor de turma funciona e o deck da Aula 01 abre.

- [ ] **Step 4: Atualizar `docs/ANDAMENTO.md`**

Registrar: data da sessão; o que ficou pronto (infraestrutura, symlinks, tema, módulo de turmas com testes, planos, Aula 01 com deck e lab, repositório-esqueleto, portal); as URLs do acervo publicado e do repositório-esqueleto; e como próximo passo, escrever o plano das Aulas 02 a 20 usando a Aula 01 como referência e o agente `construtor-aulas-uninove`.

- [ ] **Step 5: Commit e push final**

```bash
git add docs/ANDAMENTO.md
git commit -m "docs(andamento): registrar a fundacao do acervo concluida

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
git push
```

---

## Auto-revisão do plano contra a spec

| Seção da spec | Task que cobre |
|---|---|
| 4 Arquitetura do repositório | 1, 2, 3 |
| 4.1 Nome `aulas-1sem/` | 2 (symlinks assumem o nome), 5, 8 |
| 5 Symlinks | 2 |
| 5.1 Ajustes na FIAP | 2, steps 1 a 4 |
| 5.2 Override local | 7 |
| 6.1 Datas | Global Constraints, 4, 6 |
| 6.2 Resolução da turma | 4, 8 (deck), 10 (portal) |
| 7 Grade das 20 aulas | 6 |
| 7.1 Git e GitHub nas aulas iniciais | 8 (Aula 01), e Aula 03 fica para o plano seguinte |
| 8 Anatomia de um deck | 5 (classes), 7 (SKILL), 8 (aplicação) |
| 9 Avaliação | 6 (plano de ensino), 8 (slide de avaliação) |
| 10 Laboratórios | 9 |
| 11 Testes e validação | 1, 4, 10, 11 |
| 12 ADRs | 3 |
| 13 Ordem de execução | ordem das tasks |
| 14 Riscos | 2 (symlink), 6 (15/10), 7 (override) |
| 15 Convenções editoriais | Global Constraints, 3 (CLAUDE.md), 7 (agente) |

**Pendência conhecida e deliberada:** a seção 7.1 da spec coloca branch e Pull Request na Aula 03, que está fora deste plano. Fica registrado como primeiro item do plano das Aulas 02 a 20.
