# ADR-001: Migração dos decks para Reveal.js

**Data:** 30/07/2026
**Status:** Aceita
**Decisores:** Prof. José Romualdo

## Contexto

O acervo de 2026.1 (`josercf/uninove-2026-1-desenvolvimento-web`) usa um motor de
slides próprio, construído sobre `slides.css` e `slides.js`. Esse motor funciona
para exibir os 20 decks em sala, mas nenhuma automação existente opera sobre ele:
não há validador de layout, não há exportação para PDF e não há agentes de
construção ou revisão que entendam a sua estrutura. Toda a automação já construída
para o acervo da FIAP (`josercf/FIAP-2026-2-3SI`), incluindo o validador
`check_slides.py`, o hook de validação a cada edição e os agentes construtor e
revisor, assume decks em Reveal.js de 1280x720.

## Decisão

Reescrever os 20 decks da disciplina em Reveal.js 5.1.0, com dimensão fixa de
1280x720, sob um tema próprio da Uninove derivado do tema visual da FIAP.

## Motivações

Migrar para Reveal.js habilita, de uma só vez, todo o ferramental já validado na
FIAP: `check_slides.py` para checar estouro de layout, o hook de validação
automática a cada edição de deck, a exportação nativa em PDF via `?print-pdf` e os
agentes construtor e revisor de slides. Reescrever o motor de exibição custa uma
vez; manter o motor próprio custaria manutenção recorrente sem nenhum desse
ferramental.

## Riscos conhecidos

- **Custo de reescrever 20 decks.** É um volume de trabalho considerável, e um
  padrão errado replicado 20 vezes é retrabalho garantido.
  - **Mitigação:** a Aula 01 é produzida primeiro, como padrão-ouro, validada
    contra o layout de 1280x720 e revisada antes de qualquer outra aula. As
    Aulas 02 a 20 são então produzidas em série contra esse padrão já travado,
    em vez de cada uma inventar sua própria estrutura.

## Consequências

**Positivas:**

- O acervo passa a se beneficiar de `check_slides.py`, do hook de validação, da
  exportação `?print-pdf` e dos agentes construtor e revisor, sem precisar
  desenvolver nada disso do zero.
- O formato fica alinhado ao acervo da FIAP, o que permite compartilhar
  ferramentas e agentes por symlink (ver ADR-003).

**Negativas:**

- O conteúdo de 2026.1 não pode ser copiado diretamente: cada slide precisa ser
  transposto individualmente para a estrutura e as classes do novo tema, o que
  consome tempo de revisão editorial além da migração técnica.

## ADRs relacionadas

- ADR-003: compartilhamento com o acervo da FIAP
