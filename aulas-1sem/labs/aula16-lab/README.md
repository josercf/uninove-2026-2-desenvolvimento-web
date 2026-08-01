# Laboratório da Aula 16

## Disciplina: Desenvolvimento Web
**Prof. José Romualdo | Uninove, Universidade Nove de Julho**

### Case: Clínica Vida+ (Fase 15, a agenda exposta por API)

Na Aula 15 você entregou o login e o logout funcionando, com a área da
recepção protegida por `[Authorize(Roles = "Recepcao")]` e o menu adaptado ao
usuário. A agenda deixou de ser pública, e tudo o que a aplicação sabe fazer
até aqui é devolver tela para uma pessoa.

Hoje aparece um consumidor que não é uma pessoa. O laboratório de análises
parceiro da clínica precisa ler a agenda do dia e agendar consultas de retorno
a partir do próprio sistema dele, sem abrir a tela da Clínica Vida+ e sem
copiar lista nenhuma. O laboratório desta aula cria o `ConsultasApiController`
com os cinco endpoints do recurso Consulta, com DTOs de entrada e de saída e
os códigos de status corretos em cada operação.

**Duração:** 60 minutos, individual, nos Ciclos 3 e 4.

---

## Pré-requisitos

- O fork de `josercf/uninove-2026-2-clinica-vida` clonado na sua máquina.
- O entregável da Aula 15 na `main`: o Identity configurado, o
  `ClinicaContext` herdando de `IdentityDbContext<IdentityUser>`, o
  `ContaController` e os perfis `Recepcao` e `Medico`.
- O CRUD da Aula 12 e o banco `clinicavida` com dados: pelo menos um paciente,
  um médico e uma consulta gravados, senão não há o que a API devolva.
- O SDK do .NET 10 e o serviço do MySQL rodando.
- Uma ferramenta para exercitar os verbos que a barra de endereços do navegador
  não faz. A recomendada é a extensão **REST Client** do VS Code, que executa
  arquivos `.http`; o Postman também serve.

Confirme o ponto de partida antes de começar:

```bash
dotnet --version           # precisa começar com 10.
dotnet ef database update  # não pode ter migration pendente
dotnet run                 # anote a porta que o terminal imprimir
```

> **A porta é sua, não é minha.** Todo endereço deste roteiro usa `7145` como
> exemplo. Use **a porta que o seu terminal imprimiu**: `dotnet new mvc` sorteia
> as portas em `Properties/launchSettings.json`, e a de cada aluno é diferente.

---

## Passo 1: a branch e o Controller de API (6 min)

```bash
git switch main && git pull
git switch -c feature/api-consultas
```

Crie `Controllers/ConsultasApiController.cs`:

```csharp
using ClinicaVida.Web.Data;
using ClinicaVida.Web.Models;
using ClinicaVida.Web.Models.Dtos;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace ClinicaVida.Web.Controllers;

[ApiController]
[Route("api/consultas")]
[Authorize]
public class ConsultasApiController : ControllerBase
{
    private readonly ClinicaContext _context;

    public ConsultasApiController(ClinicaContext context)
    {
        _context = context;
    }
}
```

Três decisões que valem a leitura com calma:

1. **`ControllerBase`, e não `Controller`.** É a mesma classe sem o que só
   serve a HTML: nada de `View()`, nada de `TempData`. Este Controller não tem
   uma única View.
2. **`[ApiController]`** liga o comportamento de API: modelo inválido vira
   **400** automaticamente, antes da action rodar, e o corpo JSON é lido sem
   precisar de `[FromBody]`.
3. **`[Route("api/consultas")]`, com a rota escrita à mão.** A convenção do
   ASP.NET Core é `[Route("api/[controller]")]`, em que o token `[controller]`
   vira o nome da classe sem o sufixo `Controller`. Aqui isso daria
   `api/consultasapi`, porque a classe se chama `ConsultasApiController`
   justamente para não colidir com o Controller MVC de consultas. Quem manda no
   endereço é o recurso, então fixamos `api/consultas`.

E **`[Authorize]`**, que é o assunto do passo 2.

