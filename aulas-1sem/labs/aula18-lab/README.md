# Laboratório da Aula 18

## Disciplina: Desenvolvimento Web
**Prof. José Romualdo | Uninove, Universidade Nove de Julho**

### Case: Clínica Vida+ (Fase 17, a interface unificada)

Na Aula 17 você entregou os três relacionamentos mapeados na Fluent API, a
agenda do dia trazendo paciente, médico e especialidade em um único comando SQL,
o histórico do paciente e o relatório por especialidade. Por dentro, a aplicação
está pronta: CRUD, sessão, AJAX, login, API REST e quatro entidades ligadas.

Por fora, ela ainda é um rascunho. Cada View repete a própria moldura, as
tabelas não têm estilo, os botões têm tamanhos diferentes e, no celular, a tela
sai da largura da janela. Quem recebe a aplicação não vê o seu
`OnModelCreating`: vê a primeira tela.

Hoje isso muda. O `_Layout.cshtml` passa a concentrar tudo o que é igual em toda
tela, três Partial Views concentram o que se repete em algumas telas, e o
Bootstrap 5 entra por baixo da paleta da clínica, que continua sendo a que você
fixou na Aula 04. **Nenhuma regra de negócio é alterada neste laboratório.**

É o primeiro laboratório do Módulo 4.

**Duração:** 60 minutos, individual, nos Ciclos 3 e 4.

---

## Pré-requisitos

- O fork de `josercf/uninove-2026-2-clinica-vida` clonado na sua máquina.
- O entregável da Aula 17 na `main`: relacionamentos mapeados, agenda do dia
  com `Include`, histórico do paciente e relatório por especialidade.
- O login da Aula 15 funcionando, com os perfis `Recepcao` e `Medico`.
- O SDK do .NET 10 e o serviço do MySQL rodando.
- VS Code e o navegador com o DevTools, que hoje é ferramenta de trabalho e não
  de depuração.

Confirme o ponto de partida antes de começar:

```bash
dotnet --version            # precisa começar com 10.
dotnet ef migrations list   # nenhuma migration pendente
ls wwwroot/lib/bootstrap/dist/css/bootstrap.min.css
```

O último comando precisa encontrar o arquivo. **O Bootstrap 5 já está no seu
projeto desde a Aula 07**, servido do seu próprio `wwwroot`, porque o
`dotnet new mvc` o traz junto. Hoje você deixa de conviver com ele e passa a
usá-lo.

Ao rodar `dotnet run`, use sempre **a porta que o seu terminal imprimiu**. Ela é
sorteada por projeto em `Properties/launchSettings.json`, então a sua não é
necessariamente a do colega ao lado, nem a `7145` que costuma aparecer como
exemplo em tutoriais.

---

## Passo 1: a branch e o inventário (5 min)

```bash
git switch main && git pull
git switch -c feature/layout-bootstrap
```

Antes de mudar qualquer coisa, rode a aplicação e **tire uma captura da tela de
pacientes**. É o "antes" que você vai comparar no fim do laboratório, e é a
evidência mais convincente do trabalho de hoje.

Liste, em uma folha, as telas que você vai padronizar. No projeto padrão são
estas:

| Tela | Arquivo |
|---|---|
| Página inicial e Sobre | `Views/Home/Index.cshtml`, `Views/Home/Sobre.cshtml` |
| Especialidades | `Views/Especialidades/Index.cshtml`, `Details.cshtml` |
| Médicos | `Views/Medicos/Index.cshtml`, `Details.cshtml` |
| CRUD de paciente | `Views/Pacientes/` (Index, Details, Create, Edit, Delete, Historico) |
| Agendamento em duas etapas | `Views/Consultas/Agendar.cshtml`, `AgendarHorario.cshtml`, `Confirmacao.cshtml` |
| Agenda do dia e relatório | `Views/Consultas/Index.cshtml`, `Relatorio.cshtml` |
| Login e registro | `Views/Conta/Login.cshtml`, `Registrar.cshtml` |

Anote também os três trechos de marcação que mais se repetem entre essas telas.
São eles que virarão Partial View nos Passos 4 e 5.

---

## Passo 2: o `_Layout.cshtml` da clínica (12 min)

