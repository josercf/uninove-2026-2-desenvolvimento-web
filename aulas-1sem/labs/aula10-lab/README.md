# Laboratório da Aula 10

## Disciplina: Desenvolvimento Web
**Prof. José Romualdo | Uninove, Universidade Nove de Julho**

### Case: Clínica Vida+ (Fase 9, o formulário processado pelo servidor)

Na Aula 09 você entregou a **lista de médicos filtrada por especialidade**,
vinda do Controller e renderizada em uma View tipada. Até aqui o dado só
**sai** do servidor para a tela: nenhuma página da Clínica Vida+ manda dado de
volta.

Hoje o caminho se inverte. O `agendamento.html` que você escreveu à mão na Aula
05, com validação nativa do navegador, entra na aplicação `ClinicaVida.Web` como
um formulário de verdade: os campos passam a ser gerados a partir do Model, o
envio vira uma requisição POST, o ASP.NET Core monta sozinho um objeto
`Consulta` com o que o paciente digitou, e o servidor decide se aquilo é válido.

A regra de ouro do dia, que vale para o resto do semestre e da sua carreira:
**validação no cliente é conforto, validação no servidor é segurança**.

**Duração:** 60 minutos, individual, nos Ciclos 3 e 4.

---

## Pré-requisitos

- O fork de `josercf/uninove-2026-2-clinica-vida` clonado na sua máquina.
- O SDK do **.NET 10** instalado (`dotnet --version`).
- O projeto **`ClinicaVida.Web`** rodando com `dotnet run`, entregue na Aula 07.
- O entregável da Aula 09 na `main`: as classes `Especialidade` e `Medico` em
  `Models`, o repositório em memória e o `MedicosController`.
- VS Code e um navegador com DevTools (`F12`).

> **Sobre o repositório em memória.** Este roteiro usa a classe estática da
> Aula 09, `ClinicaEmMemoria`, em `Models/ClinicaEmMemoria.cs`. Se você deu
> outro nome a ela, **mantenha o seu** e troque as chamadas ao longo do
> roteiro. O que não muda é o resto do contrato do módulo: projeto
> `ClinicaVida.Web`, Models `Especialidade`, `Medico`, `Paciente` e
> `Consulta`.

> **Banco de dados ainda não.** As listas suspensas desta aula são alimentadas
> pelas listas em memória. MySQL e Entity Framework Core entram na Aula 11.

---

## Passo 1: a branch e o Model `Consulta` (10 min)

```bash
git switch main && git pull
git switch -c feature/formulario-agendamento
```

Crie `Models/Consulta.cs`. Por enquanto, só as propriedades:

```csharp
namespace ClinicaVida.Web.Models;

public class Consulta
{
    public int Id { get; set; }
    public int PacienteId { get; set; }
    public int MedicoId { get; set; }
    public DateTime Data { get; set; }
    public TimeSpan Horario { get; set; }
    public string? Observacoes { get; set; }
}
```

Repare no que **não** está aqui: a especialidade. Ela continua aparecendo na
tela, para filtrar a lista de médicos, mas não vira propriedade da `Consulta`,
porque o médico já carrega a dele em `Medico.EspecialidadeId`. Guardar o mesmo
dado em dois lugares é onde a divergência começa.

Antes das listas, falta uma classe. A `Consulta` guarda `PacienteId`, mas o
paciente ainda não existe como Model: nas Aulas 09 e 10 você criou
`Especialidade`, `Medico` e agora `Consulta`. Crie `Models/Paciente.cs` com as
seis propriedades que o paciente terá até o fim do semestre, para não precisar
mexer nesta classe de novo na Aula 11, quando ela virar tabela no banco.

```csharp
namespace ClinicaVida.Web.Models;

public class Paciente
{
    public int Id { get; set; }
    public string Nome { get; set; } = string.Empty;
    public string Cpf { get; set; } = string.Empty;
    public DateTime DataNascimento { get; set; }
    public string? Telefone { get; set; }
    public string? Email { get; set; }
}
```

