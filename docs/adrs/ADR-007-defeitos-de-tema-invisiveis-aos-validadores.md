# ADR-007: Defeitos de tema invisíveis aos validadores

**Data:** 31/07/2026
**Status:** Aceita
**Decisores:** Prof. José Romualdo

## Contexto

A produção do lote das Aulas 02 a 06 rodou cinco construtores em paralelo, cada
um sobre uma aula, e cada um conferiu o próprio deck no navegador além de rodar
os validadores. Três deles, trabalhando isolados e sem se comunicarem,
relataram o **mesmo par de defeitos**. Coincidência tripla em agentes
independentes não é erro de autoria: é defeito do tema, e cada aula nova ia
pagar o mesmo pedágio.

Os dois defeitos têm a mesma assinatura perversa: **passam nos quatro
validadores** e só aparecem na tela. Nenhum estoura os 1280x720 e nenhum
sobrepõe blocos, que é tudo o que `check_slides.py` mede.

### Defeito 1: código cortado silenciosamente

O `reveal.css`, que vem do jsDelivr por CDN, traz
`pre code { max-height: 400px; overflow: auto }`. Num deck que rola, isso é um
recurso: o bloco ganha barra de rolagem. Aqui é um defeito, porque a `section`
tem altura travada e ninguém rola nada em sala. O código simplesmente chega
cortado ao projetor e ao PDF.

E `check_slides.py` não vê, pelo mesmo motivo pelo qual não vê o `.decor-coral`
do ADR-005: quem estoura é o `<code>`, não a caixa do `<pre>`, que continua
dentro dos 720px.

Medido no laboratório do passo 2 da Aula 03, com o `max-height` do `reveal.css`
valendo:

```
max-height=400px  visivel=410px  real=433px  CORTADO=True
```

Vinte e três pixels de código fora da tela, com o validador imprimindo
"OK: nada estourando 1280x720".

### Defeito 2: alternativa de quiz partida pelo flex

`.quiz-slide .quiz-options li` é `display: flex` com `gap: 12px`. Numa
alternativa de texto puro isso é inofensivo: o texto vira um único item
anônimo. Mas **todo elemento inline dentro da alternativa vira um item
separado**, e o `gap` de 12px passa a ser aplicado em volta dele, no lugar onde
deveria haver um espaço normal de palavra.

Medido numa cópia do padrão-ouro, com `<code>git diff</code>` no meio da
alternativa A:

```
alternativa 0:  span "A" x=193 | texto x=231 w=118 | code x=361 w=82 | texto x=455 w=281
alternativa 1:  span "B" x=193 | texto x=231 w=646
```

Três itens onde as outras têm um. Em alternativa longa o estrago é maior,
porque item de flex não quebra linha sem `flex-wrap`.

## Decisão

Corrigir os dois no tema, `aulas-1sem/assets/css/uninove-theme.css`, e não
aula a aula:

1. `.reveal pre code { max-height: none; }`
2. `.quiz-slide .quiz-options .option-text { flex: 1; min-width: 0; }`, com a
   convenção de markup correspondente: **alternativa que contenha qualquer
   elemento inline precisa ter o texto envolvido em
   `<span class="option-text">`.**

## Motivações

- **Trocar falha silenciosa por falha ruidosa.** Zerado o `max-height`, o bloco
  de código cresce até a altura real; se não couber, estoura a `section` e o
  `check_slides.py` acusa. É exatamente o que se quer de um validador. A
  alternativa, manter o corte, é preferir que o defeito chegue à sala em vez de
  ao terminal.
- **Correção no tema, não na aula.** A Aula 03 já tinha contornado o defeito 1
  com `style="max-height:none;"` inline em três blocos. Contorno inline resolve
  um deck e deixa os dezenove seguintes para descobrirem o mesmo problema
  sozinhos. Os três contornos foram removidos depois da correção no tema.
- **Retrocompatibilidade.** `.option-text` é aditivo: alternativa de texto puro
  continua funcionando sem `span` nenhum, como nas Aulas 01, 02 e 04. Só quem
  precisa de markup inline paga o custo do `span`.
- **`min-width: 0` junto com `flex: 1`.** Sem ele, um item de flex não encolhe
  abaixo do próprio conteúdo mínimo, e uma alternativa com trecho longo de
  código voltaria a vazar.

## Riscos conhecidos

| Risco | Mitigação |
|---|---|
| Um bloco de código muito longo agora estoura a `section` em vez de rolar | É o comportamento desejado, e `check_slides.py` pega antes da sala. A saída é dividir o slide ou usar `code-compact`, nunca reduzir fonte abaixo de 0,62em (ADR-005) |
| Autor esquecer o `.option-text` numa alternativa com `<code>` | Nenhum validador pega hoje. Documentado no `SKILL.md` e nos dois agentes; candidato a oitava checagem do `check_decks.py` |
| A correção do `max-height` depende do tema local vencer o `reveal.css` da CDN | O `uninove-theme.css` é carregado depois do `reveal.css` no `<head>`, e a especificidade `.reveal pre code` é igual à da regra original, então a ordem resolve. Conferido nos seis decks |

## Consequências

**Positivas.** Os seis decks existentes passam nos quatro validadores com a
correção aplicada, e a Aula 03 ficou mais limpa, sem os três contornos inline.
As Aulas 05 e 06 puderam **restaurar** o `<code>` que tinham sido obrigadas a
remover das alternativas do quiz, recuperando fidelidade tipográfica em
`type` e `form`. O acervo ganhou o vocabulário `.option-text`.

**Negativas.** Mais uma convenção de markup que o autor precisa lembrar, sem
validador que a cobre. E o acervo acumula uma segunda entrada na lista de
"lugares onde o validador diz OK e a tela discorda", ao lado do `.decor-coral`
do ADR-005. Essa lista merece virar checagem automatizada antes de crescer para
três.

## ADRs relacionadas

- **ADR-005**, legibilidade do código projetado e integridade das decorações do
  tema. É a mesma família de problema: o validador mede caixa do DOM, e há
  defeitos que só existem no pixel renderizado. O `.decor-coral` de lá ganhou
  validador dedicado, `tools/check_canto_coral.py`; os dois defeitos daqui
  ainda não têm.
- **ADR-001**, migração dos decks para Reveal.js. O defeito 1 nasce de uma
  regra do próprio `reveal.css`, que é a consequência assumida de carregar o
  framework por CDN em vez de manter um fork.
