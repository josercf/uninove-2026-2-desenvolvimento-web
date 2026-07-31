# Laboratório da Aula 03

## Disciplina: Desenvolvimento Web
**Prof. José Romualdo | Uninove, Universidade Nove de Julho**

### Case: Clínica Vida+ (Fase 1, a página inicial em HTML semântico)

Na Aula 02 você entregou `docs/arquitetura.md`, com o caminho da requisição
desenhado e as evidências coletadas no DevTools. Lá ficou claro que o corpo
da resposta que o servidor devolve, no fim das contas, é **um documento
HTML**. Hoje você escreve esse documento: a página inicial do site da
Clínica Vida+, com estrutura semântica completa, validada no W3C, entregue
em uma branch própria e com Pull Request aberto no seu fork.

**Duração:** 60 minutos, individual, dentro dos Ciclos 3 e 4 da aula.

---

## Pré-requisitos

- O fork `uninove-2026-2-clinica-vida` clonado na sua máquina, da Aula 01.
- Git configurado com o seu nome e o seu e-mail.
- VS Code e um navegador.

---

## Passo 1: a branch da funcionalidade (5 min)

A partir desta aula, nenhum código novo entra direto na `main`. Cada
funcionalidade nasce na própria branch.

```bash
cd uninove-2026-2-clinica-vida

git switch main
git pull

git switch -c feature/pagina-inicial
git status          # On branch feature/pagina-inicial
```

Se o `git status` ainda disser `On branch main`, pare e chame o professor.
Todo o trabalho de hoje precisa nascer dentro da branch, senão não haverá o
que revisar no Pull Request.

---

## Passo 2: header, nav e a abertura do main (15 min)

Crie `index.html` na **raiz do repositório**, com o esqueleto completo do
documento (`<!DOCTYPE html>`, `html` com `lang="pt-BR"`, `head` com
`meta charset` e `title`, e `body`). Dentro do `body`:

```html
<body>
  <header>
    <h1>Clínica Vida+</h1>
    <p>Agendamento de consultas em seis especialidades.</p>
  </header>

  <nav>
    <ul>
      <li><a href="#apresentacao">A clínica</a></li>
      <li><a href="#especialidades">Especialidades</a></li>
      <li><a href="#corpo-clinico">Corpo clínico</a></li>
    </ul>
  </nav>

  <main>
    <!-- passo 3 e passo 4 entram aqui -->
  </main>
</body>
```

Um menu é uma **lista de destinos**, por isso o `nav` traz uma `ul` de
links, e não uma sequência de `<a>` soltos.

---

## Passo 3: apresentação e especialidades (15 min)

Dentro do `<main>`, duas seções. Os `id` são o que faz os links do menu
funcionarem, e cada `id` aparece **uma única vez** na página inteira.

```html
<section id="apresentacao">
  <h2>A clínica</h2>
  <p>Dois parágrafos apresentando a Clínica Vida+ e o problema
     que o agendamento por telefone causa hoje.</p>
</section>

<section id="especialidades">
  <h2>Especialidades</h2>
  <ul>
    <li>Cardiologia</li>
    <li>Pediatria</li>
    <li>Dermatologia</li>
  </ul>
</section>
```

No seu entregável são **seis especialidades**, não três. Use `<strong>` ou
`<em>` onde houver importância ou ênfase de verdade, e não para engordar a
letra.

---

## Passo 4: corpo clínico em tabela e rodapé (15 min)

A tabela fecha o `<main>`. O `<footer>` vem **depois** dele, como irmão, e
não dentro.

```html
  <section id="corpo-clinico">
    <h2>Corpo clínico</h2>
    <table>
      <caption>Médicos da Clínica Vida+</caption>
      <thead>
        <tr>
          <th scope="col">Nome</th>
          <th scope="col">CRM</th>
          <th scope="col">Especialidade</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Ana Prado</td>
          <td>CRM-SP 112233</td>
          <td>Cardiologia</td>
        </tr>
      </tbody>
    </table>
  </section>
</main>

<footer>
  <p>Rua das Acácias, 120, São Paulo. Telefone: (11) 4002-8922</p>
</footer>
```

São **pelo menos quatro médicos** na tabela do entregável, cada um com nome,
CRM e especialidade.

---

## Passo 5: validar no W3C (5 min)

1. Abra <https://validator.w3.org/nu> e escolha a aba **Check by file
   upload**.
2. Envie o seu `index.html` e clique em **Check**.
3. Leia cada mensagem: o validador informa a **linha** e a **coluna** do
   problema.
