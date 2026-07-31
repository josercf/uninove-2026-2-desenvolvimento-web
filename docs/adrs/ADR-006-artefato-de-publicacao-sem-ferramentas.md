# ADR-006: Artefato de publicação sem as ferramentas

**Data:** 31/07/2026
**Status:** Aceita
**Decisores:** Prof. José Romualdo

## Contexto

O workflow de publicação (`.github/workflows/static.yml`) usava
`actions/upload-pages-artifact@v3` com `path: '.'`, empacotando o repositório
inteiro para o GitHub Pages. Essa action monta o artefato com
`tar --dereference --hard-dereference`, que precisa seguir todo symlink até um
arquivo real. Os seis symlinks documentados na ADR-003
(`tools/check_slides.py`, `tools/scaffold_labs.py`, `.claude/settings.json`,
`.claude/agents/construtor-aulas.md`, `.claude/agents/revisor-slides.md`,
`docs/referencia/SKILL-fiap.md`) apontam para o acervo da FIAP, um repositório
irmão que só existe na máquina local do professor. No runner do GitHub
Actions, `actions/checkout@v4` traz apenas este repositório: o alvo dos
symlinks não existe ali, eles ficam quebrados (dangling), e o `tar` aborta com
código de saída 1 ao tentar dereferenciá-los. O primeiro push que continha os
seis symlinks (criados só na Task 2, depois do workflow inicial) já
reproduziu essa falha em produção, derrubando a publicação.

A ADR-003 já havia identificado o risco de symlink quebrado fora da máquina do
professor, mas avaliou que o workflow "não executa nenhum desses arquivos,
apenas publica o repositório" e por isso o risco não afetaria o site. Essa
mitigação estava incompleta: não é a execução do conteúdo do symlink que
quebra o deploy, é o próprio mecanismo de empacotamento do artefato
(`tar --dereference`), que trata symlink quebrado como erro fatal,
independentemente de o link ser lido, executado ou referenciado pelo HTML
publicado.

## Decisão

Publicar apenas um subconjunto do repositório, e não o repositório inteiro. Um
passo novo no workflow monta um diretório `_site` com `rsync`, excluindo
`.git`, `.github`, `.claude`, `tools`, `tests`, `docs/referencia`,
`node_modules`, `.superpowers` e o próprio `_site`, conforme o mínimo exigido,
mais duas exclusões adicionais decididas nesta ADR: `docs/superpowers`
(specs e planos de execução do processo de construção do acervo, mesma
natureza de `.superpowers`, só que versionado) e os dois arquivos de estado
interno de sessão, `CLAUDE.md` e `docs/ANDAMENTO.md`. O `upload-pages-artifact`
passa a apontar para `_site`, não mais para `.`. Um passo de verificação roda
`find _site -type l` logo depois de montar o diretório e falha o build se
encontrar qualquer symlink, para que uma regressão futura (por exemplo, um
novo symlink compartilhado criado fora de `tools/`, `.claude/` ou
`docs/referencia/`) seja pega em CI, e não descoberta de novo em produção. Os
seis symlinks continuam versionados no repositório: documentam a relação de
compartilhamento com o acervo da FIAP e continuam propagando melhorias feitas
lá (ver ADR-003). O que muda é só o que vai para o artefato do Pages.

`docs/adrs/`, `PLANO_DE_ENSINO.md`, `PLANEJAMENTO_AULA_A_AULA.md` e
`README.md` continuam sendo publicados, por decisão consciente e não por
omissão: os dois planos são referência direta para os alunos (ementa,
cronograma, avaliação) e não fazem sentido escondidos; os ADRs são curtos,
não contêm segredo algum e servem como exemplo de documentação de decisão de
engenharia, coerente com uma disciplina de desenvolvimento web; o `README.md`
é a porta de entrada padrão de qualquer repositório e não custa nada deixá-lo
acessível. Já `CLAUDE.md` e `docs/ANDAMENTO.md` são registro de processo
interno de sessão (instruções para um agente de IA, estado de tarefas entre
sessões, notas de armadilhas de ambiente) sem valor para quem visita o site
como aluno, e por isso ficam de fora do artefato publicado, embora continuem
públicos no repositório Git.

## Motivações

- O `tar --dereference` da action de upload é comportamento de terceiros,
  fora do nosso controle, e não tem opção documentada para ignorar symlinks
  quebrados silenciosamente.
- Excluir os diretórios que contêm symlinks resolve a causa raiz sem desfazer
  a decisão da ADR-003: os symlinks continuam existindo e propagando
  melhorias da FIAP, só não fazem parte do artefato publicado.
- Publicar um subconjunto também restringe o que fica público a material
  didático de fato: ferramentas de validação, agentes de IA e documentação de
  processo interno (planejamento de sessão, specs de construção) não têm
  valor para quem visita o site como aluno.

## Riscos conhecidos

- **Um novo symlink criado fora dos diretórios já excluídos (`tools/`,
  `.claude/`, `docs/referencia/`) voltaria a quebrar o deploy.**
  - **Mitigação:** o passo `find _site -type l` falha o build explicitamente
    se qualquer symlink chegar ao `_site`, transformando a falha em algo
    visível e diagnosticável em CI, em vez de um `tar` abortando sem
    contexto.
- **A lista de exclusões do `rsync` pode ficar desatualizada** se um novo
  diretório interno (ferramenta, teste, documentação de processo) for criado
  sem atualizar o workflow, publicando-o por engano.
  - **Mitigação:** a lista de exclusões é curta e nomeada por categoria
    (ferramentas, testes, documentação de referência e de processo), não por
    arquivo individual; revisar o workflow ao criar uma nova categoria de
    diretório interno é parte do checklist de qualquer task futura que crie
    esse tipo de diretório.
- **Divergência entre o que existe no repositório e o que é publicado** pode
  confundir quem espera que "tudo que está no Git está no ar".
  - **Mitigação:** esta ADR e a entrada correspondente no `CLAUDE.md`
    documentam exatamente o que é publicado e por quê.

## Consequências

**Positivas:**

- A publicação volta a funcionar de forma resiliente a symlinks quebrados no
  runner, sem abrir mão do compartilhamento por symlink com a FIAP.
- O site publicado fica mais enxuto e focado em material didático, sem
  ferramentas internas, agentes de IA ou documentação de processo.
- A validação `find _site -type l` cobre a classe inteira do problema
  (qualquer symlink, não só os seis atuais), então symlinks futuros não
  reintroduzem a mesma falha sem aviso.

**Negativas:**

- O workflow fica mais complexo, com um passo a mais de montagem e um passo a
  mais de validação, em vez de publicar o repositório diretamente.
- `CLAUDE.md` e `docs/ANDAMENTO.md`, que documentam o processo de construção
  do acervo, deixam de estar acessíveis pelo Pages (continuam visíveis pelo
  repositório Git no GitHub, só não pelo site).

## ADRs relacionadas

- ADR-003: compartilhamento com o acervo da FIAP