---

## Passo 2: o 401 que o cookie não devolve sozinho (4 min)

A API é a mesma aplicação da Aula 15, então ela herda a autenticação por
cookie do Identity. O `[Authorize]` no Controller já barra quem não está
autenticado, mas a resposta que o cookie dá ao barrar é **302 para a tela de
login**, com HTML no corpo. Para um navegador isso é útil; para um sistema
integrador é lixo.

Em `Program.cs`, antes do `builder.Build()`:

```csharp
builder.Services.ConfigureApplicationCookie(options =>
{
    options.Events.OnRedirectToLogin = ctx =>
    {
        if (ctx.Request.Path.StartsWithSegments("/api"))
        {
            ctx.Response.StatusCode = 401;
        }
        else
        {
            ctx.Response.Redirect(ctx.RedirectUri);
        }
        return Task.CompletedTask;
    };
});
```

> **A limitação, dita com todas as letras.** Cookie foi feito para navegador, e
> é o navegador quem o reenvia sozinho a cada requisição. Um sistema parceiro
> não tem navegador e teria de guardar o nosso cookie na mão, como você vai
> fazer no passo 7. Integração de verdade entre sistemas usa **token**, com
> padrões como OAuth 2.0 e JWT. Isso não está na ementa da disciplina e não
> entra nesta aula: fica como estudo adiante.

---

## Passo 3: os dois DTOs (8 min)

Crie a pasta `Models/Dtos/` e, dentro dela, `ConsultaDtos.cs`:

```csharp
using System.ComponentModel.DataAnnotations;

namespace ClinicaVida.Web.Models.Dtos;

// Saída: o que a API mostra. `record` é uma classe enxuta, só de dados.
public record ConsultaResponse(
    int Id,
    int PacienteId,
    int MedicoId,
    string Data,
    string Horario,
    string? Observacoes);

// Entrada: o que a API aceita receber. Sem Id, porque quem gera o Id é o banco.
public class ConsultaRequest
{
    [Required(ErrorMessage = "Informe o paciente.")]
    public int PacienteId { get; set; }

    [Required(ErrorMessage = "Informe o médico.")]
    public int MedicoId { get; set; }

    [Required(ErrorMessage = "Informe a data.")]
    public DateTime Data { get; set; }

    [Required(ErrorMessage = "Informe o horário.")]
    [RegularExpression(@"^\d{2}:\d{2}$", ErrorMessage = "Use o formato HH:mm.")]
    public string Horario { get; set; } = "";

    [StringLength(300)]
    public string? Observacoes { get; set; }
}
```

**Por que não devolver a entidade `Consulta` direto?** Porque o contrato da
API não pode ser uma cópia da sua tabela:

- renomear uma coluna passaria a quebrar o sistema do parceiro;
- os tipos são os do banco, e `TimeSpan` sai serializado como `"14:30:00"`;
- a partir da Aula 17 as entidades vão se referenciar, e serializar navegação
  gera ciclo e resposta gigante;
- o DTO de entrada define exatamente o que a API **aceita**, e nada além disso.

Ainda no Controller, escreva o método de conversão que três actions vão usar:

```csharp
private static ConsultaResponse ParaResposta(Consulta c) => new(
    c.Id,
    c.PacienteId,
    c.MedicoId,
    c.Data.ToString("yyyy-MM-dd"),
    c.Horario.ToString(@"hh\:mm"),
    c.Observacoes);
```

A conversão roda **em memória**, sobre a lista já materializada. Chamar
`ToString` com formato dentro de uma consulta LINQ que o EF Core ainda vai
traduzir para SQL costuma falhar em tempo de execução: primeiro
`ToListAsync()`, depois `Select(ParaResposta)`.

---

## Passo 4: `GET api/consultas`, com filtros (8 min)

