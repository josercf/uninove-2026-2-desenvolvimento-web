# ADR-002: Resolução de turma no cliente

**Data:** 30/07/2026
**Status:** Aceita
**Decisores:** Prof. José Romualdo

## Contexto

A disciplina é ministrada para duas turmas com conteúdo idêntico, uma às
quartas-feiras e outra às quintas-feiras, cada uma com seu próprio calendário de
20 encontros. Os identificadores institucionais das turmas no Google Classroom
ainda não foram divulgados. Não há como distinguir as turmas por URL ou por
matrícula ainda, e o professor abre o mesmo portal em sala independentemente de
qual turma está lecionando naquele dia.

## Decisão

Manter um único conjunto de materiais para as duas turmas. A turma exibida é
resolvida em tempo de execução, no navegador, pela função pura
`resolverTurma({hoje, salva})`, com a seguinte ordem de precedência: primeiro a
escolha salva pelo usuário, depois o dia da semana da data corrente, e um modal de
escolha manual como último recurso quando nenhuma das duas se aplica.

## Motivações

Essa abordagem elimina qualquer duplicação de conteúdo entre as duas turmas: os
mesmos decks, o mesmo portal e o mesmo planejamento servem as duas. Além disso, o
professor consegue abrir o portal em sala no dia da aula sem precisar escolher
nada: o dia da semana já resolve a turma correta automaticamente.

## Riscos conhecidos

- **Aluno que abre o portal fora dos dias de aula precisa escolher manualmente.**
  Um aluno que acessa num sábado, por exemplo, não tem dia da semana que resolva
  a turma sozinho.
  - **Mitigação:** a escolha feita no modal é gravada em `localStorage`, então o
    aluno só escolhe uma vez. Um seletor permanece disponível no cabeçalho do
    portal para trocar de turma a qualquer momento, sem depender do modal.

## Consequências

**Positivas:**

- Zero duplicação de conteúdo entre as duas turmas.
- O fluxo em sala de aula fica livre de qualquer interação extra: o professor abre
  o portal e a data certa já aparece.

**Negativas:**

- A data deixa de ser conteúdo estático do HTML e passa a depender de JavaScript
  habilitado no navegador para ser resolvida. Um usuário com JavaScript desligado
  não vê a data correta automaticamente.

## ADRs relacionadas

- ADR-004: case Clínica Vida+ e encontro de 150 minutos
