# Laboratório da Aula 12

## Disciplina: Desenvolvimento Web
**Prof. José Romualdo | Uninove, Universidade Nove de Julho**

### Case: Clínica Vida+ (Fase 11, o CRUD de pacientes)

Na Aula 11 você entregou o `ClinicaContext` configurado, a migration
`InicialClinicaVida` aplicada e o banco `clinicavida` criado no MySQL, com as
quatro tabelas e as especialidades semeadas por `HasData`. O banco existe, e
nenhuma tela da aplicação lê ou escreve uma única linha dele.

Hoje a ponte é construída. O laboratório cria o `PacientesController`
recebendo o contexto por injeção de dependência e implementa as cinco
operações do CRUD, todas assíncronas, com as Views correspondentes, o padrão
Post-Redirect-Get e a mensagem de sucesso em `TempData`. É o último passo do
Módulo 2: ao fim desta aula, a Clínica Vida+ guarda dados que sobrevivem ao
reinício da aplicação.

**Duração:** 60 minutos, individual, nos Ciclos 3 e 4.

---

## Pré-requisitos

- O fork de `josercf/uninove-2026-2-clinica-vida` clonado na sua máquina.
- O entregável da Aula 11 na `main`: `Data/ClinicaContext.cs`, a connection
  string em `DefaultConnection` e o banco `clinicavida` criado no MySQL.
- O SDK do .NET 10 e o serviço do MySQL rodando.
- VS Code e o MySQL Workbench, para conferir as linhas gravadas.

Confirme o ponto de partida antes de começar:

```bash
dotnet --version          # precisa começar com 10.
dotnet ef database update # não pode ter migration pendente
```

---

## Passo 1: a branch e o Controller (10 min)

```bash
git switch main && git pull
git switch -c feature/crud-pacientes
```

Crie `Controllers/PacientesController.cs`. O contexto **não** é criado aqui:
ele é declarado no construtor e o contêiner de serviços do ASP.NET Core o
entrega pronto, porque a Aula 11 já o registrou em `Program.cs` com
`AddDbContext<ClinicaContext>`.

```csharp
using ClinicaVida.Web.Data;
using ClinicaVida.Web.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace ClinicaVida.Web.Controllers;

public class PacientesController : Controller
{
    private readonly ClinicaContext _context;

    public PacientesController(ClinicaContext context)
    {
        _context = context;
    }
}
```

Rode `dotnet run` e abra `/Pacientes`. O erro esperado neste momento é o de
action inexistente, e não o de serviço não registrado: se aparecer
`InvalidOperationException: Unable to resolve service for type
'ClinicaVida.Web.Data.ClinicaContext'`, o problema está no `Program.cs`, não
aqui.

---

## Passo 2: a listagem (10 min)

A action é assíncrona porque ir ao banco é esperar por outro processo. Com
`await`, a thread do servidor é devolvida ao pool durante a espera e volta a
atender outra requisição.

```csharp
public async Task<IActionResult> Index()
{
    var pacientes = await _context.Pacientes
        .OrderBy(p => p.Nome)
        .ToListAsync();
    return View(pacientes);
}
```

Crie `Views/Pacientes/Index.cshtml`:

```cshtml
@model IEnumerable<ClinicaVida.Web.Models.Paciente>
@{ ViewData["Title"] = "Pacientes"; }

<h1>Pacientes</h1>

@if (TempData["Sucesso"] != null)
{
    <p class="alerta-sucesso">@TempData["Sucesso"]</p>
}

<a asp-action="Create">Novo paciente</a>

<table>
    <thead>
        <tr><th>Nome</th><th>CPF</th><th>Telefone</th><th></th></tr>
    </thead>
    <tbody>
        @foreach (var paciente in Model)
        {
            <tr>
                <td>@paciente.Nome</td>
                <td>@paciente.Cpf</td>
                <td>@paciente.Telefone</td>
                <td>
                    <a asp-action="Details" asp-route-id="@paciente.Id">Ver</a>
                    <a asp-action="Edit" asp-route-id="@paciente.Id">Editar</a>
                    <a asp-action="Delete" asp-route-id="@paciente.Id">Excluir</a>
                </td>
            </tr>
        }
    </tbody>
</table>
```

