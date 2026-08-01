# Laboratório da Aula 15

## Disciplina: Desenvolvimento Web
**Prof. José Romualdo | Uninove, Universidade Nove de Julho**

### Case: Clínica Vida+ (Fase 14, o controle de acesso)

Na Aula 14 você entregou a consulta de médicos e de horários livres por AJAX,
sem recarregar a página. A aplicação ficou fluida, e continuou aberta: qualquer
pessoa que digite o endereço abre a agenda da clínica, lista o CPF e o telefone
dos pacientes e chega a um botão que exclui cadastro de gente de verdade.

Hoje essa porta é fechada, e ela tem duas fechaduras. **Autenticação** é provar
quem se é. **Autorização** é decidir o que essa pessoa pode fazer. O laboratório
instala o ASP.NET Core Identity no projeto que já existe, faz o `ClinicaContext`
passar a herdar de `IdentityDbContext<IdentityUser>`, escreve as telas de conta
à mão em MVC, cria os perfis `Recepcao` e `Medico` e protege a área da recepção.

**Duração:** 60 minutos, individual, nos Ciclos 3 e 4.

---

## Pré-requisitos

- O fork de `josercf/uninove-2026-2-clinica-vida` clonado na sua máquina.
- O entregável da Aula 14 na `main`, com o banco `clinicavida` funcionando.
- O SDK do .NET 10 e o serviço do MySQL rodando.
- VS Code e o MySQL Workbench, para conferir as tabelas criadas.

Confirme o ponto de partida antes de começar:

```bash
dotnet --version          # precisa começar com 10.
dotnet ef database update # não pode ter migration pendente
```

---

## Passo 1: a branch e a configuração (10 min)

```bash
git checkout main && git pull
git checkout -b feature/autenticacao
dotnet add package Microsoft.AspNetCore.Identity.EntityFrameworkCore
```

Em `Program.cs`, registre o Identity **antes** do `builder.Build()`. O
`AddEntityFrameworkStores<ClinicaContext>()` é o que diz ao Identity onde
guardar usuários e perfis: no seu contexto, no seu banco.

```csharp
using Microsoft.AspNetCore.Identity;

builder.Services.AddIdentity<IdentityUser, IdentityRole>(opcoes =>
    {
        opcoes.Password.RequiredLength = 8;
        opcoes.Password.RequireNonAlphanumeric = false;
        opcoes.User.RequireUniqueEmail = true;
    })
    .AddEntityFrameworkStores<ClinicaContext>()
    .AddDefaultTokenProviders();

builder.Services.ConfigureApplicationCookie(opcoes =>
{
    opcoes.LoginPath = "/Conta/Login";
    opcoes.AccessDeniedPath = "/Conta/AcessoNegado";
    opcoes.ExpireTimeSpan = TimeSpan.FromHours(2);
});
```

Depois do `builder.Build()`, no pipeline:

```csharp
app.UseRouting();

app.UseAuthentication();   // lê o cookie e monta o HttpContext.User
app.UseAuthorization();    // confere [Authorize] e decide

app.UseSession();          // a sessão da Aula 13 continua onde estava
```

**A ordem não é decorativa.** `UseAuthentication` precisa vir antes de
`UseAuthorization`: invertidos, a autorização decide com o `HttpContext.User`
ainda vazio e todo mundo é barrado, inclusive quem acabou de entrar.

Rode `dotnet run`. A aplicação precisa subir normalmente; nada mudou na tela
ainda.

---

## Passo 2: um contexto só, e a migration (10 min)

O Identity precisa de um `DbContext`. Em vez de criar um segundo, o contexto
que você escreveu na Aula 11 muda de classe base. Uma cadeia de migrations, um
banco coerente, e a mesma classe que você já conhece.

Em `Data/ClinicaContext.cs`:

