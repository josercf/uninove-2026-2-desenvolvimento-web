# Laboratório da Aula 17

## Disciplina: Desenvolvimento Web
**Prof. José Romualdo | Uninove, Universidade Nove de Julho**

### Case: Clínica Vida+ (Fase 16, as entidades ligadas)

Na Aula 16 você entregou o `ConsultasApiController` com os cinco endpoints
testados e documentados. A API responde, e é justamente por responder que a
limitação aparece: cada consulta devolve `pacienteId` e `medicoId`, números que
não dizem nada a quem consome. O mesmo vale para as telas: a agenda mostra
identificadores onde deveria mostrar nomes.

A causa é anterior à API. As quatro tabelas do banco `clinicavida` guardam
números umas das outras desde a Aula 11, mas as quatro classes do projeto ainda
não se enxergam. Hoje isso muda: os três relacionamentos são mapeados com a
Fluent API, com navegação nos dois sentidos, o comportamento de exclusão passa a
preservar o histórico de consultas, e as consultas LINQ trazem os dados
relacionados em uma única ida ao banco.

É o último laboratório do Módulo 3.

**Duração:** 60 minutos, individual, nos Ciclos 3 e 4.

---

## Pré-requisitos

- O fork de `josercf/uninove-2026-2-clinica-vida` clonado na sua máquina.
- O entregável da Aula 16 na `main`: o `ConsultasApiController` funcionando.
- O `ClinicaContext` herdando de `IdentityDbContext<IdentityUser>` desde a
  Aula 15.
- O SDK do .NET 10 e o serviço do MySQL rodando.
- VS Code e o MySQL Workbench, para conferir as chaves estrangeiras criadas.

Confirme o ponto de partida antes de começar:

```bash
dotnet --version            # precisa começar com 10.
dotnet ef migrations list   # nenhuma migration pendente
```

Ao rodar `dotnet run`, use sempre **a porta que o seu terminal imprimiu**. Ela é
sorteada por projeto em `Properties/launchSettings.json`, então a sua não é
necessariamente a do colega ao lado, nem a `7145` usada como exemplo nos slides.

---

## Passo 1: a branch e as propriedades de navegação (10 min)

```bash
git checkout main && git pull
git checkout -b feature/relacionamentos
```

As chaves estrangeiras já existem desde a Aula 11 e **não mudam de nome**. O que
entra hoje são as propriedades de navegação, nos dois sentidos: coleção no lado
1, referência no lado N.

`Models/Especialidade.cs`:

```csharp
public class Especialidade
{
    public int Id { get; set; }
    public string Nome { get; set; } = string.Empty;
    public string? Descricao { get; set; }

    // Novo hoje: o lado 1 do relacionamento com Medico.
    public ICollection<Medico> Medicos { get; set; } = new List<Medico>();
}
```

`Models/Medico.cs`:

```csharp
public class Medico
{
    public int Id { get; set; }
    public string Nome { get; set; } = string.Empty;
    public string Crm { get; set; } = string.Empty;

    public int EspecialidadeId { get; set; }          // chave estrangeira, Aula 11
    public Especialidade? Especialidade { get; set; } // referência, Aula 11

    // Novo hoje: o lado 1 do relacionamento com Consulta.
    public ICollection<Consulta> Consultas { get; set; } = new List<Consulta>();
}
```

`Models/Paciente.cs` ganha apenas a coleção, sem tocar em mais nada:

```csharp
public ICollection<Consulta> Consultas { get; set; } = new List<Consulta>();
```

`Models/Consulta.cs` ganha as duas referências:

```csharp
public class Consulta
{
    public int Id { get; set; }

    public int PacienteId { get; set; }           // chave estrangeira, Aula 11
    public Paciente? Paciente { get; set; }       // navegação, nova hoje

    public int MedicoId { get; set; }             // chave estrangeira, Aula 11
    public Medico? Medico { get; set; }           // navegação, nova hoje

    public DateTime Data { get; set; }
    public TimeSpan Horario { get; set; }
    public string? Observacoes { get; set; }
}
```

As referências são anuláveis de propósito: enquanto você não pedir o dado
relacionado com `Include` ou com uma projeção, elas chegam nulas, e o
compilador obriga você a lembrar disso.

