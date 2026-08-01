# Laboratório da Aula 14

## Disciplina: Desenvolvimento Web
**Prof. José Romualdo | Uninove, Universidade Nove de Julho**

### Case: Clínica Vida+ (Fase 13, os dados que chegam durante o uso)

Na Aula 13 você entregou o agendamento em duas etapas usando a sessão do
ASP.NET Core, mais o cookie com a unidade preferida da clínica. O fluxo
funciona, e cobra um preço: **cada escolha do usuário custa um envio de
formulário e uma página inteira de volta**. A tela pisca, a rolagem retorna ao
topo e, para descobrir se há horário livre, é preciso avançar de tela.

Hoje isso muda. O laboratório cria duas actions que devolvem **JSON** a partir
do banco, `MedicosPorEspecialidade` e `HorariosDisponiveis`, e escreve o
JavaScript que consome as duas com `fetch`, `async` e `await`, redesenhando
apenas o pedaço da página que precisa mudar. Nada de recarregar.

O JavaScript é o mesmo da Aula 06: `addEventListener`, `querySelector`,
`createElement` e `appendChild`. **O que muda é a origem do dado**, que agora
vem do servidor durante o uso, e não está mais escrito na página.

**Duração:** 60 minutos, individual, nos Ciclos 3 e 4.

---

## Fronteira desta aula: isto ainda não é uma API REST

As duas actions de hoje vivem em um Controller MVC comum e existem para servir
**a sua própria tela**. Nenhum outro sistema as consome.

Portanto, **nada disto aparece hoje**: `[ApiController]`, `ControllerBase`,
rota `api/[controller]`, DTOs, `CreatedAtAction`, POST, PUT ou DELETE em JSON.
Esse é o assunto inteiro da **Aula 16**, e a comparação vai começar exatamente
por estas duas actions que você escreve agora. Escrevê-las no estilo da Aula 16
hoje não adianta a matéria: apaga a diferença que a Aula 16 precisa mostrar.

Autenticação também não entra aqui. `[Authorize]` e Identity são a **Aula 15**.

---

## Pré-requisitos

- O fork de `josercf/uninove-2026-2-clinica-vida` clonado na sua máquina.
- O entregável da Aula 13 na `main`: o agendamento em duas etapas com sessão.
- O CRUD e o banco `clinicavida` das Aulas 11 e 12, com médicos e
  especialidades cadastrados. Sem médico cadastrado, o JSON de hoje volta
  vazio e você vai depurar um problema que não existe.
- O SDK do .NET 10 e o serviço do MySQL rodando.

Confirme o ponto de partida antes de começar:

```bash
dotnet --version           # precisa começar com 10.
dotnet ef database update  # não pode ter migration pendente
```

E confirme no MySQL Workbench que há dado para devolver:

```sql
SELECT e.Nome AS Especialidade, COUNT(m.Id) AS Medicos
FROM clinicavida.Especialidades e
LEFT JOIN clinicavida.Medicos m ON m.EspecialidadeId = e.Id
GROUP BY e.Nome;
```

---

## Passo 1: a branch e a action `MedicosPorEspecialidade` (10 min)

```bash
git checkout main && git pull
git checkout -b feature/ajax-horarios
```

No `Controllers/ConsultasController.cs`, o contexto já chega por injeção desde
a Aula 12. Acrescente a action:

```csharp
public async Task<JsonResult> MedicosPorEspecialidade(int especialidadeId)
{
    var medicos = await _context.Medicos
        .Where(m => m.EspecialidadeId == especialidadeId)
        .OrderBy(m => m.Nome)
        .Select(m => new { id = m.Id, nome = m.Nome, crm = m.Crm })
        .ToListAsync();

    return Json(medicos);
}
```

Três pontos que valem a leitura com calma:

1. É o mesmo LINQ da Aula 12. Muda só o final: `Json(...)` no lugar de
   `View(...)`. `return Ok(medicos);` faz a mesma coisa e também vale.