Hoje o formulário usa só `Id`, `Nome` e `Cpf`. As outras três entram agora
porque o cadastro completo de paciente é o laboratório da Aula 12, e mudar a
classe depois significaria refazer a migration.

Agora, em `Models/ClinicaEmMemoria.cs`, acrescente duas listas: a dos
pacientes, que vai alimentar a lista suspensa, e a que vai receber os
agendamentos.

```csharp
public static List<Paciente> Pacientes { get; } = new()
{
    new Paciente { Id = 1, Nome = "Ana Beatriz Rocha", Cpf = "123.456.789-09" },
    new Paciente { Id = 2, Nome = "Carlos Eduardo Lima", Cpf = "987.654.321-00" },
    new Paciente { Id = 3, Nome = "Mariana Tavares", Cpf = "111.222.333-44" },
};

public static List<Consulta> Consultas { get; } = new();
```

Compile antes de seguir:

```bash
dotnet build
```

---

## Passo 2: as Data Annotations (10 min)

As regras moram ao lado do dado. Toda mensagem em português: quem lê é o
paciente, não o programador.

```csharp
using System.ComponentModel.DataAnnotations;

namespace ClinicaVida.Web.Models;

public class Consulta
{
    public int Id { get; set; }

    [Display(Name = "Paciente")]
    [Range(1, int.MaxValue, ErrorMessage = "Selecione o paciente.")]
    public int PacienteId { get; set; }

    [Display(Name = "Médico")]
    [Range(1, int.MaxValue, ErrorMessage = "Selecione o médico.")]
    public int MedicoId { get; set; }

    [Display(Name = "Data da consulta")]
    [Required(ErrorMessage = "Informe a data da consulta.")]
    [DataType(DataType.Date)]
    public DateTime Data { get; set; }

    [Display(Name = "Horário")]
    [Required(ErrorMessage = "Informe o horário da consulta.")]
    [DataType(DataType.Time)]
    public TimeSpan Horario { get; set; }

    [Display(Name = "Observações")]
    [StringLength(300, ErrorMessage = "As observações têm no máximo {1} caracteres.")]
    public string? Observacoes { get; set; }
}
```

Quatro detalhes que valem a leitura com calma:

- `[Display]` muda o rótulo que aparece na tela **e** o texto das mensagens
  padrão do framework.
- `[Range(1, int.MaxValue)]` nas listas suspensas: quando o paciente não escolhe
  nada, o valor chega como `0`, e `[Required]` não reclama de `0` em um `int`.
- `[DataType(DataType.Date)]` é o que faz o `asp-for` gerar `type="date"`; o
  mesmo vale para `DataType.Time` e o `type="time"`.
- `{1}` dentro da mensagem de `[StringLength]` é substituído pelo tamanho
  máximo. Assim a mensagem e a regra nunca divergem.

Agora anote também o CPF do paciente, em `Models/Paciente.cs`. O CPF é `string`
e chega com a máscara `000.000.000-00`, então as regras precisam **aceitar** a
máscara:

```csharp
[Display(Name = "CPF")]
[Required(ErrorMessage = "Informe o CPF do paciente.")]
[StringLength(14, MinimumLength = 14, ErrorMessage = "O CPF tem 14 caracteres com a máscara.")]
[RegularExpression(@"^\d{3}\.\d{3}\.\d{3}-\d{2}$", ErrorMessage = "Use o formato 000.000.000-00.")]
public string Cpf { get; set; } = string.Empty;
```

Teste mentalmente três entradas: em branco (barrado pelo `[Required]`),
`123456` (barrado pelo tamanho e pelo formato) e `123.456.789-09` (aceito).

---

## Passo 3: o `ConsultasController` e as listas suspensas (15 min)

Crie `Controllers/ConsultasController.cs`. A action de GET só mostra o
formulário; as listas suspensas saem do repositório em memória.

