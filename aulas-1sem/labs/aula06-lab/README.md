# Laboratório da Aula 06

## Disciplina: Desenvolvimento Web
**Prof. José Romualdo | Uninove, Universidade Nove de Julho**

### Case: Clínica Vida+ (Fase 5, comportamento no navegador)

Na Aula 05 você entregou o `agendamento.html` responsivo, com Grid, media
queries, o formulário completo do paciente e da consulta, e a validação
nativa do navegador ligada nos campos obrigatórios. Ela funciona, mas para
onde a regra de negócio começa: o HTML sabe dizer que um campo não pode
ficar vazio, e não sabe dizer que **a data da consulta precisa estar no
futuro**.

Hoje o site ganha comportamento. O laboratório cria
`assets/js/agendamento.js`, intercepta o envio do formulário, valida o que o
HTML não expressa, mostra o resumo do agendamento na própria tela e
acrescenta um filtro de busca na página inicial. É o último passo do
Módulo 1: ao fim desta aula, o front-end da Clínica Vida+ está de pé.

**Duração:** 60 minutos, individual, nos Ciclos 3 e 4.

---

## Pré-requisitos

- O fork de `josercf/uninove-2026-2-clinica-vida` clonado na sua máquina.
- O entregável da Aula 05 na `main`: `agendamento.html` responsivo, com o
  formulário completo e `assets/css/site.css` aplicado.
- VS Code e um navegador com DevTools (`F12`).

---

## Passo 1: a branch e o arquivo (8 min)

```bash
git switch main && git pull
git switch -c feature/js-agendamento
mkdir -p assets/js
```

Crie `assets/js/agendamento.js` e ligue o script no fim do `<head>` do
`agendamento.html`:

```html
<script src="assets/js/agendamento.js" defer></script>
```

O `defer` faz o navegador ler o HTML inteiro antes de executar o script.
Sem ele, o código roda antes de os campos existirem e `querySelector`
devolve `null`.

Escreva no arquivo a primeira linha e confirme, no console do navegador,
que ela aparece:

```javascript
console.log('agendamento.js carregado');
```

---

## Passo 2: interceptar o submit (10 min)

Antes do JavaScript, o HTML precisa oferecer pontos de acesso. Dê um `id`
ao formulário, a cada campo que o código vai ler e a cada `span` onde a
mensagem de erro vai aparecer:

```html
<form id="form-agendamento" action="#" method="post">
  <label for="nome">Nome completo</label>
  <input type="text" id="nome" name="nome" required>

  <label for="cpf">CPF</label>
  <input type="text" id="cpf" name="cpf" required>
  <span class="aviso" id="aviso-cpf"></span>

  <label for="data">Data da consulta</label>
  <input type="date" id="data" name="data" required>
  <span class="aviso" id="aviso-data"></span>

  <label for="horario">Horário</label>
  <input type="time" id="horario" name="horario" required>
  <span class="aviso" id="aviso-horario"></span>

  <p id="resumo-agendamento" class="oculto"></p>
</form>
```

Acrescente ao `assets/css/site.css`:

```css
.oculto { display: none; }
.aviso { color: #C84B31; font-size: 0.9rem; }
.campo-invalido { border-color: #C84B31; }
```

E no `agendamento.js`:

```javascript
const form = document.querySelector('#form-agendamento');

form.addEventListener('submit', (event) => {
  event.preventDefault();
  console.log('submit interceptado, a página não recarregou');
});
```

Envie o formulário e olhe a barra de endereços: ela **não** mudou e a
página **não** piscou. Sem `event.preventDefault()`, o comportamento padrão
do navegador é enviar o formulário e recarregar a página, apagando tudo o
que o seu código escreveu na tela.

---

## Passo 3: a validação do CPF (13 min)

A primeira regra que o HTML não expressa. A mensagem aparece **ao lado do
campo**, nunca em um `alert`.

