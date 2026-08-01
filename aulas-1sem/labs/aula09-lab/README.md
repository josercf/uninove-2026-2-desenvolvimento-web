# Laboratório da Aula 09

## Disciplina: Desenvolvimento Web
**Prof. José Romualdo | Uninove, Universidade Nove de Julho**

### Case: Clínica Vida+ (Fase 8, o corpo clínico vira dado)

Na Aula 08 você entregou o `EspecialidadesController` com as actions `Index` e
`Details`, as Views correspondentes em `Views/Especialidades/` e a navegação
funcionando. A requisição já percorre rota, Controller, action e View. O que
falta é o dado: as especialidades estão **escritas à mão dentro da View**, uma
a uma, em `<li>`. Dado escrito à mão não pode ser filtrado, contado nem
reordenado, e acrescentar um médico hoje significa editar HTML.

Hoje o dado sai da View e vira **objeto em uma coleção**. O laboratório cria as
classes `Especialidade` e `Medico` em `Models/`, a classe estática
`ClinicaEmMemoria` com o corpo clínico da Vida+, o `MedicosController` com uma
listagem filtrada por especialidade e as Views tipadas com `@model`. Nenhuma
linha de banco de dados: os dados vivem em memória e só passam a vir do MySQL
na Aula 11.

**Duração:** 60 minutos, nos Ciclos 3 e 4. Os passos 1 a 3 são guiados pelo
professor; os passos 4 a 6 você faz sozinho.

---

## Pré-requisitos

- O fork de `josercf/uninove-2026-2-clinica-vida` clonado na sua máquina.
- O SDK do **.NET 10** instalado (`dotnet --version` responde).
- O projeto **`ClinicaVida.Web`** executando com `dotnet watch run`, entregue na
  Aula 07.
- O entregável da Aula 08 na `main`: `EspecialidadesController` com `Index` e
  `Details`, as Views correspondentes e o menu com os links.
- VS Code com o kit de C#, ou Visual Studio.

> **O contrato do módulo, que não muda em nenhuma aula.** Projeto
> `ClinicaVida.Web`, namespace raiz `ClinicaVida.Web`, Models `Especialidade`,
> `Medico`, `Paciente` e `Consulta` na pasta `Models/`. Use exatamente esses
> nomes: as Aulas 10 a 12 continuam de onde esta parar.

---

## Passo 1: a branch e os dois Models (10 min)

```bash
git switch main
git pull

git switch -c feature/medicos-em-memoria

cd ClinicaVida.Web
dotnet watch run
```

Deixe o `dotnet watch run` rodando até o fim da aula.

Crie `Models/Especialidade.cs`:

```csharp
namespace ClinicaVida.Web.Models;

public class Especialidade
{
    public int Id { get; set; }
    public string Nome { get; set; } = string.Empty;
    public string Descricao { get; set; } = string.Empty;
}
```

E `Models/Medico.cs`:

```csharp
namespace ClinicaVida.Web.Models;

public class Medico
{
    public int Id { get; set; }
    public string Nome { get; set; } = string.Empty;
    public string Crm { get; set; } = string.Empty;

    public int EspecialidadeId { get; set; }             // a chave: só um número
    public Especialidade? Especialidade { get; set; }    // o objeto inteiro
}
```

As duas propriedades do fim têm papéis diferentes: `EspecialidadeId` é o que
você **filtra e compara**; `Especialidade` é o que você **exibe**. O `?` avisa
que o objeto pode estar ausente, e na Aula 11 esse par vira chave estrangeira e
relacionamento no banco.

Rode `dotnet build` antes de seguir. Nenhum erro, nenhum aviso.

---

## Passo 2: o corpo clínico em memória (10 min)

Crie `Models/ClinicaEmMemoria.cs`. É a fonte única de dados da aplicação até a
Aula 11: um só lugar guarda as listas, e todo Controller lê dele.

