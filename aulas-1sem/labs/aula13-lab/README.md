# Laboratório da Aula 13

## Disciplina: Desenvolvimento Web
**Prof. José Romualdo | Uninove, Universidade Nove de Julho**

### Case: Clínica Vida+ (Fase 12, o agendamento em duas etapas)

Na Aula 12 você entregou o CRUD completo de `Paciente` persistindo no banco
`clinicavida`, com Post-Redirect-Get nos três POST e a mensagem de sucesso em
`TempData`. A aplicação guarda dados, e ainda não guarda contexto: cada
requisição chega ao servidor como se fosse a primeira da vida.

Hoje abre o **Módulo 3**, e a aplicação passa a reconhecer o navegador entre
uma requisição e outra. O agendamento vira um fluxo de duas etapas: a primeira
escolhe especialidade e médico e guarda a escolha na **sessão**; a segunda
recupera a sessão, completa a consulta com paciente, data e horário, grava no
banco e limpa o que ficou para trás. Por cima disso, um **cookie** guarda a
unidade preferida da clínica de uma visita para a próxima.

**Duração:** 60 minutos, individual, nos Ciclos 3 e 4.

---

## Pré-requisitos

- O fork de `josercf/uninove-2026-2-clinica-vida` clonado na sua máquina.
- O entregável da Aula 12 na `main`: o `PacientesController` completo e o banco
  `clinicavida` respondendo.
- O SDK do .NET 10 e o serviço do MySQL rodando.
- Pelo menos **um paciente cadastrado** pela tela da Aula 12. Sem paciente no
  banco, a etapa 2 não tem o que selecionar.

Confirme o ponto de partida antes de começar:

```bash
dotnet --version           # precisa começar com 10.
dotnet ef database update  # não pode ter migration pendente
dotnet run
```

Abra `/Pacientes` **na porta que o seu terminal imprimiu** (a sua não é a mesma
do colega ao lado: `dotnet new mvc` sorteia as portas em
`Properties/launchSettings.json`; neste roteiro `7145` aparece só como
exemplo). A listagem precisa carregar com pelo menos um paciente.

### Contrato técnico, que não muda

| O quê | Valor |
|---|---|
| Projeto e namespace raiz | `ClinicaVida.Web` |
| `DbContext` | `ClinicaContext`, em `Data/ClinicaContext.cs` |
| Banco | `clinicavida`, no MySQL |
| Connection string | chave `DefaultConnection` |
| Provedor EF Core | `Pomelo.EntityFrameworkCore.MySql` |
| Migration nova de hoje | `MedicosIniciais` |
| Branch | `feature/sessao-agendamento` |

---

## Passo 1: a branch e a sessão no pipeline (10 min)

```bash
git switch main && git pull
git switch -c feature/sessao-agendamento
```

A sessão do ASP.NET Core precisa de duas coisas: um **lugar para guardar** o
conteúdo e um **middleware** que, a cada requisição, encontre a sessão certa
pelo identificador que veio no cookie.

Em `Program.cs`, **antes** do `builder.Build()`:

```csharp
builder.Services.AddDistributedMemoryCache();

builder.Services.AddSession(options =>
{
    options.IdleTimeout = TimeSpan.FromMinutes(20);
    options.Cookie.Name = ".ClinicaVida.Sessao";
    options.Cookie.HttpOnly = true;
    options.Cookie.IsEssential = true;
});
```

O que cada linha faz:

- `AddDistributedMemoryCache` registra o armazenamento da sessão na **memória
  do processo**. O nome tem "distributed" porque a interface é a mesma de um
  cache distribuído de verdade, como Redis; a implementação registrada aqui é
  local. Consequência prática: reiniciar a aplicação apaga todas as sessões.
- `IdleTimeout` é a janela de **inatividade**, não a duração total. Cada
  requisição que toca a sessão reinicia a contagem.
- `Cookie.HttpOnly = true` esconde o identificador do JavaScript da página.
- `Cookie.IsEssential = true` diz que este cookie é indispensável para o
  funcionamento da aplicação, e por isso não depende do aceite do aviso de
  cookies.

Agora o middleware, no pipeline, **depois** de `UseRouting` e **antes** do
mapeamento das rotas:

```csharp
app.UseRouting();

app.UseSession();          // esta linha é nova

app.UseAuthorization();
app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");
```

A ordem não é decoração. `HttpContext.Session` só existe porque o middleware de
sessão passou antes na cadeia; se `UseSession` vier depois do mapeamento das
rotas, ou não vier, o primeiro acesso à sessão lança
`InvalidOperationException: Session has not been configured for this application
or request`.

Suba a aplicação, abra qualquer página e confira no DevTools, aba
**Application**, seção **Cookies**: o cookie `.ClinicaVida.Sessao` precisa
aparecer, com a coluna `HttpOnly` marcada.

---

## Passo 2: médicos no banco (10 min)

A etapa 1 pede uma lista de médicos, e a tabela `Medicos` está vazia desde a
Aula 11: a migration `EspecialidadesIniciais` semeou apenas as quatro
especialidades. Semeie os médicos do mesmo jeito, pela migration, para que todo
mundo da turma tenha os mesmos dados.

Em `Data/ClinicaContext.cs`, dentro do `OnModelCreating` que já existe, logo
depois do `HasData` das especialidades:

```csharp
modelBuilder.Entity<Medico>().HasData(
    new Medico { Id = 1, Nome = "Dra. Helena Braga",   Crm = "SP-100234", EspecialidadeId = 1 },
    new Medico { Id = 2, Nome = "Dr. Paulo Nakano",    Crm = "SP-118907", EspecialidadeId = 2 },
    new Medico { Id = 3, Nome = "Dra. Renata Vasques", Crm = "SP-127450", EspecialidadeId = 3 },
    new Medico { Id = 4, Nome = "Dr. Caio Bertoldi",   Crm = "SP-133098", EspecialidadeId = 4 }
);
```

Os `EspecialidadeId` de 1 a 4 apontam para Clínica Geral, Cardiologia,
Pediatria e Dermatologia, exatamente na ordem semeada na Aula 11. Como em todo
`HasData`, a chave primária é escrita à mão: o EF Core precisa do `Id` para
saber se aquela linha já existe.

```bash
dotnet ef migrations add MedicosIniciais
dotnet ef database update
```

Confira no MySQL Workbench antes de seguir:

```sql
SELECT * FROM clinicavida.Medicos;   -- 4 linhas
```

---

## Passo 3: a etapa 1 do agendamento (15 min)

O `ConsultasController` nasceu na Aula 10 lendo listas de memória. Agora ele
recebe o `ClinicaContext` por injeção, como o `PacientesController` da Aula 12,
e as listas passam a vir do banco.

Reescreva o começo de `Controllers/ConsultasController.cs`:

```csharp
using ClinicaVida.Web.Data;
using ClinicaVida.Web.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;

namespace ClinicaVida.Web.Controllers;

public class ConsultasController : Controller
{
    private const string ChaveEspecialidade = "AgendamentoEspecialidadeId";
    private const string ChaveMedico = "AgendamentoMedicoId";
    private const string CookieUnidade = "unidade-preferida";

    private static readonly string[] Unidades =
        { "Tatuapé", "Santana", "Vila Mariana" };

    private readonly ClinicaContext _context;

    public ConsultasController(ClinicaContext context)
    {
        _context = context;
    }
}
```

As três chaves viram constantes porque texto solto repetido em cinco lugares é
erro de digitação esperando acontecer, e o compilador não avisa quando
`"AgendamentoMedicoId"` vira `"AgendamentoMedicold"` em um deles.

A etapa 1 em GET monta as duas listas e já deixa a unidade do cookie
selecionada:

```csharp
[HttpGet]
public async Task<IActionResult> Agendar(int? especialidadeId)
{
    var especialidades = await _context.Especialidades
        .OrderBy(e => e.Nome)
        .ToListAsync();

    var medicos = await _context.Medicos
        .Where(m => especialidadeId == null
                 || m.EspecialidadeId == especialidadeId)
        .OrderBy(m => m.Nome)
        .ToListAsync();

    ViewBag.Especialidades = new SelectList(especialidades, "Id", "Nome", especialidadeId);
    ViewBag.Medicos = new SelectList(medicos, "Id", "Nome");
    ViewBag.Unidades = new SelectList(Unidades, Request.Cookies[CookieUnidade]);

    return View();
}
```