Todo o conteúdo deste passo mora em **um arquivo só**,
`Views/Shared/_Layout.cshtml`. É esse o ponto: mexer aqui muda todas as telas de
uma vez.

```cshtml
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>@ViewData["Title"] - Clínica Vida+</title>
    <link rel="stylesheet" href="~/lib/bootstrap/dist/css/bootstrap.min.css" />
    <link rel="stylesheet" href="~/css/site.css" asp-append-version="true" />
</head>
<body class="d-flex flex-column min-vh-100">
    <header>
        <nav class="navbar navbar-expand-lg navbar-vida" data-bs-theme="dark">
            <div class="container">
                <a class="navbar-brand fw-bold" asp-controller="Home" asp-action="Index">Clínica Vida+</a>

                <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                        data-bs-target="#menuVida" aria-controls="menuVida"
                        aria-expanded="false" aria-label="Abrir o menu">
                    <span class="navbar-toggler-icon"></span>
                </button>

                <div class="collapse navbar-collapse" id="menuVida">
                    <ul class="navbar-nav me-auto">
                        <li class="nav-item">
                            <a class="nav-link" asp-controller="Especialidades" asp-action="Index">Especialidades</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" asp-controller="Medicos" asp-action="Index">Médicos</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" asp-controller="Consultas" asp-action="Agendar">Agendar</a>
                        </li>
                        @if (User.Identity is not null && User.Identity.IsAuthenticated && User.IsInRole("Recepcao"))
                        {
                            <li class="nav-item">
                                <a class="nav-link" asp-controller="Pacientes" asp-action="Index">Pacientes</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" asp-controller="Consultas" asp-action="Index">Agenda do dia</a>
                            </li>
                        }
                    </ul>

                    @if (User.Identity is not null && User.Identity.IsAuthenticated)
                    {
                        <form class="d-flex" asp-controller="Conta" asp-action="Logout" method="post">
                            <span class="navbar-text me-3">@User.Identity.Name</span>
                            <button type="submit" class="btn btn-outline-light btn-sm">Sair</button>
                        </form>
                    }
                    else
                    {
                        <a class="btn btn-outline-light btn-sm" asp-controller="Conta" asp-action="Login">Entrar</a>
                    }
                </div>
            </div>
        </nav>
    </header>

    <main class="container py-4 flex-grow-1">
        <partial name="_Mensagens" />
        @RenderBody()
    </main>

    <footer class="footer-vida mt-auto py-3">
        <div class="container d-flex justify-content-between flex-wrap">
            <span>Clínica Vida+, 2026</span>
            <span>Unidade: @(Context.Request.Cookies["unidade-preferida"] ?? "não escolhida")</span>
        </div>
    </footer>

    <script src="~/lib/jquery/dist/jquery.min.js"></script>
    <script src="~/lib/bootstrap/dist/js/bootstrap.bundle.min.js"></script>
    <script src="~/js/site.js" asp-append-version="true"></script>
    @await RenderSectionAsync("Scripts", required: false)
</body>
</html>
```

Cinco pontos deste arquivo que valem atenção:

1. **A ordem das folhas de estilo.** O `site.css` vem **depois** do
   `bootstrap.min.css`, e é isso que permite customizar o framework no Passo 3
   sem editar o arquivo dele. **Nunca edite o `bootstrap.min.css`**: a próxima
   atualização apaga a sua alteração.
2. **`data-bs-theme="dark"` na `<nav>`** é o que deixa o texto do menu claro
   sobre o verde da clínica. No Bootstrap 5.3 essa é a forma atual; a classe
   `navbar-dark` das versões anteriores está obsoleta.
3. **O `bootstrap.bundle.min.js` no fim do `<body>`** é obrigatório. Sem ele o
   botão sanduíche e o modal do Passo 6 viram enfeite que não abre, sem nenhum
   erro na tela.
4. **`@await RenderSectionAsync("Scripts", required: false)`** precisa continuar
   existindo, senão as Views da Aula 10 e da Aula 14, que declaram
   `@section Scripts`, quebram em tempo de execução.
5. **O cookie da unidade preferida, da Aula 13**, muda de lugar mas não some.
   Se você o apagar, o teste do cookie daquela aula deixa de passar.

Se o seu projeto tem `~/ClinicaVida.Web.styles.css` no `<head>`, deixe a linha
onde está: é o CSS isolado por View que o próprio SDK gera.

