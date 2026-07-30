# Plano de Ensino

## 1. Identificação

| Campo | Valor |
|---|---|
| Disciplina | Desenvolvimento Web |
| Instituição | Uninove, Universidade Nove de Julho |
| Nível | Graduação |
| Semestre | 2026.2 |
| Professor | José Romualdo |
| Contato | <jose.romualdo@uni9.pro.br> |
| Turmas | Duas turmas com conteúdo idêntico: uma às quartas-feiras, outra às quintas-feiras |
| Horário | 19h30 às 22h00 |
| Encontros | 20 encontros de 150 minutos cada |
| Carga horária total | 50 horas-aula |
| Entrega de atividades | Google Classroom, quando as turmas forem configuradas pela instituição |
| Repositório do acervo | <https://github.com/josercf/uninove-2026-2-desenvolvimento-web> |
| Repositório-esqueleto do case | <https://github.com/josercf/uninove-2026-2-clinica-vida> |

As duas turmas cobrem exatamente o mesmo conteúdo, na mesma ordem, com os mesmos
entregáveis. O que muda entre elas é apenas o calendário, registrado no
cronograma da seção 5.

## 2. Ementa

Fundamentos da web e arquitetura cliente-servidor. Protocolos e infraestrutura:
TCP/IP, DNS, HTTP e HTTPS. Marcação de conteúdo com HTML5 semântico.
Estilização e layout responsivo com CSS3, Flexbox e Grid. Formulários e
validação nativa. Programação no navegador com JavaScript: tipos, funções,
manipulação do DOM e eventos. Linguagem C# e a plataforma .NET. Padrão MVC com
ASP.NET Core: rotas, Controllers, Views e Razor. Models, Data Annotations e
validação no servidor. Persistência com Entity Framework Core sobre MySQL:
migrations, CRUD e relacionamentos. Estado no servidor com cookies e sessões.
Requisições assíncronas com AJAX e `fetch`. Autenticação e autorização. Serviços
web no estilo REST. Layout, Partial Views e Bootstrap 5. Publicação e deploy de
aplicações web. Desenvolvimento de um projeto integrador ao longo do semestre.

### Objetivos gerais

Ao final da disciplina, o aluno deve ser capaz de:

1. Explicar como uma requisição sai do navegador e volta como resposta,
   nomeando as camadas envolvidas.
2. Construir páginas com HTML semântico e CSS responsivo.
3. Programar comportamento no navegador com JavaScript.
4. Desenvolver uma aplicação web completa em ASP.NET Core MVC com C#.
5. Persistir e recuperar dados em MySQL usando Entity Framework Core.
6. Proteger áreas da aplicação com autenticação e autorização.
7. Expor e consumir uma API REST.
8. Publicar a aplicação em um ambiente acessível pela internet.
9. Versionar o próprio trabalho com Git e GitHub de forma disciplinada.

## 3. Metodologia

A disciplina **não usa sala de aula invertida**. Cada encontro é
autossuficiente: tudo o que o aluno precisa para acompanhar chega dentro da
própria aula. Não há atividade prévia obrigatória, não há leitura antecipada e
nenhum conteúdo é cobrado antes de ter sido apresentado em sala.

### 3.1 A estrutura do encontro

Os 150 minutos são organizados em quatro ciclos, mais um quiz de fixação e um
fechamento. Não há intervalo formal: a própria troca de ciclo funciona como
respiro.

```
19h30 às 20h05  Ciclo 1: conceito, demonstração, exercício curto
20h05 às 20h40  Ciclo 2: conceito, demonstração, exercício curto
20h40 às 20h50  Quiz de fixação
20h50 às 21h25  Ciclo 3: laboratório guiado, parte 1
21h25 às 21h50  Ciclo 4: laboratório, parte 2, e entregável
21h50 às 22h00  Fechamento, commit e prévia da próxima aula
```

Os ciclos 1 e 2 seguem sempre o mesmo ritmo interno: o professor apresenta o
conceito, demonstra ao vivo no projetor e o aluno reproduz num exercício curto,
ainda dentro do ciclo. Os ciclos 3 e 4 são laboratório: o aluno constrói uma
etapa do case com o professor circulando pela sala. O entregável nasce dentro do
ciclo 4, não fora da aula.

### 3.2 A espiral de conteúdo

O conteúdo avança em espiral, não em blocos isolados. Toda aula a partir da
Aula 02 abre com uma recapitulação curta da anterior e acrescenta uma camada
sobre o que já existe. O entregável de uma aula é o ponto de partida da
seguinte, de modo que ninguém começa do zero em nenhum encontro.

### 3.3 Recursos

Slides Reveal.js publicados no portal da disciplina, demonstrações ao vivo,
roteiros de laboratório versionados, repositório-esqueleto do case no GitHub e
quizzes de fixação aplicados em sala.

## 4. O case integrador: Clínica Vida+

Todo o semestre é construído em torno de um único sistema, a **Clínica Vida+**,
um sistema de agendamento de consultas médicas. Não existem exercícios soltos de
tema aleatório: cada aula faz o mesmo sistema avançar um passo concreto.

