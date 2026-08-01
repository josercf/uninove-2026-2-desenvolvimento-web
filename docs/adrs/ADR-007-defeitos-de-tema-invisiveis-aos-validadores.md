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

### Defeito 3: título de exercício partido pelo flex (achado no Módulo 3)

`.exercise-slide .exercise-container h3` era `display: flex` com `gap: 8px`,
exatamente a mesma armadilha do defeito 2, em outro seletor. Um `<code>` no
meio do título do exercício vira item de flex próprio e ganha 8px de buraco
onde deveria haver um espaço de palavra.

Foi encontrado durante a produção do Módulo 3, por dois autores independentes,
e estava **vivo em produção**: a Aula 09, já publicada, trazia
`Em <code>ClinicaVida.Web/Models</code>` com o buraco. Medido antes da
correção:

```
display=flex  gap=8px
  texto x= 90 w= 31  "Em"          -> termina em 121
  code  x=129 w=314  "ClinicaVida.Web/Models"
```

A oitava checagem do `check_decks.py`, criada para o defeito 2, **não pegava
este**, porque só inspeciona `li` de `.quiz-options`.

## Decisão

Corrigir os três no tema, `aulas-1sem/assets/css/uninove-theme.css`, e não
aula a aula:

1. `.reveal pre code { max-height: none; }`
2. `.quiz-slide .quiz-options .option-text { flex: 1; min-width: 0; }`, com a
   convenção de markup correspondente: **alternativa que contenha qualquer
   elemento inline precisa ter o texto envolvido em
   `<span class="option-text">`.**
3. `.exercise-slide .exercise-container h3` deixa de ser `display: flex` e
   volta a ser bloco.

**Repare que as correções 2 e 3 são de naturezas diferentes, de propósito.** No
quiz, a `li` precisa de flex de verdade, porque a letra da alternativa é um
círculo alinhado ao texto: ali o flex serve a alguma coisa, e a saída foi dar
ao texto um elemento próprio, ao custo de uma convenção que o autor precisa
lembrar. No título do exercício não havia nada a alinhar, nenhum deck do acervo
põe elemento antes dele, e o flex não servia a nada: ali dá para **remover a
armadilha na origem**, sem convenção nova e sem checagem nova.

Preferir a correção que não cria regra para o autor lembrar, sempre que o
layout permitir. Regra documentada é regra que alguém esquece; foi o que
aconteceu três vezes com o defeito 2 antes de virar checagem.

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
| Autor esquecer o `.option-text` numa alternativa com `<code>` | Virou a **oitava checagem** do `check_decks.py`, provada por defeito induzido em `<code>`, `<strong>` e `<br>` soltos, mais controle negativo |
| **Corte horizontal continua silencioso.** Zerar o `max-height` resolveu a altura; o `overflow-x` do `pre code` segue cortando linha longa sem estourar a `section` | Nenhum validador cobre. Virou etapa de lote: medir `scrollWidth` contra `clientWidth` em todo `pre code` de todos os decks. Zero cortes nos 17 decks atuais |
| Existir um quarto seletor com a mesma armadilha de flex, ainda não descoberto | O padrão a procurar é `display: flex` com `gap` em elemento que contém **texto corrido**. Ao criar bloco novo no tema, perguntar se ele vai receber texto com `<code>` no meio |
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
