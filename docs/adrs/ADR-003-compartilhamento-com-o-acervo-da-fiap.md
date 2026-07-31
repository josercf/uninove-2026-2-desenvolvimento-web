# ADR-003: Compartilhamento com o acervo da FIAP

**Data:** 30/07/2026
**Status:** Aceita
**Decisores:** Prof. José Romualdo

## Contexto

O acervo da FIAP (`josercf/FIAP-2026-2-3SI`) já resolve boa parte do que este
acervo precisa: agentes de construção e revisão de decks, um hook que valida o
layout a cada edição de deck e o validador `check_slides.py` que confere estouro
de conteúdo em 1280x720. Esses artefatos servem tal como estão para o acervo da
Uninove. Ao mesmo tempo, parte do conteúdo da FIAP é específico daquela
disciplina: o case LogiTech, a paleta rosa, o encontro de 3,5 horas com intervalo
e a stack poliglota não se aplicam aqui.

## Decisão

Compartilhar arquivo a arquivo, por symlink relativo, tudo o que é genérico entre
os dois acervos: `.claude/settings.json`, `.claude/agents/construtor-aulas.md`,
`.claude/agents/revisor-slides.md`, `tools/check_slides.py`,
`tools/scaffold_labs.py` e `docs/referencia/SKILL-fiap.md`. O que é específico da
Uninove vive em `construtor-aulas-uninove.md`, um arquivo local que sobrescreve o
que muda em relação ao agente da FIAP.

## Motivações

Melhorias feitas no acervo da FIAP, como ajustes no validador ou no agente
construtor, passam a refletir automaticamente aqui, sem cópia manual e sem o
risco de os dois acervos divergirem silenciosamente.

## Riscos conhecidos

- **Symlink para fora do repositório quebra em qualquer máquina que não tenha os
  dois clones lado a lado**, incluindo o ambiente do GitHub Actions.
  - **Mitigação:** os arquivos espelhados ficam sob `.claude/`, `tools/` e
    `docs/`, diretórios que o GitHub Pages não serve como página. O workflow de
    publicação também não executa nenhum desses arquivos, apenas publica o
    repositório; portanto um symlink quebrado no ambiente do Actions não afeta o
    site publicado.

    > **Nota de superação, 31/07/2026.** A mitigação acima está errada e foi
    > superada pela **ADR-006**. Um symlink quebrado no runner **derrubou** a
    > publicação: `actions/upload-pages-artifact@v3` empacota o artefato com
    > `tar --dereference`, que segue todo symlink até um arquivo real. Os seis
    > symlinks apontam para o acervo da FIAP, que não existe no runner, e o
    > `tar` abortava com código 1 antes de qualquer deploy. Não bastava não
    > executar os arquivos: bastava que eles estivessem dentro do artefato. A
    > correção real está na ADR-006, que monta um `_site` com `rsync` excluindo
    > `tools/`, `.claude/`, `tests/` e `docs/referencia/`, e falha o build se
    > sobrar qualquer symlink dentro de `_site`. A decisão original desta ADR,
    > compartilhar por symlink relativo, continua valendo; o que caiu foi a
    > avaliação do risco.

## Consequências

**Positivas:**

- Melhorias no acervo da FIAP chegam aqui sem esforço adicional.
- Não há duplicação de código entre os dois acervos para o que é genuinamente
  compartilhável.

**Negativas:**

- Um clone isolado deste repositório, feito numa máquina que não tenha também o
  acervo da FIAP clonado ao lado, fica sem os validadores, os agentes e o hook até
  que o acervo da FIAP também seja clonado na posição relativa esperada.

## ADRs relacionadas

- ADR-001: migração dos decks para Reveal.js
- ADR-006: artefato de publicação sem as ferramentas, que supera a mitigação de
  risco registrada aqui