```csharp
namespace ClinicaVida.Web.Models;

public static class ClinicaEmMemoria
{
    public static List<Especialidade> Especialidades { get; } = new()
    {
        new Especialidade { Id = 1, Nome = "Cardiologia",  Descricao = "Coração e vasos" },
        new Especialidade { Id = 2, Nome = "Pediatria",    Descricao = "Crianças e adolescentes" },
        new Especialidade { Id = 3, Nome = "Dermatologia", Descricao = "Pele, cabelos e unhas" },
        new Especialidade { Id = 4, Nome = "Ortopedia",    Descricao = "Ossos, músculos e articulações" },
    };

    public static List<Medico> Medicos { get; } = new()
    {
        new Medico { Id = 1, Nome = "Dra. Marta Lisboa",   Crm = "55307", EspecialidadeId = 1 },
        new Medico { Id = 2, Nome = "Dr. Caio Nunes",      Crm = "41880", EspecialidadeId = 2 },
        new Medico { Id = 3, Nome = "Dra. Helena Prado",   Crm = "34211", EspecialidadeId = 1 },
        new Medico { Id = 4, Nome = "Dr. Ivo Reis",        Crm = "60912", EspecialidadeId = 4 },
        new Medico { Id = 5, Nome = "Dra. Sofia Brandão",  Crm = "62145", EspecialidadeId = 2 },
        new Medico { Id = 6, Nome = "Dr. Otávio Lemos",    Crm = "70233", EspecialidadeId = 3 },
    };
}
```

Os identificadores 1, 2 e 3 das especialidades são **os mesmos** que a sua View
da Aula 08 já usa nos links de `Details`. Mantenha-os.

São **no mínimo 4 especialidades e 6 médicos**, com pelo menos duas
especialidades tendo mais de um médico. Sem isso o filtro do Passo 3 não tem o
que provar.

---

## Passo 3: o `MedicosController` com filtro (15 min)

Crie `Controllers/MedicosController.cs`.

```csharp
using Microsoft.AspNetCore.Mvc;
using ClinicaVida.Web.Models;

namespace ClinicaVida.Web.Controllers;

public class MedicosController : Controller
{
    public IActionResult Index(int? especialidadeId)
    {
        var medicos = ClinicaEmMemoria.Medicos.AsEnumerable();

        if (especialidadeId is not null)
        {
            medicos = medicos.Where(m => m.EspecialidadeId == especialidadeId);
        }

        ViewBag.Especialidades = ClinicaEmMemoria.Especialidades;

        return View(medicos.OrderBy(m => m.Nome).ToList());
    }
}
```

Três decisões que valem o dia inteiro:

- **`int?`, e não `int`.** O ponto de interrogação permite que o parâmetro não
  venha na URL. Sem filtro, `especialidadeId` é `null` e a lista vai inteira.
- **O Model leva os médicos; o `ViewBag` leva o resto.** A coleção principal da
  tela vai tipada, no Model. A lista de especialidades, que só existe para
  montar o campo de filtro, vai pelo `ViewBag`.
- **`ToList()` no fim.** É ele que executa a consulta. Antes dele, `Where` e
  `OrderBy` só descrevem o que fazer.

---

## Passo 4: a View tipada da listagem (10 min)

Crie a pasta `Views/Medicos/` e, dentro dela, `Index.cshtml`.

```cshtml
@model IEnumerable<Medico>
@{
    ViewData["Title"] = "Corpo clínico";
}

<h2>Corpo clínico da Clínica Vida+</h2>

<form method="get">
    <label for="especialidadeId">Especialidade</label>
    <select id="especialidadeId" name="especialidadeId">
        <option value="">Todas as especialidades</option>
        @foreach (var e in (List<Especialidade>)ViewBag.Especialidades)
        {
            <option value="@e.Id">@e.Nome</option>
        }
    </select>
    <button type="submit">Filtrar</button>
</form>

<p>@Model.Count() médico(s) na lista.</p>

<ul>
@foreach (var medico in Model)
{
    <li>
        <a href="/Medicos/Details/@medico.Id">@medico.Nome</a>, CRM @medico.Crm
    </li>
}
</ul>
```