---

## Passo 2: o mapeamento com a Fluent API (10 min)

Em `Data/ClinicaContext.cs`, no `OnModelCreating`. A **primeira** linha do método
precisa continuar sendo `base.OnModelCreating(builder)`: desde a Aula 15 o
`ClinicaContext` herda de `IdentityDbContext<IdentityUser>`, e é a chamada da
base que mapeia as tabelas de usuário. Omitir essa linha derruba o login.

```csharp
protected override void OnModelCreating(ModelBuilder builder)
{
    base.OnModelCreating(builder);

    builder.Entity<Medico>()
        .HasOne(m => m.Especialidade)
        .WithMany(e => e.Medicos)
        .HasForeignKey(m => m.EspecialidadeId);

    builder.Entity<Consulta>()
        .HasOne(c => c.Medico)
        .WithMany(m => m.Consultas)
        .HasForeignKey(c => c.MedicoId);

    builder.Entity<Consulta>()
        .HasOne(c => c.Paciente)
        .WithMany(p => p.Consultas)
        .HasForeignKey(c => c.PacienteId);

    builder.Entity<Especialidade>().HasData(/* as quatro da Aula 11 */);
}
```

Leia a cadeia em voz alta: **um** Medico tem **uma** Especialidade
(`HasOne`), que por sua vez tem **muitos** médicos (`WithMany`), e o elo entre
os dois é a coluna `EspecialidadeId` (`HasForeignKey`).

O `HasData` das especialidades continua onde estava, depois do mapeamento.

---

## Passo 3: comportamento de exclusão, índices e migration (15 min)

### O comportamento de exclusão

As três chaves estrangeiras são obrigatórias, e para relacionamento obrigatório
o padrão do EF Core é `Cascade`: excluir uma médica apagaria, em silêncio, todas
as consultas dela. Em uma clínica isso é perda de prontuário. Acrescente
`OnDelete` aos três mapeamentos:

```csharp
    .OnDelete(DeleteBehavior.Restrict);
```

Com `Restrict`, o banco recusa a exclusão e a aplicação recebe uma
`DbUpdateException`. Trate isso no Controller, para que a recepção veja um aviso
e não uma página de erro:

```csharp
try
{
    _context.Medicos.Remove(medico);
    await _context.SaveChangesAsync();
}
catch (DbUpdateException)
{
    TempData["Erro"] = "Não é possível excluir um médico que já tem consultas.";
    return RedirectToAction(nameof(Index));
}
```

### Os índices únicos

```csharp
builder.Entity<Medico>().HasIndex(m => m.Crm).IsUnique();
builder.Entity<Paciente>().HasIndex(p => p.Cpf).IsUnique();
builder.Entity<Consulta>()
    .HasIndex(c => new { c.MedicoId, c.Data, c.Horario })
    .IsUnique();
```

O terceiro é o índice composto que resolve, no banco, o problema que deu origem
ao case: o mesmo médico com duas consultas no mesmo dia e horário.

### A migration

```bash
dotnet ef migrations add RelacionamentosClinicaVida
dotnet ef database update
```

Confira no MySQL Workbench que as chaves estrangeiras foram criadas com
`RESTRICT`:

```sql
SHOW CREATE TABLE clinicavida.Consultas;
```

Se o banco já tiver dados que violem um índice único, o `database update` falha.
É esperado: limpe as linhas duplicadas e rode de novo.

---

## Passo 4: a agenda do dia com `Include` (10 min)

Fim do Ciclo 3. Daqui em diante você trabalha sozinho, com o professor
circulando pela sala.

Antes de mudar qualquer coisa, rode a agenda como ela está e **conte no terminal
quantos comandos SQL** aparecem no log. Anote o número.

```csharp
public async Task<IActionResult> Index(DateTime? data)
{
    var dia = data?.Date ?? DateTime.Today;

    var agenda = await _context.Consultas
        .Include(c => c.Paciente)
        .Include(c => c.Medico)
            .ThenInclude(m => m.Especialidade)
        .Where(c => c.Data == dia)
        .OrderBy(c => c.Horario)
        .AsNoTracking()
        .ToListAsync();

    ViewData["Data"] = dia;
    return View(agenda);
}
```

