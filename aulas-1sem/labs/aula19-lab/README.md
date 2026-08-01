# Laboratório da Aula 19

## Disciplina: Desenvolvimento Web
**Prof. José Romualdo | Uninove, Universidade Nove de Julho**

### Case: Clínica Vida+ (Fase 18, a clínica no ar)

Na Aula 18 você entregou o `_Layout.cshtml` e as Partial Views com Bootstrap 5
na paleta da clínica, com todas as telas responsivas. A aplicação está pronta:
cadastro de pacientes, agendamento com regra de conflito, agenda do dia, login
com perfis, API REST e interface unificada.

E ela responde em um endereço só: `https://localhost:` mais a porta que o seu
terminal sorteou. Ninguém fora da sua máquina alcança isso, nem a recepção da
clínica, nem o professor, nem o seu celular.

Hoje a Clínica Vida+ vira **dois contêineres Docker**, sobe no **GitHub
Codespaces** e ganha um endereço `https://` que qualquer navegador abre.

**Duração:** 60 minutos, individual, nos Ciclos 3 e 4.

---

## Pré-requisitos

- O fork de `josercf/uninove-2026-2-clinica-vida` clonado na sua máquina.
- O entregável da Aula 18 na `main`: o layout Bootstrap aplicado a todas as
  telas.
- Conta no GitHub com Codespaces habilitado. A cota mensal gratuita da conta
  pessoal basta para esta aula; o GitHub Student Developer Pack amplia essa
  cota.
- O SDK do .NET 10 e o MySQL locais, que você já usa desde a Aula 11.
- Docker instalado na sua máquina é **desejável, não obrigatório**: os Passos 2
  e 3 podem ser feitos apenas escrevendo os arquivos, e o primeiro `docker
  compose up` acontece dentro do codespace, no Passo 4.

Confirme o ponto de partida antes de começar:

```bash
dotnet --version            # precisa começar com 10.
git status                  # árvore limpa, na main
```

### Aviso sobre senhas

Todas as senhas deste roteiro são **didáticas e locais**, criadas para a aula e
válidas apenas dentro do seu contêiner. Não reaproveite nenhuma senha sua de
outro serviço, e não copie literalmente as daqui: troque cada uma por um valor
seu. Nenhuma delas pode terminar em arquivo versionado.

---

## Passo 1: a branch e a faxina de segredos (8 min)

```bash
git checkout main && git pull
git checkout -b feature/deploy
```

### O `.gitignore` primeiro, o arquivo depois

Esta ordem não é detalhe: um `.env` criado antes de o `.gitignore` conhecê-lo
entra no primeiro `git add .` distraído.

```bash
echo ".env" >> .gitignore
git add .gitignore && git commit -m "chore: ignora o .env"
```

### Tirar a senha do que é versionado

Em `ClinicaVida.Web/appsettings.json`, a connection string fica **sem senha e
sem host de produção**. Ela existe apenas como documentação da chave:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": ""
  },
  "Logging": { "LogLevel": { "Default": "Information" } },
  "AllowedHosts": "*"
}
```

A sua configuração local passa a viver no gerenciador de segredos, como já
acontece com a senha do seed desde a Aula 15:

```bash
cd ClinicaVida.Web
dotnet user-secrets set "ConnectionStrings:DefaultConnection" \
  "server=localhost;database=clinicavida;user=root;password=<a sua senha local>"