### 4.1 Mini mundo

A Clínica Vida+ é uma clínica com várias especialidades e um corpo clínico
próprio. Hoje o agendamento é feito por telefone, anotado em papel, o que gera
consultas em duplicidade, pacientes sem confirmação e nenhuma visão de agenda.
A clínica quer um sistema web onde o paciente consulte especialidades e
horários, a recepção registre e acompanhe os agendamentos e o médico veja a
própria agenda do dia.

### 4.2 Atores

| Ator | O que faz no sistema |
|---|---|
| Paciente | Consulta especialidades e horários disponíveis e solicita um agendamento |
| Recepção | Cadastra pacientes, confirma, remarca e cancela consultas, acompanha a agenda do dia |
| Médico | Consulta a própria agenda e o histórico do paciente que vai atender |

### 4.3 Entidades principais

| Entidade | Descrição |
|---|---|
| Paciente | Quem é atendido. Nome, CPF, data de nascimento, telefone, e-mail |
| Médico | Quem atende. Nome, CRM, especialidade a que pertence |
| Especialidade | Área de atuação, por exemplo Cardiologia ou Pediatria. Nome e descrição |
| Consulta | O agendamento em si. Liga um paciente a um médico em uma data e hora, com status e observações |

### 4.4 Como o case evolui

| Etapa | Aulas | Estado do case |
|---|---|---|
| Página estática | 01 a 05 | Site institucional da clínica em HTML e CSS, com página inicial, lista de especialidades e formulário de agendamento sem envio |
| Interatividade no navegador | 06 | O formulário valida no cliente e a lista de especialidades filtra sem recarregar a página |
| Aplicação MVC | 07 a 10 | O site vira uma aplicação ASP.NET Core MVC, com Controllers, Views Razor e Models validados no servidor |
| Persistência | 11 e 12 | Os dados passam a viver em MySQL via Entity Framework Core, com CRUD completo |
| Funcionalidades avançadas | 13 a 17 | Sessões, AJAX, autenticação, API REST e relacionamentos entre as quatro entidades |
| Produção | 18 a 20 | Layout profissional com Bootstrap, deploy publicado e apresentação do projeto final |

Ao final do semestre, o aluno terá em seu próprio repositório uma aplicação
ASP.NET Core MVC funcional, com banco MySQL, autenticação, API REST e deploy
acessível pela internet.

## 5. Cronograma

| Aula | Data quarta | Data quinta | Módulo | Tema | Entregável |
|---|---|---|---|---|---|
| 01 | 05/08/2026 | 06/08/2026 | 1 Fundamentos da Web e Front-End | Apresentação, panorama da web, Git e GitHub | Link do fork do repositório-esqueleto com pelo menos um commit de autoria do aluno |
| 02 | 12/08/2026 | 13/08/2026 | 1 | Estrutura da web e redes TCP/IP | `docs/arquitetura.md` no fork, com o diagrama da requisição e as evidências de DNS e HTTP coletadas em aula |
| 03 | 19/08/2026 | 20/08/2026 | 1 | Introdução ao HTML | `index.html` da Clínica Vida+ com estrutura semântica completa, em branch própria e Pull Request aberto |
| 04 | 26/08/2026 | 27/08/2026 | 1 | Introdução ao CSS | `assets/css/site.css` estilizando a página inicial com a identidade visual da clínica |
| 05 | 02/09/2026 | 03/09/2026 | 1 | CSS avançado e formulários HTML | `agendamento.html` responsivo, com formulário completo e validação nativa |
| 06 | 09/09/2026 | 10/09/2026 | 1 | Introdução ao JavaScript | `assets/js/agendamento.js` validando o formulário e filtrando a lista de especialidades |
| 07 | 16/09/2026 | 17/09/2026 | 2 Backend com C# e ASP.NET Core MVC | Ambiente de desenvolvimento .NET | Projeto `ClinicaVida.Web` criado, executando localmente, com o print do `dotnet --info` no README |
| 08 | 23/09/2026 | 24/09/2026 | 2 | Primeiros passos com ASP.NET Core MVC | `EspecialidadesController` com a action `Index` e View Razor correspondente |
| 09 | 30/09/2026 | 01/10/2026 | 2 | Estruturas de controle e coleções em C# | Lista de médicos em memória, filtrada por especialidade e exibida na View |
| 10 | 07/10/2026 | 08/10/2026 | 2 | Formulários e Models no MVC | Model `Consulta` com Data Annotations e formulário de agendamento validando no servidor |
| 11 | 14/10/2026 | 15/10/2026 | 2 | Entity Framework Core e MySQL | `ClinicaContext` configurado, migration inicial aplicada e banco `clinicavida` criado no MySQL |
| 12 | 21/10/2026 | 22/10/2026 | 2 | CRUD completo com EF Core | CRUD completo de Paciente, com listagem, cadastro, edição e exclusão persistindo no banco |
| 13 | 28/10/2026 | 29/10/2026 | 3 Acesso a Dados e Funcionalidades Avançadas | Cookies e sessões | Fluxo de agendamento em duas etapas guardado em sessão, mais cookie de preferência de unidade |
| 14 | 04/11/2026 | 05/11/2026 | 3 | Requisições HTTP assíncronas com AJAX | Consulta de horários livres por AJAX, sem recarregar a página |
| 15 | 11/11/2026 | 12/11/2026 | 3 | Autenticação e autorização | Login e logout funcionando, com a área da recepção protegida por perfil |
| 16 | 18/11/2026 | 19/11/2026 | 3 | API REST com ASP.NET Core | `ConsultasApiController` com os endpoints REST, testados e documentados |
| 17 | 25/11/2026 | 26/11/2026 | 3 | Relacionamentos e EF Core avançado | Relacionamentos entre as quatro entidades mapeados, com consultas usando `Include` e projeção |
| 18 | 02/12/2026 | 03/12/2026 | 4 Tópicos Avançados e Projeto Final | Layout, Partial Views e Bootstrap | `_Layout.cshtml` e Partial Views com Bootstrap 5 aplicados a todas as telas |
| 19 | 09/12/2026 | 10/12/2026 | 4 | Publicação e deploy | Aplicação publicada, com URL acessível e banco de produção configurado |
| 20 | 16/12/2026 | 17/12/2026 | 4 | Revisão geral e projeto final | Apresentação do projeto final, repositório no GitHub e deploy funcional |

