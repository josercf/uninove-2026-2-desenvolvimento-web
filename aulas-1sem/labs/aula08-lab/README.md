# Laboratório da Aula 08

## Disciplina: Desenvolvimento Web
**Prof. José Romualdo | Uninove, Universidade Nove de Julho**

### Case: Clínica Vida+ (Fase 7, as primeiras telas servidas pelo MVC)

Na Aula 07 você entregou o projeto `ClinicaVida.Web`, criado com
`dotnet new mvc`, executando localmente, com o `.gitignore` do .NET no lugar
e o `README.md` atualizado com a versão do SDK e o comando de execução. O que
aparece no navegador, porém, ainda é a página de exemplo do template.

Hoje a clínica entra na aplicação. O laboratório cria o
`EspecialidadesController` com as actions `Index` e `Details`, as Views Razor
correspondentes em `Views/Especialidades/`, a action `Sobre` no
`HomeController` e os links das duas telas novas no menu do layout. Nenhuma
linha de banco de dados: as especialidades são escritas à mão dentro da View,
e passam a ser objetos em uma coleção só na Aula 09.

**Duração:** 60 minutos, nos Ciclos 3 e 4. Os passos 1 a 3 são guiados pelo
professor; os passos 4 a 6 você faz sozinho.

---

## Pré-requisitos

- O fork de `josercf/uninove-2026-2-clinica-vida` clonado na sua máquina.
- O entregável da Aula 07 na `main`: o projeto `ClinicaVida.Web` executando
  com `dotnet watch run`.
- SDK .NET 10 instalado (`dotnet --info` responde com a versão).
- VS Code com o kit de C#, ou Visual Studio.

---

## Passo 1: a branch e a aplicação no ar (5 min)

```bash
git checkout main
git pull

git checkout -b feature/controllers-iniciais

cd ClinicaVida.Web
dotnet watch run
```

Deixe o `dotnet watch run` rodando até o fim da aula. A cada arquivo salvo ele
recompila e recarrega o navegador sozinho, e você vê o efeito de cada passo sem
parar o servidor.

---

## Passo 2: o EspecialidadesController (10 min)

Crie o arquivo `Controllers/EspecialidadesController.cs`. O nome do arquivo, o
nome da classe e o sufixo `Controller` não são detalhe de estilo: é por eles
que o roteamento encontra o seu código.

```csharp
using Microsoft.AspNetCore.Mvc;

namespace ClinicaVida.Web.Controllers;

public class EspecialidadesController : Controller
{
    public IActionResult Index()
    {
        ViewData["Titulo"] = "Especialidades da Clínica Vida+";

        return View();
    }
}
```

Abra `/Especialidades` na porta que o seu terminal imprimiu ao subir a
aplicação, algo como `https://localhost:7145/Especialidades`. A porta é
sorteada quando o projeto é criado e fica em `Properties/launchSettings.json`,
então a sua provavelmente não é a mesma do colega ao lado. O erro que aparece é **esperado**:
a action existe, mas a View ainda não. Leia a mensagem com atenção, porque ela
lista exatamente os caminhos onde o framework procurou o arquivo. É o próximo
passo.

---

## Passo 3: a View Index (10 min)

Crie a pasta `Views/Especialidades/` e, dentro dela, o arquivo `Index.cshtml`.
O nome da pasta é o nome do Controller sem o sufixo, e o nome do arquivo é o
nome da action: é assim que `return View()` acha o arquivo sem receber caminho
nenhum.

```html
@{
    ViewData["Title"] = "Especialidades";
}

<h1>@ViewData["Titulo"]</h1>

<ul>
    <li><a href="/Especialidades/Details/1?nome=Cardiologia">Cardiologia</a></li>
    <li><a href="/Especialidades/Details/2?nome=Pediatria">Pediatria</a></li>
    <li><a href="/Especialidades/Details/3?nome=Dermatologia">Dermatologia</a></li>
</ul>
```

Os links são escritos à mão de propósito, com a URL inteira, para você
reconhecer nela os três segmentos da rota padrão. Na Aula 10 eles são
substituídos por Tag Helpers, que geram o endereço a partir do nome da action.

**Checkpoint do Ciclo 3:** ao abrir `/Especialidades`, a lista precisa aparecer
dentro do layout, com o menu no topo e o rodapé embaixo. O professor confere
esta tela de mesa em mesa.

---

## Passo 4: a action Details (10 min)

Ciclo 4, sozinho. Volte ao `EspecialidadesController` e acrescente a segunda
action. Ela recebe **dois** parâmetros de origens diferentes: o `id` vem do
terceiro segmento da rota e o `nome` vem da query string.

```csharp
public IActionResult Details(int id, string nome)
{
    if (id < 1 || id > 3)
    {
        return NotFound();      // 404: essa especialidade não existe na clínica
    }

    ViewData["Id"] = id;
    ViewData["Nome"] = nome;

    return View();
}
```

O nome do parâmetro é o contrato: se ele se chamasse `codigo` em vez de `id`, a
rota não teria onde encaixar o `3` e o método receberia zero, sem nenhum erro
de compilação.

A estrutura `if` usada aqui ganha tratamento formal na Aula 09.

---