E a etapa 1 em POST guarda a escolha na sessão, grava o cookie e redireciona:

```csharp
[HttpPost]
[ValidateAntiForgeryToken]
public IActionResult Agendar(int especialidadeId, int medicoId, string unidade)
{
    if (medicoId <= 0)
    {
        TempData["Aviso"] = "Selecione um médico para continuar.";
        return RedirectToAction(nameof(Agendar), new { especialidadeId });
    }

    HttpContext.Session.SetInt32(ChaveEspecialidade, especialidadeId);
    HttpContext.Session.SetInt32(ChaveMedico, medicoId);

    Response.Cookies.Append(CookieUnidade, unidade, new CookieOptions
    {
        Expires = DateTimeOffset.UtcNow.AddDays(30),
        HttpOnly = true,
        Secure = true,
        SameSite = SameSiteMode.Lax,
        IsEssential = true
    });

    return RedirectToAction(nameof(AgendarHorario));
}
```

Repare que a etapa 1 termina em `RedirectToAction`, e não em `View`: é o mesmo
Post-Redirect-Get da Aula 12, agora aplicado a um fluxo de várias telas.

Substitua `Views/Consultas/Agendar.cshtml` inteira. A View da Aula 10 tinha os
cinco campos da consulta; a da etapa 1 tem três:

```cshtml
@{ ViewData["Title"] = "Agendar consulta, etapa 1 de 2"; }

<h1>Agendar consulta</h1>
<p>Etapa 1 de 2: especialidade, médico e unidade.</p>

@if (TempData["Aviso"] != null)
{
    <p class="alerta-aviso">@TempData["Aviso"]</p>
}

<label for="especialidadeId">Especialidade</label>
<select id="especialidadeId" asp-items="ViewBag.Especialidades"
        onchange="location.href = '/Consultas/Agendar?especialidadeId=' + this.value;">
    <option value="">Todas as especialidades</option>
</select>

<form asp-action="Agendar" method="post">
    <input type="hidden" name="especialidadeId" value="@Context.Request.Query["especialidadeId"]" />

    <label for="medicoId">Médico</label>
    <select id="medicoId" name="medicoId" asp-items="ViewBag.Medicos">
        <option value="">Selecione o médico</option>
    </select>

    <label for="unidade">Unidade da clínica</label>
    <select id="unidade" name="unidade" asp-items="ViewBag.Unidades"></select>

    <button type="submit">Continuar para data e horário</button>
</form>
```

O `onchange` recarrega a página inteira só para trocar a lista de médicos. É
proposital, e é exatamente o desperdício que a **Aula 14** vai eliminar com
`fetch`.

---

## Passo 4: a etapa 2 e a guarda de acesso (10 min)

Começa o Ciclo 4. A etapa 2 só existe se a etapa 1 tiver acontecido, e quem
sabe disso é a sessão.

```csharp
[HttpGet]
public async Task<IActionResult> AgendarHorario()
{
    var medicoId = HttpContext.Session.GetInt32(ChaveMedico);

    if (medicoId is null)
    {
        TempData["Aviso"] = "Comece pela escolha do médico.";
        return RedirectToAction(nameof(Agendar));
    }

    await CarregarEtapa2(medicoId.Value);

    return View(new Consulta { Data = DateTime.Today });
}

private async Task CarregarEtapa2(int medicoId)
{
    var medico = await _context.Medicos.FindAsync(medicoId);

    ViewBag.MedicoNome = medico?.Nome ?? "médico não encontrado";
    ViewBag.Pacientes = new SelectList(
        await _context.Pacientes.OrderBy(p => p.Nome).ToListAsync(), "Id", "Nome");
}
```

`GetInt32` devolve `int?`. O `null` tem **dois** significados, e os dois levam
ao mesmo lugar: ou a chave nunca foi gravada, porque a pessoa digitou a URL
direto na barra de endereços, ou os 20 minutos de inatividade passaram e a
sessão expirou. Nos dois casos, mandar de volta para a etapa 1 com um aviso é
melhor do que estourar uma exceção na cara do usuário.