2. O `Select` **não é enfeite**. Devolver a entidade `Medico` inteira entrega
   ao navegador tudo o que ela carrega, e ainda arrasta a `Especialidade`
   junto se ela estiver carregada. Escolha campo a campo o que sai.
3. Os nomes do objeto anônimo saem em JSON como você escreveu, em minúsculas:
   `id`, `nome` e `crm`. É por eles que o JavaScript vai perguntar.

---

## Passo 2: conferir o JSON antes de escrever JavaScript (8 min)

Uma action de JSON se testa direto na barra de endereços. Depurar JavaScript
contra um servidor que ainda não funciona é procurar defeito em dois lugares ao
mesmo tempo.

Rode `dotnet run` e abra o endereço abaixo **trocando a porta**. A porta é
sorteada em `Properties/launchSettings.json` e é diferente em cada máquina: use
a que apareceu no **seu** terminal, e não a deste roteiro.

```text
https://localhost:7145/Consultas/MedicosPorEspecialidade?especialidadeId=1
```

O que precisa aparecer é um vetor JSON, mais ou menos assim:

```json
[
  { "id": 3, "nome": "Dra. Helena Vasques", "crm": "SP-118240" },
  { "id": 7, "nome": "Dr. Rafael Nakano", "crm": "SP-204915" }
]
```

Abra o DevTools na aba **Network**, recarregue e confira o cabeçalho de
resposta: precisa ser `Content-Type: application/json`. Se vier
`text/html`, você está olhando uma página, e não a sua action.

Se vier `[]`, não é defeito de código: não há médico com aquela
`EspecialidadeId`. Confira no Workbench e cadastre um pela tela da Aula 12.

---

## Passo 3: a lista de médicos que troca sozinha (12 min)

Este é o fim do Ciclo 3, ainda com o professor conduzindo.

A tela em que isto acontece é a **etapa 1** do fluxo da Aula 13,
`Views/Consultas/Agendar.cshtml`, onde o usuário escolhe especialidade e
médico. A View precisa de identificadores estáveis para o JavaScript achar os
elementos:

```cshtml
@* Views/Consultas/Agendar.cshtml, etapa 1 *@
<select id="especialidadeId" name="EspecialidadeId" asp-items="ViewBag.Especialidades">
    <option value="">Selecione a especialidade</option>
</select>

<select id="medicoId" name="MedicoId">
    <option value="">Selecione o médico</option>
</select>

@section Scripts {
    <script src="~/js/agendamento-ajax.js" defer></script>
}
```

Crie `wwwroot/js/agendamento-ajax.js`:

```javascript
const especialidade = document.querySelector("#especialidadeId");
const medico = document.querySelector("#medicoId");

// O mesmo arquivo é carregado pelas duas telas do fluxo, e cada uma tem só
// parte dos elementos. Por isso todo listener é registrado sob uma guarda.
async function buscarJson(url) {
  const resposta = await fetch(url);

  // 404 e 500 NÃO lançam erro no fetch: quem avisa é o resposta.ok
  if (!resposta.ok) {
    throw new Error(`O servidor respondeu ${resposta.status}`);
  }

  return await resposta.json();
}

if (especialidade) {
  especialidade.addEventListener("change", async () => {
    medico.innerHTML = "<option>Carregando...</option>";

    try {
      const url =
        `/Consultas/MedicosPorEspecialidade?especialidadeId=${especialidade.value}`;
      const medicos = await buscarJson(url);

      medico.innerHTML = "<option value=''>Selecione o médico</option>";
      for (const m of medicos) {
        const opcao = document.createElement("option");
        opcao.value = m.id;
        opcao.textContent = `${m.nome} (${m.crm})`;
        medico.appendChild(opcao);
      }
    } catch (erro) {
      console.error(erro);
      medico.innerHTML = "<option value=''>Não foi possível carregar</option>";
    }
  });
}
```