```csharp
using ClinicaVida.Web.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;

namespace ClinicaVida.Web.Controllers;

public class ConsultasController : Controller
{
    [HttpGet]
    public IActionResult Agendar()
    {
        CarregarListas();
        return View(new Consulta { Data = DateTime.Today });
    }

    private void CarregarListas()
    {
        ViewBag.Pacientes = new SelectList(ClinicaEmMemoria.Pacientes, "Id", "Nome");
        ViewBag.Medicos   = new SelectList(ClinicaEmMemoria.Medicos,   "Id", "Nome");
    }
}
```

`SelectList` recebe a coleção, o nome da propriedade que vira o `value` do
`option` e o nome da propriedade que vira o texto visível. É por isso que o
`select` de médicos manda `MedicoId` e mostra o nome.

A lista `Pacientes` é a que você criou no Passo 1: a tela precisa de gente para
escolher.

Suba a aplicação e confirme que `/Consultas/Agendar` responde, mesmo que a View
ainda não exista: o erro que aparece precisa ser o de View não encontrada, e não
o de rota.

```bash
dotnet run
```

---

## Passo 4: a View com Tag Helpers (10 min)

Crie `Views/Consultas/Agendar.cshtml`. Cada campo é sempre o mesmo trio de
linhas: rótulo, campo e mensagem.

```cshtml
@model ClinicaVida.Web.Models.Consulta
@{ ViewData["Title"] = "Agendar consulta"; }

<h1>Agendar consulta</h1>

<form asp-controller="Consultas" asp-action="Agendar" method="post">
  <div asp-validation-summary="ModelOnly" class="erro-resumo"></div>

  <label asp-for="PacienteId"></label>
  <select asp-for="PacienteId" asp-items="ViewBag.Pacientes">
    <option value="">Selecione o paciente</option>
  </select>
  <span asp-validation-for="PacienteId" class="erro-campo"></span>

  <label asp-for="MedicoId"></label>
  <select asp-for="MedicoId" asp-items="ViewBag.Medicos">
    <option value="">Selecione o médico</option>
  </select>
  <span asp-validation-for="MedicoId" class="erro-campo"></span>

  <label asp-for="Data"></label>
  <input asp-for="Data" />
  <span asp-validation-for="Data" class="erro-campo"></span>

  <label asp-for="Horario"></label>
  <input asp-for="Horario" />
  <span asp-validation-for="Horario" class="erro-campo"></span>

  <label asp-for="Observacoes"></label>
  <textarea asp-for="Observacoes" rows="3"></textarea>
  <span asp-validation-for="Observacoes" class="erro-campo"></span>

  <button type="submit">Confirmar agendamento</button>
</form>

@section Scripts {
  <partial name="_ValidationScriptsPartial" />
}
```

Três pontos para conferir no navegador, com `Ctrl+U` ou o inspetor:

1. O `action` do formulário saiu como `/Consultas/Agendar`, resolvido pela rota,
   e não escrito à mão por você.
2. Existe um `<input type="hidden" name="__RequestVerificationToken" ...>` que
   você não digitou: é o **token antifalsificação**, injetado pelo Tag Helper de
   `form`.
3. Os campos têm atributos `data-val-*` com as suas mensagens em português. São
   eles que a validação do cliente lê.

Acrescente ao `assets/css/site.css` (ou ao CSS do projeto) as duas classes de
erro, na paleta do case:

```css
.erro-campo  { color: #E4572E; font-size: 0.9rem; display: block; }
.erro-resumo { color: #E4572E; border-left: 4px solid #E4572E; padding-left: 12px; }
```

---

## Passo 5: a action de POST e o `ModelState` (10 min)

A segunda action se chama igual e muda o verbo. Teste **primeiro o caminho do
erro**: envie o formulário vazio.

