# Laboratório da Aula 04

## Disciplina: Desenvolvimento Web
**Prof. José Romualdo | Uninove, Universidade Nove de Julho**

### Case: Clínica Vida+ (Fase 2, identidade visual da página inicial)

Na Aula 03 você entregou o `index.html` semântico da Clínica Vida+, validado
no W3C, na branch `feature/pagina-inicial`, com Pull Request aberto no seu
fork. Hoje essa mesma página ganha identidade visual: uma folha de estilos
externa, a paleta e a tipografia da clínica em variáveis, o cabeçalho e o
menu estilizados, as especialidades em cards com Flexbox, a tabela do corpo
clínico formatada e o rodapé.

**Nenhuma tag muda de significado.** O HTML cuida do significado, o CSS cuida
da apresentação: é essa divisão que o laboratório de hoje coloca em prática.

**Duração:** 60 minutos. Passos 1 a 3 guiados com o professor, passos 4 e 5
individuais.

---

## Pré-requisitos

- O fork de `josercf/uninove-2026-2-clinica-vida` clonado na sua máquina.
- O `index.html` da Aula 03 já integrado à `main` do seu fork.
- Git configurado e VS Code.
- Um navegador com o inspetor de elementos.

> **Sobre os nomes de classe.** Os seletores deste roteiro usam as tags
> semânticas que você escreveu na Aula 03 (`header`, `nav`, `main`, `table`,
> `footer`) e só duas classes novas, criadas hoje. Se a sua marcação usou
> outros nomes, ajuste os seletores: o critério de aceitação é o resultado na
> tela, não o nome escolhido.

---

## Passo 1: a branch e a folha de estilos (10 min)

Confirme que o Pull Request da Aula 03 já entrou na `main` do seu fork, e só
então abra a branch de hoje.

```bash
git switch main
git pull
git switch -c feature/estilo-inicial
```

Crie a pasta `assets/css` e, dentro dela, o arquivo `site.css`. Ligue a folha
ao documento, dentro do `<head>` do `index.html`:

```html
<link rel="stylesheet" href="assets/css/site.css">
```

Antes de escrever qualquer estilo de verdade, **prove que a ligação
funcionou**. Ponha esta única regra no `site.css` e recarregue a página:

```css
body { background-color: #F4F7F6; }
```

Se o fundo não mudar, o caminho do `href` está errado e não adianta seguir.

---

## Passo 2: paleta, reset e tipografia base (10 min)

A ordem importa: variáveis, reset e base do `body`, antes de qualquer estilo
de componente.

```css
:root {
  --vida-primaria:   #0B6E75;   /* verde-azulado do logotipo  */
  --vida-secundaria: #2E9E7E;   /* confirmação de agendamento */
  --vida-destaque:   #E4572E;   /* chamada para ação          */
  --vida-fundo:      #F4F7F6;
  --vida-texto:      #1F2A30;
  --vida-borda:      #D6E2E0;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  font-family: 'Segoe UI', Arial, sans-serif;
  font-size: 1rem;
  line-height: 1.6;
  color: var(--vida-texto);
  background-color: var(--vida-fundo);
}
```

A `color` e a `font-family` declaradas no `body` descem por herança para a
página inteira, e não se repetem em nenhuma outra regra. O
`box-sizing: border-box` faz o `width` passar a valer a caixa inteira, borda e
padding inclusive: é o comportamento que o resto do roteiro assume.

---

## Passo 3: cabeçalho e menu (15 min)

O menu é a primeira aplicação real de Flexbox no seu projeto.

```css
header {
  background-color: var(--vida-primaria);
  color: #FFFFFF;
  padding: 24px 32px;
}

header h1 { margin: 0; font-size: 1.8rem; }

nav ul {
  display: flex;                 /* os itens do menu, lado a lado */
  gap: 24px;
  list-style: none;
  margin: 12px 0 0 0;
  padding: 0;
}

nav a { color: #FFFFFF; text-decoration: none; font-weight: 600; }
```

**Checkpoint em sala:** o cabeçalho precisa estar no verde-azulado da clínica
e o menu, em uma única linha horizontal, sem os marcadores de lista.

---

## Passo 4: as especialidades viram cards (15 min)

A partir daqui você trabalha sozinho, com o professor circulando pela sala.

Acrescente `class="lista-especialidades"` ao `<ul>` das especialidades e
escreva as duas regras abaixo. Repare na divisão de papéis: o **contêiner**
decide o arranjo do conjunto, o **item** decide a própria caixa.

```css
.lista-especialidades {          /* o contêiner: decide o arranjo do conjunto */
  display: flex;
  flex-wrap: wrap;               /* deixa a fileira quebrar em tela estreita  */
  gap: 20px;                     /* espaço entre os cards, sem margem         */
  justify-content: center;       /* centraliza a fileira no eixo principal    */
  list-style: none;
  padding: 0;
}

.lista-especialidades li {       /* o item: decide a própria caixa            */
  width: 260px;
  padding: 20px;
  background-color: #FFFFFF;
  border-left: 4px solid var(--vida-secundaria);
  border-radius: 8px;
}
```

