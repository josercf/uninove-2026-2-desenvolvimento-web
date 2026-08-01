# Laboratório da Aula 20

## Disciplina: Desenvolvimento Web
**Prof. José Romualdo | Uninove, Universidade Nove de Julho**

### Case: Clínica Vida+ (Fase 19, a entrega e a apresentação)

Na Aula 19 você entregou a Clínica Vida+ containerizada com Docker, publicada
pelo GitHub Codespaces, com URL acessível pela internet e registrada no
`README.md`. É o último degrau de uma escada que começou na Aula 01, com um fork
vazio.

Hoje o laboratório não constrói peça nova. Ele **fecha** o que existe e
**entrega**: checklist final rodado com o professor, pendências corrigidas,
branches integradas à `main` e a apresentação do projeto em cinco minutos, com
dois de arguição. O que estiver de fora da `main` ao final do encontro não entra
na correção.

Este é o último laboratório do semestre e o entregável dele é o **projeto
final**.

**Duração:** 60 minutos, individual, nos Ciclos 3 e 4.

---

## Pré-requisitos

- O fork de `josercf/uninove-2026-2-clinica-vida`, com a `main` atualizada.
- O entregável da Aula 19: `Dockerfile`, `compose.yaml`, `.dockerignore`,
  `.env` fora do repositório e `.devcontainer/devcontainer.json`.
- O codespace do seu fork, com Docker disponível.
- Acesso ao Google Classroom da disciplina, onde a entrega é postada.

O contrato técnico do semestre, que a correção confere:

| O quê | Valor |
|---|---|
| Projeto e namespace raiz | `ClinicaVida.Web` |
| `DbContext` | `ClinicaContext`, herdando de `IdentityDbContext<IdentityUser>` desde a Aula 15 |
| Banco | `clinicavida`, no MySQL, com o provedor `Pomelo.EntityFrameworkCore.MySql` |
| Entidades | `Especialidade`, `Medico`, `Paciente` e `Consulta` |
| Actions | em inglês: `Index`, `Details`, `Create`, `Edit`, `Delete` e `DeleteConfirmed` |
| Perfis | `Recepcao` e `Medico` |
| API | `ConsultasApiController`, na rota literal `api/consultas` |
| Publicação | Docker mais GitHub Codespaces, com a porta encaminhada em modo público |

Ao rodar a aplicação fora do contêiner, use sempre **a porta que o seu terminal
imprimiu**. Ela é sorteada por projeto em `Properties/launchSettings.json` e a
sua não é necessariamente a do colega ao lado.

---

## Aviso que decide a sua nota: a URL vive enquanto o codespace roda

A URL pública do Codespaces responde **apenas enquanto o codespace está em
execução**. Ele hiberna por inatividade, e a URL para de responder. Isso não é
defeito do seu projeto, é o funcionamento normal da plataforma, mas o efeito na
apresentação é o mesmo de um sistema fora do ar.

Por isso:

1. **Inicie o codespace pelo menos dez minutos antes de apresentar.**
2. Suba os contêineres e espere o serviço `db` ficar saudável.
3. Confirme que a porta encaminhada está marcada como **pública**, e não
   privada. Porta privada devolve **401** para quem não é você, inclusive para
   o professor.
4. Abra a URL em uma janela anônima, ou no celular fora da sua conta do GitHub,
   e faça um login de verdade.
5. Tenha a aplicação rodando também na sua máquina, como plano B.

---

## Passo 1: a aplicação publicada respondendo (12 min)

No codespace do seu fork:

```bash
docker compose up -d --build
docker compose ps          # o serviço db precisa aparecer como healthy
docker compose logs -f web # acompanhe até a aplicação anunciar que está ouvindo
```

Com os serviços de pé, teste na URL pública, em janela anônima:

- Cadastro de paciente, com o CPF mascarado sendo aceito.
- Agendamento de consulta, do começo ao fim, gravando no banco.
- Login com um usuário do perfil `Recepcao` e outro do perfil `Medico`.
- `GET api/consultas`, que precisa devolver **200** com a lista, e **401** para
  quem não está autenticado.

Anote a URL exata. Ela vai para o `README.md` e para o Google Classroom.

---

## Passo 2: o `README.md` que a banca lê primeiro (8 min)

Na raiz do seu fork, o `README.md` precisa responder, na primeira tela, a três
perguntas: o que é isso, como eu executo e onde eu vejo funcionando.

