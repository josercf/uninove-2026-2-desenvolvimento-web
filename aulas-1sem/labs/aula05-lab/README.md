# Laboratório da Aula 05

## Disciplina: Desenvolvimento Web
**Prof. José Romualdo | Uninove, Universidade Nove de Julho**

### Case: Clínica Vida+ (Fase 3, a página de agendamento)

Na Aula 04 você entregou `assets/css/site.css` aplicado ao `index.html`, com a
página inicial da Clínica Vida+ estilizada. Hoje o site ganha a primeira página
que **recebe dados**: o agendamento de consulta, aquilo que na clínica ainda é
um telefonema anotado em papel.

O laboratório de hoje faz três coisas sobre esse mesmo repositório: cria
`agendamento.html` com um formulário completo e acessível, organiza os campos
com CSS Grid e adapta o layout a três larguras de tela na abordagem mobile
first.

**Duração:** 60 minutos. Passos 1 e 2 guiados com o professor, passos 3 e 4
individuais.

---

## Pré-requisitos

- O fork de `josercf/uninove-2026-2-clinica-vida` clonado na sua máquina.
- O entregável da Aula 04 commitado: `index.html` estilizado por
  `assets/css/site.css`.
- VS Code e um navegador com DevTools.

---

## Passo 1: a branch e o esqueleto da página (10 min)

```bash
git switch main
git pull
git switch -c feature/agendamento
git branch              # a branch atual aparece com um asterisco
```

Crie `agendamento.html` na raiz do repositório, copiando do `index.html` o
`<head>`, o cabeçalho e o rodapé. A página precisa continuar sendo o mesmo
site: mesmo logotipo, mesmo menu, mesmo `site.css`.

Acrescente o link **Agendar consulta** no menu de navegação das duas páginas,
apontando para `agendamento.html`.

---

## Passo 2: os dados do paciente (20 min)

Cinco campos, cada um com o seu `label` ligado por `for` ao `id` do campo, e
cada um com o seu `name`, porque **só o que tem `name` é enviado**.

```html
<form class="form-agendamento" action="/agendamento" method="post">
  <fieldset>
    <legend>Dados do paciente</legend>
    <div class="form-grid">
      <div class="campo">
        <label for="nome">Nome completo</label>
        <input type="text" id="nome" name="nome" minlength="5" required>
      </div>
      <div class="campo">
        <label for="cpf">CPF</label>
        <input type="text" id="cpf" name="cpf"
               placeholder="000.000.000-00"
               pattern="\d{3}\.\d{3}\.\d{3}-\d{2}" required>
      </div>
      <div class="campo">
        <label for="nascimento">Data de nascimento</label>
        <input type="date" id="nascimento" name="nascimento" required>
      </div>
      <div class="campo">
        <label for="telefone">Telefone</label>
        <input type="tel" id="telefone" name="telefone" required>
      </div>
      <div class="campo">
        <label for="email">E-mail</label>
        <input type="email" id="email" name="email" required>
      </div>
    </div>
  </fieldset>
```

Repare na escolha de cada tipo: o CPF é `text` com `pattern`, e não `number`,
porque tem pontuação e pode começar com zero; o telefone é `tel` para abrir o
teclado numérico no celular sem impor um formato de país.

---

## Passo 3: os dados da consulta (15 min)

Agora sozinho. Especialidade e médico em `select`, data em `date`, horário em
`time` e observações em `textarea`.

```html
  <fieldset>
    <legend>Dados da consulta</legend>
    <div class="form-grid">
      <div class="campo">
        <label for="especialidade">Especialidade</label>
        <select id="especialidade" name="especialidade" required>
          <option value="">Selecione</option>
          <option value="cardiologia">Cardiologia</option>
          <option value="pediatria">Pediatria</option>
          <option value="ortopedia">Ortopedia</option>
        </select>
      </div>
      <div class="campo">
        <label for="medico">Médico</label>
        <select id="medico" name="medico" required>
          <option value="">Selecione</option>
        </select>
      </div>
      <div class="campo">
        <label for="data">Data da consulta</label>
        <input type="date" id="data" name="data" min="2026-09-01" required>
      </div>
      <div class="campo">
        <label for="horario">Horário</label>
        <input type="time" id="horario" name="horario" min="08:00" max="18:00" required>
      </div>
      <div class="campo campo-largo">
        <label for="observacoes">Observações</label>
        <textarea id="observacoes" name="observacoes" rows="3" maxlength="300"></textarea>
      </div>
    </div>
  </fieldset>

  <button type="submit">Agendar consulta</button>
</form>
```