Troque a especialidade três vezes. A lista de médicos precisa mudar **sem a
página piscar** e sem a URL da barra de endereços mudar.

Escutamos `change`, e não `input`, de propósito: `change` em uma lista suspensa
dispara uma requisição por escolha do usuário. `input` em um campo de texto
dispararia uma requisição por caractere digitado.

---

## Passo 4: a action `HorariosDisponiveis` (12 min)

Ciclo 4, sozinho a partir daqui.

A grade da clínica vai das 07:00 às 18:30, de 30 em 30 minutos, cobrindo o expediente das 07h às 19h que você já validou nas Aulas 06 e 10. Horário livre é
o que está na grade e **não** está marcado para aquele médico naquela data.

```csharp
public async Task<JsonResult> HorariosDisponiveis(int medicoId, DateTime data)
{
    var ocupados = await _context.Consultas
        .Where(c => c.MedicoId == medicoId && c.Data == data.Date)
        .Select(c => c.Horario)
        .ToListAsync();

    var livres = new List<string>();
    var inicio = new TimeSpan(8, 0, 0);
    var fim = new TimeSpan(18, 0, 0);

    for (var h = inicio; h < fim; h += TimeSpan.FromMinutes(30))
    {
        if (!ocupados.Contains(h))
        {
            livres.Add(h.ToString(@"hh\:mm"));
        }
    }

    return Json(livres);
}
```

Detalhes que decidem se isto funciona:

- `Consulta.Data` é `DateTime` e `Consulta.Horario` é `TimeSpan`, conforme o
  Model da Aula 10. A comparação usa `data.Date` para ignorar a hora que possa
  vir junto na data.
- O filtro dos ocupados roda no banco; a grade é montada em memória, depois. Só
  o que a `Where` alcança vira SQL.
- Sai texto `"HH:mm"`, e não `TimeSpan`, porque é isso que o botão da tela vai
  exibir sem nenhum tratamento adicional.

Teste na barra de endereços, de novo com a **sua** porta:

```text
https://localhost:7145/Consultas/HorariosDisponiveis?medicoId=3&data=2026-11-04
```

---

## Passo 5: os horários como botões, e o caso vazio (10 min)

Agora estamos na **etapa 2** do fluxo da Aula 13,
`Views/Consultas/AgendarHorario.cshtml`. O médico já foi escolhido e está na
sessão, então a action `AgendarHorario` em GET, que já lê
`AgendamentoMedicoId` da sessão, só precisa expor esse valor para a View:

```csharp
ViewBag.MedicoId = medicoId;   // na action AgendarHorario, em GET
```

```cshtml
@* Views/Consultas/AgendarHorario.cshtml, etapa 2 *@
<input type="hidden" id="medicoId" value="@ViewBag.MedicoId" />
<input type="date" id="data" name="Data" />

<div id="horarios" class="grade-horarios"></div>
<input type="hidden" id="horarioEscolhido" name="Horario" />

@section Scripts {
    <script src="~/js/agendamento-ajax.js" defer></script>
}
```

Repare que `#medicoId` é um `<select>` na etapa 1 e um `<input type="hidden">`
aqui. Para o JavaScript tanto faz: os dois têm `.value`, e o mesmo código serve
às duas telas.

```javascript
const data = document.querySelector("#data");
const caixa = document.querySelector("#horarios");
const horarioEscolhido = document.querySelector("#horarioEscolhido");

function desenharHorarios(horarios) {
  caixa.innerHTML = "";
  horarioEscolhido.value = "";

  if (horarios.length === 0) {
    caixa.innerHTML =
      "<p class='vazio'>Nenhum horário livre nesta data. Escolha outro dia.</p>";
    return;
  }

  for (const h of horarios) {
    const botao = document.createElement("button");
    botao.type = "button";
    botao.className = "horario";
    botao.textContent = h;

    botao.addEventListener("click", () => {
      caixa.querySelectorAll(".horario")
        .forEach(b => b.classList.remove("selecionado"));
      botao.classList.add("selecionado");
      horarioEscolhido.value = h;
    });

    caixa.appendChild(botao);
  }
}
```