---

## Passo 3: a paleta da clínica por cima do Bootstrap (8 min)

Aplicação com Bootstrap e sem customização tem a mesma cara de milhares de
outras. Acrescente ao fim de `wwwroot/css/site.css`:

```css
:root {
  /* As mesmas seis variáveis da Aula 04. Se já estiverem no arquivo,
     não duplique: apenas confira os valores. */
  --vida-primaria:   #0B6E75;
  --vida-secundaria: #2E9E7E;
  --vida-destaque:   #E4572E;
  --vida-fundo:      #F4F7F6;
  --vida-texto:      #1F2A30;
  --vida-borda:      #D6E2E0;

  /* Variáveis do próprio Bootstrap, redefinidas com a paleta da clínica. */
  --bs-body-bg:      #F4F7F6;
  --bs-body-color:   #1F2A30;
  --bs-border-color: #D6E2E0;
  --bs-primary-rgb:  11, 110, 117;   /* text-primary, bg-primary, link-primary */
}

/* O .btn-primary traz a cor compilada dentro dele e ignora o --bs-primary.
   Quem manda no botão são as variáveis do próprio componente. */
.btn-primary {
  --bs-btn-bg:                 var(--vida-primaria);
  --bs-btn-border-color:       var(--vida-primaria);
  --bs-btn-hover-bg:           #095A60;
  --bs-btn-hover-border-color: #095A60;
  --bs-btn-active-bg:          #074A50;
  --bs-btn-active-border-color:#074A50;
}

.btn-danger {
  --bs-btn-bg:           var(--vida-destaque);
  --bs-btn-border-color: var(--vida-destaque);
}

.navbar-vida { background-color: var(--vida-primaria); }

.footer-vida {
  background-color: #FFFFFF;
  border-top: 3px solid var(--vida-secundaria);
  font-size: 0.9rem;
}

.card { border-color: var(--vida-borda); }

/* A validação da Aula 10 marca o campo inválido com classes que NÃO são do
   Bootstrap. Estas duas regras ligam aquelas classes à paleta da clínica,
   sem trocar uma linha das Views. */
.input-validation-error { border-color: var(--vida-destaque); }
.field-validation-error {
  color: var(--vida-destaque);
  font-size: 0.875rem;
  display: block;
}
```

**Por que `--bs-primary` sozinho não pinta o botão.** No Bootstrap 5.3 as
utilitárias de cor (`text-primary`, `bg-primary`) leem `--bs-primary-rgb` em
tempo de execução, mas os componentes trazem a cor já compilada dentro deles: o
`.btn-primary` declara `--bs-btn-bg: #0d6efd` literalmente. Por isso o botão
precisa da sobrescrita própria acima. Abra o DevTools, inspecione um botão e
confira na aba de estilos qual regra venceu: é assim que se descobre isso sem
adivinhar.

Rode a aplicação. Antes de mexer em qualquer View, a mudança de fundo, de cor de
texto e de botão já deve estar visível em **todas** as telas.

---

## Passo 4: a Partial View de mensagens (10 min)

Desde a Aula 12 o projeto grava mensagens em `TempData`, e desde então cada View
repete o próprio bloco para exibi-las. São três chaves em uso no projeto:
`Sucesso`, `Aviso` e `Erro`.

Crie `Views/Shared/_Mensagens.cshtml`:

```cshtml
@if (TempData["Sucesso"] != null)
{
    <div class="alert alert-success alert-dismissible fade show" role="alert">
        @TempData["Sucesso"]
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
    </div>
}

@if (TempData["Aviso"] != null)
{
    <div class="alert alert-warning alert-dismissible fade show" role="alert">
        @TempData["Aviso"]
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
    </div>
}

@if (TempData["Erro"] != null)
{
    <div class="alert alert-danger alert-dismissible fade show" role="alert">
        @TempData["Erro"]
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
    </div>
}
```

A chamada já está no `_Layout.cshtml` do Passo 2, logo antes do `@RenderBody()`:

```cshtml
<partial name="_Mensagens" />
```

Agora **apague os blocos de mensagem soltos** que você escreveu nas Views da
Aula 12, da Aula 13 e da Aula 17. Eles não somem sozinhos, e se ficarem a
mensagem aparece duas vezes na tela.

