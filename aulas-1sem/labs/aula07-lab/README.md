# Laboratório da Aula 07

## Disciplina: Desenvolvimento Web
**Prof. José Romualdo | Uninove, Universidade Nove de Julho**

### Case: Clínica Vida+ (Fase 6, o ambiente e o projeto .NET)

Na Aula 06 você entregou o `assets/js/agendamento.js`, com validação de CPF,
data futura, horário de expediente, resumo na tela e filtro de
especialidades. O front-end da clínica está de pé, e é aí que ele para: o
agendamento existe apenas na memória daquela aba. Fechou o navegador,
acabou.

Guardar dado é trabalho de servidor, e o servidor desta disciplina fala C#.
Hoje começa o Módulo 2. O laboratório instala o SDK do .NET, cria o projeto
`ClinicaVida.Web` com `dotnet new mvc` e coloca a aplicação no ar na sua
máquina. Não há regra de negócio nova: o objetivo é ter, ao fim da aula, um
ambiente que compila e executa, porque é dele que as Aulas 08 a 20 partem.

**Duração:** 60 minutos, individual, nos Ciclos 3 e 4.

---

## Pré-requisitos

- O fork de `josercf/uninove-2026-2-clinica-vida` clonado na sua máquina.
- O entregável da Aula 06 na `main`: `assets/js/agendamento.js` com validação
  e filtro.
- **SDK do .NET 10 LTS.** Se ainda não estiver instalado, baixe em
  <https://dotnet.microsoft.com/download>. O passo 1 confere isso.
- VS Code com a extensão **C# Dev Kit**, ou Visual Studio.

---

## Contrato desta etapa, que vale até a Aula 20

Estes nomes são fixos e usados pelas próximas cinco aulas. Trocar qualquer um
deles quebra os comandos dos laboratórios seguintes.

| O quê | Valor |
|---|---|
| SDK | .NET 10 LTS, `TargetFramework` igual a `net10.0` |
| Projeto | `ClinicaVida.Web`, criado com `dotnet new mvc -n ClinicaVida.Web` |
| Branch desta aula | `feature/projeto-dotnet` |
| Banco (a partir da Aula 11) | `clinicavida`, no MySQL |

---

## Passo 1: o SDK na sua máquina (12 min)

```bash
dotnet --list-sdks      # precisa aparecer uma linha começando com 10.
dotnet --info
```

Se o terminal responder que `dotnet` não é um comando reconhecido, ou se a
maior versão listada for menor que 10, instale o **SDK do .NET 10 LTS**,
**feche e abra o terminal** e repita o comando. Terminal aberto antes da
instalação não enxerga o `dotnet`.

Anote a versão exata que o `dotnet --list-sdks` imprimiu: ela vai para o
`README.md` no passo 6.

> **SDK ou runtime?** Na sua máquina, sempre o **SDK**: ele traz a CLI, o
> compilador, os modelos de projeto e já inclui o runtime dentro. O runtime
> sozinho apenas executa uma aplicação já compilada, e é o que se instala em
> servidor, assunto da Aula 19.

---

## Passo 2: a branch do módulo (5 min)

Trabalho novo, branch nova, sempre a partir da `main` atualizada.

```bash
cd uninove-2026-2-clinica-vida

git switch main
git pull

git switch -c feature/projeto-dotnet
git status
```

---

## Passo 3: criar o projeto (11 min)

Na **raiz do fork**, ao lado do `index.html` e do `agendamento.html` que você
já tem:

```bash
dotnet new mvc -n ClinicaVida.Web

cd ClinicaVida.Web
ls          # dir, no Windows
```

O nome é `ClinicaVida.Web`, exatamente assim, com o ponto e sem acento. Ele
aparece no namespace do código, no nome da pasta e nos comandos das próximas
aulas.

Abra o `ClinicaVida.Web.csproj` e confirme o alvo de compilação:

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
</Project>
```

Se aparecer outra versão no `TargetFramework`, o SDK ativo não é o 10: volte
ao passo 1.

### O que foi criado, pasta por pasta

| Caminho | O que guarda |
|---|---|
| `Program.cs` | Ponto de entrada: liga os serviços e as rotas da aplicação |
| `ClinicaVida.Web.csproj` | O projeto: `net10.0` e os pacotes NuGet |
| `appsettings.json` | Configuração; na Aula 11 recebe a conexão com o MySQL |
| `Controllers/` | Recebem a requisição e decidem o que responder (Aula 08) |
| `Models/` | Paciente, Médico, Especialidade e Consulta (Aula 10) |
| `Views/` | As telas em Razor, arquivos `.cshtml` (Aula 08) |
| `wwwroot/` | Servido como está: CSS, JavaScript e imagens |

---

## Passo 4: o `.gitignore` do .NET (5 min)

Compilar gera as pastas `bin/` e `obj/`, com centenas de arquivos binários
recriados a cada build. Eles não vão para o Git.

```bash
cd ..                    # de volta à raiz do fork
dotnet new gitignore     # gera o .gitignore oficial do .NET