```javascript
const cpf = document.querySelector('#cpf');
const avisoCpf = document.querySelector('#aviso-cpf');

function validarCpf(campo, aviso) {
  const digitos = campo.value.replace(/\D/g, '');   // descarta ponto e traço
  const valido = digitos.length === 11;
  aviso.textContent = valido ? '' : 'O CPF precisa ter 11 dígitos.';
  campo.classList.toggle('campo-invalido', !valido);
  return valido;
}
```

Repare no **contrato da função**: ela recebe o campo e o `span` de aviso,
escreve a mensagem e devolve `true` ou `false`. As duas validações do Passo
4 seguem exatamente esse mesmo contrato, e é isso que permite juntá-las no
Passo 5.

---

## Passo 4: data futura e horário no expediente (10 min)

Ciclo 4, sozinho. As duas regras que nenhum atributo do HTML consegue
declarar. A Clínica Vida+ atende das 07h às 19h.

```javascript
function validarData(campo, aviso) {
  const hoje = new Date();
  hoje.setHours(0, 0, 0, 0);
  const escolhida = new Date(`${campo.value}T00:00:00`);   // evita o fuso UTC
  const valida = escolhida > hoje;
  aviso.textContent = valida ? '' : 'A consulta precisa ser em uma data futura.';
  return valida;
}

function validarHorario(campo, aviso) {
  const hora = Number(campo.value.split(':')[0]);
  const valida = hora >= 7 && hora < 19;
  aviso.textContent = valida ? '' : 'A Clínica Vida+ atende das 07h às 19h.';
  return valida;
}
```

O `T00:00:00` no fim da string existe por um motivo: `new Date('2026-09-10')`
é interpretado como UTC e vira 09/09 no fuso de São Paulo. Com a hora
explícita, a data é lida no fuso local.

Teste os dois extremos: uma data de **ontem** e o horário **21h00**. Cada
mensagem precisa aparecer ao lado do seu campo, com a página parada.

---

## Passo 5: o resumo do agendamento na tela (10 min)

Todas as regras precisam rodar, e não só até a primeira falhar: o paciente
merece ver os erros de uma vez.

```javascript
const nome = document.querySelector('#nome');
const especialidade = document.querySelector('#especialidade');
const data = document.querySelector('#data');
const horario = document.querySelector('#horario');
const avisoData = document.querySelector('#aviso-data');
const avisoHorario = document.querySelector('#aviso-horario');
const resumo = document.querySelector('#resumo-agendamento');

form.addEventListener('submit', (event) => {
  event.preventDefault();

  const resultados = [
    validarCpf(cpf, avisoCpf),
    validarData(data, avisoData),
    validarHorario(horario, avisoHorario),
  ];
  if (resultados.includes(false)) return;   // alguma regra falhou

  resumo.textContent =
    `${nome.value} agendou ${especialidade.value} em ${data.value} às ${horario.value}.`;
  resumo.classList.remove('oculto');
});
```

Use `textContent`, e não `innerHTML`: o que o paciente digitou é texto, e
tratar texto do usuário como HTML é a porta de entrada de injeção de
código.

---

## Passo 6: o filtro de especialidades (9 min)

Na página inicial, um campo de busca que filtra os cards de especialidade
enquanto o paciente digita. Aqui o evento é `input`, que dispara a cada
tecla, e não `submit`.

No `index.html`, acrescente o campo de busca logo antes da lista de
especialidades. A lista em si você não precisa mexer: ela já é o
`<ul class="lista-especialidades">` que você estilizou na Aula 04, e é dele
que o filtro vai partir.

```html
<label for="busca-especialidade">Buscar especialidade</label>
<input type="search" id="busca-especialidade" placeholder="Cardiologia, Pediatria...">
```

No `assets/js/agendamento.js` (ou em um `assets/js/home.js`, se preferir
separar):