Teste na ordem:

1. Cadastre um paciente. A mensagem verde aparece na listagem.
2. Clique no `X` do alerta. Ele fecha, o que só funciona porque o
   `bootstrap.bundle.min.js` está carregado.
3. Recarregue a página. A mensagem não volta, porque `TempData` sobrevive a um
   único redirecionamento.
4. Tente excluir um médico que já tem consultas. O aviso vermelho da Aula 17
   aparece, agora dentro do mesmo componente.

**Por que isto é uma Partial View e não um View Component.** Todo o dado de que
ela precisa já está no `TempData`, que é do contexto da requisição. Ela não
consulta o banco e não tem lógica própria: é marcação reaproveitada.

---

## Passo 5: as Partials de card e de linha (12 min)

A partir daqui você trabalha sozinho, com o professor circulando pela sala.

### `Views/Shared/_CardMedico.cshtml`

```cshtml
@model ClinicaVida.Web.Models.Medico

<div class="card h-100 shadow-sm">
    <div class="card-body d-flex flex-column">
        <h5 class="card-title mb-1">@Model.Nome</h5>
        <p class="card-text text-muted mb-2">CRM @Model.Crm</p>
        <span class="badge text-bg-secondary align-self-start mb-3">
            @Model.Especialidade?.Nome
        </span>
        <a class="btn btn-primary btn-sm mt-auto"
           asp-controller="Medicos" asp-action="Details" asp-route-id="@Model.Id">
            Ver detalhes
        </a>
    </div>
</div>
```

Em `Views/Medicos/Index.cshtml`, o laço passa a montar a grade e delegar o card:

```cshtml
<div class="row g-4">
    @foreach (var medico in Model)
    {
        <div class="col-12 col-md-6 col-lg-4">
            <partial name="_CardMedico" model="medico" />
        </div>
    }
</div>
```

**O `Include` não é detalhe.** Se a action não carregar a especialidade,
`Model.Especialidade` chega nula dentro da Partial e o `badge` sai vazio, sem
nenhum erro. No `MedicosController`:

```csharp
var medicos = await _context.Medicos
    .Include(m => m.Especialidade)
    .OrderBy(m => m.Nome)
    .AsNoTracking()
    .ToListAsync();
```

### `Views/Shared/_LinhaConsulta.cshtml`

A agenda do dia da Aula 17 é uma tabela, então a Partial da linha é um `<tr>`:

```cshtml
@model ClinicaVida.Web.Models.Consulta

<tr>
    <td class="fw-semibold">@Model.Horario.ToString(@"hh\:mm")</td>
    <td>@Model.Paciente?.Nome</td>
    <td>@Model.Medico?.Nome</td>
    <td><span class="badge text-bg-secondary">@Model.Medico?.Especialidade?.Nome</span></td>
</tr>
```

E `Views/Consultas/Index.cshtml`:

```cshtml
<div class="table-responsive">
    <table class="table table-striped table-hover align-middle">
        <thead>
            <tr>
                <th>Horário</th><th>Paciente</th><th>Médico</th><th>Especialidade</th>
            </tr>
        </thead>
        <tbody>
            @foreach (var consulta in Model)
            {
                <partial name="_LinhaConsulta" model="consulta" />
            }
        </tbody>
    </table>
</div>
```

O `table-responsive` em volta é o que evita a barra de rolagem horizontal na
página inteira quando a tabela não cabe no celular: quem rola é a tabela, e não
o documento.

---

## Passo 6: grid e componentes em todas as telas (13 min)

Agora as telas restantes. O padrão é sempre o mesmo.

### Formulários, em `Pacientes/Create`, `Pacientes/Edit` e `Conta/Registrar`

```cshtml
<form asp-action="Create" method="post">
    <div asp-validation-summary="ModelOnly" class="text-danger mb-3"></div>

    <div class="row g-3">
        <div class="col-12 col-md-6">
            <label asp-for="Nome" class="form-label"></label>
            <input asp-for="Nome" class="form-control" />
            <span asp-validation-for="Nome"></span>
        </div>
        <div class="col-12 col-md-6">
            <label asp-for="Cpf" class="form-label"></label>
            <input asp-for="Cpf" class="form-control" />
            <span asp-validation-for="Cpf"></span>
        </div>
        <div class="col-12 col-md-4">
            <label asp-for="DataNascimento" class="form-label"></label>
            <input asp-for="DataNascimento" class="form-control" />
            <span asp-validation-for="DataNascimento"></span>
        </div>
    </div>

    <div class="mt-4 d-flex gap-2">
        <button type="submit" class="btn btn-primary">Salvar</button>
        <a class="btn btn-outline-secondary" asp-action="Index">Cancelar</a>
    </div>
</form>
```