4. Corrija no editor e envie de novo, até a página ficar **sem nenhum
   erro**. Os avisos em amarelo, os *warnings*, não bloqueiam a entrega.
5. Guarde a captura de tela da mensagem verde: ela vai na descrição do seu
   Pull Request.

Erros mais comuns nesta aula:

| O que o validador diz | O que está acontecendo | Como corrigir |
|---|---|---|
| `End tag "div" seen, but there were open elements` | Uma tag ficou aberta dentro de outra | Fechar na ordem inversa da abertura |
| `An "img" element must have an "alt" attribute` | Imagem sem descrição alternativa | Acrescentar `alt`, mesmo que vazio |
| `Element "h2" not allowed as child of element "ul"` | Filho inválido dentro da lista | Dentro de `ul`, só `li` |
| `Duplicate ID "contato"` | Dois elementos com o mesmo `id` | O `id` é único na página inteira |

---

## Passo 6: commit, push e Pull Request (5 min)

```bash
git add index.html
git commit -m "feat: pagina inicial semantica da Clinica Vida+"

git push -u origin feature/pagina-inicial
```

No GitHub, na página do seu fork:

1. Clique em **Compare & pull request**, no aviso que aparece no topo.
2. Confira o destino: da sua `feature/pagina-inicial` para a `main`
   **do seu próprio fork**, e não para o repositório do professor.
3. Escreva um título claro e, na descrição, o que foi feito e a evidência
   da validação no W3C.
4. Clique em **Create pull request**. **Não faça o merge:** o Pull Request
   aberto é o entregável.

---

## Entregável

- `index.html` na raiz do fork, com estrutura semântica completa e sem
  nenhum erro no validador do W3C.
- Tudo na branch `feature/pagina-inicial`, com pelo menos **um commit de
  sua autoria**.
- **Pull Request aberto** no seu fork, da branch para a `main`, com a
  evidência da validação na descrição.

### Critérios de aceitação

| # | Critério | Como o professor confere |
|---|---|---|
| 1 | O trabalho está em uma branch própria | O Pull Request mostra `feature/pagina-inicial` como origem, e a `main` do fork como destino |
| 2 | O documento tem a estrutura mínima do HTML5 | `index.html` abre com `<!DOCTYPE html>` e traz `html` com `lang="pt-BR"`, `head` com `meta charset` e `title`, e `body` |
| 3 | A página é semântica | Existem `header`, `nav`, `main`, pelo menos três `section` e `footer`, e nenhuma `div` fazendo o papel de uma dessas tags |
| 4 | A hierarquia de títulos faz sentido | Um único `h1`, e os `h2` das seções sem pular níveis |
| 5 | O menu é uma lista de links que funcionam | O `nav` traz uma `ul` de `li` com `a`, e cada `href="#..."` encontra o `id` correspondente na página |
| 6 | As especialidades estão em lista | Uma `ul` com **seis** `li`, dentro da seção de especialidades |
| 7 | O corpo clínico está em tabela de dados | `table` com `caption`, `thead`, `tbody` e `th scope="col"`, com pelo menos quatro médicos, cada um com nome, CRM e especialidade |
| 8 | A página é válida | O Nu Html Checker reporta **zero erro**, e a captura de tela está na descrição do Pull Request |
| 9 | O trabalho foi enviado e está em revisão | A branch aparece no GitHub e existe um Pull Request **aberto**, sem merge |

---

## Se algo der errado

- **`fatal: a branch named 'feature/pagina-inicial' already exists`**: a
  branch já foi criada antes. Só troque para ela:
  ```bash
  git switch feature/pagina-inicial
  ```
- **`fatal: The current branch has no upstream branch`**: faltou o `-u` no
  primeiro push. Resolve com:
  ```bash
  git push -u origin feature/pagina-inicial
  ```
- **Os links do menu não rolam a página**: o `href="#especialidades"`
  precisa encontrar um elemento com `id="especialidades"`. Confira se o
  texto depois do `#` é idêntico ao `id`, inclusive maiúsculas, minúsculas
  e acentos. Evite acento em `id`.
- **O acento aparece quebrado no navegador**: falta
  `<meta charset="UTF-8">` no `head`, ou o arquivo foi salvo em outra
  codificação. No VS Code, a codificação aparece na barra inferior e deve
  ser UTF-8.
- **O botão "Compare & pull request" não aparece**: atualize a página do
  fork ou abra a aba **Pull requests** e clique em **New pull request**,
  escolhendo `feature/pagina-inicial` como origem.
- **Você commitou na `main` sem querer**: não apague nada. Crie a branch a
  partir do estado atual e chame o professor:
  ```bash
  git switch -c feature/pagina-inicial
  ```