`ThenInclude` continua o caminho a partir do `Include` imediatamente anterior:
da Consulta para o Medico, e do Medico para a Especialidade. Para incluir outro
ramo a partir da raiz, comece um `Include` novo.

Na View, o dado relacionado já está carregado e nenhuma ida extra ao banco
acontece:

```cshtml
@model IEnumerable<ClinicaVida.Web.Models.Consulta>

<table>
    <thead>
        <tr><th>Horário</th><th>Paciente</th><th>Médico</th><th>Especialidade</th></tr>
    </thead>
    <tbody>
        @foreach (var consulta in Model)
        {
            <tr>
                <td>@consulta.Horario.ToString(@"hh\:mm")</td>
                <td>@consulta.Paciente?.Nome</td>
                <td>@consulta.Medico?.Nome</td>
                <td>@consulta.Medico?.Especialidade?.Nome</td>
            </tr>
        }
    </tbody>
</table>
```

Rode de novo e conte os comandos outra vez. Precisa sobrar **um**.

---

## Passo 5: o histórico do paciente (10 min)

Uma tela nova, que parte do lado 1 do relacionamento: um paciente e as consultas
dele.

```csharp
public async Task<IActionResult> Historico(int? id)
{
    if (id == null) return NotFound();

    var paciente = await _context.Pacientes
        .Include(p => p.Consultas.OrderByDescending(c => c.Data))
            .ThenInclude(c => c.Medico)
        .AsNoTracking()
        .FirstOrDefaultAsync(p => p.Id == id);

    if (paciente == null) return NotFound();

    return View(paciente);
}
```

A ordenação dentro do `Include` ordena a coleção carregada, e não a consulta
principal. Na View, cabeçalho com os dados do paciente e uma tabela com data,
horário e médico de cada consulta, mais o link de volta para a ficha.

Acrescente na ficha do paciente, da Aula 12, o link para a tela nova:

```cshtml
<a asp-action="Historico" asp-route-id="@Model.Id">Histórico de consultas</a>
```

---

## Passo 6: o relatório por especialidade (10 min)

A direção da clínica quer um número por especialidade, não uma lista de
consultas. Agrupar no banco significa trafegar cinco linhas em vez de cinco mil.

Crie o ViewModel em `Models/ViewModels/RelatorioItemViewModel.cs`:

```csharp
public class RelatorioItemViewModel
{
    public string Especialidade { get; set; } = string.Empty;
    public int Total { get; set; }
}
```

E a action:

```csharp
public async Task<IActionResult> Relatorio()
{
    var relatorio = await _context.Consultas
        .GroupBy(c => c.Medico!.Especialidade!.Nome)
        .Select(g => new RelatorioItemViewModel
        {
            Especialidade = g.Key,
            Total = g.Count()
        })
        .OrderByDescending(item => item.Total)
        .ToListAsync();

    return View(relatorio);
}
```

Confira no log do terminal que o `GROUP BY` foi traduzido e executado no MySQL.
Se ele não aparecer no SQL, o agrupamento aconteceu em memória, o que significa
que a tabela inteira veio para a aplicação antes de ser contada.

---

## Commit e push

```bash
git add Models/ Data/ClinicaContext.cs Migrations/ Controllers/ Views/
git commit -m "feat: relacionamentos entre as entidades da Clinica Vida"
git push -u origin feature/relacionamentos
```

---

## Entregável

Relacionamentos mapeados e aplicados no banco `clinicavida`, na branch
`feature/relacionamentos`, commitados e enviados ao seu fork. Especificamente:

- **3** relacionamentos um-para-muitos mapeados na Fluent API, com navegação nos
  dois sentidos: Especialidade para Medico, Medico para Consulta e Paciente para
  Consulta.
- **1** migration gerada e aplicada, com as três chaves estrangeiras em
  `RESTRICT`.
- **3** índices únicos: `Crm`, `Cpf` e o composto de `MedicoId`, `Data` e
  `Horario`.
- **1** agenda do dia exibindo nome do paciente, nome do médico e especialidade
  em um único comando SQL.
- **1** tela de histórico do paciente e **1** relatório de consultas por
  especialidade.