Regras que não mudam:

- `<select>` recebe `form-select`, **não** `form-control`.
- `<input type="checkbox">` recebe `form-check-input`, dentro de um
  `div.form-check`.
- O `<span asp-validation-for>` **não** leva classe do Bootstrap: quem o pinta
  são as duas regras que você escreveu no Passo 3.
- O `@section Scripts { <partial name="_ValidationScriptsPartial" /> }` no fim
  da View continua onde estava, desde a Aula 10.

### Listagens

`table table-striped table-hover align-middle` dentro de um
`div.table-responsive`, com os links de ação virando
`btn btn-sm btn-outline-primary` e `btn btn-sm btn-outline-danger`.

### Agendamento em duas etapas

Ponha os campos da Aula 13 dentro de uma `row` com `col-12 col-md-6`. **Não
mude nenhum `id`**: o `wwwroot/js/agendamento-ajax.js` da Aula 14 encontra os
campos por `id`, e trocar um deles faz a busca de horários livres parar de
funcionar sem nenhum erro visível na tela. Classes você troca à vontade.

### Exclusão de paciente, com modal (opcional, se sobrar tempo)

```cshtml
<button type="button" class="btn btn-sm btn-outline-danger"
        data-bs-toggle="modal" data-bs-target="#confirmaExclusao">
    Excluir
</button>
```

O `<div class="modal fade" id="confirmaExclusao">` fica no fim da View, com o
`form` de POST para `DeleteConfirmed` dentro do `modal-footer`.

### A conferência nas três larguras

Abra o DevTools, ative o modo dispositivo e percorra **todas** as telas em:

| Largura | O que precisa acontecer |
|---|---|
| 360px | Menu vira sanduíche e abre ao clique; cards em uma coluna; nenhuma rolagem horizontal na página |
| 768px | Cards em duas colunas; formulários em duas colunas |
| 1280px | Cards em três colunas; conteúdo centralizado pelo `container` |

Se aparecer barra de rolagem horizontal em 360px, o culpado quase sempre é uma
tabela sem `table-responsive` ou uma imagem sem `img-fluid`.

---

## Commit e push

```bash
git add Views/ wwwroot/css/site.css
git commit -m "feat: layout unificado com Partial Views e Bootstrap 5"
git push -u origin feature/layout-bootstrap
```

---

## Entregável

Interface unificada da Clínica Vida+, na branch `feature/layout-bootstrap`,
commitada e enviada ao seu fork. Especificamente:

- **1** `_Layout.cshtml` com navbar responsiva, área de conteúdo em `container`
  e rodapé, contendo `@RenderBody()` e a seção `Scripts` opcional.
- **3** Partial Views novas em `Views/Shared/`: `_Mensagens.cshtml`,
  `_CardMedico.cshtml` e `_LinhaConsulta.cshtml`.
- **0** blocos de cabeçalho, menu, rodapé ou mensagem repetidos dentro das
  Views.
- Bootstrap 5 aplicado a **todas** as telas listadas no Passo 1, incluindo o
  CRUD de pacientes, o agendamento em duas etapas e a agenda do dia.
- A paleta da Clínica Vida+ por cima do Bootstrap, no `wwwroot/css/site.css`.
- **3** larguras conferidas, sem rolagem horizontal em nenhuma delas.

### Critérios de aceitação