```csharp
[HttpGet]
public async Task<ActionResult<IEnumerable<ConsultaResponse>>> GetConsultas(
    [FromQuery] DateTime? data,
    [FromQuery] int? medicoId)
{
    var query = _context.Consultas.AsQueryable();

    if (data is not null) query = query.Where(c => c.Data == data.Value.Date);
    if (medicoId is not null) query = query.Where(c => c.MedicoId == medicoId);

    var consultas = await query
        .OrderBy(c => c.Data)
        .ThenBy(c => c.Horario)
        .ToListAsync();

    return Ok(consultas.Select(ParaResposta));
}
```

Os dois filtros são **opcionais**: sem nenhum deles, a resposta é a agenda
inteira. E lista vazia é **200 com `[]` no corpo**, nunca 404: a coleção
existe, ela só não tem nada dentro naquele dia.

---

## Passo 5: `GET api/consultas/{id}` (6 min)

```csharp
[HttpGet("{id:int}")]
public async Task<ActionResult<ConsultaResponse>> GetConsulta(int id)
{
    var consulta = await _context.Consultas.FindAsync(id);
    if (consulta is null) return NotFound();

    return Ok(ParaResposta(consulta));
}
```

A restrição `{id:int}` na rota descarta sozinha um `/api/consultas/abc`, que
nem chega à sua action. Guarde o nome desta action: é para ela que o
`CreatedAtAction` do passo 6 vai apontar.

**Aqui termina o Ciclo 3.** Do passo 6 em diante é sozinho.

---

## Passo 6: `POST`, `PUT` e `DELETE` (16 min)

```csharp
[HttpPost]
public async Task<ActionResult<ConsultaResponse>> PostConsulta(ConsultaRequest dto)
{
    if (!TimeSpan.TryParse(dto.Horario, out var horario))
        return BadRequest("Horário inválido. Use o formato HH:mm.");

    if (!await _context.Pacientes.AnyAsync(p => p.Id == dto.PacienteId))
        return BadRequest("Paciente inexistente.");

    if (!await _context.Medicos.AnyAsync(m => m.Id == dto.MedicoId))
        return BadRequest("Médico inexistente.");

    var consulta = new Consulta
    {
        PacienteId = dto.PacienteId,
        MedicoId = dto.MedicoId,
        Data = dto.Data.Date,
        Horario = horario,
        Observacoes = dto.Observacoes
    };

    _context.Consultas.Add(consulta);
    await _context.SaveChangesAsync();

    var resposta = ParaResposta(consulta);
    return CreatedAtAction(nameof(GetConsulta), new { id = consulta.Id }, resposta);
}
```

`CreatedAtAction` faz três coisas de uma vez: devolve **201**, monta o
cabeçalho `Location` apontando para `api/consultas/{id}` a partir da action
que lê o item, e põe o recurso criado no corpo. É esse cabeçalho que permite
ao parceiro consultar depois a consulta que ele acabou de agendar.

Repare também na diferença entre os dois tipos de 400: o de campo obrigatório
faltando você **não escreve**, porque `[ApiController]` valida as Data
Annotations antes da action rodar; o `BadRequest` escrito à mão é para a regra
de negócio, como um `MedicoId` que não existe no banco.

```csharp
[HttpPut("{id:int}")]
public async Task<IActionResult> PutConsulta(int id, ConsultaRequest dto)
{
    var consulta = await _context.Consultas.FindAsync(id);
    if (consulta is null) return NotFound();

    if (!TimeSpan.TryParse(dto.Horario, out var horario))
        return BadRequest("Horário inválido. Use o formato HH:mm.");

    consulta.PacienteId = dto.PacienteId;
    consulta.MedicoId = dto.MedicoId;
    consulta.Data = dto.Data.Date;
    consulta.Horario = horario;
    consulta.Observacoes = dto.Observacoes;

    await _context.SaveChangesAsync();
    return NoContent();
}

[HttpDelete("{id:int}")]
public async Task<IActionResult> DeleteConsulta(int id)
{
    var consulta = await _context.Consultas.FindAsync(id);
    if (consulta is null) return NotFound();

    _context.Consultas.Remove(consulta);
    await _context.SaveChangesAsync();
    return NoContent();
}
```

`PUT` **substitui** o recurso inteiro, por isso o DTO de entrada é o mesmo do
`POST` e todos os campos são obrigatórios. Alteração parcial é o verbo
`PATCH`, que fica fora desta aula.