```javascript
const busca = document.querySelector('#busca-especialidade');
const cards = document.querySelectorAll('.lista-especialidades li');

busca.addEventListener('input', () => {
  const termo = busca.value.trim().toLowerCase();
  cards.forEach((card) => {
    const nome = card.textContent.toLowerCase();
    card.classList.toggle('oculto', !nome.includes(termo));
  });
});
```

Campo vazio significa `termo` vazio, e `includes('')` é sempre `true`:
todos os cards voltam sozinhos. Regra bem escrita não precisa de caso
especial.

---

## Commit e push

```bash
git add assets/js/agendamento.js agendamento.html index.html assets/css/site.css
git commit -m "feat: validacao e filtro em JavaScript no agendamento"
git push -u origin feature/js-agendamento
```

---

## Entregável

`assets/js/agendamento.js` com validação e filtro funcionando, na branch
`feature/js-agendamento`, commitado e enviado ao seu fork. Especificamente:

- **1** arquivo `assets/js/agendamento.js`, ligado ao `agendamento.html` com
  `defer`.
- **3** regras de negócio validadas: CPF com 11 dígitos, data no futuro e
  horário entre 07h e 19h.
- **1** resumo do agendamento exibido na tela em caso de sucesso.
- **1** filtro de especialidades funcionando na página inicial.

### Critérios de aceitação

| # | Critério | Como o professor confere |
|---|---|---|
| 1 | O script está ligado com `defer` | O `agendamento.html` traz `<script src="assets/js/agendamento.js" defer></script>` e o console não acusa erro de elemento nulo |
| 2 | O `submit` é interceptado | Ao enviar o formulário, a página não recarrega e a barra de endereços não muda |
| 3 | O CPF é validado | CPF com menos de 11 dígitos exibe a mensagem ao lado do campo e o envio é interrompido |
| 4 | A data é validada como futura | Uma data de ontem exibe a mensagem de data futura e o envio é interrompido |
| 5 | O horário respeita o expediente | O horário 21h00 exibe a mensagem das 07h às 19h e o envio é interrompido |
| 6 | O resumo aparece em caso de sucesso | Com todos os campos válidos, o bloco `#resumo-agendamento` deixa de estar oculto e mostra nome, especialidade, data e horário |
| 7 | O filtro de especialidades funciona | Digitar "car" na página inicial deixa apenas os cards que contêm o termo; apagar o campo traz todos de volta |
| 8 | O console está limpo | Nenhum erro em vermelho no console durante a navegação e o envio |
| 9 | O trabalho foi enviado | A branch `feature/js-agendamento` aparece no seu fork no GitHub, com o commit de sua autoria |

---

## Se algo der errado

- **`Cannot read properties of null (reading 'addEventListener')`**: o
  `querySelector` não encontrou o elemento e devolveu `null`. As duas causas
  comuns são o `id` escrito diferente no HTML e no JavaScript, e o script
  ligado sem `defer`, rodando antes de o campo existir. Confira o `id` e o
  atributo:
  ```html
  <script src="assets/js/agendamento.js" defer></script>
  ```
- **A página recarrega ao enviar o formulário**: falta `event.preventDefault()`
  como primeira linha do tratador de `submit`, ou o tratador foi registrado
  no botão, com `click`, e não no `form`, com `submit`.
- **A data de hoje é recusada como passada**: a comparação foi feita sem
  zerar as horas do `hoje`, ou a data foi montada com
  `new Date(campo.value)`, que é lida como UTC. Use as duas linhas do Passo
  4, `setHours(0, 0, 0, 0)` e o sufixo `T00:00:00`.
- **O filtro esconde tudo quando o campo está vazio**: a condição está
  invertida. `classList.toggle('oculto', !nome.includes(termo))` esconde
  quando o nome **não** contém o termo.
- **A mensagem aparece e some sozinha**: o `span` de aviso está dentro de um
  elemento que o navegador reconstrói, ou o formulário está sendo enviado
  mesmo assim. Volte ao Passo 2 e confirme a interceptação.