| # | Critério | Como o professor confere |
|---|---|---|
| 1 | O layout concentra a moldura | `Views/Shared/_Layout.cshtml` traz navbar, `@RenderBody()` e rodapé, e nenhuma View repete esses três elementos |
| 2 | A seção de scripts continua existindo | O layout tem `@await RenderSectionAsync("Scripts", required: false)`, e as telas com validação e AJAX continuam funcionando |
| 3 | As três Partial Views existem | `_Mensagens.cshtml`, `_CardMedico.cshtml` e `_LinhaConsulta.cshtml` estão em `Views/Shared/` e são chamadas com `<partial>` |
| 4 | A mensagem aparece uma vez só | Cadastrar um paciente mostra **um** alerta verde, não dois, e ele some no F5 seguinte |
| 5 | O Bootstrap está carregado do projeto | O `<head>` referencia `~/lib/bootstrap/dist/css/bootstrap.min.css`, e o `bootstrap.bundle.min.js` está no fim do `<body>` |
| 6 | A ordem das folhas de estilo está certa | O `site.css` é carregado **depois** do `bootstrap.min.css`, e o `bootstrap.min.css` não foi editado |
| 7 | A identidade visual é da clínica | O botão principal está no verde `#0B6E75` e não no azul padrão do Bootstrap, e o fundo usa `--vida-fundo` |
| 8 | A validação da Aula 10 segue visível | Enviar o formulário de paciente vazio mostra as mensagens de erro, em laranja avermelhado, e o campo inválido fica com a borda destacada |
| 9 | O menu responde ao celular | Em 360px o menu vira botão sanduíche e abre ao clique |
| 10 | A grade funciona nas três larguras | A lista de médicos mostra 1 card em 360px, 2 em 768px e 3 em 1280px |
| 11 | Nenhuma tela rola na horizontal | Em 360px, nenhuma das telas do Passo 1 apresenta barra de rolagem horizontal na página |
| 12 | O AJAX da Aula 14 continua funcionando | Escolher o médico no agendamento ainda carrega os horários livres sem recarregar a página |
| 13 | O login da Aula 15 continua funcionando | Entrar e sair funciona, e o menu mostra os links de recepção só para quem tem o perfil `Recepcao` |
| 14 | O trabalho foi enviado | A branch `feature/layout-bootstrap` aparece no seu fork no GitHub, com o commit de sua autoria |

---

## Se algo der errado

- **O menu sanduíche não abre em tela estreita**: falta o
  `bootstrap.bundle.min.js` no fim do `<body>`, ou o `data-bs-target` do botão
  não bate com o `id` da `div.collapse`. Os dois precisam ser idênticos,
  incluindo o `#`.
- **O botão continua azul depois do Passo 3**: você redefiniu só
  `--bs-primary`. O `.btn-primary` traz a cor compilada dentro dele; sobrescreva
  `--bs-btn-bg` e `--bs-btn-border-color`, como no Passo 3.
- **Nada do `site.css` faz efeito**: confira a ordem no `<head>`. Se o
  `site.css` vier antes do `bootstrap.min.css`, o framework vence toda vez.
- **`InvalidOperationException: The layout view '_Layout' could not be
  found`**: o arquivo foi renomeado ou saiu de `Views/Shared/`. O
  `Views/_ViewStart.cshtml` procura por esse nome exato.
- **`InvalidOperationException: The following sections have been defined but
  have not been rendered by the page at '/Views/Shared/_Layout.cshtml':
  'Scripts'`**: você removeu o `RenderSectionAsync` do layout, e alguma View
  ainda declara `@section Scripts`. Recoloque a linha.
- **`The partial view '_CardMedico' was not found`**: o arquivo não está em
  `Views/Shared/`, ou o nome no atributo `name` não bate com o nome do arquivo.
  O sublinhado inicial faz parte do nome.
- **O `badge` da especialidade sai vazio**: a action não trouxe o relacionado.
  Acrescente o `Include(m => m.Especialidade)`, como no Passo 5.
- **A mensagem de sucesso aparece duas vezes**: o bloco antigo continua dentro
  da View, além da Partial no layout. Apague o da View.
- **A busca de horários livres parou de funcionar**: algum `id` de campo mudou
  no Passo 6. O `agendamento-ajax.js` encontra os campos por `id`; devolva os
  nomes originais.
- **Aparece barra de rolagem horizontal no celular**: uma tabela sem
  `table-responsive`, uma imagem sem `img-fluid` ou um bloco com largura fixa em
  pixels. O DevTools mostra o elemento culpado ao selecionar o `<body>` e
  procurar quem ultrapassa a largura.
- **O texto do menu ficou escuro sobre o verde**: falta o `data-bs-theme="dark"`
  na `<nav>`. No Bootstrap 5.3 é ele quem clareia os links do menu.