O `<option value="">Selecione</option>` existe por causa do `required`: sem uma
opção vazia como primeira, o `select` já nasce preenchido e a validação nunca
dispara.

---

## Passo 4: Grid responsivo, validação e envio (15 min)

No `assets/css/site.css`, acrescente a grade do formulário na ordem mobile
first: a regra base é a de uma coluna, e cada media query **acrescenta**
colunas.

```css
.form-grid {                 /* base: o celular, uma coluna */
  display: grid;
  grid-template-columns: 1fr;
  gap: 18px 24px;
}

.campo { display: flex; flex-direction: column; gap: 6px; }
.campo-largo { grid-column: 1 / -1; }   /* ocupa a linha inteira */

.campo input:focus,
.campo select:focus,
.campo textarea:focus { outline: 3px solid #C84B31; }

@media (min-width: 640px) {
  .form-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (min-width: 1024px) {
  .form-grid { grid-template-columns: repeat(3, 1fr); }
}
```

Depois:

1. Confira que os campos sem os quais a recepção não consegue agendar estão
   marcados como `required`.
2. Tente enviar o formulário vazio e leia a mensagem que o navegador exibe
   sozinho. Nenhuma linha de JavaScript foi escrita para isso.
3. Teste em 360px, 768px e 1200px no modo responsivo do DevTools.

```bash
git add agendamento.html index.html assets/css/site.css
git commit -m "feat: pagina de agendamento com formulario responsivo"
git push -u origin feature/agendamento
```

---

## Entregável

`agendamento.html` responsivo, com o formulário completo (dados do paciente e
dados da consulta) e a validação nativa funcionando, commitado e enviado na
branch `feature/agendamento` do seu fork.

### Critérios de aceitação

| # | Critério | Como o professor confere |
|---|---|---|
| 1 | A página existe e pertence ao site | `agendamento.html` abre com o mesmo cabeçalho, menu e rodapé do `index.html`, e o menu das duas páginas tem o link **Agendar consulta** |
| 2 | Os dados do paciente estão completos | O formulário tem nome, CPF, data de nascimento, telefone e e-mail, cada um com o tipo de campo adequado |
| 3 | Os dados da consulta estão completos | O formulário tem especialidade e médico em `select`, data em `date`, horário em `time` e observações em `textarea` |
| 4 | Todo campo tem rótulo associado | Cada `label` tem `for` igual ao `id` do campo, e clicar no texto do rótulo coloca o cursor no campo |
| 5 | Os campos estão agrupados | Existem dois `fieldset` com `legend`: dados do paciente e dados da consulta |
| 6 | A validação nativa funciona | Enviar o formulário vazio é bloqueado pelo navegador, com mensagem no primeiro campo obrigatório |
| 7 | O layout responde em três larguras | Em 360px o formulário fica em uma coluna, em 768px em duas e em 1200px em três, usando `grid-template-columns` e media queries com `min-width` |
| 8 | O trabalho foi enviado | A branch `feature/agendamento` aparece no GitHub com o commit de sua autoria |

---

## Se algo der errado

- **O formulário envia mesmo com campo vazio**: o campo provavelmente está sem
  `required`, ou o `select` não tem uma primeira opção com `value=""`. Sem essa
  opção vazia o `select` já nasce válido.
- **Clicar no rótulo não foca o campo**: o `for` do `label` não bate com o `id`
  do campo. Os dois precisam ser idênticos, incluindo maiúsculas e minúsculas.
- **O layout não muda de colunas ao estreitar a janela**: confira se as media
  queries vêm **depois** da regra base no arquivo. Como as duas têm a mesma
  especificidade, quem vier por último vence, e uma media query escrita antes
  da regra base é desfeita por ela.
- **Um campo ocupa a linha inteira sem querer**: a classe `campo-largo` está
  aplicada onde não deveria. Ela existe só para as observações.
- **O CPF nunca é aceito**: o `pattern` exige a pontuação
  (`000.000.000-00`). Ou o usuário digita com pontos e traço, ou o `pattern`
  precisa ser trocado por `\d{11}`. Escolha um dos dois e mantenha o
  `placeholder` coerente com a escolha.