O `_ViewImports.cshtml` gerado pelo template já traz
`@using ClinicaVida.Web.Models`, por isso o nome curto `Medico` basta na
diretiva `@model`.

O formulário usa `method="get"`: o filtro vira query string, o endereço fica
compartilhável e o botão Voltar do navegador funciona.

**Checkpoint do Ciclo 3:** `/Medicos` lista os seis médicos em ordem
alfabética, e escolher uma especialidade no campo recarrega a página em
`/Medicos?especialidadeId=1`, com a lista menor.

---

## Passo 5: a action `Details` e a View do médico (10 min)

Ciclo 4, sozinho. Acrescente ao `MedicosController`:

```csharp
public IActionResult Details(int id)
{
    var medico = ClinicaEmMemoria.Medicos.FirstOrDefault(m => m.Id == id);
    if (medico is null) return NotFound();      // 404: esse médico não existe

    medico.Especialidade = ClinicaEmMemoria.Especialidades
        .FirstOrDefault(e => e.Id == medico.EspecialidadeId);

    return View(medico);
}
```

`FirstOrDefault` devolve **um só** item, ou `null` quando não encontra nada.
Testar esse `null` não é preciosismo: sem o `if`, a linha seguinte quebra a
requisição com uma exceção.

Crie `Views/Medicos/Details.cshtml`:

```cshtml
@model Medico

<h2>@Model.Nome</h2>

<p>CRM: @Model.Crm</p>
<p>Especialidade: @(Model.Especialidade?.Nome ?? "não informada")</p>

<p><a href="/Medicos">Voltar para o corpo clínico</a></p>
```

O `?.` e o `??` juntos evitam a exceção quando a especialidade não foi
preenchida: o primeiro para a leitura em `null`, o segundo entrega um texto no
lugar.

Teste os dois caminhos: `/Medicos/Details/2` mostra o médico, e
`/Medicos/Details/999` devolve 404.

---

## Passo 6: quantos médicos por especialidade (5 min)

De volta ao `EspecialidadesController` da Aula 08. Substitua a lista escrita à
mão pela lista em memória e acrescente a contagem.

```csharp
public IActionResult Index()
{
    var contagem = new Dictionary<int, int>();

    foreach (var e in ClinicaEmMemoria.Especialidades)
    {
        contagem[e.Id] = ClinicaEmMemoria.Medicos.Count(m => m.EspecialidadeId == e.Id);
    }

    ViewBag.MedicosPorEspecialidade = contagem;

    return View(ClinicaEmMemoria.Especialidades);
}
```

E em `Views/Especialidades/Index.cshtml`, troque os `<li>` escritos à mão:

```cshtml
@model IEnumerable<Especialidade>
@{
    var contagem = (Dictionary<int, int>)ViewBag.MedicosPorEspecialidade;
}

<ul>
@foreach (var e in Model)
{
    <li>
        <a href="/Medicos?especialidadeId=@e.Id">@e.Nome</a>
        (@contagem[e.Id] médico(s))
    </li>
}
</ul>
```

Duas telas da clínica, ligadas pelo mesmo dado. Nenhuma delas sabe quantos
médicos existem: quem conta é o Controller.

---

## Commit e push

```bash
git add .
git commit -m "feat: corpo clinico em memoria com filtro por especialidade"
git push -u origin feature/medicos-em-memoria
```

---

## Entregável

Lista de médicos filtrada por especialidade, vinda do Controller e renderizada
em View tipada, na branch `feature/medicos-em-memoria`, commitada e enviada ao
seu fork. Especificamente:

- **3** arquivos novos em `Models/`: `Especialidade.cs`, `Medico.cs` e
  `ClinicaEmMemoria.cs`.
- **4** especialidades e **6** médicos na classe em memória, com pelo menos duas
  especialidades tendo mais de um médico.