```markdown
# Clínica Vida+

Agendamento de consultas para uma clínica multiespecialidades, substituindo o
controle por telefone e papel. Cadastro de pacientes, médicos e especialidades,
agendamento com validação, área da recepção protegida por login e API REST de
consultas.

Feito em ASP.NET Core MVC, Entity Framework Core e MySQL.

## Deploy

https://SEU-CODESPACE-XXXX.app.github.dev

A URL responde enquanto o codespace está em execução.

## Como executar

1. Abra o repositório em um codespace, ou clone e use Docker localmente.
2. Crie o `.env` na raiz com as senhas do MySQL e a connection string. Ele não
   está no repositório, de propósito, e precisa ser recriado a cada ambiente.
3. `docker compose up -d --build`
4. Aplique as migrations conforme a seção abaixo.

## Usuários de demonstração

| Perfil    | Usuário                  |
|-----------|--------------------------|
| Recepcao  | recepcao@clinicavida.local |
| Medico    | medico@clinicavida.local   |

## Autor

Seu nome, Desenvolvimento Web, Uninove, 2026.2.
```

Nunca versione o `.env` nem a senha do banco. A connection string chega por
variável de ambiente, com a convenção de duplo sublinhado
`ConnectionStrings__DefaultConnection`, como na Aula 19.

---

## Passo 3: banco com dados de demonstração (8 min)

Sistema vazio não demonstra nada, e uma lista de "teste 1, teste 2" custa nota em
**banco de dados** e em **apresentação**.

Garanta, no banco `clinicavida` da sua publicação:

- **4** especialidades.
- **3** médicos, com CRM plausível e especialidade preenchida.
- **5** pacientes, com nome, CPF, data de nascimento, telefone e e-mail.
- **8** consultas, distribuídas entre datas passadas e futuras, para a agenda do
  dia, o histórico do paciente e o relatório por especialidade terem o que
  mostrar.

Se o banco da publicação estiver vazio, as migrations se aplicam sozinhas: o
`contexto.Database.Migrate()` que você pôs no `Program.cs` na Aula 19 roda a
cada subida da aplicação.

```bash
docker compose ps                 # o serviço db precisa estar healthy
docker compose up -d --build      # o Migrate() do Program.cs aplica o que faltar
docker compose logs web | tail    # confirme que subiu sem erro de conexão
```

**Não tente `dotnet ef database update` do terminal do codespace.** O
`compose.yaml` da Aula 19 publica só a porta do `web`; o serviço `db` não expõe
porta nenhuma para fora, e o nome de host `db` só existe dentro da rede do
compose. Do terminal você não alcança o banco, e o comando falha por timeout de
conexão, que é um erro que parece de configuração e não é.

Depois cadastre pelos próprios formulários, ou pelo `HasData` do
`ClinicaContext`, e confira na tela que nenhuma página quebra com o banco cheio.

---

## Passo 4: tudo integrado na `main` (7 min)

A correção clona a `main` do seu fork. Funcionalidade que ficou numa branch
esquecida não existe para quem corrige.

```bash
git branch -a
git switch main && git pull
git merge feature/deploy   # repita para cada branch que faltar
# resolva os conflitos, rode a aplicação e só então siga para a próxima branch
git push origin main
```

Depois de integrar tudo, rode a aplicação a partir da `main` limpa e repita o
teste do Passo 1. Confira pelo navegador, no GitHub, que o código está mesmo lá.

---

## Passo 5: a apresentação, Ciclo 4 (25 min da turma)

Cinco minutos de apresentação e dois de arguição, seguindo o roteiro escrito no
Ciclo 2:

| Bloco | Tempo | O que dizer |
|---|---|---|
| 1. O problema | 40 s | O agendamento por telefone e papel, e o que ele custava à clínica |
| 2. Demonstração ao vivo | 2 min | Um agendamento inteiro, na URL pública, do login à consulta gravada |
| 3. Arquitetura | 1 min | MVC, EF Core sobre MySQL, onde ficam autenticação e API |
| 4. A decisão difícil | 1 min | Uma decisão sua, com o motivo e a alternativa descartada |
| 5. O que faria diferente | 20 s | O próximo passo, se houvesse mais um mês |

O que não fazer: ler código linha a linha, começar instalando ou compilando algo,
pedir desculpa pelo que faltou e passar de cinco minutos. O tempo é cronometrado.

Enquanto um colega apresenta, preencha a **ficha de observação**: nome de quem
apresentou, nota de **1 a 5** em funcionalidade, código, banco de dados,
interface e apresentação, e uma frase sobre o que você levaria daquele projeto
para o seu.

---

## Commit e push

```bash
git add README.md
git commit -m "docs: entrega final da Clinica Vida"
git push origin main
```

---

## Entregável

O projeto final da disciplina, apresentado em sala e entregue no Google
Classroom ainda dentro do encontro. Especificamente:

- **1** apresentação realizada, de cinco minutos, com dois de arguição.
- **1** link do fork no GitHub, com a `main` atualizada e o histórico de commits
  do semestre.
- **1** URL de deploy funcional, com o codespace em execução no momento da
  apresentação.
- **1** linha, no post do Classroom, dizendo qual funcionalidade foi demonstrada.

### Critérios de aceitação

| # | Critério | Como o professor confere |
|---|---|---|
| 1 | O repositório tem histórico do aluno | `git log --oneline` mostra commits de sua autoria distribuídos ao longo do semestre, e não um único commit no último dia |
| 2 | Tudo está na `main` | Nenhuma funcionalidade apresentada vive apenas em branch: a `main` clonada roda o que foi demonstrado |
| 3 | O `README.md` responde às três perguntas | Descrição do sistema, instruções de execução e URL do deploy, todas na primeira tela do arquivo |
| 4 | A aplicação publicada responde | A URL abre em janela anônima, faz login e grava um agendamento, com o codespace iniciado antes da apresentação |
| 5 | A porta está pública | A URL responde para quem não é o dono do codespace, sem devolver 401 |
| 6 | O banco tem dados de demonstração | 4 especialidades, 3 médicos, 5 pacientes e 8 consultas com nomes plausíveis, e as telas de agenda, histórico e relatório exibem conteúdo |
| 7 | Nenhum segredo foi versionado | `.env` no `.gitignore`, e nenhuma senha em `appsettings.json` ou no histórico |
| 8 | O contrato técnico foi respeitado | `ClinicaVida.Web`, `ClinicaContext` herdando de `IdentityDbContext<IdentityUser>`, banco `clinicavida`, actions em inglês, perfis `Recepcao` e `Medico` e a API em `api/consultas` |
| 9 | A apresentação cumpriu o formato | Cinco minutos, os cinco blocos do roteiro e demonstração ao vivo na URL pública |
| 10 | A entrega foi postada | Link do repositório e URL do deploy no Google Classroom, dentro do encontro |

### Pesos da avaliação do projeto final

| Critério | Peso | O que é conferido |
|---|---|---|
| Funcionalidade | 30% | CRUD das quatro entidades, agendamento do começo ao fim, login com perfil e API respondendo |
| Código | 25% | MVC respeitado, validação no servidor, nenhum segredo versionado e histórico de commits de sua autoria |
| Banco de dados | 20% | Banco `clinicavida` com as quatro tabelas, chaves estrangeiras, índices e migrations aplicadas |
| Interface | 15% | Layout único em todas as telas, leitura confortável no celular e mensagens de erro visíveis |
| Apresentação | 10% | Cinco minutos cumpridos, demonstração ao vivo na URL pública e decisão técnica explicada |

A composição da média da disciplina continua a mesma: AV1 é
`(checkpoints x 0,40) + (prova objetiva x 0,60)`, a AV2 é a avaliação
institucional, a média é `(AV1 + AV2) / 2` e a aprovação exige **média maior ou
igual a 6,0**.

---

## Se algo der errado

- **A URL do Codespaces não abre, ou devolve 401 para o colega**: a porta está
  privada, ou o codespace hibernou. Reinicie o codespace, suba os contêineres e
  troque a visibilidade da porta para pública.
- **A aplicação sobe e o banco não conecta**: dentro do compose o host do banco é
  `db`, o nome do serviço, e não `localhost`. Confirme também que o `db` está
  saudável antes de o `web` tentar conectar.
- **`Pending model changes` ao subir**: existe alteração de Model sem migration
  correspondente. Gere a migration **na sua máquina ou no terminal do
  codespace**, com `dotnet ef migrations add NomeDaMigration`, commite o arquivo
  gerado e refaça `docker compose up -d --build`: o `Migrate()` do `Program.cs`
  aplica a nova migration ao subir. Gerar migration é trabalho de SDK e acontece
  fora do contêiner; aplicar acontece dentro dele, no arranque.
- **`git merge` acusa conflito em arquivo que você nem lembra de ter mexido**:
  resolva mantendo o que está na `main` quando a dúvida for só de formatação, e
  rode a aplicação depois de cada merge, um por vez.
- **A `main` roda, mas uma tela que funcionava sumiu**: aquela tela estava só na
  branch. Volte à branch, confira o arquivo que falta e integre de novo.
- **O login não funciona na publicação, mas funciona local**: o banco publicado
  não tem os usuários. Cadastre os dois usuários de demonstração diretamente na
  aplicação publicada.
- **A apresentação passou de cinco minutos no ensaio**: corte o bloco de
  arquitetura, nunca a demonstração ao vivo. É a demonstração que sustenta a nota
  de funcionalidade.