`Views/Consultas/AgendarHorario.cshtml`:

```cshtml
@model ClinicaVida.Web.Models.Consulta
@{ ViewData["Title"] = "Agendar consulta, etapa 2 de 2"; }

<h1>Agendar consulta</h1>
<p>Etapa 2 de 2, com <strong>@ViewBag.MedicoNome</strong>.</p>

<form asp-action="AgendarHorario" method="post">
    <div asp-validation-summary="ModelOnly" class="erro-resumo"></div>

    <label asp-for="PacienteId"></label>
    <select asp-for="PacienteId" asp-items="ViewBag.Pacientes">
        <option value="">Selecione o paciente</option>
    </select>
    <span asp-validation-for="PacienteId" class="erro-campo"></span>

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
    <a asp-action="Agendar">Voltar para a etapa 1</a>
</form>

@section Scripts {
  <partial name="_ValidationScriptsPartial" />
}
```

**Não existe campo de médico nesta tela.** O médico veio da etapa 1 e mora na
sessão, no servidor. Um campo oculto com o `MedicoId` seria um valor vindo do
computador do usuário, editável em três cliques no DevTools.

Teste a guarda agora, antes de seguir: abra uma aba anônima e digite
`/Consultas/AgendarHorario` direto na barra de endereços. A aplicação precisa
levar você para a etapa 1 com o aviso, e não mostrar a tela nem quebrar.

---

## Passo 5: gravar a consulta e limpar a sessão (10 min)

```csharp
[HttpPost]
[ValidateAntiForgeryToken]
public async Task<IActionResult> AgendarHorario(Consulta consulta)
{
    var medicoId = HttpContext.Session.GetInt32(ChaveMedico);

    if (medicoId is null)
    {
        TempData["Aviso"] = "Sua sessão expirou. Comece de novo.";
        return RedirectToAction(nameof(Agendar));
    }

    consulta.MedicoId = medicoId.Value;

    // O formulário desta tela não tem campo de médico, então o binder deixou
    // MedicoId em zero e o [Range] da Aula 10 reprovou o campo. O valor certo
    // acabou de ser atribuído a partir da sessão, então esta entrada do
    // ModelState não descreve mais a realidade e sai da conta.
    ModelState.Remove(nameof(Consulta.MedicoId));

    if (!ModelState.IsValid)
    {
        await CarregarEtapa2(medicoId.Value);
        return View(consulta);
    }

    _context.Consultas.Add(consulta);
    await _context.SaveChangesAsync();

    HttpContext.Session.Remove(ChaveEspecialidade);
    HttpContext.Session.Remove(ChaveMedico);

    TempData["Sucesso"] = "Consulta agendada com sucesso.";
    return RedirectToAction(nameof(Confirmacao), new { id = consulta.Id });
}
```

A guarda aparece **de novo** aqui, e não é redundância: entre a tela ser
desenhada e o botão ser clicado podem passar 25 minutos, e a sessão expira em
20. Toda action que depende da sessão confere a sessão.

Limpar a sessão depois de gravar também não é detalhe. Sem o `Remove`, o
agendamento seguinte começaria com o médico da consulta anterior já escolhido,
e a recepção agendaria com o médico errado sem perceber.

A `Confirmacao` da Aula 10 lia de memória. Passe-a a ler do banco:

```csharp
public async Task<IActionResult> Confirmacao(int id)
{
    var consulta = await _context.Consultas.FirstOrDefaultAsync(c => c.Id == id);

    if (consulta == null) return NotFound();

    ViewBag.MedicoNome = (await _context.Medicos.FindAsync(consulta.MedicoId))?.Nome;
    ViewBag.PacienteNome = (await _context.Pacientes.FindAsync(consulta.PacienteId))?.Nome;

    return View(consulta);
}
```

As duas idas extras ao banco para descobrir dois nomes são feias de propósito:
é o problema das consultas N mais 1 em miniatura, e a **Aula 17** resolve isso
com `Include` em uma única consulta.

Em `Views/Consultas/Confirmacao.cshtml`, troque os identificadores crus pelos
nomes que acabaram de chegar, e mostre a mensagem de `TempData`:

```cshtml
@model ClinicaVida.Web.Models.Consulta

@if (TempData["Sucesso"] != null)
{
    <p class="alerta-sucesso">@TempData["Sucesso"]</p>
}

<h1>Consulta confirmada</h1>
<dl>
    <dt>Paciente</dt><dd>@ViewBag.PacienteNome</dd>
    <dt>Médico</dt><dd>@ViewBag.MedicoNome</dd>
    <dt>Data</dt><dd>@Model.Data.ToString("dd/MM/yyyy")</dd>
    <dt>Horário</dt><dd>@Model.Horario.ToString(@"hh\:mm")</dd>
</dl>
<a asp-action="Agendar">Agendar outra consulta</a>
```

Agende **duas** consultas seguidas. A segunda precisa começar com a etapa 1 em
branco; se ela já vier com o médico da primeira, faltou o `Remove`.

---

## Passo 6: o cookie da unidade preferida (5 min)

O cookie já é gravado no POST da etapa 1, no Passo 3. Falta usá-lo como valor
padrão e provar que ele sobrevive ao fechar o navegador.

Mostre a unidade no `Views/Shared/_Layout.cshtml`, no cabeçalho:

```cshtml
<span class="unidade-atual">
    Unidade: @(Context.Request.Cookies["unidade-preferida"] ?? "não escolhida")
</span>
```

O teste do cookie, na ordem:

1. Abra `/Consultas/Agendar`. O cabeçalho mostra "não escolhida".
2. Escolha médico e unidade e continue. O cabeçalho passa a mostrar a unidade.
3. Feche o navegador inteiro e reabra a aplicação. A unidade continua lá, e o
   `select` da etapa 1 já vem com ela selecionada.
4. No DevTools, aba **Application**, apague o cookie `unidade-preferida` e
   recarregue. Volta a "não escolhida".

O passo 3 é o que separa cookie de sessão: o cookie de sessão morre ao fechar
o navegador, porque não tem `Expires`; o de unidade tem 30 dias e sobrevive.

### Uma linha sobre `Secure` no ambiente de desenvolvimento

`Secure = true` manda o navegador enviar o cookie **apenas** por HTTPS. Rode a
aplicação pelo perfil HTTPS, na porta que o seu terminal imprimiu, e não pelo
HTTP: sobre `http://localhost`, o cookie é gravado e simplesmente nunca volta,
e você passa vinte minutos procurando um defeito que não existe.

---

## Commit e push

```bash
git add Program.cs Data/ Migrations/ Controllers/ConsultasController.cs Views/
git commit -m "feat: agendamento em duas etapas com sessao e cookie de unidade"
git push -u origin feature/sessao-agendamento
```

---

## Entregável

Agendamento em duas etapas usando sessão, mais o cookie de preferência de
unidade, na branch `feature/sessao-agendamento`, commitado e enviado ao seu
fork. Especificamente:

- **1** `Program.cs` com `AddDistributedMemoryCache`, `AddSession` e
  `UseSession` na posição correta do pipeline.
- **1** migration `MedicosIniciais`, com **4** médicos semeados.
- **4** actions no `ConsultasController`: `Agendar` em GET e em POST,
  `AgendarHorario` em GET e em POST, mais a `Confirmacao` migrada para o banco.
- **2** chaves de sessão, gravadas na etapa 1 e removidas depois de gravar.
- **2** guardas de acesso direto, uma no GET e outra no POST da etapa 2.
- **1** cookie `unidade-preferida`, com validade de 30 dias e os atributos
  `HttpOnly`, `Secure` e `SameSite`.

### Critérios de aceitação

