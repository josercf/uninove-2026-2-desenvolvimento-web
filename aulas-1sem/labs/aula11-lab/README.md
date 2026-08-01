# Laboratório da Aula 11

## Disciplina: Desenvolvimento Web
**Prof. José Romualdo | Uninove, Universidade Nove de Julho**

### Case: Clínica Vida+ (Fase 10, persistência em MySQL)

Na Aula 10 você entregou o **formulário de agendamento validando no
servidor**, com mensagens de erro por campo e tela de confirmação. Ele
funciona, e é aí que aparece o buraco: os agendamentos vivem em uma lista em
memória. Memória pertence ao processo, e o processo morre no primeiro
`Ctrl + C`. Nenhuma recepcionista consulta a agenda de ontem, nenhum médico
abre a agenda em outra máquina.

Hoje a Clínica Vida+ ganha um banco de dados de verdade. O laboratório
instala o Entity Framework Core com o provedor de MySQL, escreve as quatro
entidades do case, cria o `ClinicaContext`, configura a conexão e aplica a
migration inicial. Ao fim da aula, o schema `clinicavida` existe no seu
MySQL, com as quatro tabelas e as especialidades da clínica já semeadas.

Nenhuma tela muda hoje, e está certo: hoje construímos o alicerce. Quem
passa a ler e escrever nesse banco é a Aula 12.

**Duração:** 60 minutos, individual, nos Ciclos 3 e 4.

---

## Pré-requisitos

- O fork de `josercf/uninove-2026-2-clinica-vida` clonado na sua máquina.
- O entregável da Aula 10 na `main`: o projeto `ClinicaVida.Web` com o
  formulário de agendamento validando no servidor.
- .NET SDK 10 instalado (`dotnet --version` mostra `10.x`).
- MySQL Community Server 8.0 ou superior **rodando**, mais o MySQL Workbench.

### Contrato técnico do Módulo 2

Estes nomes são fixos e valem para as Aulas 07 a 12. Não invente variantes.

| Item | Valor |
|---|---|
| SDK | .NET 10 LTS, `TargetFramework` `net10.0` |
| Projeto | `ClinicaVida.Web`, namespace raiz `ClinicaVida.Web` |
| DbContext | `ClinicaContext`, em `Data/ClinicaContext.cs` |
| Banco | `clinicavida`, no MySQL |
| Connection string | chave `"DefaultConnection"` em `appsettings.json` |
| Provedor EF Core | `Pomelo.EntityFrameworkCore.MySql` |
| Migration inicial | `InicialClinicaVida` |
| Branch desta aula | `feature/ef-core-mysql` |

---

## Passo 0: o MySQL no ar e o usuário da aplicação (5 min)

Antes de qualquer linha de C#, confirme que o servidor responde e crie o
usuário que a aplicação vai usar. **Nunca** conecte a aplicação como `root`.

```sql
CREATE USER 'clinicaapp'@'localhost' IDENTIFIED BY 'Senha123';
GRANT ALL PRIVILEGES ON clinicavida.* TO 'clinicaapp'@'localhost';
FLUSH PRIVILEGES;
```

O banco `clinicavida` ainda não existe, e o `GRANT` funciona mesmo assim.
Quem vai criar o banco é a migration, no Passo 5.

---

## Passo 1: a branch e os pacotes (10 min)

```bash
git switch main && git pull
git switch -c feature/ef-core-mysql

dotnet tool install --global dotnet-ef      # se ainda não tiver a ferramenta
dotnet add package Pomelo.EntityFrameworkCore.MySql
dotnet add package Microsoft.EntityFrameworkCore.Design
dotnet build
```

- `Pomelo.EntityFrameworkCore.MySql` é o **provedor**: o EF Core sozinho não
  fala MySQL. A versão instalada precisa ser da mesma linha do EF Core 10.
