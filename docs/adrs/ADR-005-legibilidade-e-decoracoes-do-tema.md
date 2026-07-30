# ADR-005: Legibilidade do código projetado e integridade das decorações do tema

**Data:** 30/07/2026
**Status:** Aceita
**Decisores:** Prof. José Romualdo

## Contexto

A revisão do deck da Aula 01, que é o padrão-ouro copiado pelas Aulas 02 a 20,
encontrou três defeitos que não nascem no conteúdo da aula e sim no tema e nos
assets, portanto se multiplicariam por 20 se corrigidos apenas dentro do HTML da
Aula 01:

1. A `uninove-logo.png` era um PNG de fundo branco **opaco**. Como
   `.reveal .slides section > *` dá `z-index: 1` à logo contra `z-index: 0` do
   `.decor-coral`, o branco do PNG pintava por cima do triângulo coral do canto
   superior direito, abrindo um retângulo pálido dentro dele em 17 dos 21 slides.
   O `tools/check_slides.py` não detecta isso, porque o `.decor-coral` tem caixa
   zerada e quem desenha o triângulo é o `::after`.
2. A JetBrains Mono, usada nos blocos de código, funde `--` num traço longo
   único por ligadura. Numa turma de primeiro contato com terminal,
   `git --version` projetado como `git –version` faz o aluno digitar um hífen só
   e o comando falha.
3. O utilitário `pre.code-compact` renderizava a 13,44px e os comentários do
   monokai saíam em `#75715e` sobre `#1e1e1e`, contraste de 3,40:1, abaixo do
   mínimo AA de 4,5:1. É justamente onde o aluno lê o que cada comando faz.

## Decisão

Corrigir os três no tema e no asset, não no deck: gerar a logo com canal alfa,
desligar as ligaduras em todo código do acervo e estabelecer um piso de
legibilidade (corpo e contraste) para os blocos de código compactos. O cartão
branco atrás da logo continua nos slides de fundo escuro.

## Motivações

- Uma correção no tema conserta os 20 decks de uma vez e impede que o defeito
  seja copiado pelas aulas seguintes.
- A logo com alfa resolve a causa-raiz: não há mais fundo opaco para cobrir
  decoração nenhuma, em nenhum canto, em nenhum slide futuro.
- Contraste e corpo de texto projetado são requisito de acessibilidade, não
  preferência estética.

## Riscos conhecidos

- **A extração do alfa poderia deixar franjas, halo ou serrilhado no contorno.**
  - **Mitigação:** o alfa foi derivado do canal mínimo com desmultiplicação
    (`A = (255 - min(R,G,B)) / 227`, sendo 227 o canal mínimo do vermelho da
    marca), e não por remoção binária do branco. Recomposta sobre branco, a logo
    difere da original em no máximo 6/255 num canal, só em pixels de
    antialiasing. Conferido em ampliação de 3x sobre coral, sobre o preto do
    tema e sobre branco: sem franja e sem halo.
- **A logo azul sobre o fundo escuro da capa e do encerramento rende 2,5:1.**
  - **Mitigação:** o cartão branco desses dois slides foi mantido de propósito.
    A transparência resolve o canto dos slides de conteúdo, que é o defeito
    real; ela não torna a marca legível sobre `#12121A`.
- **`pre.code-compact` passou de 0,48em para 0,6em e pode estourar slides que já
  estavam no limite.**
  - **Mitigação:** `tools/check_slides.py` continua obrigatório antes de dar
    qualquer deck por pronto, e é ele que acusa o estouro.

## Consequências

**Positivas:**

- O triângulo coral chega inteiro em todos os slides, e passa a existir um
  verificador por pixel para garantir isso, `tools/check_canto_coral.py`, que é
  o ponto cego declarado do `check_slides.py`.
- Comando de terminal projetado é copiável sem erro de digitação.
- Comentário de código no `code-compact` passou de 3,40:1 para 6,42:1 e de
  13,44px para 16,8px.

**Negativas:**

- Existe agora um segundo validador para rodar, além do `check_slides.py`.
- O tema ficou responsável por um detalhe tipográfico (ligadura) que, em outro
  acervo com outra fonte, seria desnecessário.

## ADRs relacionadas

- ADR-001: migração dos decks para Reveal.js
- ADR-003: compartilhamento com o acervo da FIAP (por que `check_slides.py` é
  symlink e não pode ser editado aqui)