| # | Critério | Como o professor confere |
|---|---|---|
| 1 | A sessão está registrada | `Program.cs` traz `AddDistributedMemoryCache()` e `AddSession(...)` antes do `builder.Build()`, com `IdleTimeout` definido |
| 2 | O middleware está na posição certa | `app.UseSession()` aparece depois de `app.UseRouting()` e antes do `MapControllerRoute`; a aplicação sobe e nenhuma tela lança `Session has not been configured` |
| 3 | O cookie de sessão existe e é protegido | No DevTools, aba Application, o cookie `.ClinicaVida.Sessao` aparece com `HttpOnly` marcado |
| 4 | Os médicos foram semeados por migration | `Migrations/` contém `<timestamp>_MedicosIniciais.cs` e `SELECT * FROM clinicavida.Medicos;` devolve 4 linhas |
| 5 | A etapa 1 lê do banco | Os `select` de especialidade e de médico da tela `/Consultas/Agendar` mostram os dados semeados, e o log do terminal mostra os `SELECT` correspondentes |
| 6 | A etapa 1 grava na sessão e redireciona | Concluir a etapa 1 leva a barra de endereços para `/Consultas/AgendarHorario`, e a tela mostra o nome do médico escolhido |
| 7 | O acesso direto à etapa 2 é barrado | Em aba anônima, `/Consultas/AgendarHorario` redireciona para a etapa 1 com aviso, sem exceção e sem tela em branco |
| 8 | A guarda existe também no POST | O POST de `AgendarHorario` relê a sessão antes de gravar; com a sessão limpa, o envio volta para a etapa 1 em vez de gravar consulta sem médico |
| 9 | A consulta é gravada com o médico da sessão | Depois do agendamento, `SELECT * FROM clinicavida.Consultas;` traz a linha nova com o `MedicoId` escolhido na etapa 1 |
| 10 | A sessão é limpa depois de gravar | O segundo agendamento seguido começa com a etapa 1 em branco, sem o médico da consulta anterior |
| 11 | O cookie de unidade persiste | Fechar e reabrir o navegador mantém a unidade escolhida no cabeçalho e já selecionada no `select` da etapa 1 |
| 12 | O cookie de unidade tem os atributos corretos | No DevTools, `unidade-preferida` aparece com data de expiração cerca de 30 dias à frente e com `HttpOnly` e `Secure` marcados |
| 13 | Nenhum dado sensível vai para cookie | Nenhum `Response.Cookies.Append` no projeto grava CPF, nome de paciente, especialidade ou diagnóstico |
| 14 | O trabalho foi enviado | A branch `feature/sessao-agendamento` aparece no seu fork no GitHub, com o commit de sua autoria |

---

## Se algo der errado

- **`InvalidOperationException: Session has not been configured for this
  application or request`**: falta `app.UseSession()`, ou ele foi escrito
  depois do `MapControllerRoute`. O middleware precisa passar antes de a action
  rodar.
- **O cookie de sessão não aparece no DevTools**: a sessão só é criada quando
  alguma coisa é **gravada** nela. Enquanto o código apenas lê, não há sessão e
  não há cookie. Conclua a etapa 1 e olhe de novo.
- **`HttpContext.Session.GetInt32` sempre devolve `null`, mesmo logo depois de
  gravar**: você está rodando sobre `http://localhost` com um cookie marcado
  como `Secure`, ou abriu a etapa 2 em outro navegador. Cookie não atravessa
  navegador nem janela anônima.
- **A etapa 2 volta para a etapa 1 mesmo tendo passado por ela**: as chaves não
  batem. Grave e leia sempre pelas constantes `ChaveEspecialidade` e
  `ChaveMedico`, nunca por texto solto.
- **A validação reprova o médico mesmo com médico escolhido**: falta o
  `ModelState.Remove(nameof(Consulta.MedicoId))` depois de atribuir o valor
  vindo da sessão. O `[Range(1, int.MaxValue)]` da Aula 10 reprovou o zero que
  o binder deixou.
- **A consulta é gravada com `MedicoId` igual a zero**: a atribuição
  `consulta.MedicoId = medicoId.Value;` está depois do `Add`, ou não existe.
- **O segundo agendamento já vem com o médico do primeiro**: faltou o
  `HttpContext.Session.Remove` das duas chaves depois do `SaveChangesAsync`.
- **`SqlException` ou `MySqlException` de chave estrangeira ao gravar**: o
  `PacienteId` enviado não existe na tabela `Pacientes`. Cadastre um paciente
  pela tela da Aula 12 antes de agendar.
- **A lista de pacientes está vazia na etapa 2**: mesma causa. O banco não tem
  paciente nenhum.
- **`dotnet ef migrations add MedicosIniciais` reclama de model pendente**:
  aplique primeiro o que já existe, com `dotnet ef database update`, e só
  depois gere a migration nova.