As datas acima são geradas a partir do módulo `aulas-1sem/assets/js/turmas.js`,
que é a fonte da verdade do calendário. Qualquer alteração de data precisa ser
feita lá e refletida nesta tabela.

## 6. Avaliação

O modelo de avaliação é o mesmo de 2026.1, sem alteração.

### 6.1 Composição

| Instrumento | Peso | Descrição |
|---|---|---|
| AV1, checkpoints em aula | 40% da AV1 | Entregáveis produzidos durante os laboratórios, avaliados ao longo do semestre |
| AV1, prova objetiva | 60% da AV1 | Prova objetiva sobre o conteúdo da disciplina |
| AV2 | Avaliação institucional | Prova institucional com questões de todas as disciplinas do semestre |

### 6.2 Cálculo da média

```
AV1   = (checkpoints x 0,40) + (prova objetiva x 0,60)
Média = (AV1 + AV2) / 2
```

Aprovação com **média maior ou igual a 6,0**.

### 6.3 Critérios do projeto final

O projeto final é a própria Clínica Vida+ construída ao longo do semestre,
apresentada na Aula 20.

| Critério | Peso |
|---|---|
| Funcionalidade | 30% |
| Código | 25% |
| Banco de dados | 20% |
| Interface | 15% |
| Apresentação | 10% |

**Forma de entrega:** repositório no GitHub, com histórico de commits do próprio
aluno, mais deploy funcional acessível por URL.

### 6.4 Frequência

Segue o regulamento institucional da Uninove. Como os entregáveis nascem dentro
da aula, a ausência custa não apenas presença, mas também o checkpoint daquele
encontro.

## 7. Observação sobre 15/10/2026

**15/10/2026 cai numa quinta-feira e é o Dia do Professor.** Pela tabela da
seção 5, essa é a data da **Aula 11, Entity Framework Core e MySQL**, da turma
de quinta. Há a possibilidade de suspensão de aula nessa data, o que precisa ser
**confirmado com a coordenação** no início do semestre. A turma de quarta não é
afetada.

**Plano B, se a aula de 15/10/2026 for suspensa:** a turma de quinta passa a ter
19 datas úteis em vez de 20. Nesse cenário, o conteúdo desloca uma semana para
frente a partir da Aula 11 e as **Aulas 18 e 19 são fundidas em um único
encontro**, combinando layout com Bootstrap e publicação em deploy. A **Aula 20
é preservada integralmente** como fechamento, revisão geral e apresentação do
projeto final. A Aula 18 e a Aula 19 são as candidatas naturais à fusão porque
ambas trabalham sobre uma aplicação já funcional: uma cuida da camada visual e a
outra da publicação, sem introduzir conceito novo de programação.

## 8. Bibliografia

### 8.1 Básica

1. Microsoft. **Documentação do ASP.NET Core.**
   <https://learn.microsoft.com/pt-br/aspnet/core/>
2. Microsoft. **Documentação do Entity Framework Core.**
   <https://learn.microsoft.com/pt-br/ef/core/>
3. Mozilla. **MDN Web Docs: HTML, CSS e JavaScript.**
   <https://developer.mozilla.org/pt-BR/docs/Web>

### 8.2 Complementar

4. Oracle. **MySQL Reference Manual.** <https://dev.mysql.com/doc/>
5. Bootstrap. **Bootstrap 5 Documentation.**
   <https://getbootstrap.com/docs/5.3/>
6. Microsoft. **Guia da linguagem C#.**
   <https://learn.microsoft.com/pt-br/dotnet/csharp/>
7. Git. **Pro Git Book.** <https://git-scm.com/book/pt-br/v2>

---

Prof. José Romualdo, Uninove, 2026.2.