## Passo 5: a View Details (10 min)

Crie `Views/Especialidades/Details.cshtml`, na mesma pasta da View anterior,
porque é o mesmo Controller.

```html
@{
    ViewData["Title"] = "Detalhes da especialidade";
}

<h1>@ViewData["Nome"]</h1>

<p>Especialidade número @ViewData["Id"] da Clínica Vida+.</p>
<p>Atendimento com hora marcada, de segunda a sexta, das 07h às 19h.</p>

<p><a href="/Especialidades">Voltar para a lista</a></p>
```

Teste os dois caminhos: `/Especialidades/Details/2?nome=Pediatria` responde
com a tela, e `/Especialidades/Details/99` devolve 404.

Passar o nome pela query string é um recurso desta aula, para você ver os dois
tipos de parâmetro funcionando. Na Aula 09 a especialidade vira objeto em uma
coleção e a URL volta a carregar só o `id`.

---

## Passo 6: menu de navegação e página Sobre (15 min)

Traga o texto institucional que você escreveu em HTML no Módulo 1 para dentro
da aplicação, servido por uma action.

```csharp
// Controllers/HomeController.cs
public IActionResult Sobre()
{
    return View();       // Views/Home/Sobre.cshtml
}
```

Crie `Views/Home/Sobre.cshtml` com um `<h1>` e ao menos um parágrafo sobre a
Clínica Vida+. Depois, ligue as duas telas novas no menu, em
`Views/Shared/_Layout.cshtml`, dentro da lista de itens que já existe:

```html
<li class="nav-item">
    <a class="nav-link text-dark" href="/Especialidades">Especialidades</a>
</li>
<li class="nav-item">
    <a class="nav-link text-dark" href="/Home/Sobre">Sobre</a>
</li>
```

Editar um arquivo só, o layout, muda o menu de todas as telas. É esse ganho que
justifica a pasta `Shared`.

---

## Commit e push

```bash
git add .
git commit -m "feat: controllers e views iniciais da clinica"
git push -u origin feature/controllers-iniciais
```

---

## Entregável

`EspecialidadesController` com `Index` e `Details`, as Views correspondentes e
a navegação funcionando, na branch `feature/controllers-iniciais`, commitado e
enviado ao seu fork. Especificamente:

- **1** Controller novo, `EspecialidadesController`, com **2** actions.
- **3** Views novas: `Especialidades/Index.cshtml`,
  `Especialidades/Details.cshtml` e `Home/Sobre.cshtml`.
- **1** action `Sobre` no `HomeController`.
- **2** links novos no menu do `_Layout.cshtml`.

### Critérios de aceitação

| # | Critério | Como o professor confere |
|---|---|---|
| 1 | O Controller segue a convenção | O arquivo está em `Controllers/`, a classe se chama `EspecialidadesController` e herda de `Controller` |
| 2 | A rota chega na listagem | `/Especialidades` responde 200 e lista as três especialidades dentro do layout |
| 3 | As Views estão na pasta certa | Os arquivos estão em `Views/Especialidades/`, com o nome exato de cada action |
| 4 | O `id` chega pela rota | `/Especialidades/Details/2?nome=Pediatria` exibe o nome e o número 2 na tela |
| 5 | O id inexistente devolve 404 | `/Especialidades/Details/99` responde com a página de não encontrado |
| 6 | A página Sobre existe | `/Home/Sobre` responde com o texto institucional da clínica |
| 7 | O menu leva às telas novas | Os links Especialidades e Sobre aparecem em qualquer página e funcionam |
| 8 | A aplicação compila sem aviso | `dotnet build` termina sem erro, e o terminal do `dotnet watch` está limpo |
| 9 | O trabalho foi enviado | A branch `feature/controllers-iniciais` aparece no seu fork, com o commit de sua autoria |

---

## Se algo der errado

- **404 ao abrir `/Especialidades`**: o roteamento não achou o Controller. As
  causas comuns são o nome da classe sem o sufixo `Controller`, o arquivo fora
  da pasta `Controllers/`, a classe sem `public` ou a action sem `public`.
- **`InvalidOperationException: The view 'Index' was not found`**: a action
  rodou, mas o arquivo não está onde o framework procura. A mensagem lista os
  caminhos tentados; compare com o seu, lembrando que a pasta leva o nome do
  Controller **sem** o sufixo.
- **A tela de detalhes mostra o número 0**: o parâmetro da action não se chama
  `id`, ou a URL foi digitada com o valor na query string em vez do terceiro
  segmento. Confira a assinatura `Details(int id, string nome)`.
- **O nome da especialidade aparece vazio**: faltou o `?nome=` na URL, ou a
  chave usada na View (`ViewData["Nome"]`) está escrita diferente da que o
  Controller gravou. `ViewData` não avisa erro de digitação: imprime vazio.
- **O menu não mudou**: você editou uma View comum em vez de
  `Views/Shared/_Layout.cshtml`, ou o navegador serviu a página do cache.
  Recarregue com `Ctrl+F5`.
- **`dotnet watch` parou de recarregar**: mudança em arquivo `.cs` novo às
  vezes exige reinício. Interrompa com `Ctrl+C` e rode `dotnet watch run` de
  novo.