Acrescente ao `wwwroot/css/site.css` o estilo da mensagem, com a paleta do
case:

```css
.alerta-sucesso {
  background: #EAF5F1;
  border-left: 4px solid #2E9E7E;
  color: #0B6E75;
  padding: 10px 16px;
  border-radius: 0 6px 6px 0;
}
```

A lista vem vazia, e está certo: ninguém cadastrou paciente nenhum ainda.
Olhe o **terminal** em que a aplicação roda: o `SELECT` gerado pelo EF Core
aparece no log.

---

## Passo 3: a ficha do paciente (8 min)

A URL é editável pelo usuário, então toda action que recebe um `id` precisa
tratar o registro inexistente. `FirstOrDefaultAsync` devolve `null` sem
lançar exceção, e quem decide o que fazer com isso é você.

```csharp
public async Task<IActionResult> Details(int? id)
{
    if (id == null) return NotFound();

    var paciente = await _context.Pacientes
        .FirstOrDefaultAsync(p => p.Id == id);

    if (paciente == null) return NotFound();

    return View(paciente);
}
```

`Views/Pacientes/Details.cshtml` mostra os seis campos do Model:

```cshtml
@model ClinicaVida.Web.Models.Paciente

<h1>@Model.Nome</h1>
<dl>
    <dt>CPF</dt><dd>@Model.Cpf</dd>
    <dt>Nascimento</dt><dd>@Model.DataNascimento.ToString("dd/MM/yyyy")</dd>
    <dt>Telefone</dt><dd>@Model.Telefone</dd>
    <dt>E-mail</dt><dd>@Model.Email</dd>
</dl>
<a asp-action="Index">Voltar</a>
```

Teste na barra de endereços: `/Pacientes/Details/9999` precisa devolver 404,
e não uma página de erro do servidor.

---

## Passo 4: o cadastro (12 min)

Duas actions com o mesmo nome: a de GET mostra o formulário vazio, a de POST
recebe o que foi digitado.

```csharp
public IActionResult Create() => View();

[HttpPost]
[ValidateAntiForgeryToken]
public async Task<IActionResult> Create(Paciente paciente)
{
    if (!ModelState.IsValid) return View(paciente);

    _context.Add(paciente);
    await _context.SaveChangesAsync();

    TempData["Sucesso"] = $"Paciente {paciente.Nome} cadastrado com sucesso.";
    return RedirectToAction(nameof(Index));
}
```

Três pontos que valem a leitura com calma:

1. `_context.Add` **não** grava nada. Ele marca a entidade como `Added` no
   rastreador de mudanças. Quem abre a transação e emite o `INSERT` é o
   `SaveChangesAsync`. Esquecer o `await _context.SaveChangesAsync()` não
   gera erro nenhum: a tela redireciona e o registro simplesmente não existe.
2. Validação que falhou devolve a View, e está correto: nada foi gravado, e
   as mensagens de erro por campo que você configurou na Aula 10 precisam
   aparecer.
3. Gravou, redireciona. É o **Post-Redirect-Get**, e o Passo 6 explica por
   quê.

`Views/Pacientes/Create.cshtml`:

```cshtml
@model ClinicaVida.Web.Models.Paciente

<h1>Novo paciente</h1>

<form asp-action="Create" method="post">
    <div asp-validation-summary="ModelOnly"></div>

    <label asp-for="Nome"></label>
    <input asp-for="Nome" />
    <span asp-validation-for="Nome"></span>

    <label asp-for="Cpf"></label>
    <input asp-for="Cpf" placeholder="000.000.000-00" />
    <span asp-validation-for="Cpf"></span>

    <label asp-for="DataNascimento"></label>
    <input asp-for="DataNascimento" type="date" />
    <span asp-validation-for="DataNascimento"></span>

    <label asp-for="Telefone"></label>
    <input asp-for="Telefone" />

    <label asp-for="Email"></label>
    <input asp-for="Email" />
    <span asp-validation-for="Email"></span>

    <button type="submit">Cadastrar</button>
    <a asp-action="Index">Cancelar</a>
</form>
```

Cadastre um paciente e confira a linha nova no MySQL Workbench:

```sql
SELECT Id, Nome, Cpf FROM clinicavida.Pacientes;
```

---

## Passo 5: a edição (10 min)

Ciclo 4, sozinho. O GET carrega o registro e devolve o formulário preenchido;
o POST grava a alteração.

```csharp
public async Task<IActionResult> Edit(int? id)
{
    if (id == null) return NotFound();

    var paciente = await _context.Pacientes.FindAsync(id);
    if (paciente == null) return NotFound();

    return View(paciente);
}

[HttpPost]
[ValidateAntiForgeryToken]
public async Task<IActionResult> Edit(int id, Paciente paciente)
{
    if (id != paciente.Id) return NotFound();
    if (!ModelState.IsValid) return View(paciente);

    _context.Update(paciente);
    await _context.SaveChangesAsync();

    TempData["Sucesso"] = "Cadastro atualizado.";
    return RedirectToAction(nameof(Index));
}
```

`Views/Pacientes/Edit.cshtml` é o formulário do Passo 4 com **uma linha a
mais**, e ela não é decorativa:

```cshtml
<input type="hidden" asp-for="Id" />
```

Sem o campo oculto, o POST chega com `Id` igual a zero, o EF Core entende que
é uma entidade nova e tenta um `INSERT` no lugar do `UPDATE`. É o defeito mais
comum do passo.

---

## Passo 6: a exclusão e o Post-Redirect-Get (10 min)

Exclusão acontece em duas etapas: o GET pergunta, o POST apaga. Excluir por
link é armadilha, porque um clique errado, um pré-carregamento do navegador ou
uma varredura automática apagam o cadastro de um paciente. **GET nunca destrói
dado.**

```csharp
public async Task<IActionResult> Delete(int? id)
{
    if (id == null) return NotFound();

    var paciente = await _context.Pacientes
        .FirstOrDefaultAsync(p => p.Id == id);

    if (paciente == null) return NotFound();

    return View(paciente);
}

[HttpPost, ActionName("Delete")]
[ValidateAntiForgeryToken]
public async Task<IActionResult> DeleteConfirmed(int id)
{
    var paciente = await _context.Pacientes.FindAsync(id);
    if (paciente != null) _context.Pacientes.Remove(paciente);

    await _context.SaveChangesAsync();

    TempData["Sucesso"] = "Paciente excluído.";
    return RedirectToAction(nameof(Index));
}
```

O par `[HttpPost, ActionName("Delete")]` sobre o método `DeleteConfirmed`
existe porque C# não aceita dois métodos com a mesma assinatura na mesma
classe. O atributo diz ao roteamento que, para a URL, esse método continua se
chamando `Delete`.

`Views/Pacientes/Delete.cshtml`:

```cshtml
@model ClinicaVida.Web.Models.Paciente

<h1>Excluir paciente</h1>
<p>Esta ação não pode ser desfeita.</p>
<dl>
    <dt>Nome</dt><dd>@Model.Nome</dd>
    <dt>CPF</dt><dd>@Model.Cpf</dd>
</dl>

<form asp-action="Delete" method="post">
    <input type="hidden" asp-for="Id" />
    <button type="submit">Confirmar exclusão</button>
    <a asp-action="Index">Cancelar</a>
</form>
```

### O teste do F5

Faça isto nas três operações que gravam, cadastrar, editar e excluir:

1. Conclua a operação.
2. Assim que a lista aparecer, aperte **F5**.
3. Nada pode ser gravado de novo, e o navegador não pode perguntar se você
   deseja reenviar o formulário.

Se a pergunta aparecer, a última requisição feita ainda é o POST, e falta o
`RedirectToAction` naquela action. Esse é o padrão **Post-Redirect-Get**: o
POST grava e responde com um redirecionamento, o navegador faz um GET, e o GET
pode ser repetido à vontade sem efeito nenhum no banco.

---

## Commit e push

```bash
git add Controllers/PacientesController.cs Views/Pacientes/ wwwroot/css/site.css
git commit -m "feat: CRUD completo de paciente com EF Core"
git push -u origin feature/crud-pacientes
```

---

## Entregável