Os dois devolvem **204**: a operação terminou e não há o que devolver no
corpo. Devolver 200 com uma mensagem de texto, como `Ok("Consulta excluída.")`,
obriga o parceiro a ler prosa em português para saber o que aconteceu, em vez
de olhar um número.

---

## Passo 7: testar os cinco endpoints (8 min)

Crie `ClinicaVida.http` na raiz do projeto. Antes de executar as chamadas,
faça login na aplicação pelo navegador, abra o DevTools em **Application,
Cookies** e copie o valor do cookie `.AspNetCore.Identity.Application`.

```http
@host = https://localhost:7145
@cookie = .AspNetCore.Identity.Application=COLE_AQUI_O_VALOR_DO_SEU_COOKIE

### 1. a agenda inteira
GET {{host}}/api/consultas
Accept: application/json
Cookie: {{cookie}}

### 2. a agenda de um dia, de um médico
GET {{host}}/api/consultas?data=2026-11-25&medicoId=3
Cookie: {{cookie}}

### 3. uma consulta específica
GET {{host}}/api/consultas/1
Cookie: {{cookie}}

### 4. id que não existe: precisa devolver 404
GET {{host}}/api/consultas/9999
Cookie: {{cookie}}

### 5. agendar: precisa devolver 201 e o cabeçalho Location
POST {{host}}/api/consultas
Content-Type: application/json
Cookie: {{cookie}}

{
  "pacienteId": 1,
  "medicoId": 3,
  "data": "2026-11-25T00:00:00",
  "horario": "14:30",
  "observacoes": "Retorno solicitado pelo laboratório parceiro"
}

### 6. corpo inválido: precisa devolver 400
POST {{host}}/api/consultas
Content-Type: application/json
Cookie: {{cookie}}

{ "pacienteId": 1, "horario": "14:30" }

### 7. remarcar: precisa devolver 204
PUT {{host}}/api/consultas/1
Content-Type: application/json
Cookie: {{cookie}}

{
  "pacienteId": 1,
  "medicoId": 3,
  "data": "2026-11-26T00:00:00",
  "horario": "09:00"
}

### 8. cancelar: precisa devolver 204
DELETE {{host}}/api/consultas/1
Cookie: {{cookie}}

### 9. sem cookie: precisa devolver 401
GET {{host}}/api/consultas
```

Na chamada 5, olhe a **aba de cabeçalhos** da resposta, e não só o corpo: o
`Location` precisa estar lá, com o endereço da consulta recém-criada.

---

## Passo 8: documentar a API (4 min)

No `README.md` do seu fork, acrescente a seção da API, com a mesma tabela que
você montou no exercício do Ciclo 1:

```markdown
## API de consultas

Todos os endpoints exigem autenticação; sem cookie válido, a resposta é 401.

| Verbo | Rota | O que faz | Sucesso | Falhas |
|---|---|---|---|---|
| GET | `/api/consultas` | lista a agenda; aceita `?data=` e `?medicoId=` | 200 | 401 |
| GET | `/api/consultas/{id}` | devolve uma consulta | 200 | 404 |
| POST | `/api/consultas` | agenda uma consulta | 201 + `Location` | 400 |
| PUT | `/api/consultas/{id}` | remarca, substituindo os dados | 204 | 400, 404 |
| DELETE | `/api/consultas/{id}` | cancela a consulta | 204 | 404 |
```

---

## Commit e push

```bash
git add Controllers/ConsultasApiController.cs Models/Dtos/ Program.cs ClinicaVida.http README.md
git commit -m "feat: API REST de consultas com os cinco endpoints"
git push -u origin feature/api-consultas
```

---

## Entregável

`ConsultasApiController` com os cinco endpoints testados e documentados, na
branch `feature/api-consultas`, commitado e enviado ao seu fork.
Especificamente:

- **1** Controller de API, com `[ApiController]`, `[Route("api/consultas")]` e
  `[Authorize]`.
