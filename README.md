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