O que precisa acontecer na tela:

1. As especialidades ficam lado a lado, em cards de largura igual, sem
   marcador de lista.
2. Existe um espaço regular entre os cards, criado por `gap` e não por
   margem.
3. Todos os cards terminam na mesma altura, mesmo com textos de tamanhos
   diferentes, por causa do `align-items: stretch` que é o padrão.
4. Ao estreitar a janela, a fileira quebra em uma segunda linha, por causa do
   `flex-wrap`.

Abra o inspetor do navegador, selecione um card e olhe o diagrama do box model
no painel lateral: ele mostra, em números, o conteúdo, o padding, a borda e a
margem daquela caixa.

---

## Passo 5: tabela, rodapé e entrega (10 min)

```css
table { width: 100%; border-collapse: collapse; background-color: #FFFFFF; }

th {
  background-color: var(--vida-primaria);
  color: #FFFFFF;
  text-align: left;
  padding: 12px 16px;
}

td { padding: 12px 16px; border-bottom: 1px solid var(--vida-borda); }

footer {
  background-color: var(--vida-texto);
  color: #FFFFFF;
  padding: 24px 32px;
  margin-top: 40px;
}
```

Confira o resultado no navegador a cada bloco de regras, e só então comite e
envie:

```bash
git add assets/css/site.css index.html
git commit -m "feat: identidade visual da página inicial com CSS"
git push -u origin feature/estilo-inicial
```

---

## Entregável

- `assets/css/site.css` ligado ao `index.html` por `<link>`, com a página
  inicial da Clínica Vida+ estilizada.
- Commitado e enviado na branch `feature/estilo-inicial` do seu fork.

### Critérios de aceitação

| # | Critério | Como o professor confere |
|---|---|---|
| 1 | A folha de estilos é externa e está ligada ao documento | Existe `assets/css/site.css` no repositório e uma linha `<link rel="stylesheet" href="assets/css/site.css">` no `<head>` do `index.html`. Nenhum atributo `style` e nenhum bloco `<style>` sobrou no HTML |
| 2 | A paleta da clínica está em variáveis | O `site.css` declara as cores em `:root` com `--vida-` e as consome com `var()`, em vez de repetir o hexadecimal em cada regra |
| 3 | Existe uma base tipográfica herdada | O `body` declara `font-family`, `line-height` e `color`, e essas propriedades não se repetem nas regras seguintes |
| 4 | O reset de caixa está aplicado | A folha tem `* { box-sizing: border-box; }` antes das regras de componente |
| 5 | O cabeçalho e o menu estão estilizados | O `header` usa a cor primária da clínica e o `nav ul` usa `display: flex`, sem marcador de lista, em uma única linha |
| 6 | As especialidades são uma fileira de cards com Flexbox | O `ul` das especialidades usa `display: flex`, `gap` e `flex-wrap`, os cards têm largura e padding próprios, e ao estreitar a janela a fileira quebra em outra linha |
| 7 | A tabela do corpo clínico e o rodapé estão formatados | A tabela usa `border-collapse: collapse` com cabeçalho na cor primária, e o `footer` tem fundo, cor de texto e padding próprios |
| 8 | O HTML continua semântico e válido | O `index.html` passa no validador do W3C sem erros, e nenhuma tag semântica foi trocada por `div` para facilitar a estilização |
| 9 | O trabalho foi enviado | A branch `feature/estilo-inicial` aparece no GitHub com o commit de sua autoria |

---

## Se algo der errado

- **O CSS não faz efeito nenhum.** Quase sempre é o caminho do `href`. Abra o
  DevTools, aba *Network*, e recarregue: se `site.css` aparecer com status
  404, o caminho está errado. Lembre que o caminho é relativo ao
  `index.html`.
- **Uma regra sua é ignorada, mas o navegador mostra outra no lugar.** É
  disputa de especificidade. Selecione o elemento no inspetor: a regra
  perdedora aparece riscada, e a vencedora está logo acima dela. Uma classe
  vence qualquer quantidade de seletores de tipo.
- **Os cards ficam maiores do que o esperado.** Falta o
  `* { box-sizing: border-box; }` do Passo 2. Sem ele, `width: 260px` mais
  `padding: 20px` dos dois lados ocupa 300px na tela.
- **O `gap` não separa os cards.** O `gap` só funciona no contêiner flex.
  Confirme que o `display: flex` está no `ul` e não no `li`.
- **O menu continua com os pontinhos da lista.** Falta `list-style: none` no
  `nav ul`, ou a regra está no `li` em vez de estar no `ul`.
- **`error: pathspec 'main' did not match`**: você ainda está numa branch
  antiga e a `main` local não existe com esse nome. Confira com
  `git branch -a` antes de repetir o Passo 1.