- **5** endpoints: `GET` da coleção, `GET` do item, `POST`, `PUT` e `DELETE`.
- **2** DTOs em `Models/Dtos/`, um de entrada e um de saída.
- **1** arquivo `ClinicaVida.http` com as chamadas registradas, cobrindo os
  cinco endpoints e pelo menos um caso de 404 e um de 400.
- **1** seção de API no `README.md`, com a tabela de endpoints.

### Critérios de aceitação

| # | Critério | Como o professor confere |
|---|---|---|
| 1 | O Controller é de API | A classe herda de `ControllerBase`, tem `[ApiController]` e `[Route("api/consultas")]`, e não existe nenhuma View em `Views/ConsultasApi/` |
| 2 | A API está protegida | `GET /api/consultas` sem cookie devolve **401**, e não 200 nem a página de login em HTML |
| 3 | A listagem responde | Com cookie válido, `GET /api/consultas` devolve **200** e um array JSON com as consultas do banco |
| 4 | Os filtros funcionam | `GET /api/consultas?medicoId=N` devolve só as consultas daquele médico, e um dia sem consulta devolve 200 com `[]` |
| 5 | O item inexistente é 404 | `GET /api/consultas/9999` devolve **404**, com corpo vazio ou de problema, nunca 200 |
| 6 | A criação devolve 201 | `POST /api/consultas` com corpo válido devolve **201** e o cabeçalho `Location` apontando para o recurso criado |
| 7 | O corpo inválido é 400 | `POST` sem `medicoId` devolve **400** com os erros de validação, e nada é gravado no banco |
| 8 | Alteração e remoção são 204 | `PUT` e `DELETE` com id existente devolvem **204** sem corpo, e o efeito aparece no MySQL |
| 9 | A entidade não vaza | As respostas trazem os campos do `ConsultaResponse`, com `data` e `horario` formatados como texto, e não a entidade `Consulta` serializada |
| 10 | A API está documentada | O `README.md` do fork tem a tabela de endpoints e o `ClinicaVida.http` executa as chamadas |
| 11 | O trabalho foi enviado | A branch `feature/api-consultas` aparece no seu fork no GitHub, com o commit de sua autoria |

---

## Se algo der errado

- **A chamada devolve 302 e um HTML de login em vez de 401**: falta o
  `ConfigureApplicationCookie` do passo 2, ou ele foi escrito depois do
  `builder.Build()`. É o comportamento padrão do cookie do Identity, e ele
  serve ao navegador, não à integração.
- **Todas as chamadas devolvem 401, mesmo com o cookie colado**: o valor
  copiado está incompleto, ou você fez logout depois de copiar. Faça login de
  novo e copie o valor inteiro do cookie `.AspNetCore.Identity.Application`.
- **`404` em todas as rotas, inclusive na listagem**: a rota do Controller
  ficou `api/consultasapi`. Confira se o `[Route]` está escrito
  `[Route("api/consultas")]` e não `[Route("api/[controller]")]`.
- **`InvalidOperationException: No route matches the supplied values` no
  `CreatedAtAction`**: o `nameof` aponta para uma action que não existe ou que
  não recebe `id`. O alvo é a action do passo 5, `GetConsulta(int id)`.
- **`The JSON value could not be converted to System.TimeSpan`**: o
  `Horario` do DTO de entrada precisa ser `string`, e a conversão para
  `TimeSpan` acontece na action, com `TimeSpan.TryParse`.
- **`InvalidOperationException` citando `ToString` não traduzível**: a
  conversão para `ConsultaResponse` está dentro da consulta que o EF Core
  traduz para SQL. Materialize antes, com `ToListAsync()`, e só depois chame
  `Select(ParaResposta)`.
- **O `POST` devolve 400 sem você ter escrito nada**: é o `[ApiController]`
  validando as Data Annotations do `ConsultaRequest`. Leia o corpo da
  resposta: ele diz qual campo reprovou.
- **`Connection refused` ou a porta não responde**: o endereço do `.http` está
  com a porta errada. Use a porta que o `dotnet run` imprimiu no seu terminal,
  não a do roteiro.