```csharp
[HttpPost]
[ValidateAntiForgeryToken]
public IActionResult Agendar(Consulta consulta)
{
    if (consulta.Data.Date < DateTime.Today)
        ModelState.AddModelError("Data", "A consulta precisa ser em uma data futura.");

    if (consulta.Horario < new TimeSpan(7, 0, 0) || consulta.Horario >= new TimeSpan(19, 0, 0))
        ModelState.AddModelError("Horario", "A Clínica Vida+ atende das 07h às 19h.");

    if (!ModelState.IsValid)
    {
        CarregarListas();          // as listas suspensas não sobrevivem ao POST
        return View(consulta);     // mesma View, com os valores digitados e os erros
    }

    consulta.Id = ClinicaEmMemoria.Consultas.Count + 1;
    ClinicaEmMemoria.Consultas.Add(consulta);
    return RedirectToAction(nameof(Confirmacao), new { id = consulta.Id });
}
```

Duas ideias moram neste método:

- **Data futura e expediente são regra de negócio, não formato.** Nenhuma
  anotação sabe o que é "hoje" nem que a clínica fecha às 19h. São as mesmas
  duas regras que você escreveu em JavaScript na Aula 06, agora do lado que
  ninguém consegue desligar. `ModelState.AddModelError` acrescenta a sua regra
  ao mesmo relatório do framework.
- **Sucesso não devolve View, devolve redirecionamento.** Sem isso, quem
  atualizar a página de resposta reenvia o mesmo agendamento, e a clínica ganha
  uma consulta em duplicidade, exatamente o problema que este case veio
  resolver.

---

## Passo 6: a tela de confirmação (5 min)

```csharp
[HttpGet]
public IActionResult Confirmacao(int id)
{
    var consulta = ClinicaEmMemoria.Consultas.FirstOrDefault(c => c.Id == id);
    if (consulta is null) return NotFound();

    ViewBag.NomePaciente = ClinicaEmMemoria.Pacientes.First(p => p.Id == consulta.PacienteId).Nome;
    ViewBag.NomeMedico   = ClinicaEmMemoria.Medicos.First(m => m.Id == consulta.MedicoId).Nome;
    return View(consulta);
}
```

E `Views/Consultas/Confirmacao.cshtml`:

```cshtml
@model ClinicaVida.Web.Models.Consulta
@{ ViewData["Title"] = "Consulta agendada"; }

<h1>Consulta agendada</h1>

<p>Paciente: <strong>@ViewBag.NomePaciente</strong></p>
<p>Médico: <strong>@ViewBag.NomeMedico</strong></p>
<p>Data: <strong>@Model.Data.ToString("dd/MM/yyyy")</strong></p>
<p>Horário: <strong>@Model.Horario.ToString(@"hh\:mm")</strong></p>

<a asp-action="Agendar">Agendar outra consulta</a>
```

Confira a barra de endereços: ela precisa terminar em
`/Consultas/Confirmacao/1`, e não em `/Consultas/Agendar`.

---

## Prova da regra de ouro

Antes do commit, faça a demonstração de 30 segundos com os seus próprios olhos:

1. Abra o formulário e o DevTools (`F12`).
2. No inspetor, apague o atributo `required` do campo de data e envie o
   formulário vazio.
3. O navegador deixa passar. O servidor recusa, com a mesma mensagem que você
   escreveu na anotação, e a View volta com os valores preenchidos.

É esta a diferença entre conforto e segurança.

---

## Commit e push

```bash
git add Models Controllers Views
git commit -m "feat: formulario de agendamento com validacao no servidor"
git push -u origin feature/formulario-agendamento
```

---

## Entregável

Formulário de agendamento validando **no servidor**, com mensagens de erro por
campo e tela de confirmação, na branch `feature/formulario-agendamento`,
commitado e enviado ao seu fork. Especificamente:

- **1** Model `Consulta` com as 6 propriedades anotadas.
- **1** propriedade `Cpf` anotada em `Paciente`, aceitando a máscara.
- **1** `ConsultasController` com `Agendar` em GET, `Agendar` em POST e
  `Confirmacao`.