```csharp
using ClinicaVida.Web.Models;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

namespace ClinicaVida.Web.Data;

public class ClinicaContext : IdentityDbContext<IdentityUser>
{
    public ClinicaContext(DbContextOptions<ClinicaContext> opcoes)
        : base(opcoes) { }

    public DbSet<Especialidade> Especialidades => Set<Especialidade>();
    public DbSet<Medico> Medicos => Set<Medico>();
    public DbSet<Paciente> Pacientes => Set<Paciente>();
    public DbSet<Consulta> Consultas => Set<Consulta>();

    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder);   // obrigatória, e é a primeira linha

        builder.Entity<Especialidade>().HasData(
            // o mesmo HasData da Aula 11, sem nenhuma alteração
        );
    }
}
```

`base.OnModelCreating(builder)` é o que mapeia as tabelas do Identity. Sem essa
linha a aplicação nem sobe: o erro é
`The entity type 'IdentityUserLogin<string>' requires a primary key to be
defined`.

Gere a migration e **leia o arquivo gerado** antes de aplicar:

```bash
dotnet ef migrations add IdentityClinicaVida
dotnet ef database update
```

A migration só pode conter `CreateTable` das sete tabelas do Identity. Se
aparecer `DropTable` de alguma das suas quatro, pare: o modelo saiu do lugar, e
aplicar levaria os dados junto.

Confira no Workbench:

```sql
SHOW TABLES FROM clinicavida;
```

Você precisa ver as suas quatro tabelas, intactas, mais `AspNetUsers`,
`AspNetRoles`, `AspNetUserRoles`, `AspNetUserClaims`, `AspNetRoleClaims`,
`AspNetUserLogins` e `AspNetUserTokens`.

---

## Passo 3: registro, login e logout (18 min)

As telas de conta são **MVC, escritas à mão**: Controller, action e View, como
em toda a disciplina. Quem conversa com o Identity é o `SignInManager`, para
validar a senha e emitir o cookie, e o `UserManager`, para criar o usuário.

### Os ViewModels

`Models/LoginViewModel.cs`:

```csharp
using System.ComponentModel.DataAnnotations;

namespace ClinicaVida.Web.Models;

public class LoginViewModel
{
    [Required(ErrorMessage = "Informe o e-mail.")]
    [EmailAddress(ErrorMessage = "E-mail inválido.")]
    public string Email { get; set; } = string.Empty;

    [Required(ErrorMessage = "Informe a senha.")]
    [DataType(DataType.Password)]
    public string Senha { get; set; } = string.Empty;

    [Display(Name = "Continuar conectado")]
    public bool Lembrar { get; set; }
}
```

`Models/RegistroViewModel.cs`:

```csharp
using System.ComponentModel.DataAnnotations;

namespace ClinicaVida.Web.Models;

public class RegistroViewModel
{
    [Required(ErrorMessage = "Informe o e-mail.")]
    [EmailAddress(ErrorMessage = "E-mail inválido.")]
    public string Email { get; set; } = string.Empty;

    [Required(ErrorMessage = "Informe a senha.")]
    [StringLength(100, MinimumLength = 8,
        ErrorMessage = "A senha precisa de pelo menos 8 caracteres.")]
    [DataType(DataType.Password)]
    public string Senha { get; set; } = string.Empty;

    [DataType(DataType.Password)]
    [Display(Name = "Confirmação da senha")]
    [Compare(nameof(Senha), ErrorMessage = "As senhas não conferem.")]
    public string Confirmacao { get; set; } = string.Empty;
}
```

### O Controller

`Controllers/ContaController.cs`:

```csharp
using ClinicaVida.Web.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;

namespace ClinicaVida.Web.Controllers;

[AllowAnonymous]
public class ContaController : Controller
{
    private readonly SignInManager<IdentityUser> _signInManager;
    private readonly UserManager<IdentityUser> _userManager;

    public ContaController(SignInManager<IdentityUser> signInManager,
                           UserManager<IdentityUser> userManager)
    {
        _signInManager = signInManager;
        _userManager = userManager;
    }

    [HttpGet]
    public IActionResult Login(string? returnUrl = null)
    {
        ViewData["ReturnUrl"] = returnUrl;
        return View();
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Login(LoginViewModel modelo,
                                           string? returnUrl = null)
    {
        if (!ModelState.IsValid) return View(modelo);

        var resultado = await _signInManager.PasswordSignInAsync(
            modelo.Email, modelo.Senha, modelo.Lembrar,
            lockoutOnFailure: true);

        if (resultado.Succeeded)
        {
            if (!string.IsNullOrEmpty(returnUrl) && Url.IsLocalUrl(returnUrl))
                return Redirect(returnUrl);

            return RedirectToAction("Index", "Home");
        }

        ModelState.AddModelError("", "E-mail ou senha inválidos.");
        return View(modelo);
    }

    [HttpGet]
    public IActionResult Registrar() => View();

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Registrar(RegistroViewModel modelo)
    {
        if (!ModelState.IsValid) return View(modelo);

        var usuario = new IdentityUser
        {
            UserName = modelo.Email,
            Email = modelo.Email
        };

        var resultado = await _userManager.CreateAsync(usuario, modelo.Senha);

        if (resultado.Succeeded)
        {
            // A conta nasce autenticada e SEM perfil, de propósito. Quem se
            // cadastra sozinho não pode entrar na área da recepção: perfil é
            // concedido, não pedido. É isso que você vai provar no passo de
            // teste, entrando com esta conta e recebendo acesso negado.
            await _signInManager.SignInAsync(usuario, isPersistent: false);
            return RedirectToAction("Index", "Home");
        }

        foreach (var erro in resultado.Errors)
            ModelState.AddModelError("", erro.Description);

        return View(modelo);
    }

    [HttpPost]
    [Authorize]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Logout()
    {
        await _signInManager.SignOutAsync();
        return RedirectToAction("Index", "Home");
    }

    [HttpGet]
    public IActionResult AcessoNegado() => View();
}
```

Três pontos que valem a leitura com calma:

1. A mensagem de erro é **genérica de propósito**. "Esse e-mail não existe"
   conta a um atacante quais contas a clínica tem.
2. `CreateAsync` gera o salt, aplica a derivação de chave e grava o resultado
   em `PasswordHash`. Você não escreve uma linha de hash.
3. `Logout` é **POST**, e não link. Logout por GET é apagado por
   pré-carregamento do navegador e derruba o usuário sozinho.

### As Views

`Views/Conta/Login.cshtml`:

```cshtml
@model ClinicaVida.Web.Models.LoginViewModel
@{ ViewData["Title"] = "Entrar"; }

<h1>Entrar</h1>

<form asp-action="Login" method="post">
    <input type="hidden" name="returnUrl" value="@ViewData["ReturnUrl"]" />
    <div asp-validation-summary="ModelOnly"></div>

    <label asp-for="Email"></label>
    <input asp-for="Email" />
    <span asp-validation-for="Email"></span>

    <label asp-for="Senha"></label>
    <input asp-for="Senha" />
    <span asp-validation-for="Senha"></span>

    <label><input asp-for="Lembrar" type="checkbox" /> Continuar conectado</label>

    <button type="submit">Entrar</button>
    <a asp-action="Registrar">Criar uma conta</a>
</form>
```

`Views/Conta/Registrar.cshtml` é o mesmo formulário com os três campos do
`RegistroViewModel`, e `Views/Conta/AcessoNegado.cshtml` é uma página curta,
dizendo que a conta atual não tem permissão para aquela área e oferecendo o
caminho de volta para a home.

Registre uma conta, faça logout, entre de novo e depois olhe a tabela:

```sql
SELECT Id, UserName, PasswordHash FROM clinicavida.AspNetUsers;
```