O `type="button"` não é detalhe: sem ele, o botão dentro de um `<form>` é do
tipo `submit` por padrão, e clicar em um horário envia o formulário. Seria
justamente a recarga que esta aula veio eliminar.

**Vetor vazio não é erro.** É uma resposta que chegou, chegou bem, e diz que
não há vaga. Tratar isso como falha esconde do usuário a informação de que ele
precisa escolher outro dia.

---

## Passo 6: carregando e erro (8 min)

Falta ligar a busca aos eventos e cobrir os dois estados que quase todo mundo
esquece.

```javascript
async function carregarHorarios() {
  if (!medico.value || !data.value) {
    caixa.innerHTML = "";
    return;
  }

  caixa.innerHTML = "<p class='carregando'>Carregando horários...</p>";

  try {
    const url =
      `/Consultas/HorariosDisponiveis?medicoId=${medico.value}&data=${data.value}`;
    desenharHorarios(await buscarJson(url));
  } catch (erro) {
    console.error(erro);
    caixa.innerHTML =
      "<p class='erro'>Não foi possível carregar os horários. Tente novamente.</p>";
  }
}

if (data) {
  data.addEventListener("change", carregarHorarios);
}

// Na etapa 1 não existe campo de data, e o médico é escolhido em um select.
// A guarda abaixo deixa o mesmo arquivo servir às duas telas sem quebrar.
if (data && medico && medico.tagName === "SELECT") {
  medico.addEventListener("change", carregarHorarios);
}
```

Acrescente ao `wwwroot/css/site.css` o estilo dos quatro estados, com a paleta
do case:

```css
.grade-horarios { display: flex; flex-wrap: wrap; gap: 10px; margin: 12px 0; }

.grade-horarios .horario {
  background: #EAF5F1;
  border: 1.5px solid #2E9E7E;
  color: #0B6E75;
  border-radius: 6px;
  padding: 8px 16px;
  cursor: pointer;
}

.grade-horarios .horario.selecionado {
  background: #0B6E75;
  border-color: #0B6E75;
  color: #FFFFFF;
}

.carregando { color: #1F2A30; font-style: italic; }
.vazio  { background: #FFF8E4; border-left: 4px solid #D9B441; padding: 10px 16px; }
.erro   { background: #FDECE8; border-left: 4px solid #E4572E; padding: 10px 16px; }
```

### Como testar os três estados difíceis

| Estado | Como provocar |
|---|---|
| Carregando | Na etapa 2, escolha uma data. O aviso aparece por um instante antes dos botões |
| Vazio | Agende consultas ocupando toda a grade de um médico em uma data e busque aquela data |
| Erro | Com a página aberta, pare a aplicação no terminal e troque a data |

---

## Commit e push

```bash
git add Controllers/ConsultasController.cs wwwroot/js/agendamento-ajax.js
git add wwwroot/css/site.css Views/Consultas/Agendar.cshtml
git add Views/Consultas/AgendarHorario.cshtml
git commit -m "feat: medicos e horarios livres por AJAX no agendamento"
git push -u origin feature/ajax-horarios
```

---

## Entregável

Consulta de médicos e de horários livres por AJAX, sem recarregar a página, na
branch `feature/ajax-horarios`, commitada e enviada ao seu fork.
Especificamente:

- **2** actions devolvendo JSON: `MedicosPorEspecialidade` e
  `HorariosDisponiveis`, as duas com projeção por `Select` ou lista de texto,
  nunca a entidade inteira.
- **1** arquivo `wwwroot/js/agendamento-ajax.js`, ligado às duas Views do
  agendamento, `Agendar.cshtml` e `AgendarHorario.cshtml`.
- **2** eventos tratados: `change` da especialidade, na etapa 1, e `change` da
  data, na etapa 2.