- **1** Controller novo, `MedicosController`, com **2** actions: `Index`, com
  filtro opcional, e `Details`.
- **2** Views novas em `Views/Medicos/`, ambas tipadas com `@model`.
- **1** contagem de médicos por especialidade na tela de especialidades.

### Critérios de aceitação

| # | Critério | Como o professor confere |
|---|---|---|
| 1 | Os Models seguem o contrato do módulo | `Models/Especialidade.cs` e `Models/Medico.cs` existem, no namespace `ClinicaVida.Web.Models`, com as propriedades exatas do Passo 1, incluindo `EspecialidadeId` |
| 2 | O corpo clínico está em memória | `Models/ClinicaEmMemoria.cs` traz no mínimo 4 especialidades e 6 médicos, com pelo menos duas especialidades tendo mais de um médico |
| 3 | A listagem responde e vem ordenada | `/Medicos` responde 200 e lista os 6 médicos em ordem alfabética de nome |
| 4 | O filtro funciona pela query string | `/Medicos?especialidadeId=1` lista somente os médicos daquela especialidade, e o campo de filtro na tela produz essa mesma URL |
| 5 | O filtro é opcional | `/Medicos`, sem parâmetro nenhum, continua listando todos, sem erro |
| 6 | A View é tipada | `Views/Medicos/Index.cshtml` começa com `@model IEnumerable<Medico>` e percorre `Model` com `foreach`, sem `ViewBag` para a lista de médicos |
| 7 | Os detalhes de um médico aparecem | `/Medicos/Details/2` exibe nome, CRM e o **nome** da especialidade, não o número |
| 8 | O id inexistente devolve 404 | `/Medicos/Details/999` responde com a página de não encontrado, e não com uma tela de erro |
| 9 | A contagem por especialidade aparece | A tela `/Especialidades` mostra cada especialidade com a quantidade de médicos ao lado, e o link leva à listagem já filtrada |
| 10 | A aplicação compila sem avisos | `dotnet build` termina com 0 erros e 0 avisos |
| 11 | O trabalho foi enviado | A branch `feature/medicos-em-memoria` aparece no seu fork no GitHub, com o commit de sua autoria |

---

## Se algo der errado

- **`The type or namespace name 'Medico' could not be found`**: falta o `using
  ClinicaVida.Web.Models;` no topo do Controller. Na View, o
  `_ViewImports.cshtml` já resolve isso; no Controller, não.
- **`InvalidOperationException: The model item passed into the ViewDataDictionary
  is of type 'List<Medico>', but this ViewDataDictionary instance requires a
  model item of type ...`**: a diretiva `@model` da View não bate com o que o
  Controller mandou. `List<Medico>` serve para `@model IEnumerable<Medico>`, mas
  não para `@model Medico`.
- **`Object reference not set to an instance of an object` na tela de
  detalhes**: o `FirstOrDefault` devolveu `null` e o código seguiu adiante. É
  exatamente o caso do `if (medico is null) return NotFound();` do Passo 5.
- **O filtro devolve sempre a lista inteira**: o `name` do `<select>` está
  diferente do nome do parâmetro da action. Os dois precisam ser
  `especialidadeId`, com a mesma grafia.
- **`Where` não existe na lista**: falta o `using System.Linq;`. Nos projetos
  .NET atuais os *implicit usings* já trazem esse namespace; se você desligou
  essa opção no `.csproj`, acrescente o `using` à mão.
- **`KeyNotFoundException` na tela de especialidades**: o dicionário não tem a
  chave pedida. Ou o `foreach` do Passo 6 não passou por todas as
  especialidades, ou a View está exibindo uma especialidade que não está na
  lista em memória.
- **A tela de especialidades continua com o texto antigo**: a View ainda tem os
  `<li>` escritos à mão da Aula 08. Apague-os; quem produz a lista agora é o
  `foreach` sobre o `Model`.