- `Microsoft.EntityFrameworkCore.Design` é o que permite ao `dotnet ef`
  inspecionar o projeto para gerar migrations.
- `dotnet build` precisa passar antes de você seguir. Erro de pacote agora é
  barato; erro de pacote depois da migration escrita, não.

---

## Passo 2: as quatro classes em `Models/` (9 min)

Uma classe por arquivo, todas no namespace `ClinicaVida.Web.Models`. As
Data Annotations da Aula 10 continuam valendo, e agora elas têm um segundo
efeito: viram o tipo da coluna no MySQL.

```csharp
using System.ComponentModel.DataAnnotations;

namespace ClinicaVida.Web.Models;

public class Especialidade
{
    public int Id { get; set; }

    [Required(ErrorMessage = "Informe o nome da especialidade.")]
    [StringLength(80)]
    public string Nome { get; set; } = string.Empty;

    [StringLength(200)]
    public string? Descricao { get; set; }
}
```

```csharp
public class Medico
{
    public int Id { get; set; }

    [Required, StringLength(120)]
    public string Nome { get; set; } = string.Empty;

    [Required, StringLength(20)]
    public string Crm { get; set; } = string.Empty;

    public int EspecialidadeId { get; set; }          // chave estrangeira
    public Especialidade? Especialidade { get; set; } // navegação
}
```

```csharp
public class Paciente
{
    public int Id { get; set; }

    [Required, StringLength(120)]
    public string Nome { get; set; } = string.Empty;

    [Required, StringLength(14)]                      // 000.000.000-00
    public string Cpf { get; set; } = string.Empty;

    [DataType(DataType.Date)]
    public DateTime DataNascimento { get; set; }

    [StringLength(20)]
    public string? Telefone { get; set; }

    [EmailAddress, StringLength(120)]
    public string? Email { get; set; }
}
```

```csharp
public class Consulta
{
    public int Id { get; set; }

    public int PacienteId { get; set; }
    public Paciente? Paciente { get; set; }

    public int MedicoId { get; set; }
    public Medico? Medico { get; set; }

    [DataType(DataType.Date)]
    public DateTime Data { get; set; }

    [DataType(DataType.Time)]
    public TimeSpan Horario { get; set; }

    [StringLength(400)]
    public string? Observacoes { get; set; }
}
```

O `Cpf` é `string`, e não número: CPF tem zero à esquerda, ponto e traço, e
nunca entra em conta de somar. A máscara do front-end é `000.000.000-00`, e
por isso a coluna tem 14 caracteres.

---

## Passo 3: o `ClinicaContext` (10 min)

Crie a pasta `Data/` e o arquivo `Data/ClinicaContext.cs`.

```csharp
using ClinicaVida.Web.Models;
using Microsoft.EntityFrameworkCore;

namespace ClinicaVida.Web.Data;

public class ClinicaContext : DbContext
{
    public ClinicaContext(DbContextOptions<ClinicaContext> options) : base(options) { }

    public DbSet<Paciente> Pacientes => Set<Paciente>();
    public DbSet<Medico> Medicos => Set<Medico>();
    public DbSet<Especialidade> Especialidades => Set<Especialidade>();
    public DbSet<Consulta> Consultas => Set<Consulta>();
}
```

O nome da propriedade `DbSet` vira o nome da tabela: `Pacientes`, e não
`Paciente`. Quatro `DbSet`, quatro tabelas.

---

## Passo 4: a connection string e o registro do contexto (8 min)

Em `appsettings.json`, no mesmo nível de `"Logging"`:

```json
"ConnectionStrings": {
  "DefaultConnection": "Server=localhost;Port=3306;Database=clinicavida;User=clinicaapp;Password=Senha123;"
}
```

Em `Program.cs`, antes de `builder.Build()`:

```csharp
using ClinicaVida.Web.Data;
using Microsoft.EntityFrameworkCore;

var conexao = builder.Configuration.GetConnectionString("DefaultConnection");

builder.Services.AddDbContext<ClinicaContext>(opcoes =>
    opcoes.UseMySql(conexao, ServerVersion.AutoDetect(conexao)));
```

Rode `dotnet build` de novo.

> **Senha de produção nunca vai para o repositório.** Em sala, a senha local
> no `appsettings.json` resolve, porque o banco é o seu e só existe na sua
> máquina. Em produção, a senha vem de variável de ambiente ou de um cofre de
> segredos, e o arquivo que a contém entra no `.gitignore`.

---

## Passo 5: a migration inicial (10 min)

Ciclo 4, sozinho. O nome da migration é fixo no case.

```bash
dotnet ef migrations add InicialClinicaVida
dotnet ef database update
```

O primeiro comando **escreve um arquivo** e não toca no banco. O segundo
**executa o SQL** no servidor. Confundir os dois é o erro mais comum de hoje.

Confira, nesta ordem:

1. A pasta `Migrations/` apareceu, com o arquivo
   `<timestamp>_InicialClinicaVida.cs` e o `ClinicaContextModelSnapshot.cs`.
2. Abra o arquivo e localize o `CreateTable` de cada uma das quatro tabelas.
3. No Workbench, o schema `clinicavida` existe, com **5** tabelas: as quatro
   do case mais `__EFMigrationsHistory`.
4. Abra `Pacientes` e compare coluna a coluna com a sua classe.

---

## Passo 6: semear as especialidades com `HasData` (8 min)

Um banco vazio não demonstra nada. As especialidades da clínica fazem parte
do esquema, então entram pela própria migration. Em `ClinicaContext`:

```csharp
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    modelBuilder.Entity<Especialidade>().HasData(
        new Especialidade { Id = 1, Nome = "Clínica Geral", Descricao = "Rotina e encaminhamentos" },
        new Especialidade { Id = 2, Nome = "Cardiologia",   Descricao = "Coração e circulação" },
        new Especialidade { Id = 3, Nome = "Pediatria",     Descricao = "Crianças e adolescentes" },
        new Especialidade { Id = 4, Nome = "Dermatologia",  Descricao = "Pele, cabelos e unhas" }
    );
}
```

Em `HasData` a chave primária é **obrigatória e escrita à mão**: o EF Core
precisa do `Id` para saber se aquela linha já existe.

```bash
dotnet ef migrations add EspecialidadesIniciais
dotnet ef database update
dotnet run
```

---

## Commit e push

```bash
git add Models/ Data/ Migrations/ appsettings.json Program.cs ClinicaVida.Web.csproj
git commit -m "feat: contexto do EF Core e migration inicial no MySQL"
git push -u origin feature/ef-core-mysql
```

A pasta `Migrations/` **vai** para o repositório: é ela que permite recriar o
seu banco em qualquer máquina, inclusive na correção.

---

## Entregável

`ClinicaContext` configurado, migration inicial aplicada e banco
`clinicavida` criado no MySQL, na branch `feature/ef-core-mysql`, commitado e
enviado ao seu fork. Especificamente:

- **4** classes em `Models/`: `Especialidade`, `Medico`, `Paciente` e
  `Consulta`.
- **1** `Data/ClinicaContext.cs` com os quatro `DbSet`.
- **1** connection string na chave `DefaultConnection`.
- **2** migrations em `Migrations/`: `InicialClinicaVida` e
  `EspecialidadesIniciais`.
- **5** tabelas no schema `clinicavida`, contando `__EFMigrationsHistory`.
- **4** especialidades semeadas.

### Critérios de aceitação