CRUD completo de `Paciente` persistindo no banco `clinicavida`, na branch
`feature/crud-pacientes`, commitado e enviado ao seu fork. Especificamente:

- **1** `PacientesController` recebendo o `ClinicaContext` por injeção no
  construtor.
- **8** actions: `Index`, `Details`, `Create` em GET e em POST, `Edit` em GET
  e em POST, `Delete` em GET e `DeleteConfirmed` em POST.
- **5** Views em `Views/Pacientes/`: `Index`, `Details`, `Create`, `Edit` e
  `Delete`.
- **3** redirecionamentos com mensagem em `TempData`, um por operação que
  grava.

### Critérios de aceitação

| # | Critério | Como o professor confere |
|---|---|---|
| 1 | O contexto chega por injeção | O `PacientesController` tem `private readonly ClinicaContext _context;` atribuído no construtor, e em nenhum lugar do arquivo aparece `new ClinicaContext(` |
| 2 | A listagem vem do banco | `/Pacientes` exibe os pacientes em ordem alfabética e o `SELECT` correspondente aparece no log do terminal |
| 3 | As operações de banco são assíncronas | Toda action que toca o banco é `async Task<IActionResult>` e usa `await` com os métodos terminados em `Async` |
| 4 | O cadastro persiste | Um paciente cadastrado pela tela aparece em `SELECT * FROM clinicavida.Pacientes` no MySQL Workbench |
| 5 | A edição persiste | Alterar o telefone e recarregar a listagem mostra o valor novo, e o banco confirma |
| 6 | A exclusão exige confirmação | O botão de excluir está dentro de um `<form method="post">`; passar o mouse sobre ele não revela URL de exclusão |
| 7 | O Post-Redirect-Get está aplicado | Depois de cadastrar, editar ou excluir, apertar F5 não duplica registro nem faz o navegador perguntar sobre reenvio |
| 8 | A mensagem de sucesso aparece uma vez | A mensagem de `TempData` é exibida na listagem e desaparece no F5 seguinte |
| 9 | O id inexistente é tratado | `/Pacientes/Details/9999`, `/Pacientes/Edit/9999` e `/Pacientes/Delete/9999` devolvem 404 |
| 10 | O trabalho foi enviado | A branch `feature/crud-pacientes` aparece no seu fork no GitHub, com o commit de sua autoria |

---

## Se algo der errado

- **`InvalidOperationException: Unable to resolve service for type
  'ClinicaVida.Web.Data.ClinicaContext'`**: o contêiner não sabe construir o
  contexto. Falta o `builder.Services.AddDbContext<ClinicaContext>(...)` no
  `Program.cs`, que é entregável da Aula 11, ou ele foi escrito depois do
  `builder.Build()`.
- **A tela redireciona, a mensagem aparece e o registro não está no banco**:
  faltou `await _context.SaveChangesAsync()`. `Add`, `Update` e `Remove`
  apenas marcam a intenção no rastreador de mudanças; nenhum deles vai ao
  banco sozinho.
- **A edição cria um paciente novo em vez de alterar o existente**: falta o
  `<input type="hidden" asp-for="Id" />` na View de edição. Sem ele o `Id`
  chega zerado e o EF Core trata a entidade como nova.
- **`The instance of entity type 'Paciente' cannot be tracked because another
  instance with the same key value is already being tracked`**: a mesma
  entidade foi carregada do banco e depois passada de novo para `Update` na
  mesma requisição. No POST de `Edit`, use o objeto que veio do formulário e
  não carregue o registro antes.
- **O navegador pergunta se deseja reenviar o formulário ao apertar F5**: a
  action de POST devolveu uma View em vez de redirecionar. Troque o
  `return View(...)` do caminho de sucesso por `RedirectToAction(nameof(Index))`.
- **A mensagem de sucesso não aparece**: `TempData` foi gravado depois do
  `return`, ou a View da listagem não tem o bloco
  `@if (TempData["Sucesso"] != null)`.
- **`MySqlException: Access denied` ou `Unable to connect to any of the
  specified MySQL hosts`**: o serviço do MySQL não está rodando, ou a
  connection string em `DefaultConnection` mudou. É o mesmo diagnóstico da
  Aula 11.