A senha que você digitou não está ali, nem em nenhuma outra coluna. É esse o
objetivo.

---

## Passo 4: perfis e usuário inicial (12 min)

Ciclo 4, sozinho. Perfil é linha na tabela `AspNetRoles`: enquanto ninguém
criar, `[Authorize(Roles = "Recepcao")]` barra todo mundo, inclusive você.

`Data/SeedIdentity.cs`:

```csharp
using Microsoft.AspNetCore.Identity;

namespace ClinicaVida.Web.Data;

public static class SeedIdentity
{
    public static async Task CriarPerfisEUsuarioInicialAsync(IServiceProvider s)
    {
        var roleManager = s.GetRequiredService<RoleManager<IdentityRole>>();
        var userManager = s.GetRequiredService<UserManager<IdentityUser>>();
        var config = s.GetRequiredService<IConfiguration>();

        foreach (var perfil in new[] { "Recepcao", "Medico" })
            if (!await roleManager.RoleExistsAsync(perfil))
                await roleManager.CreateAsync(new IdentityRole(perfil));

        const string email = "recepcao@clinicavida.local";

        if (await userManager.FindByEmailAsync(email) is null)
        {
            var senha = config["SeedRecepcao:Senha"]
                ?? throw new InvalidOperationException(
                    "Defina SeedRecepcao:Senha no user-secrets.");

            var usuario = new IdentityUser
            {
                UserName = email,
                Email = email,
                EmailConfirmed = true
            };

            await userManager.CreateAsync(usuario, senha);
            await userManager.AddToRoleAsync(usuario, "Recepcao");
        }
    }
}
```

E, em `Program.cs`, logo depois do `builder.Build()` e antes do `app.Run()`:

```csharp
using (var escopo = app.Services.CreateScope())
{
    await SeedIdentity.CriarPerfisEUsuarioInicialAsync(escopo.ServiceProvider);
}
```

### A senha inicial não fica no código

Ela é lida da configuração, e no laboratório de hoje a configuração é o
`user-secrets`, um arquivo fora da pasta do projeto, que o Git nunca enxerga:

```bash
dotnet user-secrets init
dotnet user-secrets set "SeedRecepcao:Senha" "<escolha uma senha local sua>"
```

Escolha um valor com pelo menos 8 caracteres, com letra maiúscula, minúscula e
número, que é o que as opções do Passo 1 exigem. **Este usuário é didático e
local:** ele existe para você conseguir entrar na aplicação da sua máquina no
primeiro acesso, e o e-mail `@clinicavida.local` nem é um domínio real. Em um
sistema de verdade, o primeiro acesso é criado por outro caminho, com senha
trocada no primeiro login. Nunca commite senha, de qualquer natureza, em
nenhum arquivo.

Suba a aplicação e confira:

```sql
SELECT Name FROM clinicavida.AspNetRoles;
SELECT * FROM clinicavida.AspNetUserRoles;
```

---

## Passo 5: proteger as telas e adaptar o menu (10 min)

Agora vale a matriz de acesso montada no Ciclo 1. No ASP.NET Core, **público é
o padrão**: protegido é o que você marcou.

```csharp
[Authorize(Roles = "Recepcao")]
public class PacientesController : Controller
{
    // as oito actions da Aula 12 ficam protegidas de uma vez
}
```

```csharp
[Authorize(Roles = "Recepcao")]
public class ConsultasController : Controller
{
    [AllowAnonymous]
    public IActionResult Solicitar() => View();   // o paciente continua entrando aqui

    // a agenda completa da clínica segue exigindo o perfil Recepcao
}
```

As páginas institucionais e a lista de especialidades continuam sem atributo
nenhum, e por isso continuam públicas.

No `Views/Shared/_Layout.cshtml`:

```cshtml
@if (User.Identity is not null && User.Identity.IsAuthenticated)
{
    @if (User.IsInRole("Recepcao"))
    {
        <a asp-controller="Pacientes" asp-action="Index">Pacientes</a>
        <a asp-controller="Consultas" asp-action="Index">Agenda</a>
    }
    <form asp-controller="Conta" asp-action="Logout" method="post">
        <button type="submit">Sair, @User.Identity.Name</button>
    </form>
}
else
{
    <a asp-controller="Conta" asp-action="Login">Entrar</a>
}
```

Esconder o link é experiência de uso, **não** é segurança: a URL continua
existindo e pode ser digitada. Quem protege de verdade é o `[Authorize]` no
servidor.

---

## O teste dos três acessos

Você vai precisar de **três** situações, e é aqui que a aula fecha. Repare que
a conta que você mesmo criou pela tela de registro **não tem perfil nenhum**:
ela serve justamente para provar que estar autenticado não é estar autorizado.

1. **Anônimo:** abra uma janela anônima, sem login.
2. **Sem perfil:** entre com a conta que você criou no registro.
3. **Recepção:** entre com o usuário semeado na subida da aplicação.

Para a quarta coluna, crie uma conta e associe-a ao perfil `Medico` pelo
Workbench, inserindo a linha correspondente em `AspNetUserRoles`, ou por um
`AddToRoleAsync` temporário. Não existe tela de administração de usuários nesta
disciplina, e conceder perfil pelo banco é justamente o que deixa claro que
perfil é concedido por quem administra, não escolhido por quem se cadastra.

Faça o teste **digitando a URL na barra de endereços**, sem passar pelo menu:

| Endereço | Anônimo | Autenticado sem perfil | Perfil `Recepcao` | Perfil `Medico` |
|---|---|---|---|---|
| `/` | abre | abre | abre | abre |
| `/Pacientes` | vai para o login | acesso negado | abre | acesso negado |
| `/Consultas` | vai para o login | acesso negado | abre | acesso negado |
| `/Consultas/Solicitar` | abre | abre | abre | abre |

A coluna do meio é a mais importante da tabela: o usuário provou quem é, e
mesmo assim não passa. **Autenticação e autorização são coisas diferentes**, e
esta linha é a demonstração disso.

Se `/Pacientes` abrir para o anônimo, o atributo não está no lugar, ou o
`UseAuthentication` está depois do `UseAuthorization`.

---

## Commit e push

```bash
git add Data/ Controllers/ContaController.cs Views/Conta/ Models/ \
        Views/Shared/_Layout.cshtml Program.cs Migrations/
git commit -m "feat: autenticacao e autorizacao por perfil com Identity"
git push -u origin feature/autenticacao
```

Antes do commit, confira que nenhum arquivo versionado tem senha escrita:

```bash
git diff --cached | grep -i "senha\s*=\s*\"" || echo "nenhuma senha literal"
```

---

## Entregável

Login e logout funcionando, com a área da recepção protegida por perfil e o
menu adaptado ao usuário, na branch `feature/autenticacao`, commitado e enviado
ao seu fork. Especificamente:

- **1** `ClinicaContext` herdando de `IdentityDbContext<IdentityUser>`, com
  `base.OnModelCreating(builder)`.
- **1** migration `IdentityClinicaVida` aplicada, com as **7** tabelas do
  Identity criadas.
- **1** `ContaController` com **6** actions: `Login` em GET e POST, `Registrar`
  em GET e POST, `Logout` em POST e `AcessoNegado`.
- **3** Views em `Views/Conta/`: `Login`, `Registrar` e `AcessoNegado`.
- **2** perfis semeados, `Recepcao` e `Medico`, e **1** usuário inicial
  associado a `Recepcao`.
- **2** Controllers protegidos com `[Authorize(Roles = "Recepcao")]`.

### Critérios de aceitação