- **2** Views: `Agendar.cshtml`, com Tag Helpers, resumo de validação e as duas
  listas suspensas, e `Confirmacao.cshtml`.
- **2** regras de negócio no `ModelState`: data futura e horário no expediente.

### Critérios de aceitação

| # | Critério | Como o professor confere |
|---|---|---|
| 1 | O Model está anotado | `Models/Consulta.cs` traz `[Display]`, `[Required]`, `[Range]`, `[DataType]` e `[StringLength]`, com todas as mensagens em português |
| 2 | O CPF aceita a máscara | `123.456.789-09` é aceito e `123456` é recusado com a mensagem de formato |
| 3 | O par GET e POST existe | `ConsultasController` tem duas actions `Agendar`, uma com `[HttpGet]` e outra com `[HttpPost]` |
| 4 | A View usa Tag Helpers | Nenhum `id`, `name` ou `action` escrito à mão no formulário: só `asp-for`, `asp-action`, `asp-controller`, `asp-items` e `asp-validation-for` |
| 5 | As listas suspensas vêm do repositório | Os `select` de paciente e de médico exibem os registros em memória da Aula 09, e não `option` digitados na View |
| 6 | O envio vazio é recusado no servidor | Com o `required` removido pelo DevTools, o envio vazio volta com mensagem em cada campo, e nenhuma consulta é criada |
| 7 | Os valores não se perdem no erro | Depois de um envio inválido, os campos preenchidos continuam preenchidos e os `select` continuam com as opções |
| 8 | As regras de negócio funcionam | Data de ontem e horário 21h00 são recusados com as mensagens específicas |
| 9 | O sucesso redireciona | Um envio válido termina em `/Consultas/Confirmacao/{id}`, com paciente, médico, data e horário na tela |
| 10 | O token antifalsificação está no formulário | O HTML gerado traz o campo oculto `__RequestVerificationToken`, e a action de POST tem `[ValidateAntiForgeryToken]` |
| 11 | O trabalho foi enviado | A branch `feature/formulario-agendamento` aparece no seu fork no GitHub, com o commit de sua autoria |

---

## Se algo der errado

- **`InvalidOperationException: The model item passed into the ViewDataDictionary
  is of type ...`**: a View está tipada com um Model e o Controller mandou
  outro. Confira o `@model` da primeira linha do `.cshtml`.
- **`NullReferenceException` no `asp-items` depois de um envio inválido**: você
  esqueceu o `CarregarListas()` dentro do `if (!ModelState.IsValid)`. O
  `ViewBag` só existe durante uma requisição, e o POST é outra requisição.
- **O campo chega sempre vazio no servidor**: o nome enviado não casou com o
  nome da propriedade. Veja o `name` no HTML gerado; com `asp-for` ele sai
  correto sozinho, então desconfie de campo que ficou escrito à mão.
- **`The value '' is invalid` em inglês**: a propriedade é um tipo de valor não
  anulável (`int`, `DateTime`, `TimeSpan`) e chegou vazia. Acrescente
  `[Required]` com a sua mensagem, e use `[Range(1, int.MaxValue)]` nas listas
  suspensas.
- **O formulário envia mas nada acontece**: sem `[ValidateAntiForgeryToken]` do
  lado do servidor e com o `form` montado à mão, sem Tag Helper, o token não
  viaja e a requisição é recusada com **400**. Confira a aba Rede do DevTools.
- **A validação do cliente não aparece**: falta o
  `@section Scripts { <partial name="_ValidationScriptsPartial" /> }` na View,
  ou o `_Layout.cshtml` não tem
  `@await RenderSectionAsync("Scripts", required: false)`. Isso não afeta a
  validação do servidor, que é a que vale.
- **A data volta errada depois do envio**: confira se a propriedade tem
  `[DataType(DataType.Date)]`. Sem ela, o `asp-for` gera `type="text"` e o
  formato do texto passa a depender da cultura do navegador.