git status               # bin/ e obj/ não podem mais aparecer
```

Se `bin/` ou `obj/` já tiverem entrado no índice antes do `.gitignore`, o Git
continua rastreando os dois. Remova do índice sem apagar do disco:

```bash
git rm -r --cached ClinicaVida.Web/bin ClinicaVida.Web/obj
```

---

## Passo 5: subir a aplicação (12 min)

```bash
cd ClinicaVida.Web
dotnet watch run
```

O terminal imprime as URLs em que o servidor está escutando, algo como:

```text
Now listening on: https://localhost:7145
Now listening on: http://localhost:5145
```

Abra **o endereço que o seu terminal imprimiu**, não o deste roteiro: a porta
varia de máquina para máquina. Se o navegador avisar que o certificado não é
confiável, rode uma vez:

```bash
dotnet dev-certs https --trust
```

O `dotnet watch run` fica observando os arquivos: salvou, ele recompila e
atualiza o navegador sozinho. Para encerrar, `Ctrl+C`.

---

## Passo 6: a home da clínica e o README (15 min)

Ciclo 4, sozinho, com o `dotnet watch run` ligado.

**6.1.** Em `Views/Home/Index.cshtml`, troque o conteúdo de exemplo pela
apresentação da clínica:

```html
@{
    ViewData["Title"] = "Clínica Vida+";
}

<div class="text-center">
    <h1>Clínica Vida+</h1>
    <p>
        Clínica multiespecialidades. Agendamento de consultas com cardiologia,
        pediatria, ortopedia e dermatologia, das 07h às 19h.
    </p>
</div>
```

Salve e olhe o navegador: a página muda sozinha.

**6.2.** No `README.md` da raiz do fork, acrescente a seção do ambiente, com a
versão que **você** obteve no passo 1:

```markdown
## Ambiente .NET

- SDK: 10.0.x (obtido com `dotnet --list-sdks`)
- Executar: `cd ClinicaVida.Web` e depois `dotnet watch run`
```

---

## Commit e push

```bash
cd ..                    # raiz do fork
git add .
git commit -m "feat: projeto ClinicaVida.Web em ASP.NET Core MVC"
git push -u origin feature/projeto-dotnet
```

Olhe a contagem de arquivos do commit: dezenas é o esperado. Milhares é sinal
de `bin/` e `obj/` versionados, e o passo 4 precisa ser refeito.

---

## Entregável

O projeto `ClinicaVida.Web` criado, executando localmente, na branch
`feature/projeto-dotnet`, commitado e enviado ao seu fork. Especificamente:

- **1** projeto `ClinicaVida.Web`, com `TargetFramework` igual a `net10.0`.
- **1** `.gitignore` do .NET na raiz do fork, sem `bin/` nem `obj/`
  versionados.
- **1** página inicial com o nome e a apresentação da Clínica Vida+.
- **1** seção `## Ambiente .NET` no `README.md`, com a versão do SDK e o
  comando de execução.

### Critérios de aceitação

| # | Critério | Como o professor confere |
|---|---|---|
| 1 | O SDK está instalado e é o 10 | `dotnet --list-sdks` na máquina do aluno mostra uma versão 10.x |
| 2 | O projeto tem o nome do contrato | Existe a pasta `ClinicaVida.Web` com `ClinicaVida.Web.csproj` dentro |
| 3 | O alvo de compilação é o correto | O `.csproj` traz `<TargetFramework>net10.0</TargetFramework>` |
| 4 | A estrutura MVC está completa | Existem `Program.cs`, `appsettings.json`, `Controllers/`, `Models/`, `Views/` e `wwwroot/` |
| 5 | A aplicação sobe | `dotnet watch run` compila sem erro e a página abre na URL impressa pelo terminal |
| 6 | Nada de `bin/` e `obj/` no Git | O `.gitignore` existe e `git status` não lista as duas pastas |
| 7 | A home é da clínica | A página inicial mostra "Clínica Vida+" e um parágrafo de apresentação, não o texto de exemplo do modelo |
| 8 | O README registra o ambiente | O `README.md` traz a versão do SDK obtida na máquina do aluno e o comando de execução |
| 9 | O trabalho foi enviado | A branch `feature/projeto-dotnet` aparece no seu fork no GitHub, com o commit de sua autoria |

---

## Se algo der errado

- **`dotnet: command not found` ou `'dotnet' não é reconhecido`**: o SDK não
  está instalado, ou o terminal foi aberto antes da instalação. Instale e
  **feche e abra o terminal**; no Windows, faça logoff se ainda assim não
  resolver.
- **`The template "ASP.NET Core Web App (Model-View-Controller)" was not
  found`**: você tem apenas o runtime instalado, não o SDK. Modelos de
  projeto vêm no SDK.
- **`TargetFramework` diferente de `net10.0`**: há mais de um SDK na máquina e
  o ativo é outro. Confira com `dotnet --list-sdks` e instale o 10, ou crie um
  `global.json` na raiz fixando a versão.
- **O navegador acusa certificado não confiável**: rode
  `dotnet dev-certs https --trust` e recarregue. Em último caso, use a URL
  `http://` que o terminal também imprimiu.
- **`Address already in use` ao subir a aplicação**: há outra instância
  rodando em outro terminal. Encerre com `Ctrl+C` na janela antiga.
- **O commit ficou com milhares de arquivos**: `bin/` e `obj/` entraram no
  índice antes do `.gitignore`. Rode
  `git rm -r --cached ClinicaVida.Web/bin ClinicaVida.Web/obj`, confira o
  `git status` e comite de novo.
- **`dotnet watch` não atualiza o navegador**: alguns editores salvam com
  atraso, e alterações fora de `Views/` exigem recompilação completa. Pare com
  `Ctrl+C` e execute novamente.