### Critérios de aceitação

| # | Critério | Como o professor confere |
|---|---|---|
| 1 | As navegações existem nos dois sentidos | `Especialidade.Medicos`, `Medico.Consultas` e `Paciente.Consultas` como coleções, e `Consulta.Paciente` e `Consulta.Medico` como referências |
| 2 | Nada foi renomeado | `EspecialidadeId`, `PacienteId` e `MedicoId` continuam com os nomes da Aula 11, e as demais propriedades dos Models estão intactas |
| 3 | O mapeamento está na Fluent API | O `OnModelCreating` traz os três blocos com `HasOne`, `WithMany` e `HasForeignKey` |
| 4 | O contexto do Identity continua íntegro | A primeira linha do `OnModelCreating` é `base.OnModelCreating(builder)`, e o login da Aula 15 continua funcionando |
| 5 | O histórico é preservado na exclusão | `SHOW CREATE TABLE clinicavida.Consultas` mostra as chaves estrangeiras com `ON DELETE RESTRICT` |
| 6 | A exclusão recusada é tratada | Tentar excluir um médico com consultas mostra aviso na tela, e não uma página de erro do servidor |
| 7 | Os índices únicos estão no banco | Cadastrar um segundo médico com o mesmo CRM é recusado, e o índice composto aparece em `SHOW INDEX FROM clinicavida.Consultas` |
| 8 | A migration foi aplicada | `dotnet ef migrations list` mostra `RelacionamentosClinicaVida` aplicada, sem migration pendente |
| 9 | A agenda usa carregamento adiantado | A agenda do dia exibe paciente, médico e especialidade, e o log do terminal mostra **um** comando SQL, não um por linha |
| 10 | O histórico do paciente funciona | `/Pacientes/Historico/1` lista as consultas do paciente com o nome do médico, da mais recente para a mais antiga, e um id inexistente devolve 404 |
| 11 | O relatório agrupa no banco | A tela de relatório mostra o total por especialidade e o log traz `GROUP BY` no SQL gerado |
| 12 | O trabalho foi enviado | A branch `feature/relacionamentos` aparece no seu fork no GitHub, com o commit de sua autoria |

---

## Se algo der errado

- **`Unable to determine the relationship represented by navigation
  'Consulta.Medico'`**: o EF Core não encontrou a chave estrangeira pela
  convenção. Confira o nome da propriedade (`MedicoId`) ou aponte-a
  explicitamente com `HasForeignKey`.
- **`The navigation 'Medico.Consultas' cannot be added because...`**: a mesma
  navegação foi mapeada duas vezes, geralmente com `HasOne`/`WithMany` repetido
  em blocos diferentes. Cada relacionamento é declarado uma vez só.
- **O login parou de funcionar depois da migration**: falta o
  `base.OnModelCreating(builder)` como primeira linha do método. Sem ele as
  tabelas do Identity somem do modelo, e a migration seguinte tenta removê-las
  do banco.
- **A migration quer apagar as tabelas `AspNetUsers` e companhia**: mesmo
  diagnóstico do item anterior. Remova a migration com
  `dotnet ef migrations remove`, corrija a herança ou a chamada da base e gere
  de novo.
- **`Cannot delete or update a parent row: a foreign key constraint fails`**:
  isto é o `Restrict` funcionando. A mensagem precisa virar um aviso amigável na
  tela, com o `try/catch` do Passo 3.
- **`Duplicate entry ... for key 'IX_Medicos_Crm'`** ao rodar o
  `database update`: já existem linhas duplicadas no banco que violam o índice
  único novo. Limpe as duplicidades e aplique a migration de novo.
- **A agenda continua disparando dezenas de comandos**: o `Include` foi escrito
  depois de um `ToListAsync`, e aí ele não faz efeito nenhum. `Include` compõe a
  consulta e precisa vir antes da execução.
- **`consulta.Paciente` chega nulo na View**: a consulta não pediu o
  relacionado. Ou acrescente o `Include`, ou troque por uma projeção com
  `Select`.
- **A projeção com `Select` reclama de tradução**: você chamou um método que o
  EF Core não sabe converter em SQL. Faça a formatação na View, não dentro do
  `Select`.