| # | Critério | Como o professor confere |
|---|---|---|
| 1 | Os pacotes corretos foram instalados | O `ClinicaVida.Web.csproj` traz `Pomelo.EntityFrameworkCore.MySql` e `Microsoft.EntityFrameworkCore.Design`; a solução compila com `dotnet build` |
| 2 | As quatro entidades existem | `Models/` tem `Especialidade`, `Medico`, `Paciente` e `Consulta`, no namespace `ClinicaVida.Web.Models`, com as propriedades do contrato |
| 3 | O CPF é texto e cabe na máscara | `Paciente.Cpf` é `string` com `[StringLength(14)]`, e a coluna gerada é `varchar(14)` |
| 4 | O contexto existe e está completo | `Data/ClinicaContext.cs` herda de `DbContext`, recebe `DbContextOptions<ClinicaContext>` e expõe os quatro `DbSet` |
| 5 | A conexão está configurada | `appsettings.json` traz `DefaultConnection` apontando para o banco `clinicavida`, e `Program.cs` registra o contexto com `UseMySql` |
| 6 | A migration inicial existe com o nome certo | `Migrations/` contém `<timestamp>_InicialClinicaVida.cs` com `Up` e `Down`, mais o `ClinicaContextModelSnapshot.cs` |
| 7 | A migration foi aplicada | No MySQL, o schema `clinicavida` tem as tabelas `Pacientes`, `Medicos`, `Especialidades`, `Consultas` e `__EFMigrationsHistory` |
| 8 | As colunas batem com as classes | Em `Pacientes`, `Id` é `int` PK `auto_increment`, `Nome` é `varchar(120) NOT NULL` e `Email` é anulável |
| 9 | As chaves estrangeiras foram geradas | `Medicos.EspecialidadeId` e `Consultas.PacienteId` e `MedicoId` aparecem como FK no Workbench |
| 10 | As especialidades foram semeadas | `SELECT * FROM Especialidades;` devolve 4 linhas, e `__EFMigrationsHistory` tem 2 linhas |
| 11 | A aplicação sobe | `dotnet run` inicia sem erro de conexão e as telas da Aula 10 continuam funcionando |
| 12 | O trabalho foi enviado | A branch `feature/ef-core-mysql` aparece no seu fork no GitHub, com a pasta `Migrations/` commitada |

---

## Se algo der errado

- **`Unable to connect to any of the specified MySQL hosts`**: o servidor não
  está no ar ou a porta está errada. Confira o serviço (`MySQL80` no Windows,
  `brew services list` no macOS) e a porta na connection string.
- **`Access denied for user 'clinicaapp'@'localhost'`**: usuário ou senha
  errados, ou o `GRANT` do Passo 0 não foi executado. Teste a mesma
  combinação no Workbench antes de voltar ao código.
- **`No project was found` ou `Unable to create a DbContext`**: rode o
  `dotnet ef` **dentro** da pasta do projeto `ClinicaVida.Web`, e confirme
  que o pacote `Microsoft.EntityFrameworkCore.Design` está instalado.
- **`dotnet ef` não é reconhecido como comando**: a ferramenta global não foi
  instalada ou o `~/.dotnet/tools` não está no `PATH`. Rode
  `dotnet tool install --global dotnet-ef` e abra um terminal novo.
- **`The entity type 'X' requires a primary key to be defined`**: a classe
  não tem a propriedade `Id`, ou ela foi escrita com outro nome. A convenção
  do EF Core é `Id` ou `<Entidade>Id`.
- **A migration saiu vazia**: você rodou `migrations add` antes de escrever as
  classes, ou os `DbSet` não estão no contexto. Rode
  `dotnet ef migrations remove`, corrija e gere de novo.
- **Errou a migration e ela já foi aplicada**: reverta primeiro, com
  `dotnet ef database update <MigrationAnterior>` (ou `0` para desfazer
  todas), e só então use `dotnet ef migrations remove`. Nunca edite à mão uma
  migration aplicada e nunca apague o arquivo pelo explorador.
- **`Specified key was too long`**: alguma coluna de texto virou índice sem
  tamanho definido. Anote a propriedade com `[StringLength(n)]` e gere uma
  nova migration.