| # | Critério | Como o professor confere |
|---|---|---|
| 1 | Existe um contexto só | `Data/ClinicaContext.cs` herda de `IdentityDbContext<IdentityUser>` e o projeto não tem um segundo `DbContext` |
| 2 | A classe base é chamada | `OnModelCreating` começa por `base.OnModelCreating(builder)`, e a aplicação sobe sem erro de chave primária |
| 3 | A migration foi aplicada | `SHOW TABLES FROM clinicavida;` lista as quatro tabelas do case mais as sete `AspNet...` |
| 4 | Os dados anteriores sobreviveram | Pacientes e consultas cadastrados antes da Aula 15 continuam nas tabelas |
| 5 | O registro grava hash | `SELECT PasswordHash FROM AspNetUsers;` mostra um valor longo, e a senha digitada não aparece em coluna nenhuma |
| 6 | O login e o logout funcionam | Entrar pela tela leva à home com o nome do usuário no menu; sair volta a exibir o link Entrar |
| 7 | O logout é POST | O botão Sair está dentro de um `<form method="post">`, e não é um link |
| 8 | O anônimo é barrado | Digitar `/Pacientes` sem estar logado redireciona para `/Conta/Login` |
| 9 | O perfil errado é barrado | Logado como `Medico`, `/Pacientes` leva ao acesso negado, e não à listagem |
| 10 | O público continua público | A home, a lista de especialidades e a solicitação de agendamento abrem sem login |
| 11 | O menu acompanha o usuário | Anônimo não vê os links da recepção; a conta da recepção vê |
| 12 | Nenhuma senha foi commitada | Nenhum arquivo versionado tem senha literal; a senha inicial vem do `user-secrets` |
| 13 | O trabalho foi enviado | A branch `feature/autenticacao` aparece no seu fork no GitHub, com o commit de sua autoria |

---

## Se algo der errado

- **`The entity type 'IdentityUserLogin<string>' requires a primary key to be
  defined`**: falta `base.OnModelCreating(builder)` no `ClinicaContext`, ou ele
  foi escrito depois do seu `HasData` e sobrescrito. É a primeira linha do
  método.
- **`InvalidOperationException: Unable to resolve service for type
  'Microsoft.AspNetCore.Identity.SignInManager...'`**: o `AddIdentity` não foi
  registrado em `Program.cs`, ou foi escrito depois do `builder.Build()`.
- **Todo mundo é redirecionado para o login, inclusive quem acabou de entrar**:
  `app.UseAuthentication()` está depois de `app.UseAuthorization()`. A
  autorização decide com o `HttpContext.User` ainda vazio.
- **O login diz "E-mail ou senha inválidos" com a senha certa**: o usuário foi
  criado com `UserName` diferente do e-mail, ou a senha do seed não é a que
  você está digitando. Confira `SELECT UserName FROM AspNetUsers;`.
- **`[Authorize(Roles = "Recepcao")]` barra até o usuário da recepção**: o
  perfil não existe em `AspNetRoles`, o vínculo não existe em
  `AspNetUserRoles`, ou o nome está escrito diferente. É sensível a acento e a
  maiúscula: `Recepcao`, sem cedilha e sem til, como no seed.
- **`InvalidOperationException: Defina SeedRecepcao:Senha no user-secrets`**: o
  seed não encontrou a senha na configuração. Rode `dotnet user-secrets init` e
  o `set` do Passo 4, na pasta do projeto.
- **`Specified key was too long`, ao aplicar a migration**: o MySQL da sua
  máquina é antigo demais para índice de 255 caracteres em `utf8mb4`. Use o
  MySQL 8, que é o da ementa.
- **A senha é recusada no registro com uma lista de exigências**: são as regras
  de `opcoes.Password` do Passo 1. Ajuste a senha, e não as regras.
- **O menu some depois do login**: `User.Identity.Name` é nulo porque o cookie
  não foi emitido. Confira se `SignInAsync` ou `PasswordSignInAsync` foi
  realmente chamado, e se `resultado.Succeeded` era verdadeiro.
