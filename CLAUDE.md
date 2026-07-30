# CLAUDE.md

Antes de qualquer outra coisa, leia `docs/ANDAMENTO.md`. Ele registra o estado do
trabalho entre sessões e diz o que já está pronto e o que falta.

## O que é este repositório

Acervo didático da disciplina **Desenvolvimento Web**, Uninove, 2026.2. Site
estático publicado no GitHub Pages, sem build e sem bundler: os decks Reveal.js
carregam do jsDelivr por CDN, o tema é CSS puro e a resolução de turma é um
módulo ES sem dependências. Não há passo de compilação em nenhum ponto do
repositório.

## Comandos

```bash
# Preview local (os decks usam caminhos relativos, por isso precisa de HTTP)
python3 -m http.server 8000

# Exportação de um deck em PDF: abrir o deck com ?print-pdf e imprimir do navegador
# http://localhost:8000/aulas-1sem/aulas/aula01.html?print-pdf

# Testes de lógica (resolução de turma)
npm test

# Validação de layout dos decks (estouro de 1280x720)
python3 tools/check_slides.py

# Validação do portal e dos links dos cards
python3 tools/check_portal.py
```

## As três camadas de conteúdo

1. **Planejamento, na raiz do repositório.** `PLANO_DE_ENSINO.md` (ementa, case,
   cronograma das duas turmas, avaliação) e `PLANEJAMENTO_AULA_A_AULA.md`
   (roteiro minuto a minuto das 20 aulas). São a fonte da verdade de datas,
   títulos e escopo; decks e portal seguem o que estiver aqui.
2. **Metodologia, em `aulas-1sem/SKILL.md`.** Descreve a espiral de conteúdo, o
   case Clínica Vida+, a estrutura do encontro de 150 minutos em quatro ciclos e
   o padrão de construção de decks e labs.
3. **Materiais, em `aulas-1sem/`.** O portal (`index.html`), os decks
   (`aulas/aulaXX.html`), os kits de laboratório (`labs/aulaXX-lab/`) e o tema
   visual (`assets/`).

## O case Clínica Vida+

Todas as aulas e laboratórios constroem a **Clínica Vida+**, um sistema de
agendamento de consultas que começa como página estática e termina como
aplicação ASP.NET Core MVC completa, com Entity Framework Core, MySQL,
autenticação, API REST e deploy. Cada aula faz o case avançar um passo; o
entregável de uma aula é o ponto de partida da seguinte. Diferente do acervo da
FIAP, aqui não existem 20 repositórios de laboratório independentes: existe um
único repositório-esqueleto, `josercf/uninove-2026-2-clinica-vida`, que o aluno
forka na Aula 01 e evolui semana a semana. Os diretórios em `aulas-1sem/labs/`
são a referência do professor e o gabarito de cada etapa, não repositórios à
parte.

## Anatomia do deck

Cada `aulaXX.html` é autocontido, mede exatamente 1280x720 e é inicializado com
`center: false, margin: 0`. A `section` do Reveal tem altura fixa: o conteúdo
não rola, e o que não couber quebra o slide visualmente sem lançar nenhum erro.

Ordem canônica de slides, em quatro ciclos de 35, 35, 35 e 25 minutos:

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

Classes de slide: `cover-slide`, `title-slide`, `content-slide`,
`section-slide`, `quiz-slide`, `exercise-slide`, `end-slide`.

Blocos reutilizáveis: `concept-cards` com `concept-card`, `side-by-side`,
`slide-title-area` com `accent-bar`, `top-bar`, `slide-footer` com `footer-bar`
e `footer-page`, e `uninove-logo-header`.

## Compartilhamento com o acervo da FIAP

Seis arquivos deste repositório são symlinks relativos para o acervo da FIAP em
`Projects/FIAP/FIAP-2026-2-3SI`: `tools/check_slides.py`,
`tools/scaffold_labs.py`, `.claude/settings.json`,
`.claude/agents/construtor-aulas.md`, `.claude/agents/revisor-slides.md` e
`docs/referencia/SKILL-fiap.md`. Cada link usa quatro ou cinco níveis de `../`,
conforme a profundidade do diretório que contém o link (`readlink` em qualquer
um deles mostra o caminho exato). Editar qualquer um deles edita o acervo da
FIAP também, porque não são cópias.

O que é específico da Uninove sobrescreve o que é genérico por arquivo local, não
por edição do symlink: `.claude/agents/construtor-aulas-uninove.md` é o override
do agente construtor da FIAP, trocando o case LogiTech pela Clínica Vida+, a
paleta rosa pela azul e coral, o encontro de 3,5 horas com intervalo pelo de 150
minutos sem intervalo, e a stack poliglota pela stack ASP.NET Core MVC, C#, EF
Core, MySQL e Bootstrap.

Ver ADR-003 para o raciocínio completo por trás dessa decisão.

## Armadilhas conhecidas

- Slide que estoura 720px não é detectável por `scrollHeight`, porque a
  `section` tem altura fixa. Usar sempre `tools/check_slides.py` para validar
  layout, nunca inspeção visual isolada.
- `tools/check_slides.py` e `.claude/settings.json` são symlinks para o acervo
  da FIAP. Editá-los altera o acervo da FIAP também.
- `new Date('2026-08-05')` é interpretado como UTC e vira 04/08 no fuso de São
  Paulo. Datas em `turmas.js` são sempre montadas componente a componente
  (ano, mês, dia), nunca pelo construtor de string ISO.
- O workflow publica o repositório inteiro. Qualquer arquivo commitado fica
  público, incluindo o que estiver fora de `aulas-1sem/`.
- O comando de push correto depende do repositório, porque cada um usa um host
  SSH diferente. Neste repositório (Uninove), o remote usa o alias de host
  `github.com-josercf`, que só existe dentro do `~/.ssh/config`; um `git push`
  simples já autentica como `josercf` e é o comando a usar aqui. Usar
  `-F /dev/null` neste repositório faz o SSH ignorar o próprio `~/.ssh/config`,
  o alias deixa de resolver e o push falha por hostname não encontrado (foi o
  que aconteceu na Task 1). Já o acervo da FIAP é o caso oposto: o remote usa o
  host `github.com` normal, onde o `~/.ssh/config` mapeia essa entrada para a
  identidade `canaldoovidio`. Ali vale a diretiva global do professor, com
  `-F /dev/null` como forma mais defensiva de forçar a identidade `josercf`:
  `GIT_SSH_COMMAND='ssh -i /Users/joseromualdocostafilho/.ssh/id_ed25519_josercf
  -o IdentitiesOnly=yes -F /dev/null' git push`.
- `.claude/settings.local.json` existe em disco mas não é versionado, por um
  gitignore global do usuário (`**/.claude/settings.local.json`). Quem clonar
  este repositório numa máquina nova precisa recriá-lo manualmente; ele não
  chega pelo `git clone`.

## Convenções editoriais

Herdadas do acervo da FIAP, com uma exceção explícita:

- Sem emojis em slides, títulos ou textos. O tom é profissional.
- Português do Brasil com acentuação completa. Nunca usar travessão em dash.
- **Exceção à convenção da FIAP:** pesos de avaliação aparecem nos slides,
  porque assim era em 2026.1 e o professor quer manter.
- Preferir diagramas e imagens didáticas a paredes de texto.
- Referências numeradas ao longo dos slides e consolidadas em um slide final.
- Todo deck termina com o slide de copyright do Prof. José Romualdo.
- Commits em Conventional Commits, com escopo pela aula: `feat(aula01): ...`,
  `fix(portal): ...`.