cd ..
```

Confira também o `appsettings.Development.json`: ele **é** versionado, e por
isso não pode guardar senha nenhuma.

> **Honestidade sobre o histórico:** se a sua senha local esteve no
> `appsettings.json` desde a Aula 11, ela continua no histórico do Git mesmo
> depois desta faxina. Para uma senha local de aula isso é aceitável; em um
> sistema real, uma senha que chegou ao repositório é considerada vazada e
> precisa ser trocada, não apenas removida do arquivo.

---

## Passo 2: `Dockerfile` e `.dockerignore` (10 min)

Na **raiz do repositório**, ao lado da pasta `ClinicaVida.Web/`, crie o
`Dockerfile`:

```dockerfile
# Etapa 1: build. O SDK completo compila e publica.
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src
COPY ClinicaVida.Web/*.csproj ClinicaVida.Web/
RUN dotnet restore ClinicaVida.Web/ClinicaVida.Web.csproj
COPY . .
RUN dotnet publish ClinicaVida.Web/ClinicaVida.Web.csproj -c Release -o /app/publish

# Etapa 2: runtime. Só o necessário para executar.
FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS final
WORKDIR /app
COPY --from=build /app/publish .
EXPOSE 8080
ENTRYPOINT ["dotnet", "ClinicaVida.Web.dll"]
```

Três decisões que valem uma leitura atenta:

1. **Multi-stage.** A imagem final parte do runtime, não do SDK: o compilador,
   os pacotes restaurados e o código-fonte ficam na etapa `build`, que é
   descartada. A imagem do SDK está na ordem de 1 GB; a do runtime, em algumas
   centenas de MB.
2. **O `.csproj` é copiado sozinho antes do `COPY . .`.** Cada instrução vira
   uma camada em cache. Enquanto as dependências não mudarem, o `restore` não
   roda de novo e o build de uma alteração de View leva segundos.
3. **A porta é a 8080.** A imagem `aspnet:10.0` escuta em HTTP na 8080 por
   padrão, e é essa porta que o Codespaces vai encaminhar.

E o `.dockerignore`, também na raiz:

```
bin/
obj/
.git/
.env
```

Sem ele, o `COPY . .` manda `bin/`, `obj/` e o histórico inteiro do Git para
dentro da imagem, e ainda arrisca levar junto o seu `.env`.

Se você tem Docker na máquina, confira o resultado:

```bash
docker build -t clinicavida .
docker images clinicavida
```

---

## Passo 3: `compose.yaml` e `.env` (10 min)

`compose.yaml`, na raiz:

```yaml
services:
  web:
    build: .
    ports: ["8080:8080"]
    environment:
      ASPNETCORE_ENVIRONMENT: Production
      ConnectionStrings__DefaultConnection: ${CONNECTION_STRING}
      SeedRecepcao__Senha: ${SEED_RECEPCAO_SENHA}
    depends_on:
      db:
        condition: service_healthy

  db:
    image: mysql:8.4
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: clinicavida
      MYSQL_USER: clinica
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    volumes: ["dados-mysql:/var/lib/mysql"]
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "127.0.0.1", "-u", "root", "-p$$MYSQL_ROOT_PASSWORD"]
      interval: 10s
      timeout: 5s
      retries: 12
      start_period: 30s

volumes:
  dados-mysql:
```

E o `.env`, na raiz, **fora do Git**:

```
MYSQL_ROOT_PASSWORD=troque-esta-raiz
MYSQL_PASSWORD=troque-esta-senha
CONNECTION_STRING=server=db;database=clinicavida;user=clinica;password=troque-esta-senha
SEED_RECEPCAO_SENHA=Troque-Esta-Senha1
```

Cinco pontos que decidem se isto sobe ou não:

- **O host do banco é `db`, não `localhost`.** Dentro do contêiner da
  aplicação, `localhost` é o próprio contêiner da aplicação, onde não existe
  MySQL nenhum. O compose publica o **nome do serviço** como nome de host na
  rede privada. Este é o erro número um de quem containeriza pela primeira vez.
- **A senha do `CONNECTION_STRING` precisa ser igual à de `MYSQL_PASSWORD`.**
  São a mesma senha, escrita em dois lugares.
- **O duplo sublinhado.** `ConnectionStrings__DefaultConnection` é a tradução
  da chave `ConnectionStrings:DefaultConnection` para nome de variável de
  ambiente, e ela sobrescreve o `appsettings.json` sem que você edite arquivo
  nenhum. O mesmo vale para `SeedRecepcao__Senha`, que na Aula 15 vinha do
  `user-secrets` e aqui vem do ambiente: sem ela, a semeadura do usuário
  inicial derruba a aplicação no arranque.
- **O `$$` no healthcheck.** Um `$` sozinho seria interpolado pelo compose; o
  `$$` escapa e entrega um `$` literal ao contêiner, que resolve a variável lá
  dentro.
- **`depends_on` com `condition: service_healthy`.** Sem isso o `web` sobe
  antes de o MySQL aceitar conexão, e a aplicação morre no primeiro
  `Migrate()`. No slide ele aparece em uma linha só,
  `depends_on: { db: { condition: service_healthy } }`, por causa do espaço da
  projeção: é o mesmo YAML escrito em notação de fluxo, e as duas formas valem.

---

## Passo 4: o codespace de pé (7 min)

Crie `.devcontainer/devcontainer.json`:

```json
{
  "name": "Clinica Vida+",
  "image": "mcr.microsoft.com/devcontainers/dotnet:10.0",
  "features": { "ghcr.io/devcontainers/features/docker-in-docker:2": {} },
  "forwardPorts": [8080],
  "customizations": {
    "vscode": { "extensions": ["ms-dotnettools.csdevkit"] }
  }
}
```

A `feature` de Docker é o que permite rodar `docker compose` **dentro** do
codespace. Sem ela, o comando não existe na máquina remota.

Envie a branch e crie o codespace:

```bash
git add Dockerfile compose.yaml .dockerignore .devcontainer/
git commit -m "feat: containeriza a Clinica Vida"
git push -u origin feature/deploy
```

No GitHub, no **seu fork**: botão **Code**, aba **Codespaces**, **Create
codespace on `feature/deploy`**.

Quando o terminal do codespace abrir, **recrie o `.env` lá dentro**:

```bash
cat > .env <<'FIM'
MYSQL_ROOT_PASSWORD=troque-esta-raiz
MYSQL_PASSWORD=troque-esta-senha
CONNECTION_STRING=server=db;database=clinicavida;user=clinica;password=troque-esta-senha
SEED_RECEPCAO_SENHA=Troque-Esta-Senha1
FIM
```

Ele não veio junto com o `git clone`, e é exatamente assim que tem de ser: o
segredo viaja por fora do repositório.

---

## Passo 5: migrations, semeadura e o proxy (12 min)

Fim do Ciclo 3. Daqui em diante você trabalha sozinho, com o professor
circulando pela sala.

### Aplicar as migrations ao subir

Em `Program.cs`, depois do `builder.Build()` e antes do `app.Run()`. O bloco de
semeadura da Aula 15 continua onde estava; o que entra hoje é o `Migrate()`
antes dele:

```csharp
using (var escopo = app.Services.CreateScope())
{
    var contexto = escopo.ServiceProvider.GetRequiredService<ClinicaContext>();
    contexto.Database.Migrate();
    await SeedIdentity.CriarPerfisEUsuarioInicialAsync(escopo.ServiceProvider);
}
```

O banco do contêiner nasce vazio, e `Migrate()` cria as tabelas e aplica o que
faltar toda vez que a aplicação sobe. É a estratégia mais simples e a adequada
a este projeto, que roda em uma instância só. Em um sistema com várias
réplicas, duas instâncias subiriam migrando ao mesmo tempo, e a migration
viraria um passo separado do deploy.

### Confiar no proxy do GitHub

O contêiner serve HTTP puro na 8080; quem termina o TLS é o proxy do
Codespaces. A aplicação precisa saber disso, senão ela se acha em HTTP,
descarta o cookie seguro e o login da Aula 15 para de funcionar.

Nos serviços, antes do `builder.Build()`:

```csharp
using Microsoft.AspNetCore.HttpOverrides;

builder.Services.Configure<ForwardedHeadersOptions>(opcoes =>
{
    opcoes.ForwardedHeaders =
        ForwardedHeaders.XForwardedFor | ForwardedHeaders.XForwardedProto;
    opcoes.KnownNetworks.Clear();
    opcoes.KnownProxies.Clear();
});
```

E no pipeline, como **primeiro** middleware:

```csharp
app.UseForwardedHeaders();
```

Ainda no pipeline, o `UseHttpsRedirection` passa a valer só em
desenvolvimento. Dentro do contêiner não existe porta HTTPS, e mantê-lo gera
redirecionamento para um endereço que não responde:

```csharp
if (app.Environment.IsDevelopment())
{
    app.UseHttpsRedirection();
}
```

### Subir e conferir

```bash
docker compose up --build
```

Acompanhe o log até ver o Kestrel escutando na 8080. Em outro terminal do
codespace:

```bash
docker compose exec db mysql -u clinica -p clinicavida -e "SHOW TABLES;"
docker compose exec db mysql -u clinica -p clinicavida -e "SELECT * FROM Especialidades;"
```

As tabelas do case e as do Identity precisam estar lá, e as quatro
especialidades da Aula 11 também.

---

## Passo 6: porta pública, teste real e o README (13 min)

### Tornar a porta pública

Na aba **PORTS** do VS Code, dentro do codespace: clique com o botão direito na
porta **8080**, escolha **Port Visibility** e marque **Public**.

Pela linha de comando, o equivalente é:

```bash
gh codespace ports visibility 8080:public -c $CODESPACE_NAME
```

A URL tem o formato
`https://<nome-do-seu-codespace>-8080.app.github.dev`.

**Confira em uma janela anônima.** Se aparecer a tela de login do GitHub ou um
`401`, a porta continua privada, e ninguém além de você abre o endereço,
inclusive o professor na hora de corrigir.

### Testar em produção, pela URL

Pela URL pública, não por `localhost`:

1. Cadastro de paciente, com CPF válido e com CPF inválido.
2. Agendamento de consulta, inclusive tentando o conflito de horário da Aula 13.
3. Login com o usuário inicial da Aula 15 e acesso à área da recepção.
4. A API: `GET /api/consultas` e `GET /api/consultas/1`.
5. Uma URL inexistente, para confirmar que aparece a **página de erro
   amigável**, e não a página de exceção detalhada.

### Registrar no `README.md`

Acrescente ao `README.md` do seu fork a seção **Publicação**, com:

- a URL pública da sua aplicação;
- o passo a passo para publicar outra vez, do zero;
- o seu checklist de publicação, em caixas de marcação;
- o aviso de que o `.env` não está no repositório e precisa ser recriado, com a
  lista dos nomes das variáveis, **sem os valores**.

---

## Commit e push

```bash
git add Dockerfile compose.yaml .dockerignore .devcontainer/ .gitignore \
        README.md ClinicaVida.Web/Program.cs ClinicaVida.Web/appsettings.json
git commit -m "feat: publicacao da Clinica Vida com Docker e Codespaces"
git push -u origin feature/deploy
```

Antes do push, rode `git status` e confirme: **o `.env` não pode aparecer**.

---

## O prazo da URL, dito com todas as letras

A URL do Codespaces existe **enquanto o codespace está rodando**. Depois de um
período sem uso ele hiberna, e o endereço para de responder até você iniciá-lo
de novo. Isso não é defeito do material nem erro seu: é como o Codespaces
funciona, e é o preço de um deploy sem cartão de crédito.

Consequência prática, e ela vale nota:

> **A apresentação do projeto final, na Aula 20, exige a URL respondendo.**
> Inicie o seu codespace, rode `docker compose up` e confira a porta pública
> **antes de entrar na sala**, não na hora de apresentar. Os dados continuam
> lá: o volume `dados-mysql` sobrevive à hibernação e ao `compose down`.

---

## Entregável

Aplicação publicada e acessível pela internet, na branch `feature/deploy`,
commitada e enviada ao seu fork. Especificamente:

- **4** arquivos novos de infraestrutura: `Dockerfile`, `compose.yaml`,
  `.dockerignore` e `.devcontainer/devcontainer.json`.
- **1** `Dockerfile` multi-stage, com build no SDK e runtime no `aspnet`.
- **2** serviços no `compose.yaml`, `web` e `db`, com volume nomeado,
  `healthcheck` e `depends_on` por saúde.
- **0** senhas em arquivo versionado: todas no `.env`, que está no
  `.gitignore`.
- **1** URL pública respondendo, aberta em janela anônima, com cadastro,
  agendamento, login e API funcionando.
- **1** seção **Publicação** no `README.md`, com a URL e o checklist.

### Critérios de aceitação

| # | Critério | Como o professor confere |
|---|---|---|
| 1 | A imagem é multi-stage | O `Dockerfile` tem duas etapas, `FROM ... sdk:10.0 AS build` e `FROM ... aspnet:10.0`, com `COPY --from=build` |
| 2 | O contexto do build é enxuto | O `.dockerignore` traz `bin/`, `obj/`, `.git/` e `.env` |
| 3 | Os dois serviços sobem juntos | `docker compose up` deixa `web` e `db` em execução, sem reiniciar em laço |
| 4 | O host do banco é o nome do serviço | A connection string usa `server=db`, e não `localhost` |
| 5 | A ordem de arranque é garantida | O `db` tem `healthcheck` e o `web` tem `depends_on` com `condition: service_healthy` |
| 6 | Os dados sobrevivem | O volume nomeado `dados-mysql` está declarado, e um `compose down` seguido de `up` mantém os pacientes cadastrados |
| 7 | Nenhum segredo versionado | `git log -p` e a árvore atual não trazem senha; o `.env` está no `.gitignore` e ausente do repositório |
| 8 | A configuração entra por variável de ambiente | `ConnectionStrings__DefaultConnection` e `SeedRecepcao__Senha` chegam pelo ambiente, com duplo sublinhado |
| 9 | O ambiente é de produção | `ASPNETCORE_ENVIRONMENT=Production` no serviço `web`, e uma URL inexistente mostra a página de erro amigável |
| 10 | As migrations foram aplicadas | As tabelas do case e as do Identity existem no banco do contêiner, e as especialidades da Aula 11 estão semeadas |
| 11 | A porta está pública | Uma janela anônima abre a URL sem pedir login do GitHub e sem devolver 401 |
| 12 | A aplicação funciona em produção | Pela URL: cadastro de paciente, agendamento com bloqueio de conflito, login e `GET /api/consultas` |
| 13 | A URL está registrada | O `README.md` traz a seção **Publicação**, com a URL, o passo a passo e o checklist |
| 14 | O trabalho foi enviado | A branch `feature/deploy` aparece no seu fork no GitHub, com o commit de sua autoria |

---

## Se algo der errado

- **`Unable to connect to any of the specified MySQL hosts`, ou conexão
  recusada na 3306**: a connection string está com `server=localhost`. Dentro
  do contêiner, `localhost` é o próprio contêiner do `web`. Troque por
  `server=db`, o nome do serviço.
- **`Access denied for user 'clinica'`**: a senha do `CONNECTION_STRING` está
  diferente da de `MYSQL_PASSWORD`. Se você já tinha subido antes, o volume
  guardou o usuário com a senha antiga: `docker compose down -v` recria o banco
  do zero, apagando os dados.
- **A aplicação sobe, tenta migrar e morre**: o `db` ainda não estava pronto.
  Confira o `healthcheck` e o `depends_on` com `condition: service_healthy`.
- **O `healthcheck` nunca fica saudável**: o `$$` virou `$` no `compose.yaml`,
  e a senha chegou vazia ao `mysqladmin`. Confira também se o `.env` existe no
  diretório de onde você rodou o `docker compose`.
- **`InvalidOperationException: Defina SeedRecepcao:Senha no user-secrets`**:
  dentro do contêiner não há `user-secrets`. A senha do usuário inicial precisa
  chegar como `SeedRecepcao__Senha`, com duplo sublinhado, pelo `.env`.
- **A URL pede login do GitHub, ou devolve 401**: a porta 8080 continua
  privada. Aba **PORTS**, botão direito, **Port Visibility**, **Public**.
- **A URL não responde nada**: o codespace hibernou. Abra-o de novo no GitHub e
  rode `docker compose up`.
- **`ERR_TOO_MANY_REDIRECTS` ou redirecionamento para uma porta estranha**: o
  `UseHttpsRedirection` continua ativo em produção. Deixe-o apenas em
  desenvolvimento.
- **O login aceita a senha e volta para a tela de login**: falta o
  `app.UseForwardedHeaders()` como primeiro middleware. Sem ele a aplicação se
  acha em HTTP atrás do proxy e descarta o cookie seguro.
- **A página de exceção detalhada aparece na URL pública**: o
  `ASPNETCORE_ENVIRONMENT` não chegou como `Production` ao contêiner. Confira o
  `environment` do serviço `web` com `docker compose config`.
- **O build demora minutos a cada alteração**: o `COPY . .` veio antes do
  `restore`, e o cache de camadas se perdeu. Copie primeiro o `.csproj`.
- **A imagem final passa de 1 GB**: a última etapa está partindo do `sdk` em
  vez do `aspnet`, ou falta o `.dockerignore`.
- **O `.env` apareceu no `git status`**: ele foi criado antes de o `.gitignore`
  conhecê-lo. Rode `git rm --cached .env`, confirme a linha no `.gitignore` e,
  se ele chegou a ser commitado, troque as senhas.
