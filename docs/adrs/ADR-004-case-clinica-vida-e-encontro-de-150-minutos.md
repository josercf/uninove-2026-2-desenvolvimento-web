# ADR-004: Case Clínica Vida+ e encontro de 150 minutos

**Data:** 30/07/2026
**Status:** Aceita
**Decisores:** Prof. José Romualdo

## Contexto

As aulas acontecem das 19h30 às 22h, 150 minutos corridos, sem intervalo formal.
O plano de 2026.1 previa sala de aula invertida, com atividade obrigatória antes
da aula, mas a adesão do público da Uninove a essa leitura prévia foi baixa: a
aula acabava perdendo tempo recuperando uma base que deveria ter chegado pronta.

## Decisão

Adotar um case integrador único, a Clínica Vida+, um sistema de agendamento de
consultas que evolui aula a aula ao longo do semestre. O encontro é estruturado
em quatro ciclos de aproximadamente 35 minutos cada, alternando conceito,
demonstração e prática, sem nenhuma atividade pré-aula.

## Motivações

Essa estrutura torna o encontro autossuficiente: tudo o que o aluno precisa para
acompanhar chega dentro da própria aula, sem depender de preparo prévio que a
experiência de 2026.1 mostrou não acontecer. Ao mesmo tempo, o entregável de cada
aula se acumula sobre o entregável da aula anterior, fazendo o case caminhar
junto com a turma rumo ao projeto final.

## Riscos conhecidos

- **150 minutos corridos, sem intervalo formal, cansam.**
  - **Mitigação:** a própria troca de ciclo, a cada aproximadamente 35 minutos,
    funciona como um respiro natural na aula, e o quiz de fixação das 20h40 quebra
    o ritmo entre o segundo e o terceiro ciclo.

## Consequências

**Positivas:**

- O encontro fica autossuficiente, sem depender de atividade prévia que a
  experiência de 2026.1 mostrou ter baixa adesão.
- O entregável de cada aula acumula progressivamente rumo ao projeto final,
  reforçando a espiral de conteúdo em vez de tópicos isolados.

**Negativas:**

- O professor perde a folga de 30 minutos de intervalo que o acervo da FIAP tem
  disponível para atender aluno individualmente durante a aula.

## ADRs relacionadas

- ADR-002: resolução de turma no cliente