- **4** estados de interface cobertos: carregando, com dados, vazio e erro.

### Critérios de aceitação

| # | Critério | Como o professor confere |
|---|---|---|
| 1 | As duas actions devolvem JSON | Abrir cada URL no navegador mostra um vetor JSON, e a aba Network traz `Content-Type: application/json` |
| 2 | O JSON não expõe a entidade inteira | O corpo devolvido traz só `id`, `nome` e `crm` no caso dos médicos, e só texto de horário no outro |
| 3 | A lista de médicos troca sem recarregar | Na etapa 1, trocar a especialidade muda o `<select>` de médicos, a URL da barra não muda e a página não pisca |
| 4 | Os horários aparecem como botões | Na etapa 2, ao escolher a data a grade é desenhada com um `<button type="button">` por horário |
| 5 | A seleção do horário é gravada | Clicar em um horário o destaca visualmente e preenche o campo oculto enviado no formulário |
| 6 | Os horários ocupados não aparecem | Agendar um horário e repetir a busca do mesmo médico e data: aquele horário sumiu da grade |
| 7 | O estado de carregando existe | O aviso de carregamento aparece na caixa antes da resposta chegar |
| 8 | O caso vazio é tratado | Uma data sem vaga mostra a mensagem de nenhum horário livre, e não uma caixa em branco |
| 9 | O erro é tratado | Com a aplicação parada, trocar a data mostra a mensagem de falha na tela, e não apenas no console |
| 10 | A resposta é checada com `resposta.ok` | O código lança ou trata explicitamente a resposta não OK, em vez de seguir direto para o `json()` |
| 11 | Nada de API REST aqui | Não existe `[ApiController]`, rota `api/...`, DTO nem `CreatedAtAction` no código entregue |
| 12 | O trabalho foi enviado | A branch `feature/ajax-horarios` aparece no seu fork no GitHub, com o commit de sua autoria |

---

## Se algo der errado

- **A página recarrega ao clicar em um horário**: falta `type="button"` no
  botão criado. Dentro de um `<form>`, o padrão de um `<button>` é `submit`.
- **`Uncaught TypeError: Cannot read properties of null (reading
  'addEventListener')`**: o script rodou antes do elemento existir, ou o `id`
  do HTML não é o mesmo do `querySelector`. Use `defer` na tag `<script>` e
  confira o `id` letra por letra.
- **O `fetch` devolve HTML em vez de JSON**: a URL está errada e o ASP.NET Core
  respondeu com a página de erro. Abra a mesma URL na barra de endereços e veja
  o que volta; o nome do Controller e da action precisam bater.
- **`SyntaxError: Unexpected token '<' ... is not valid JSON`**: é o sintoma do
  caso acima. O `resposta.json()` tentou converter uma página HTML.
- **O JSON volta `[]` sempre**: não há médico cadastrado com aquela
  `EspecialidadeId`, ou o parâmetro chegou vazio. Confira o valor no
  `console.log` e no banco antes de mexer no código.
- **Os horários ocupados continuam aparecendo**: a `Consulta` foi gravada com
  hora junto na coluna `Data`, e a comparação com `data.Date` não bate. Grave
  sempre a data zerada e confira com
  `SELECT Data, Horario FROM clinicavida.Consultas;`.
- **A data chega nula na action**: o `<input type="date">` envia
  `2026-11-04`, e o parâmetro precisa se chamar exatamente `data`, igual ao
  nome usado na query string da URL.
- **Nada acontece e o console não acusa nada**: o erro foi engolido por um
  `catch` vazio. Todo `catch` desta aula tem, no mínimo, um `console.error` e
  uma mensagem na tela.
- **A aplicação responde na porta errada**: a porta de `localhost` é sorteada
  em `Properties/launchSettings.json` e muda de máquina para máquina. Use
  sempre a que o seu terminal imprimiu ao subir a aplicação.
