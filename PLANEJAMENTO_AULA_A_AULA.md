# Planejamento Aula a Aula

Disciplina Desenvolvimento Web, Uninove, 2026.2. Prof. José Romualdo,
<jose.romualdo@uni9.pro.br>. Duas turmas com conteúdo idêntico, uma às
quartas-feiras e outra às quintas-feiras, das 19h30 às 22h00.

Este documento é a fonte da verdade do roteiro de cada encontro. Os decks em
`aulas-1sem/aulas/` e o portal em `aulas-1sem/index.html` seguem o que estiver
aqui. Ementa, cronograma e avaliação estão em `PLANO_DE_ENSINO.md`.

## Estrutura padrão do encontro

Todo encontro tem 150 minutos, sem intervalo formal, organizados em quatro
ciclos de 35, 35, 35 e 25 minutos, mais quiz e fechamento de 10 minutos cada:

```
19h30 às 20h05  Ciclo 1: conceito, demonstração, exercício curto
20h05 às 20h40  Ciclo 2: conceito, demonstração, exercício curto
20h40 às 20h50  Quiz de fixação
20h50 às 21h25  Ciclo 3: laboratório guiado, parte 1
21h25 às 21h50  Ciclo 4: laboratório, parte 2, e entregável
21h50 às 22h00  Fechamento, commit e prévia da próxima aula
```

Regras que valem para os 20 encontros:

1. **Não há atividade pré-aula.** Nenhum conteúdo é cobrado antes de ter sido
   apresentado em sala. A aula é autossuficiente.
2. **Todo encontro a partir da Aula 02 abre com recapitulação** da aula
   anterior, dentro dos primeiros minutos do Ciclo 1.
3. **Todo encontro tem quiz de fixação**, aplicado às 20h40, com enunciado e
   alternativas definidos aqui.
4. **Todo encontro tem laboratório** que faz o case Clínica Vida+ avançar um
   passo concreto, e termina com um entregável nascido em aula.
5. **O fechamento inclui o commit e o push** do trabalho do dia no fork do
   aluno, mais a prévia da aula seguinte.

## Índice das 20 aulas

| Aula | Quarta | Quinta | Módulo | Título |
|---|---|---|---|---|
| 01 | 05/08/2026 | 06/08/2026 | 1 | Apresentação, panorama da web, Git e GitHub |
| 02 | 12/08/2026 | 13/08/2026 | 1 | Estrutura da web e redes TCP/IP |
| 03 | 19/08/2026 | 20/08/2026 | 1 | Introdução ao HTML |
| 04 | 26/08/2026 | 27/08/2026 | 1 | Introdução ao CSS |
| 05 | 02/09/2026 | 03/09/2026 | 1 | CSS avançado e formulários HTML |
| 06 | 09/09/2026 | 10/09/2026 | 1 | Introdução ao JavaScript |
| 07 | 16/09/2026 | 17/09/2026 | 2 | Ambiente de desenvolvimento .NET |
| 08 | 23/09/2026 | 24/09/2026 | 2 | Primeiros passos com ASP.NET Core MVC |
| 09 | 30/09/2026 | 01/10/2026 | 2 | Estruturas de controle e coleções em C# |
| 10 | 07/10/2026 | 08/10/2026 | 2 | Formulários e Models no MVC |
| 11 | 14/10/2026 | 15/10/2026 | 2 | Entity Framework Core e MySQL |
| 12 | 21/10/2026 | 22/10/2026 | 2 | CRUD completo com EF Core |
| 13 | 28/10/2026 | 29/10/2026 | 3 | Cookies e sessões |
| 14 | 04/11/2026 | 05/11/2026 | 3 | Requisições HTTP assíncronas com AJAX |
| 15 | 11/11/2026 | 12/11/2026 | 3 | Autenticação e autorização |
| 16 | 18/11/2026 | 19/11/2026 | 3 | API REST com ASP.NET Core |
| 17 | 25/11/2026 | 26/11/2026 | 3 | Relacionamentos e EF Core avançado |
| 18 | 02/12/2026 | 03/12/2026 | 4 | Layout, Partial Views e Bootstrap |
| 19 | 09/12/2026 | 10/12/2026 | 4 | Publicação e deploy |
| 20 | 16/12/2026 | 17/12/2026 | 4 | Revisão geral e projeto final |

A Aula 11 da turma de quinta cai em 15/10/2026, Dia do Professor. Ver a seção 7
do `PLANO_DE_ENSINO.md` para o plano B de fusão das Aulas 18 e 19 caso a data
seja suspensa.

---

# Módulo 1: Fundamentos da Web e Front-End

Aulas 01 a 06. O aluno sai deste módulo com o site da Clínica Vida+ no ar
localmente, em HTML semântico, estilizado, responsivo e com comportamento em
JavaScript, tudo versionado no próprio fork.

---

## Aula 01: Apresentação, panorama da web, Git e GitHub

**Datas:** quarta 05/08/2026, quinta 06/08/2026
**Módulo:** 1, Fundamentos da Web e Front-End

### Objetivos de aprendizagem

Ao final desta aula, o aluno deve ser capaz de:

1. Descrever como a disciplina funciona, como será avaliado e o que precisa
   entregar até o fim do semestre.
2. Explicar a arquitetura cliente-servidor e situar front-end e back-end nela.
3. Descrever o case Clínica Vida+ e o que ele será ao final do semestre.
4. Justificar por que se versiona código.
5. Explicar o que um commit representa no Git.
6. Explicar o que é uma branch.
7. Fazer fork, clone, configurar identidade no Git e produzir o primeiro commit
   com push.

### Recapitulação

Não se aplica: é o primeiro encontro.

### Ciclo 1, 19h30 às 20h05: a disciplina, a web e o case

**Conceito, aproximadamente 20 minutos.**

- Apresentação do professor: formação, atuação profissional e contato,
  <jose.romualdo@uni9.pro.br>.
- Apresentação da disciplina: o que é Desenvolvimento Web, o que o aluno vai
  saber fazer em dezembro que não sabe hoje, e a ementa em uma tela.
- Metodologia: 20 encontros de 150 minutos, quatro ciclos por encontro, sem
  atividade pré-aula, tudo acontece em sala. Apresentar a grade de horários do
  encontro exatamente como ela é.
- Avaliação, com os pesos explícitos:
  - AV1 igual a checkpoints em aula com peso 40% mais prova objetiva com peso
    60%.
  - AV2 é a avaliação institucional, com questões de todas as disciplinas do
    semestre.
  - Média igual a `(AV1 + AV2) / 2`.
  - Aprovação com média maior ou igual a 6,0.
  - Critérios do projeto final: funcionalidade 30%, código 25%, banco de dados
    20%, interface 15%, apresentação 10%.
  - Entrega por repositório no GitHub mais deploy funcional.
  - Combinado de entrega: as atividades serão postadas no Google Classroom
    assim que as turmas forem configuradas pela instituição.
- Panorama do desenvolvimento web: o que é a web, front-end e back-end, o que
  cada camada faz, onde entram HTML, CSS, JavaScript, C#, ASP.NET Core, banco de
  dados e deploy. Situar as tecnologias da disciplina no mapa.
- Arquitetura cliente-servidor: quem é o cliente, quem é o servidor, o que
  trafega entre os dois, por que a mesma página pode ser montada no navegador ou
  no servidor.

**Demonstração, aproximadamente 8 minutos.**

Abrir um site real e mostrar, no DevTools, o HTML que chegou, o CSS aplicado e a
lista de requisições feitas ao servidor. Nomear cada peça enquanto aponta para
ela na tela.

**Apresentação do case Clínica Vida+, aproximadamente 7 minutos.**

- O mini mundo: clínica multiespecialidades, agendamento hoje feito por telefone
  e anotado em papel, com consultas em duplicidade e nenhuma visão de agenda.
- Os atores: paciente, recepção e médico.
- As entidades principais: Paciente, Médico, Especialidade e Consulta.
- A trajetória: nas primeiras aulas o case é uma página estática; ao final do
  semestre é uma aplicação ASP.NET Core MVC com Entity Framework Core, MySQL,
  autenticação, API REST e deploy publicado.
- Mensagem central: cada aula faz o mesmo sistema avançar um passo. Não haverá
  exercícios de tema aleatório.

**Exercício curto:** em duplas, escrever em uma frase qual problema da clínica o
sistema resolve, e apontar, entre paciente, recepção e médico, quem sofre mais
com o processo atual. Três duplas leem em voz alta.

### Ciclo 2, 20h05 às 20h40: versionamento, Git e GitHub

**Conceito, aproximadamente 22 minutos.**

- **Por que versionar.** O problema real: `trabalho_final.docx`,
  `trabalho_final_v2.docx`, `trabalho_final_final_agora_vai.docx`. Perda de
  histórico, impossibilidade de voltar atrás, trabalho de duas pessoas se
  sobrescrevendo, nenhuma resposta para "quem mudou isso e por quê".
- **Evolução do controle de versão até o Git.** Cópia manual de pastas, depois
  sistemas centralizados como CVS e Subversion, com um servidor único que
  precisa estar no ar e que é ponto único de falha, e finalmente os sistemas
  distribuídos, com o Git nascido em 2005 para o desenvolvimento do kernel do
  Linux. No Git cada clone é um repositório completo, com todo o histórico.
- **O que é de fato um commit.** Um commit não é a lista de linhas alteradas.
  Um commit é uma **fotografia completa e imutável do projeto** naquele
  instante, endereçada por um hash e **ligada ao commit anterior**. Desdobrar
  cada parte da definição:
  - fotografia completa: guarda o estado de todos os arquivos, não só o diff;
  - imutável: alterar qualquer coisa gera outro commit, com outro hash;
  - endereçada por hash: o identificador é derivado do próprio conteúdo, o que
    torna o histórico verificável;
  - ligada ao commit anterior: a corrente de pais é o que forma o histórico.
  - O "diff" que o aluno vê na tela é calculado entre duas fotografias, não é o
    que está guardado.
- **O que é uma branch.** Um ponteiro leve para um commit. Criar branch é criar
  um ponteiro, por isso é barato e instantâneo. Trabalhar em uma branch é fazer
  o ponteiro caminhar sobre novos commits, sem tocar na `main`. Desenhar no
  quadro a linha de commits com dois ponteiros.
- **O ecossistema GitHub.** Repositório remoto, fork, clone, push e pull, issues,
  Pull Request, README como cartão de visitas, GitHub Pages, e o papel do
  histórico público como portfólio profissional.

**Demonstração, aproximadamente 8 minutos.**

No terminal, ao vivo: `git init`, criar um arquivo, `git status`, `git add`,
`git commit`, `git log --oneline`. Mostrar o hash gerado. Alterar o arquivo,
commitar de novo e mostrar que o primeiro commit continua lá, intacto, com o
mesmo hash. Rodar `git checkout -b experimento` e mostrar `git log --oneline
--graph --all` com os dois ponteiros.

**Exercício curto:** cada aluno responde por escrito, em uma frase, o que
acontece com o histórico se alguém tentar alterar um commit antigo. Discussão
rápida em plenária, ancorando na imutabilidade e no encadeamento por hash.

### Quiz de fixação, 20h40 às 20h50

**Enunciado:** O que um commit representa no Git?

- (a) Apenas as linhas alteradas no arquivo desde o commit anterior do projeto.
- (b) Um backup do arquivo que está aberto no editor no momento da gravação.
- (c) Uma fotografia completa e imutável do projeto, ligada ao commit anterior.
- (d) Uma cópia do repositório remoto guardada na sua própria máquina local.

**Resposta correta: (c).**

**Comentário das alternativas:** (a) descreve o diff, que é calculado entre dois
commits e não é o que fica guardado; (b) confunde commit com salvamento de
arquivo, sendo que o commit abrange o projeto inteiro; (d) descreve o clone, não
o commit.

### Ciclo 3, 20h50 às 21h25: laboratório guiado, parte 1

**Missão no case:** colocar cada aluno de posse do próprio repositório da
Clínica Vida+, com o Git configurado e funcionando na máquina.

1. Criar ou confirmar a conta no GitHub. Orientar o uso de um nome de usuário
   profissional, porque esse endereço vira portfólio.
2. Instalar ou verificar a instalação do Git: `git --version`.
3. Fazer **fork** do repositório-esqueleto
   <https://github.com/josercf/uninove-2026-2-clinica-vida> para a conta do
   próprio aluno. Explicar, enquanto todos executam, que o fork é a cópia do
   repositório sob a conta do aluno, e que é nela que ele vai trabalhar o
   semestre inteiro.
4. **Clonar** o fork para a máquina local com `git clone` e abrir a pasta no
   editor.
5. Configurar a identidade, que é o que assina cada commit:
   ```
   git config --global user.name "Nome Sobrenome"
   git config --global user.email "email@exemplo.com"
   ```
   Reforçar que o e-mail deve ser o mesmo cadastrado no GitHub, senão os commits
   não são atribuídos ao aluno no perfil.
6. Reconhecer a estrutura do repositório-esqueleto e ler o `README.md`.

**Checkpoint do ciclo:** o professor circula e confirma, aluno por aluno, que o
`git clone` funcionou e que `git config user.name` e `git config user.email`
retornam os valores corretos.

### Ciclo 4, 21h25 às 21h50: laboratório, parte 2, e entregável

1. Editar o `README.md` do fork acrescentando uma seção de identificação com
   **nome completo, RA e turma** (quarta ou quinta), mais uma linha sobre o que
   o aluno espera aprender na disciplina.
2. Rodar `git status` e ler a saída em voz alta com a turma, identificando o
   arquivo modificado.
3. `git add README.md`, depois `git status` de novo, observando a mudança de
   estado.
4. `git commit -m "docs: identificação do aluno no README"`. Comentar o padrão
   de mensagem: verbo no presente, escopo curto, mensagem que explica a
   intenção.
5. `git log --oneline` para ver o próprio commit no histórico, com o hash.
6. `git push` e conferir o commit já visível na página do fork no GitHub.

**Entregável:** link do fork no GitHub com pelo menos um commit de autoria do
aluno, visível no histórico e assinado com o nome e e-mail configurados.

### Fechamento, 21h50 às 22h00

- Retomar as três ideias que precisam sobreviver à semana: cliente-servidor,
  commit como fotografia imutável encadeada, e o fork como o repositório do
  aluno para o semestre inteiro.
- Confirmar que todos deram push e que o commit aparece no GitHub.
- Prévia da Aula 02: o que acontece, camada por camada, entre digitar um
  endereço e a página aparecer na tela. TCP/IP, DNS e HTTP.

---

## Aula 02: Estrutura da web e redes TCP/IP

**Datas:** quarta 12/08/2026, quinta 13/08/2026
**Módulo:** 1, Fundamentos da Web e Front-End

### Objetivos de aprendizagem

1. Descrever o caminho completo de uma requisição, do navegador ao servidor e de
   volta.
2. Nomear as camadas do modelo TCP/IP e o que cada uma resolve.
3. Explicar o papel do DNS e da resolução de nomes.
4. Ler uma requisição e uma resposta HTTP, identificando método, cabeçalhos,
   corpo e código de status.
5. Explicar o que o HTTPS acrescenta ao HTTP.

### Recapitulação da Aula 01

Cliente e servidor, o case Clínica Vida+ e o que é um commit. Conferir que todos
têm o fork clonado e funcionando, resolvendo pendências de quem faltou.

### Ciclo 1, 19h30 às 20h05

**Conceito:** o que acontece quando se digita um endereço no navegador, passo a
passo. Camadas do modelo TCP/IP: aplicação, transporte, internet e acesso à
rede. Endereço IP, porta, cliente e servidor. Diferença entre TCP e UDP e por
que a web usa TCP.
**Demonstração:** `ping`, `traceroute` ou `tracert` e `ipconfig` ou `ifconfig`,
mostrando o caminho até um servidor real.
**Exercício curto:** desenhar no papel as caixas do caminho de uma requisição,
do navegador do paciente até o servidor da Clínica Vida+.

### Ciclo 2, 20h05 às 20h40

**Conceito:** DNS e a tradução de nome em endereço IP. Anatomia de uma URL:
esquema, host, porta, caminho, query string e fragmento. HTTP: métodos GET e
POST, cabeçalhos, corpo e códigos de status por família, 2xx, 3xx, 4xx e 5xx.
HTTPS, TLS e por que um formulário de dados de paciente jamais pode trafegar sem
criptografia.
**Demonstração:** `nslookup` de um domínio conhecido e a aba Network do DevTools,
inspecionando cabeçalhos e status de uma requisição real.
**Exercício curto:** dada uma URL longa de agendamento, identificar cada parte e
dizer qual código de status seria esperado se o médico informado não existisse.

### Quiz de fixação, 20h40 às 20h50

**Enunciado:** Qual é o papel do DNS em uma requisição web?

- (a) Criptografar o tráfego entre o navegador e o servidor, para que ninguém no
  caminho consiga ler o conteúdo.
- (b) Comprimir o HTML antes de enviá-lo ao navegador, para reduzir o tempo de
  carregamento da página.
- (c) Traduzir o nome do domínio no endereço IP do servidor, para que a conexão
  possa ser estabelecida.
- (d) Guardar os cookies do usuário entre uma visita e outra, para que o servidor
  reconheça quem está acessando.

**Resposta correta: (c).**

### Ciclo 3, 20h50 às 21h25: laboratório guiado, parte 1

**Missão no case:** documentar a arquitetura pela qual o site da Clínica Vida+
vai passar a operar.

Parte guiada, com o professor conduzindo passo a passo: rodar `nslookup` de um
domínio investigado e guardar a saída; abrir o DevTools e registrar pelo menos
quatro requisições observadas, com método, recurso e código de status.

### Ciclo 4, 21h25 às 21h50: laboratório, parte 2, e entregável

Sozinho, montar `docs/arquitetura.md` no próprio fork, reunindo o diagrama, em
texto ou Mermaid, do caminho da requisição do navegador do paciente até o
servidor e de volta, as evidências coletadas no ciclo anterior e um parágrafo
explicando por que o formulário de agendamento precisará de HTTPS. Commit e
push.

**Entregável:** `docs/arquitetura.md` commitado e enviado ao fork.

### Fechamento, 21h50 às 22h00

Commit e push. Prévia da Aula 03: começa a construção real do site, com HTML
semântico, e a retomada do Git com branch por funcionalidade e Pull Request.

---

## Aula 03: Introdução ao HTML

**Datas:** quarta 19/08/2026, quinta 20/08/2026
**Módulo:** 1, Fundamentos da Web e Front-End

### Objetivos de aprendizagem

1. Escrever um documento HTML5 válido do zero.
2. Escolher a tag correta pelo significado do conteúdo, não pela aparência.
3. Estruturar uma página com HTML semântico.
4. Construir listas, tabelas, links e imagens acessíveis.
5. Criar uma branch por funcionalidade e abrir um Pull Request.

### Recapitulação da Aula 02

O caminho da requisição, o papel do HTTP e o fato de que o que o servidor
devolve, no fim das contas, é um documento HTML.

### Ciclo 1, 19h30 às 20h05

**Conceito:** o que é HTML e o que ele não é. Tags, atributos, elementos
aninhados e a árvore do documento. Estrutura mínima: `<!DOCTYPE html>`, `html`,
`head` com `meta charset` e `title`, e `body`. Títulos de `h1` a `h6` e a
hierarquia correta. Parágrafos, ênfase, quebras e entidades.
**Demonstração:** escrever do zero, ao vivo, a primeira página da Clínica Vida+,
abrindo no navegador a cada linha acrescentada.
**Exercício curto:** cada aluno cria um `index.html` mínimo com título e um
parágrafo apresentando a clínica.

### Ciclo 2, 20h05 às 20h40

**Conceito:** HTML semântico: `header`, `nav`, `main`, `section`, `article`,
`aside` e `footer`, e por que eles importam para acessibilidade e para
buscadores. Listas ordenadas e não ordenadas, links internos e externos, imagens
com `alt`, e tabelas com `thead`, `tbody`, `th` e `caption`. Validação no
validador do W3C.
**Retomada de Git, últimos 10 minutos do ciclo:** agora que existe código de
verdade para versionar, entra o fluxo de trabalho por funcionalidade. Branch por
funcionalidade com `git switch -c feature/pagina-inicial`, commits pequenos e
com mensagem clara, push da branch e abertura de **Pull Request** no GitHub para
revisão antes de integrar à `main`.
**Demonstração:** transformar a página do ciclo anterior em uma página semântica
e passar o resultado pelo validador do W3C, corrigindo os erros ao vivo.
**Exercício curto:** substituir as `div` genéricas de um trecho projetado na
tela pelas tags semânticas corretas.

### Quiz de fixação, 20h40 às 20h50

**Enunciado:** Por que usar `<header>`, `<nav>` e `<main>` em vez de `<div>`
para tudo?

- (a) Porque elas dão significado ao conteúdo, o que ajuda leitores de tela,
  buscadores e a manutenção do próprio código.
- (b) Porque elas são processadas mais rápido que a `<div>`, o que reduz de forma
  perceptível o tempo de renderização.
- (c) Porque somente elas aceitam regras de CSS, já que a `<div>` não pode receber
  nem classe nem identificador próprio.
- (d) Porque a `<div>` foi removida do HTML5 e só é mantida por compatibilidade com
  páginas escritas antes da versão 5.

**Resposta correta: (a).**

### Ciclo 3, 20h50 às 21h25: laboratório guiado, parte 1

**Missão no case:** construir a página inicial do site da Clínica Vida+ com
estrutura semântica completa.

Parte guiada: criar a branch `feature/pagina-inicial` e montar, junto com o
professor, o esqueleto de `index.html`, com `header` contendo o nome da clínica,
`nav` com os links do menu e a abertura do `main`.

### Ciclo 4, 21h25 às 21h50: laboratório, parte 2, e entregável

Sozinho, completar o `main` com a seção de apresentação, a seção de
especialidades em lista e a do corpo clínico em tabela com nome, CRM e
especialidade, mais o `footer` com endereço e telefone. Validar no W3C e
corrigir os erros apontados. Commitar, dar push da branch e abrir o Pull
Request.

**Entregável:** `index.html` semântico e validado, na branch
`feature/pagina-inicial`, com Pull Request aberto no fork do aluno.

### Fechamento, 21h50 às 22h00

Revisar dois Pull Requests projetados na tela. Prévia da Aula 04: a página
ganha identidade visual com CSS.

---

## Aula 04: Introdução ao CSS

**Datas:** quarta 26/08/2026, quinta 27/08/2026
**Módulo:** 1, Fundamentos da Web e Front-End

### Objetivos de aprendizagem

1. Vincular uma folha de estilos externa a um documento HTML.
2. Selecionar elementos por tipo, classe, identificador e descendência.
3. Prever o resultado da cascata, da especificidade e da herança.
4. Aplicar o box model corretamente.
5. Montar um layout simples com Flexbox.

### Recapitulação da Aula 03

A página semântica construída, o fluxo de branch e Pull Request, e a ideia de
que o HTML cuida do significado enquanto o CSS cuida da apresentação.

### Ciclo 1, 19h30 às 20h05

**Conceito:** o que é CSS e as três formas de aplicá-lo, inline, interno e
externo, com a justificativa de sempre preferir o arquivo externo. Anatomia de
uma regra: seletor, propriedade e valor. Seletores de tipo, de classe, de
identificador, de agrupamento e de descendência. Cascata, especificidade e
herança. Cores em hexadecimal e `rgb`, tipografia com `font-family`,
`font-size`, `font-weight` e `line-height`, e unidades `px`, `rem`, `em` e `%`.
Variáveis CSS com `:root` para a paleta da clínica.
**Demonstração:** criar `assets/css/site.css`, ligar ao `index.html` e ver a
página mudar. Provocar um conflito de especificidade de propósito e resolvê-lo
no DevTools.
**Exercício curto:** dado um trecho com três regras conflitantes, dizer qual cor
prevalece e por quê.

### Ciclo 2, 20h05 às 20h40

**Conceito:** box model: conteúdo, `padding`, `border` e `margin`, e o efeito de
`box-sizing: border-box`. `display` com `block`, `inline` e `inline-block`.
Colapso de margens. Introdução ao Flexbox: `display: flex`,
`flex-direction`, `justify-content`, `align-items` e `gap`.
**Demonstração:** transformar a lista de especialidades em uma fileira de cards
com Flexbox, ao vivo, com o inspetor aberto mostrando as caixas.
**Exercício curto:** calcular a largura ocupada por uma caixa com `width: 300px`,
`padding: 20px` e `border: 2px`, primeiro sem e depois com `border-box`.

### Quiz de fixação, 20h40 às 20h50

**Enunciado:** No box model padrão do CSS, sem `border-box`, o que a propriedade
`width` define?

- (a) A largura total do elemento, já somando a área de conteúdo, o padding e a
  borda declarada.
- (b) A largura da margem externa, que é o espaço reservado entre o elemento e os
  seus vizinhos na página.
- (c) A largura da janela do navegador, da qual o elemento passa a ocupar uma
  fração proporcional.
- (d) Apenas a largura da área de conteúdo, sem contar o padding nem a borda, que
  são somados depois.

**Resposta correta: (d).**

### Ciclo 3, 20h50 às 21h25: laboratório guiado, parte 1

**Missão no case:** dar identidade visual à página inicial da Clínica Vida+.

Parte guiada: na branch `feature/estilo-inicial`, criar `assets/css/site.css`,
declarar em variáveis a paleta e a tipografia da clínica e estilizar o cabeçalho
e o menu de navegação junto com o professor.

### Ciclo 4, 21h25 às 21h50: laboratório, parte 2, e entregável

Sozinho, transformar as especialidades em cards com Flexbox, formatar a tabela
do corpo clínico e estilizar o rodapé, conferindo o resultado no navegador a
cada bloco de regras.

**Entregável:** `assets/css/site.css` aplicado ao `index.html`, com a página
inicial estilizada, commitado e enviado.

### Fechamento, 21h50 às 22h00

Comparar na tela a página da Aula 03 e a de hoje. Prévia da Aula 05: layout
responsivo e o formulário de agendamento.

---

## Aula 05: CSS avançado e formulários HTML

**Datas:** quarta 02/09/2026, quinta 03/09/2026
**Módulo:** 1, Fundamentos da Web e Front-End

### Objetivos de aprendizagem

1. Montar layouts bidimensionais com CSS Grid.
2. Adaptar o layout a diferentes larguras com media queries, na abordagem mobile
   first.
3. Construir um formulário HTML completo e acessível.
4. Escolher o tipo de campo adequado a cada dado.
5. Usar a validação nativa do navegador.

### Recapitulação da Aula 04

Seletores, cascata, box model e Flexbox, e a página inicial já estilizada.

### Ciclo 1, 19h30 às 20h05

**Conceito:** CSS Grid: `display: grid`, `grid-template-columns`,
`grid-template-areas`, `gap` e o uso da unidade `fr` e de `repeat` com
`minmax`. Quando usar Grid e quando usar Flexbox. Media queries e a estratégia
mobile first. Pseudo-classes `:hover`, `:focus` e `:nth-child`, pseudo-elementos
`::before` e `::after`, e transições suaves.
**Demonstração:** reorganizar a página inicial em Grid e mostrar, no modo
responsivo do DevTools, o layout se reorganizando em três larguras.
**Exercício curto:** escrever a media query que faz os cards de especialidade
passarem de três colunas para uma coluna abaixo de 640 pixels.

### Ciclo 2, 20h05 às 20h40

**Conceito:** formulários: `form` com `action` e `method`, e a diferença entre
GET e POST no envio. Campos: `text`, `email`, `tel`, `date`, `time`, `number`,
`select`, `textarea`, `radio` e `checkbox`. `label` associado por `for` e por que
isso é acessibilidade e não enfeite. `fieldset` e `legend`. Validação nativa com
`required`, `pattern`, `min`, `max`, `minlength` e `maxlength`, e as mensagens
que o navegador exibe sozinho.
**Demonstração:** montar ao vivo o esqueleto do formulário de agendamento e
tentar enviá-lo vazio, mostrando a validação nativa em ação.
**Exercício curto:** escolher o tipo de campo mais adequado para CPF, data de
nascimento, telefone, e-mail, especialidade e observações.

### Quiz de fixação, 20h40 às 20h50

**Enunciado:** O que o atributo `required` em um `<input>` faz?

- (a) Faz o campo ser enviado ao servidor mesmo vazio, para que a action receba a
  propriedade preenchida com nulo.
- (b) Impede o envio do formulário enquanto o campo estiver vazio, pela validação
  nativa que o próprio navegador executa.
- (c) Garante que o dado também será validado no servidor, dispensando qualquer
  verificação adicional na action.
- (d) Formata automaticamente o conteúdo digitado no campo, conforme o tipo
  declarado no atributo `type`.

**Resposta correta: (b).**

### Ciclo 3, 20h50 às 21h25: laboratório guiado, parte 1

**Missão no case:** criar a página de agendamento da Clínica Vida+.

Parte guiada: na branch `feature/agendamento`, criar `agendamento.html`
reaproveitando o cabeçalho e o rodapé do site e montar, com o professor, os
campos do paciente, nome, CPF, data de nascimento, telefone e e-mail.

### Ciclo 4, 21h25 às 21h50: laboratório, parte 2, e entregável

Sozinho, acrescentar os dados da consulta, especialidade em `select`, médico em
`select`, data, horário e observações em `textarea`; aplicar Grid ao formulário
com a media query que empilha os campos no celular; e ativar a validação nativa
nos campos obrigatórios.

**Entregável:** `agendamento.html` responsivo, com formulário completo e
validação nativa funcionando, commitado e enviado.

### Fechamento, 21h50 às 22h00

Testar o formulário em três larguras de tela. Prévia da Aula 06: o formulário
ganha comportamento com JavaScript.

---

## Aula 06: Introdução ao JavaScript

**Datas:** quarta 09/09/2026, quinta 10/09/2026
**Módulo:** 1, Fundamentos da Web e Front-End

### Objetivos de aprendizagem

1. Explicar onde o JavaScript é executado e como ele chega à página.
2. Declarar variáveis, escrever condicionais e laços e criar funções.
3. Manipular arrays com métodos básicos.
4. Selecionar e alterar elementos do DOM.
5. Reagir a eventos do usuário, inclusive ao envio de um formulário.

### Recapitulação da Aula 05

Grid, responsividade, formulário de agendamento e o limite da validação nativa:
ela cobre o básico, mas não expressa regra de negócio.

### Ciclo 1, 19h30 às 20h05

**Conceito:** o que é JavaScript, onde ele roda e como incluí-lo com `<script
src>` e `defer`. `let` e `const`, e por que evitar `var`. Tipos primitivos,
`typeof`, operadores, comparação com `===` e o perigo do `==`. Condicionais,
`for`, `for...of` e `while`. Funções declaradas e funções de seta. Arrays e os
métodos `push`, `filter`, `map` e `find`. Template literals. O `console` como
ferramenta de trabalho.
**Demonstração:** no console do navegador, criar um array de especialidades da
clínica e filtrá-lo ao vivo.
**Exercício curto:** escrever uma função que recebe uma lista de médicos e
devolve apenas os de uma especialidade informada.

### Ciclo 2, 20h05 às 20h40

**Conceito:** o DOM como árvore de objetos. `querySelector` e
`querySelectorAll`. Leitura e escrita de `textContent`, `value` e atributos.
`classList` com `add`, `remove` e `toggle`. Eventos com `addEventListener`,
tratando `click`, `input`, `change` e `submit`. O objeto `event` e
`event.preventDefault()`.
**Demonstração:** interceptar o `submit` do formulário de agendamento, impedir o
recarregamento da página e exibir uma mensagem de confirmação na própria tela.
**Exercício curto:** fazer um botão alternar a visibilidade de um bloco da
página usando `classList.toggle`.

### Quiz de fixação, 20h40 às 20h50

**Enunciado:** Para que serve `event.preventDefault()` dentro do tratador do
evento `submit` de um formulário?

- (a) Impede o comportamento padrão do navegador, que é enviar o formulário e
  recarregar a página, deixando o controle com o código JavaScript.
- (b) Limpa todos os campos do formulário, devolvendo cada um ao valor que tinha
  quando a página foi carregada pela primeira vez.
- (c) Envia o formulário por AJAX automaticamente, montando a requisição a partir
  dos campos declarados dentro do elemento `form`.
- (d) Valida sozinho todos os campos obrigatórios do formulário, exibindo as
  mensagens de erro que o navegador traz por padrão.

**Resposta correta: (a).**

### Ciclo 3, 20h50 às 21h25: laboratório guiado, parte 1

**Missão no case:** dar comportamento ao site da Clínica Vida+.

Parte guiada: na branch `feature/js-agendamento`, criar
`assets/js/agendamento.js`, interceptar o `submit` e implementar com o professor
a primeira regra de validação, o CPF com 11 dígitos, exibindo a mensagem ao lado
do campo.

### Ciclo 4, 21h25 às 21h50: laboratório, parte 2, e entregável

Sozinho, acrescentar as demais regras que o HTML não expressa, data da consulta
no futuro e horário dentro do expediente da clínica, mostrar o resumo do
agendamento na tela em caso de sucesso e criar, na página inicial, o campo de
busca que filtra a lista de especialidades enquanto o usuário digita.

**Entregável:** `assets/js/agendamento.js` com validação e filtro funcionando,
commitado e enviado.

### Fechamento, 21h50 às 22h00

Fechamento do Módulo 1: o front-end da Clínica Vida+ está de pé. Prévia da Aula
07: começa o back-end, com C# e a plataforma .NET. Pedir que quem puder já traga
o notebook com espaço em disco para o SDK.

---

# Módulo 2: Backend com C# e ASP.NET Core MVC

Aulas 07 a 12. O site estático vira aplicação ASP.NET Core MVC, com Controllers,
Views Razor, Models validados e dados persistidos em MySQL via Entity Framework
Core.

---

## Aula 07: Ambiente de desenvolvimento .NET

**Datas:** quarta 16/09/2026, quinta 17/09/2026
**Módulo:** 2, Backend com C# e ASP.NET Core MVC

### Objetivos de aprendizagem

1. Explicar o que é a plataforma .NET e a diferença entre SDK e runtime.
2. Instalar o SDK e validar o ambiente pela linha de comando.
3. Escrever e executar um programa simples em C#.
4. Criar, compilar e executar um projeto ASP.NET Core MVC.
5. Reconhecer a estrutura de pastas de um projeto MVC.

### Recapitulação da Aula 06

O front-end pronto e a pergunta que abre o módulo: onde ficam guardados os
agendamentos depois que o navegador fecha? A resposta exige servidor.

### Ciclo 1, 19h30 às 20h05

**Conceito:** o que é o .NET, o papel do SDK e do runtime, e o que significa uma
versão LTS. A CLI `dotnet`. A linguagem C#: tipagem estática, comparada com o
JavaScript que a turma acabou de ver. Tipos, variáveis, `var`, conversões,
interpolação de strings, entrada e saída no console.
**Demonstração:** `dotnet --info`, `dotnet new console`, escrever um programa que
calcula a idade de um paciente a partir da data de nascimento, e `dotnet run`.
**Exercício curto:** cada aluno cria o próprio console e imprime uma linha de
agenda formatada com interpolação de string.

### Ciclo 2, 20h05 às 20h40

**Conceito:** projeto e solução, o arquivo `.csproj`, pacotes NuGet e o comando
`dotnet add package`. Editor: Visual Studio Code com o kit de C# ou Visual
Studio. Comandos `dotnet new`, `dotnet build`, `dotnet run` e `dotnet watch`.
Anatomia do projeto MVC gerado: `Program.cs`, `Controllers`, `Views`, `Models`,
`wwwroot`, `appsettings.json`.
**Demonstração:** `dotnet new mvc -n ClinicaVida.Web`, executar, abrir no
navegador e percorrer as pastas explicando o que cada uma guarda.
**Exercício curto:** localizar, no projeto recém-criado, o arquivo responsável
pelo texto que aparece na página inicial e alterá-lo.

### Quiz de fixação, 20h40 às 20h50

**Enunciado:** Qual comando cria um novo projeto ASP.NET Core MVC chamado
`ClinicaVida.Web`?

- (a) `dotnet build mvc ClinicaVida.Web`, que compila o projeto a partir do modelo
  MVC e o deixa pronto para execução.
- (b) `dotnet add mvc ClinicaVida.Web`, que acrescenta o modelo MVC a um projeto
  vazio criado anteriormente.
- (c) `dotnet run mvc ClinicaVida.Web`, que gera o projeto a partir do modelo MVC e
  já o executa no servidor local.
- (d) `dotnet new mvc -n ClinicaVida.Web`, que gera a estrutura completa do projeto
  a partir do modelo MVC.

**Resposta correta: (d).**

### Ciclo 3, 20h50 às 21h25: laboratório guiado, parte 1

**Missão no case:** preparar o ambiente e criar o projeto que hospedará a
Clínica Vida+ pelo resto do semestre.

Parte guiada, com o professor atendendo os problemas de instalação: instalar ou
confirmar o SDK, criar a branch `feature/projeto-dotnet`, criar
`ClinicaVida.Web` com `dotnet new mvc`, acrescentar o `.gitignore` do .NET para
não versionar `bin` e `obj`, e executar com `dotnet watch run`.

### Ciclo 4, 21h25 às 21h50: laboratório, parte 2, e entregável

Sozinho, alterar a página inicial para o nome e a apresentação da clínica e
registrar no `README.md` a versão do SDK obtida em `dotnet --info` e o comando
para executar o projeto.

**Entregável:** projeto `ClinicaVida.Web` criado, executando localmente, com
`.gitignore` adequado e o `README.md` atualizado, commitado e enviado.

### Fechamento, 21h50 às 22h00

Conferir que a aplicação sobe na máquina de todos. Prévia da Aula 08: o padrão
MVC e a primeira tela de verdade da clínica.

---

## Aula 08: Primeiros passos com ASP.NET Core MVC

**Datas:** quarta 23/09/2026, quinta 24/09/2026
**Módulo:** 2, Backend com C# e ASP.NET Core MVC

### Objetivos de aprendizagem

1. Explicar o padrão MVC e a responsabilidade de cada camada.
2. Descrever o ciclo de uma requisição dentro do ASP.NET Core.
3. Interpretar a rota convencional e prever qual action atende uma URL.
4. Criar um Controller com actions que devolvem Views.
5. Escrever uma View Razor que exibe dados vindos do Controller.

### Recapitulação da Aula 07

O projeto criado, a estrutura de pastas e o ciclo `dotnet run`.

### Ciclo 1, 19h30 às 20h05

**Conceito:** o padrão MVC: Model como dado e regra, View como apresentação,
Controller como coordenador. Por que separar. O ciclo da requisição no ASP.NET
Core: requisição, pipeline de middleware, roteamento, Controller, action, View,
resposta. `Program.cs` e o registro de serviços e middlewares. Roteamento
convencional `{controller=Home}/{action=Index}/{id?}`.
**Demonstração:** seguir uma requisição com o depurador, do roteamento à View.
**Exercício curto:** dadas quatro URLs, dizer qual Controller e qual action
atendem cada uma.

### Ciclo 2, 20h05 às 20h40

**Conceito:** Controllers e actions, `IActionResult` e os retornos `View`,
`Content`, `NotFound` e `RedirectToAction`. Parâmetros de action vindos da rota e
da query string. Views Razor: a sintaxe `@`, mistura de C# e HTML, `ViewData` e
`ViewBag`, `_ViewStart.cshtml` e a convenção de localização de arquivos.
**Demonstração:** criar `EspecialidadesController` com a action `Index` e a View
correspondente, exibindo uma lista de especialidades escrita à mão.
**Exercício curto:** criar uma action `Sobre` no `HomeController` com a
respectiva View, contendo o texto institucional da clínica.

### Quiz de fixação, 20h40 às 20h50

**Enunciado:** Com a rota padrão `{controller=Home}/{action=Index}/{id?}`, qual
método atende a URL `/Especialidades/Details/3`?

- (a) `HomeController.Index`, porque a rota cai no padrão sempre que o primeiro
  segmento não corresponde a um Controller.
- (b) `DetailsController.Especialidades`, recebendo `id` igual a 3 no terceiro
  segmento da rota.
- (c) `EspecialidadesController.Details`, recebendo `id` igual a 3 no terceiro
  segmento da rota.
- (d) Nenhum, porque o roteamento convencional não aceita três segmentos sem uma
  rota específica declarada.

**Resposta correta: (c).**

### Ciclo 3, 20h50 às 21h25: laboratório guiado, parte 1

**Missão no case:** trazer o conteúdo estático da clínica para dentro do MVC.

Parte guiada: na branch `feature/controllers-iniciais`, criar
`EspecialidadesController` com a action `Index` e a View correspondente,
listando as especialidades, com o professor conduzindo a convenção de nomes e de
pastas.

### Ciclo 4, 21h25 às 21h50: laboratório, parte 2, e entregável

Sozinho, acrescentar a action `Details`, que recebe o identificador e exibe os
dados de uma especialidade, com a View correspondente em `Views/Especialidades`;
incluir os links no menu de navegação; e migrar o texto institucional para a
action `Sobre` do `HomeController`.

**Entregável:** `EspecialidadesController` com `Index` e `Details`, Views
correspondentes e navegação funcionando, commitado e enviado.

### Fechamento, 21h50 às 22h00

Percorrer o fluxo de uma requisição na aplicação da turma. Prévia da Aula 09:
lógica de verdade em C#, com estruturas de controle e coleções.

---

## Aula 09: Estruturas de controle e coleções em C#

**Datas:** quarta 30/09/2026, quinta 01/10/2026
**Módulo:** 2, Backend com C# e ASP.NET Core MVC

### Objetivos de aprendizagem

1. Escrever condicionais e laços em C# com a sintaxe correta.
2. Criar classes com propriedades para representar as entidades do case.
3. Trabalhar com `List<T>` e `Dictionary<TKey, TValue>`.
4. Filtrar, ordenar e projetar coleções com LINQ.
5. Passar uma coleção do Controller para a View de forma tipada.

### Recapitulação da Aula 08

MVC, roteamento e a primeira tela da clínica, ainda com dados escritos à mão
dentro da View.

### Ciclo 1, 19h30 às 20h05

**Conceito:** `if`, `else if`, `else`, operador ternário, `switch` e a expressão
`switch`. Laços `for`, `foreach`, `while` e `do while`, com `break` e
`continue`. Métodos: assinatura, parâmetros, retorno e sobrecarga. Classes,
propriedades automáticas, construtores e instanciação de objetos.
**Demonstração:** criar as classes `Especialidade` e `Medico` em `Models` e uma
lista de médicos em memória.
**Exercício curto:** escrever um método que recebe a hora de uma consulta e
devolve se ela está no período da manhã, da tarde ou fora do expediente.

### Ciclo 2, 20h05 às 20h40

**Conceito:** arrays, `List<T>` com `Add`, `Remove`, `Count` e indexação, e
`Dictionary<TKey, TValue>`. Introdução ao LINQ com `Where`, `Select`,
`OrderBy`, `FirstOrDefault`, `Any` e `Count`, e a sintaxe de expressão lambda.
Views tipadas com `@model`.
**Demonstração:** filtrar a lista de médicos por especialidade com `Where` e
enviá-la à View tipada, substituindo o HTML escrito à mão por um `foreach`
Razor.
**Exercício curto:** escrever a consulta LINQ que devolve os médicos ordenados
por nome e apenas os da especialidade informada.

### Quiz de fixação, 20h40 às 20h50

**Enunciado:** O que a expressão `medicos.Where(m => m.EspecialidadeId == 2)`
devolve?

- (a) O primeiro médico cuja especialidade é a de identificador 2, ou nulo quando
  não houver nenhum.
- (b) Uma sequência com todos os médicos cuja `EspecialidadeId` é igual a 2, na
  ordem em que estão na lista.
- (c) A quantidade de médicos da especialidade 2, como um número inteiro pronto
  para ser exibido na View.
- (d) Um valor booleano indicando se existe pelo menos um médico cadastrado na
  especialidade de identificador 2.

**Resposta correta: (b).**

### Ciclo 3, 20h50 às 21h25: laboratório guiado, parte 1

**Missão no case:** dar vida ao corpo clínico da Clínica Vida+, ainda em
memória.

Parte guiada: na branch `feature/medicos-em-memoria`, criar as classes
`Especialidade` e `Medico` em `Models` e a classe de repositório em memória com
a lista de especialidades e de médicos da clínica, junto com o professor.

### Ciclo 4, 21h25 às 21h50: laboratório, parte 2, e entregável

Sozinho, criar `MedicosController` com `Index`, aceitando um filtro opcional por
especialidade, e `Details`; montar as Views tipadas com
`@model IEnumerable<Medico>`; e exibir a contagem de médicos por especialidade na
tela de especialidades.

**Entregável:** lista de médicos filtrada por especialidade, vinda do Controller
e renderizada em View tipada, commitada e enviada.

### Fechamento, 21h50 às 22h00

Commit e push. Prévia da Aula 10: o formulário de agendamento passa a ser
processado pelo servidor, com Model e validação.

---

## Aula 10: Formulários e Models no MVC

**Datas:** quarta 07/10/2026, quinta 08/10/2026
**Módulo:** 2, Backend com C# e ASP.NET Core MVC

### Objetivos de aprendizagem

1. Explicar o papel do Model e do model binding no MVC.
2. Diferenciar as actions GET e POST de um mesmo formulário.
3. Construir formulários com Tag Helpers.
4. Declarar regras de validação com Data Annotations.
5. Tratar `ModelState` e devolver mensagens de erro ao usuário.

### Recapitulação da Aula 09

Classes, coleções, LINQ e Views tipadas, com o corpo clínico já vindo do
Controller.

### Ciclo 1, 19h30 às 20h05

**Conceito:** o Model como representação do dado e da regra. Model binding: como
o ASP.NET Core transforma os campos enviados no formulário em um objeto C#. O
par de actions, `[HttpGet]` exibindo o formulário e `[HttpPost]` recebendo o
envio. Tag Helpers: `asp-for`, `asp-action`, `asp-controller`,
`asp-validation-for` e `asp-validation-summary`. O token antifalsificação.
**Demonstração:** criar o Model `Consulta`, a action `Agendar` em GET e em POST,
e mostrar no depurador o objeto já preenchido pelo model binding.
**Exercício curto:** converter três campos do `agendamento.html` da Aula 05 para
Tag Helpers.

### Ciclo 2, 20h05 às 20h40

**Conceito:** Data Annotations: `[Required]`, `[StringLength]`,
`[EmailAddress]`, `[Phone]`, `[Range]`, `[DataType]`, `[Display]` e
`[RegularExpression]`, com mensagens em português. `ModelState.IsValid` e o
fluxo de devolver a View com os erros. Validação no cliente gerada a partir das
anotações, e a regra de ouro: validação no cliente é conforto, validação no
servidor é segurança.
**Demonstração:** enviar o formulário com dados inválidos e acompanhar o
`ModelState` no depurador, com as mensagens aparecendo na tela.
**Exercício curto:** anotar a propriedade `Cpf` com as regras adequadas e testar
o resultado.

### Quiz de fixação, 20h40 às 20h50

**Enunciado:** Um formulário é enviado com um campo obrigatório em branco e a
validação do cliente foi contornada. O que acontece na action de POST?

- (a) A action executa, `ModelState.IsValid` fica falso e cabe ao Controller
  devolver a View com as mensagens de erro.
- (b) A action não chega a ser executada, porque o framework bloqueia a requisição
  antes do model binding.
- (c) O Entity Framework Core rejeita o registro no `SaveChangesAsync` e devolve à
  action uma exceção de validação.
- (d) O navegador exibe uma tela de erro do servidor, porque a propriedade
  obrigatória ficou sem valor no Model.

**Resposta correta: (a).**

### Ciclo 3, 20h50 às 21h25: laboratório guiado, parte 1

**Missão no case:** trazer o formulário de agendamento para dentro da
aplicação.

Parte guiada: na branch `feature/formulario-agendamento`, criar o Model
`Consulta` com paciente, especialidade, médico, data, horário e observações,
anotá-lo com Data Annotations e mensagens em português e criar
`ConsultasController` com `Agendar` em GET, acompanhado pelo professor.

### Ciclo 4, 21h25 às 21h50: laboratório, parte 2, e entregável

Sozinho, construir a View com Tag Helpers, resumo de validação e listas
suspensas alimentadas pelo repositório em memória, implementar `Agendar` em POST
e, no caso válido, redirecionar para uma tela de confirmação exibindo os dados do
agendamento.

**Entregável:** formulário de agendamento validando no servidor, com mensagens
de erro por campo e tela de confirmação, commitado e enviado.

### Fechamento, 21h50 às 22h00

Registrar a limitação atual: o agendamento se perde quando a aplicação reinicia.
Prévia da Aula 11: banco de dados, MySQL e Entity Framework Core.

---

## Aula 11: Entity Framework Core e MySQL

**Datas:** quarta 14/10/2026, quinta 15/10/2026
**Módulo:** 2, Backend com C# e ASP.NET Core MVC

> A data da turma de quinta, 15/10/2026, é o Dia do Professor e pode ser
> suspensa. Ver a seção 7 do `PLANO_DE_ENSINO.md`.

### Objetivos de aprendizagem

1. Explicar o que é um ORM e o que o EF Core resolve.
2. Configurar o EF Core com o provedor de MySQL.
3. Escrever um `DbContext` com os `DbSet` das entidades do case.
4. Criar e aplicar migrations.
5. Conferir no MySQL o esquema gerado a partir das classes.

### Recapitulação da Aula 10

Models, Data Annotations e validação no servidor, e o problema em aberto: os
dados só existem enquanto a aplicação está no ar.

### Ciclo 1, 19h30 às 20h05

**Conceito:** persistência e bancos relacionais em uma revisão rápida: tabela,
coluna, linha, chave primária e chave estrangeira. O que é um ORM e por que
mapear objeto em tabela. EF Core e a abordagem Code First. Instalação do MySQL,
criação do usuário e verificação do serviço. Pacotes necessários e a connection
string em `appsettings.json`, com a advertência de que a senha de produção nunca
vai para o repositório.
**Demonstração:** instalar os pacotes do EF Core e do provedor de MySQL e
registrar o contexto em `Program.cs`.
**Exercício curto:** identificar, na connection string projetada, o servidor, a
porta, o banco e o usuário.

### Ciclo 2, 20h05 às 20h40

**Conceito:** `DbContext` e `DbSet<T>`. Convenções de mapeamento: nome de
tabela, chave primária por convenção `Id`, tipos e nulidade. Migrations: o que
são, o que fica no arquivo gerado, `dotnet ef migrations add` e `dotnet ef
database update`. Como reverter e como remover uma migration ainda não aplicada.
Carga inicial de dados com `HasData`.
**Demonstração:** criar a migration inicial, aplicá-la e abrir o banco recém
criado no MySQL Workbench, comparando as tabelas com as classes.
**Exercício curto:** prever quais colunas serão geradas para a classe `Paciente`
antes de rodar a migration, e conferir depois.

### Quiz de fixação, 20h40 às 20h50

**Enunciado:** O que o comando `dotnet ef database update` faz?

- (a) Gera as classes de entidade a partir de um banco já existente, invertendo o
  sentido do mapeamento.
- (b) Apaga o banco de dados e o recria vazio, descartando as tabelas e os dados
  que existiam antes.
- (c) Aplica ao banco as migrations pendentes, criando ou alterando as tabelas
  conforme o modelo atual.
- (d) Atualiza os pacotes NuGet do projeto para a versão mais recente, inclusive os
  do próprio EF Core.

**Resposta correta: (c).**

### Ciclo 3, 20h50 às 21h25: laboratório guiado, parte 1

**Missão no case:** dar ao case um banco de dados de verdade.

Parte guiada, com o professor atendendo os problemas de conexão: na branch
`feature/ef-core-mysql`, instalar os pacotes do EF Core e do provedor de MySQL,
criar as classes `Paciente`, `Medico`, `Especialidade` e `Consulta` em `Models`,
criar `ClinicaContext` com os quatro `DbSet`, configurar a connection string e
registrar o contexto.

### Ciclo 4, 21h25 às 21h50: laboratório, parte 2, e entregável

Sozinho, criar a migration `InicialClinicaVida` e aplicá-la, semear as
especialidades da clínica com `HasData` e conferir no MySQL as tabelas geradas,
comparando as colunas com as propriedades das classes.

**Entregável:** `ClinicaContext` configurado, migration inicial aplicada e banco
`clinicavida` criado no MySQL com as quatro tabelas e as especialidades
semeadas, commitado e enviado.

### Fechamento, 21h50 às 22h00

Conferir o banco criado na máquina de todos, resolvendo problemas de conexão.
Prévia da Aula 12: o CRUD completo, com dados que sobrevivem ao reinício.

---

## Aula 12: CRUD completo com EF Core

**Datas:** quarta 21/10/2026, quinta 22/10/2026
**Módulo:** 2, Backend com C# e ASP.NET Core MVC

### Objetivos de aprendizagem

1. Injetar o `DbContext` em um Controller.
2. Consultar dados com LINQ sobre o EF Core.
3. Inserir, alterar e excluir registros com `SaveChangesAsync`.
4. Escrever actions assíncronas com `async` e `await`.
5. Aplicar o padrão Post-Redirect-Get e mensagens de feedback.

### Recapitulação da Aula 11

O `DbContext`, as migrations e o banco `clinicavida` no ar, ainda sem nenhuma
tela que leia ou escreva nele.

### Ciclo 1, 19h30 às 20h05

**Conceito:** injeção de dependência no ASP.NET Core e como o `DbContext` chega
ao Controller pelo construtor. Consultas: `ToListAsync`, `FindAsync`,
`FirstOrDefaultAsync`, `Where` e `OrderBy` traduzidos para SQL. `async` e
`await` e por que operações de banco são assíncronas. Tratamento de registro
inexistente com `NotFound`.
**Demonstração:** substituir o repositório em memória pelo acesso ao banco na
listagem de médicos e mostrar o SQL gerado no log da aplicação.
**Exercício curto:** escrever a action `Index` de pacientes, listando do banco em
ordem alfabética.

### Ciclo 2, 20h05 às 20h40

**Conceito:** escrita: `Add`, `Update`, `Remove` e `SaveChangesAsync`, e o
rastreamento de mudanças do EF Core. O ciclo completo de cada operação do CRUD e
as Views correspondentes. Padrão Post-Redirect-Get e por que redirecionar após
gravar. `TempData` para a mensagem de sucesso. Tela de confirmação antes de
excluir.
**Demonstração:** implementar cadastro e edição de paciente do início ao fim,
mostrando o registro aparecendo no MySQL Workbench.
**Exercício curto:** implementar a confirmação de exclusão, cuidando para que a
exclusão em si aconteça em POST.

### Quiz de fixação, 20h40 às 20h50

**Enunciado:** Por que redirecionar após um POST bem-sucedido, em vez de
devolver a View diretamente?

- (a) Porque o redirecionamento consome menos memória no servidor do que renderizar
  a View mais uma vez.
- (b) Porque o Entity Framework Core exige um redirecionamento logo depois da
  chamada de `SaveChangesAsync`.
- (c) Porque uma action anotada com `[HttpPost]` não pode retornar uma View, apenas
  um redirecionamento.
- (d) Para evitar o reenvio duplicado do formulário quando o usuário atualiza a
  página, no padrão Post-Redirect-Get.

**Resposta correta: (d).**

### Ciclo 3, 20h50 às 21h25: laboratório guiado, parte 1

**Missão no case:** dar à recepção da Clínica Vida+ o cadastro completo de
pacientes.

Parte guiada: na branch `feature/crud-pacientes`, criar `PacientesController`
recebendo o `ClinicaContext` por injeção e implementar `Index`, `Details` e
`Create` em GET e POST, todos assíncronos, com as Views correspondentes, junto
com o professor.

### Ciclo 4, 21h25 às 21h50: laboratório, parte 2, e entregável

Sozinho, implementar `Edit` em GET e POST e `Delete` com tela de confirmação,
aplicar Post-Redirect-Get com a mensagem de sucesso em `TempData` e tratar
identificador inexistente com `NotFound`.

**Entregável:** CRUD completo de Paciente, com listagem, detalhe, cadastro,
edição e exclusão persistindo no banco, commitado e enviado.

### Fechamento, 21h50 às 22h00

Fechamento do Módulo 2: a aplicação já guarda dados. Prévia da Aula 13: como o
servidor lembra quem é o usuário entre uma requisição e outra.

---

# Módulo 3: Acesso a Dados e Funcionalidades Avançadas

Aulas 13 a 17. A aplicação ganha estado, comunicação assíncrona, controle de
acesso, uma API REST e o mapeamento completo dos relacionamentos entre as
entidades.

---

## Aula 13: Cookies e sessões

**Datas:** quarta 28/10/2026, quinta 29/10/2026
**Módulo:** 3, Acesso a Dados e Funcionalidades Avançadas

### Objetivos de aprendizagem

1. Explicar por que o HTTP é um protocolo sem estado.
2. Ler e gravar cookies em uma aplicação ASP.NET Core.
3. Configurar e usar a sessão do ASP.NET Core.
4. Escolher entre cookie, sessão e `TempData` conforme o caso.
5. Reconhecer os cuidados de segurança e privacidade envolvidos.

### Recapitulação da Aula 12

O CRUD de pacientes persistindo no banco, e a pergunta: como o servidor sabe que
duas requisições vieram da mesma pessoa?

### Ciclo 1, 19h30 às 20h05

**Conceito:** HTTP sem estado e as consequências práticas. Cookies: o que são,
como trafegam nos cabeçalhos, atributos de expiração, `HttpOnly`, `Secure`,
`SameSite` e domínio. Limites de tamanho. Cookies e privacidade, com um
comentário sobre a LGPD aplicada a dados de saúde.
**Demonstração:** gravar e ler um cookie com `Response.Cookies.Append` e
`Request.Cookies`, acompanhando o cabeçalho no DevTools.
**Exercício curto:** gravar um cookie com a unidade preferida da clínica e
exibi-la no cabeçalho da página.

### Ciclo 2, 20h05 às 20h40

**Conceito:** sessão no ASP.NET Core: `AddDistributedMemoryCache`, `AddSession` e
`UseSession`, e a ordem correta no pipeline. `HttpContext.Session` com
`SetString`, `GetString`, `SetInt32` e `GetInt32`. Guardar objetos serializando
em JSON. Tempo de expiração. Comparação entre cookie, que fica no cliente,
sessão, que fica no servidor com o identificador em um cookie, e `TempData`, que
sobrevive a um único redirecionamento.
**Demonstração:** montar um fluxo de duas etapas guardando a escolha da primeira
em sessão.
**Exercício curto:** decidir, para cinco dados diferentes do case, qual mecanismo
é o adequado e justificar.

### Quiz de fixação, 20h40 às 20h50

**Enunciado:** Por padrão, onde ficam guardados os dados de uma sessão do
ASP.NET Core?

- (a) No servidor, com o navegador guardando apenas o identificador da sessão em um
  cookie enviado a cada requisição.
- (b) No navegador do usuário, inteiros dentro do próprio cookie, que trafega
  completo a cada requisição feita.
- (c) No banco de dados da aplicação, gravados pelo EF Core a cada alteração que
  for feita no conteúdo da sessão.
- (d) Na query string de cada URL da aplicação, acrescentada pelo framework no
  momento em que a página é renderizada.

**Resposta correta: (a).**

### Ciclo 3, 20h50 às 21h25: laboratório guiado, parte 1

**Missão no case:** transformar o agendamento da Clínica Vida+ em um fluxo de
duas etapas.

Parte guiada: na branch `feature/sessao-agendamento`, habilitar a sessão no
pipeline e implementar a etapa 1, escolha de especialidade e médico, guardada em
sessão, com o professor conduzindo a ordem correta dos middlewares.

### Ciclo 4, 21h25 às 21h50: laboratório, parte 2, e entregável

Sozinho, implementar a etapa 2, escolha de data e horário, que recupera a etapa
1 da sessão, grava a consulta no banco e limpa a sessão; impedir o acesso direto
à etapa 2 sem a etapa 1; e gravar em cookie a unidade preferida do usuário,
usando-a como valor padrão nas próximas visitas.

**Entregável:** agendamento em duas etapas usando sessão, mais o cookie de
preferência de unidade, commitado e enviado.

### Fechamento, 21h50 às 22h00

Commit e push. Prévia da Aula 14: atualizar parte da tela sem recarregar a
página.

---

## Aula 14: Requisições HTTP assíncronas com AJAX

**Datas:** quarta 04/11/2026, quinta 05/11/2026
**Módulo:** 3, Acesso a Dados e Funcionalidades Avançadas

### Objetivos de aprendizagem

1. Explicar o que é AJAX e o que muda na experiência do usuário.
2. Ler e escrever JSON.
3. Fazer requisições com `fetch`, usando `async` e `await`.
4. Escrever actions que devolvem JSON em vez de HTML.
5. Atualizar o DOM com a resposta e tratar erros e estado de carregamento.

### Recapitulação da Aula 13

Sessão, cookies e o fluxo de agendamento em duas etapas, que hoje recarrega a
página inteira a cada passo.

### Ciclo 1, 19h30 às 20h05

**Conceito:** o problema do recarregamento total. O que é AJAX e o que significa
uma requisição assíncrona. JSON: sintaxe, tipos e a diferença entre JSON e um
objeto JavaScript. `fetch`, promessas, `then` e a forma preferida com `async` e
`await`. Códigos de status na resposta e a checagem de `response.ok`.
**Demonstração:** consumir no console uma action que devolve JSON, inspecionando
a resposta na aba Network.
**Exercício curto:** escrever a função `async` que busca uma URL e imprime o JSON
no console.

### Ciclo 2, 20h05 às 20h40

**Conceito:** do lado do servidor: actions que retornam `Json(...)` ou
`JsonResult`, serialização de objetos anônimos e DTOs, e o cuidado de não expor a
entidade inteira. Do lado do cliente: montar elementos no DOM a partir da
resposta, indicar carregamento, tratar erro e evitar requisições em excesso.
**Demonstração:** ao escolher a especialidade, carregar os médicos daquela
especialidade por AJAX e preencher a lista suspensa sem recarregar a página.
**Exercício curto:** acrescentar o tratamento de erro e a mensagem de
carregamento à chamada demonstrada.

### Quiz de fixação, 20h40 às 20h50

**Enunciado:** O que a action precisa retornar para que o `fetch` do navegador
receba dados e não uma página inteira?

- (a) `View()`, porque o navegador consegue extrair os dados do HTML devolvido e
  montar o objeto sozinho.
- (b) `Json(...)` ou outro resultado cujo corpo seja JSON, que é o formato que o
  `fetch` converte em objeto.
- (c) `RedirectToAction`, apontando para a action que carrega os dados e devolve a
  tela já preenchida.
- (d) `Content` com o tipo `text/html`, entregando apenas o trecho de página que
  será inserido no DOM.

**Resposta correta: (b).**

### Ciclo 3, 20h50 às 21h25: laboratório guiado, parte 1

**Missão no case:** deixar o agendamento fluido.

Parte guiada: na branch `feature/ajax-horarios`, criar as actions
`MedicosPorEspecialidade` e `HorariosDisponiveis` devolvendo JSON a partir do
banco e escrever, com o professor, o JavaScript que recarrega a lista de médicos
ao trocar a especialidade.

### Ciclo 4, 21h25 às 21h50: laboratório, parte 2, e entregável

Sozinho, implementar a exibição dos horários livres como botões selecionáveis ao
escolher médico e data, tratar o caso de nenhum horário disponível e acrescentar
a indicação de carregamento e a mensagem de erro.

**Entregável:** consulta de médicos e de horários livres por AJAX, sem recarregar
a página, commitada e enviada.

### Fechamento, 21h50 às 22h00

Commit e push. Prévia da Aula 15: quem pode ver a agenda da clínica, e como o
sistema garante isso.

---

## Aula 15: Autenticação e autorização

**Datas:** quarta 11/11/2026, quinta 12/11/2026
**Módulo:** 3, Acesso a Dados e Funcionalidades Avançadas

### Objetivos de aprendizagem

1. Distinguir autenticação de autorização.
2. Explicar por que senhas são armazenadas como hash com salt.
3. Configurar o ASP.NET Core Identity em uma aplicação existente.
4. Proteger Controllers e actions com `[Authorize]`.
5. Restringir o acesso por perfil de usuário.

### Recapitulação da Aula 14

AJAX e as actions que devolvem JSON, e a constatação de que hoje qualquer pessoa
com o endereço acessa a agenda da clínica.

### Ciclo 1, 19h30 às 20h05

**Conceito:** autenticação, provar quem se é, contra autorização, decidir o que
essa pessoa pode fazer. Por que nunca guardar senha em texto puro: hash, salt e
funções lentas de derivação. Autenticação por cookie no ASP.NET Core e o fluxo
de login, emissão do cookie e requisições seguintes. Visão geral do ASP.NET Core
Identity e das tabelas que ele cria.
**Demonstração:** mostrar no banco o campo de hash de senha e o que acontece com
duas contas que usam a mesma senha.
**Exercício curto:** listar, para o case, quais telas são públicas, quais são da
recepção e quais são do médico.

### Ciclo 2, 20h05 às 20h40

**Conceito:** instalação e configuração do Identity, migration das tabelas de
identidade, telas de registro e login, `SignInManager` e `UserManager`. Perfis
com `RoleManager`, `[Authorize]` sem argumento e `[Authorize(Roles = "...")]`,
`[AllowAnonymous]`, e a exibição condicional de menu com `User.Identity` e
`User.IsInRole`.
**Demonstração:** proteger o cadastro de pacientes e mostrar o redirecionamento
para o login de quem não está autenticado.
**Exercício curto:** anotar corretamente três actions do case conforme a matriz
de acesso montada no ciclo anterior.

### Quiz de fixação, 20h40 às 20h50

**Enunciado:** O que o atributo `[Authorize]` aplicado a um Controller garante?

- (a) Que o usuário autenticado tem perfil de administrador, com acesso irrestrito
  a todas as actions do Controller.
- (b) Que a senha do usuário é armazenada de forma criptografada nas tabelas
  criadas pelo Identity.
- (c) Que a aplicação passa a responder somente por HTTPS, recusando qualquer
  requisição feita em texto puro.
- (d) Que somente requisições autenticadas chegam às actions, sendo as demais
  redirecionadas para a tela de login.

**Resposta correta: (d).**

### Ciclo 3, 20h50 às 21h25: laboratório guiado, parte 1

**Missão no case:** controlar o acesso à Clínica Vida+.

Parte guiada: na branch `feature/autenticacao`, instalar e configurar o Identity,
gerar e aplicar a migration das tabelas de identidade e disponibilizar registro,
login e logout, com o professor conduzindo a configuração.

### Ciclo 4, 21h25 às 21h50: laboratório, parte 2, e entregável

Sozinho, criar os perfis `Recepcao` e `Medico` e semear um usuário
administrativo inicial; deixar públicas as páginas institucionais e o formulário
de solicitação de agendamento; proteger o cadastro de pacientes e a agenda com
`[Authorize(Roles = "Recepcao")]`; e ajustar o menu para exibir apenas o que o
usuário pode acessar.

**Entregável:** login e logout funcionando, com a área da recepção protegida por
perfil e o menu adaptado ao usuário, commitado e enviado.

### Fechamento, 21h50 às 22h00

Testar o acesso com dois usuários de perfis diferentes. Prévia da Aula 16: expor
os dados da clínica para outros sistemas, com uma API REST.

---

## Aula 16: API REST com ASP.NET Core

**Datas:** quarta 18/11/2026, quinta 19/11/2026
**Módulo:** 3, Acesso a Dados e Funcionalidades Avançadas

### Objetivos de aprendizagem

1. Explicar o estilo arquitetural REST e o conceito de recurso.
2. Associar cada verbo HTTP à operação correspondente.
3. Escolher o código de status adequado para cada resposta.
4. Construir um Controller de API com `[ApiController]`.
5. Testar os endpoints com uma ferramenta de requisições.

### Recapitulação da Aula 15

Identity, perfis e a área protegida, e a nova demanda: o laboratório parceiro
quer consultar a agenda por integração, não por tela.

### Ciclo 1, 19h30 às 20h05

**Conceito:** o que é uma API e o que é REST. Recursos e a modelagem de URLs no
plural, `api/consultas` e `api/consultas/5`. Verbos: GET para ler, POST para
criar, PUT para substituir, PATCH para alterar parcialmente e DELETE para
remover. Códigos de status: 200, 201, 204, 400, 401, 403, 404 e 500. Ausência de
estado entre requisições. Diferença entre um Controller MVC, que devolve HTML, e
um Controller de API, que devolve JSON.
**Demonstração:** consumir uma API pública e ler a resposta, apontando verbo,
recurso e status.
**Exercício curto:** desenhar a tabela de endpoints do recurso Consulta, com
verbo, rota, o que faz e o status de sucesso esperado.

### Ciclo 2, 20h05 às 20h40

**Conceito:** `[ApiController]`, a rota do recurso, atributos de
verbo, `ActionResult<T>`, `Ok`, `CreatedAtAction`, `NoContent`, `BadRequest` e
`NotFound`. DTOs de entrada e de saída, e por que não devolver a entidade do EF
Core diretamente. Validação automática do `[ApiController]`. Teste com Swagger,
Postman ou arquivo `.http`.

> **Sobre a rota, e isto é conteúdo de aula, não detalhe.** A convenção do
> ASP.NET Core é `[Route("api/[controller]")]`, mas o token `[controller]`
> resolve para o nome da classe sem o sufixo `Controller`. Como a classe se
> chama `ConsultasApiController`, para não colidir com o `ConsultasController`
> do MVC, o token daria `api/consultasapi`, e não o `api/consultas` usado em
> toda esta aula. O deck ensina a convenção, explica por que ela não serve
> aqui e escreve a rota literal `[Route("api/consultas")]`. Não "corrija" o
> deck de volta para o token: o conflito é real e é didático.
**Demonstração:** criar o endpoint de listagem e o de criação, e exercitá-los
pela ferramenta de teste, mostrando o cabeçalho `Location` do 201.
**Exercício curto:** corrigir uma action que devolve 200 na criação e 200 na
exclusão, apontando os status corretos.

### Quiz de fixação, 20h40 às 20h50

**Enunciado:** Qual código de status uma API REST deve devolver ao criar um
recurso com sucesso?

- (a) 200 OK sempre, porque a requisição foi processada com sucesso e o corpo já
  traz o recurso criado.
- (b) 204 No Content, porque o cliente conhece os dados que enviou e o corpo da
  resposta se torna dispensável.
- (c) 201 Created, com o cabeçalho `Location` apontando para o endereço do recurso
  recém-criado.
- (d) 302 Found, redirecionando o cliente para o endereço em que o recurso criado
  pode ser consultado.

**Resposta correta: (c).**

### Ciclo 3, 20h50 às 21h25: laboratório guiado, parte 1

**Missão no case:** expor a agenda da Clínica Vida+ para integração.

Parte guiada: na branch `feature/api-consultas`, criar `ConsultasApiController`
com os DTOs de entrada e de saída e implementar `GET api/consultas`, aceitando
filtro por data e por médico, e `GET api/consultas/{id}`, junto com o
professor.

### Ciclo 4, 21h25 às 21h50: laboratório, parte 2, e entregável

Sozinho, implementar `POST api/consultas`, `PUT api/consultas/{id}` e
`DELETE api/consultas/{id}` devolvendo os status corretos em cada caso; testar
todos os endpoints registrando as chamadas em um arquivo `ClinicaVida.http` ou em
uma coleção exportada; e documentar a API no `README.md`.

**Entregável:** `ConsultasApiController` com os cinco endpoints testados e
documentados, commitado e enviado.

### Fechamento, 21h50 às 22h00

Commit e push. Prévia da Aula 17: ligar de verdade as quatro entidades do case.

---

## Aula 17: Relacionamentos e EF Core avançado

**Datas:** quarta 25/11/2026, quinta 26/11/2026
**Módulo:** 3, Acesso a Dados e Funcionalidades Avançadas

### Objetivos de aprendizagem

1. Modelar relacionamentos um-para-muitos e muitos-para-muitos no EF Core.
2. Declarar chaves estrangeiras e propriedades de navegação.
3. Configurar mapeamentos com a Fluent API quando a convenção não basta.
4. Carregar dados relacionados com `Include` e `ThenInclude`.
5. Reconhecer e evitar o problema das consultas N mais 1.

### Recapitulação da Aula 16

A API REST no ar, e a limitação atual: a consulta devolve identificadores em vez
do nome do paciente e do médico.

### Ciclo 1, 19h30 às 20h05

**Conceito:** relacionamentos um-para-muitos, muitos-para-muitos e um-para-um.
Chave estrangeira e propriedade de navegação, nos dois sentidos. Convenções do
EF Core para descobrir o relacionamento e quando elas falham. Fluent API em
`OnModelCreating` com `HasOne`, `WithMany`, `HasForeignKey` e o comportamento de
exclusão em cascata. Índices e restrições únicas.
**Demonstração:** mapear Especialidade para Médico e Médico para Consulta, gerar
a migration e mostrar as chaves estrangeiras criadas no MySQL.
**Exercício curto:** classificar os relacionamentos entre Paciente, Médico,
Especialidade e Consulta e desenhar o diagrama resultante.

### Ciclo 2, 20h05 às 20h40

**Conceito:** estratégias de carregamento: eager com `Include` e `ThenInclude`,
explícito e lazy, com as vantagens e armadilhas de cada uma. O problema N mais 1,
como identificá-lo no log de SQL e como resolvê-lo. Projeção com `Select` para
trazer apenas o necessário. `AsNoTracking` em consultas somente de leitura.
Agregações com `GroupBy` e `Count`.
**Demonstração:** exibir a agenda do dia com `Include`, comparando no log o
número de comandos SQL antes e depois.
**Exercício curto:** reescrever com `Include` uma listagem que hoje faz uma
consulta por linha.

### Quiz de fixação, 20h40 às 20h50

**Enunciado:** Para trazer cada consulta já acompanhada do paciente e do médico
em um único acesso ao banco, o que se usa?

- (a) Um `foreach` sobre as consultas, buscando o paciente e o médico de cada uma
  em acessos separados ao banco.
- (b) `Include` das propriedades de navegação na própria consulta LINQ, que gera
  uma única ida ao banco.
- (c) Três consultas ao banco, uma por entidade, unidas depois em memória com
  `Select` sobre as listas.
- (d) `AsNoTracking` sozinho, que ao dispensar o rastreamento já traz junto os
  dados relacionados.

**Resposta correta: (b).**

### Ciclo 3, 20h50 às 21h25: laboratório guiado, parte 1

**Missão no case:** ligar as quatro entidades da Clínica Vida+.

Parte guiada: na branch `feature/relacionamentos`, mapear Especialidade
um-para-muitos Médico, Médico um-para-muitos Consulta e Paciente um-para-muitos
Consulta, com propriedades de navegação nos dois sentidos, ajustar o
comportamento de exclusão para não perder histórico de consultas e gerar e
aplicar a migration, com o professor conduzindo.

### Ciclo 4, 21h25 às 21h50: laboratório, parte 2, e entregável

Sozinho, refazer a agenda do dia com `Include`, exibindo nome do paciente, nome
do médico e especialidade; criar a tela de histórico do paciente; e montar um
relatório de consultas por especialidade com `GroupBy` e projeção.

**Entregável:** relacionamentos mapeados e aplicados no banco, com agenda do dia
e histórico do paciente exibindo dados relacionados, commitado e enviado.

### Fechamento, 21h50 às 22h00

Fechamento do Módulo 3. Prévia da Aula 18: a aplicação ganha aparência
profissional com layout, Partial Views e Bootstrap.

---

# Módulo 4: Tópicos Avançados e Projeto Final

Aulas 18 a 20. A aplicação recebe acabamento visual, vai ao ar em ambiente de
produção e é apresentada como projeto final.

---

## Aula 18: Layout, Partial Views e Bootstrap

**Datas:** quarta 02/12/2026, quinta 03/12/2026
**Módulo:** 4, Tópicos Avançados e Projeto Final

### Objetivos de aprendizagem

1. Explicar o papel do `_Layout.cshtml` e das seções Razor.
2. Extrair trechos repetidos para Partial Views.
3. Reconhecer quando usar uma View Component em vez de uma Partial View.
4. Montar telas com o sistema de grid e os componentes do Bootstrap 5.
5. Entregar uma interface responsiva e consistente em todas as telas.

### Recapitulação da Aula 17

Relacionamentos, `Include` e a agenda do dia funcionando, com a interface ainda
sem padronização entre as telas.

### Ciclo 1, 19h30 às 20h05

**Conceito:** `_Layout.cshtml`, `@RenderBody()`, `@RenderSection` com seções
obrigatórias e opcionais, `_ViewStart.cshtml` e `_ViewImports.cshtml`. Partial
Views com `<partial>` e `@await Html.PartialAsync`, e a passagem de modelo.
View Components e quando elas são necessárias, por terem lógica própria.
**Demonstração:** extrair o cabeçalho, o rodapé e o bloco de mensagens para
Partial Views e ver todas as telas mudarem de uma vez.
**Exercício curto:** identificar, no projeto do aluno, três trechos repetidos que
deveriam virar Partial View.

### Ciclo 2, 20h05 às 20h40

**Conceito:** Bootstrap 5: como incluí-lo, o sistema de grid com `container`,
`row` e `col` em pontos de quebra, e os componentes navbar, card, table, form,
alert, badge, modal e pagination. Classes utilitárias de espaçamento, tipografia,
cores e flex. Como preservar a identidade visual da clínica sobre o Bootstrap.
**Demonstração:** reconstruir a listagem de médicos com cards e grid do
Bootstrap, testando em três larguras.
**Exercício curto:** converter um formulário do projeto para as classes de
formulário do Bootstrap.

### Quiz de fixação, 20h40 às 20h50

**Enunciado:** Qual é o papel de `@RenderBody()` dentro do `_Layout.cshtml`?

- (a) Marca o ponto onde o conteúdo específico de cada View é inserido dentro do
  layout compartilhado.
- (b) Renderiza o menu de navegação compartilhado, que por isso não precisa ser
  repetido em cada View.
- (c) Importa as folhas de estilo e os scripts do Bootstrap declarados no
  `_ViewImports.cshtml`.
- (d) Executa a action do Controller correspondente à View atual, devolvendo o
  modelo já preenchido.

**Resposta correta: (a).**

### Ciclo 3, 20h50 às 21h25: laboratório guiado, parte 1

**Missão no case:** padronizar a interface da Clínica Vida+.

Parte guiada: na branch `feature/layout-bootstrap`, incluir o Bootstrap 5,
ajustar o `_Layout.cshtml` com navbar responsiva, área de conteúdo e rodapé, e
criar as Partial Views de mensagens de sucesso e erro, junto com o professor.

### Ciclo 4, 21h25 às 21h50: laboratório, parte 2, e entregável

Sozinho, criar as Partial Views de card de médico e de linha de consulta;
aplicar grid e componentes a todas as telas do projeto, incluindo o CRUD de
pacientes, o agendamento e a agenda do dia; e conferir cada tela em largura de
celular, tablet e desktop.

**Entregável:** `_Layout.cshtml` e Partial Views com Bootstrap 5 aplicados a
todas as telas, com interface responsiva e consistente, commitados e enviados.

### Fechamento, 21h50 às 22h00

Comparar a aplicação de hoje com a da Aula 08. Prévia da Aula 19: colocar a
Clínica Vida+ no ar, acessível pela internet.

---

## Aula 19: Publicação e deploy

**Datas:** quarta 09/12/2026, quinta 10/12/2026
**Módulo:** 4, Tópicos Avançados e Projeto Final

### Objetivos de aprendizagem

1. Diferenciar os ambientes de desenvolvimento e de produção.
2. Configurar a aplicação por ambiente sem expor segredos.
3. Gerar o pacote de publicação com `dotnet publish`.
4. Publicar a aplicação e o banco em um provedor acessível pela internet.
5. Aplicar migrations e validar a aplicação em produção.

### Recapitulação da Aula 18

O layout unificado e a aplicação pronta, funcionando apenas na máquina do aluno.

### Ciclo 1, 19h30 às 20h05

**Conceito:** ambientes e a variável `ASPNETCORE_ENVIRONMENT`,
`appsettings.Development.json` e `appsettings.Production.json`. Segredos fora do
repositório: variáveis de ambiente, gerenciador de segredos do provedor e o User
Secrets em desenvolvimento. Compilação em Release e `dotnet publish`. Página de
erro amigável em produção contra a página de exceção detalhada em
desenvolvimento. Logging.
**Demonstração:** publicar em uma pasta local, mostrar o conteúdo gerado e
executar a aplicação publicada.
**Exercício curto:** apontar, em um `appsettings.json` projetado na tela, tudo o
que não pode ir para o repositório.

### Ciclo 2, 20h05 às 20h40

**Conceito:** opções de hospedagem para uma aplicação ASP.NET Core com MySQL,
com a comparação de custo, esforço e limites da camada gratuita. Banco gerenciado
e connection string por variável de ambiente. Estratégias para aplicar migrations
em produção. HTTPS e certificado. Checklist de publicação: ambiente correto,
segredos configurados, migrations aplicadas, dados iniciais semeados, URL
respondendo e erro amigável ativo.
**Demonstração:** publicar a aplicação no provedor escolhido e acessá-la pelo
celular, na frente da turma.
**Exercício curto:** montar o próprio checklist de publicação no `README.md`.

### Quiz de fixação, 20h40 às 20h50

**Enunciado:** Onde deve ficar a senha do banco de dados de produção?

- (a) No `appsettings.json`, que é versionado junto com o código e por isso
  acompanha cada publicação.
- (b) No `README.md`, junto das instruções de instalação, para quem precisar
  publicar a aplicação outra vez.
- (c) Fora do repositório, em variável de ambiente ou no serviço de segredos do
  provedor de hospedagem.
- (d) Em um comentário ao lado da connection string, separado do restante da
  configuração da aplicação.

**Resposta correta: (c).**

### Ciclo 3, 20h50 às 21h25: laboratório guiado, parte 1

**Missão no case:** colocar a Clínica Vida+ no ar.

Parte guiada, com o professor acompanhando cada etapa: na branch
`feature/deploy`, separar as configurações por ambiente e remover qualquer
segredo do repositório; criar a conta no provedor e provisionar a aplicação e o
banco MySQL.

### Ciclo 4, 21h25 às 21h50: laboratório, parte 2, e entregável

Sozinho, configurar a connection string por variável de ambiente; publicar;
aplicar as migrations no banco remoto e semear os dados iniciais; testar em
produção o cadastro de paciente, o agendamento, o login e a API; e registrar no
`README.md` a URL pública e as instruções de publicação.

**Entregável:** aplicação publicada, com URL acessível pela internet, banco de
produção configurado e URL registrada no `README.md`.

### Fechamento, 21h50 às 22h00

Cada aluno abre a própria URL no celular e confirma o funcionamento. Prévia da
Aula 20: revisão geral, prova objetiva e apresentação do projeto final.

---

## Aula 20: Revisão geral e projeto final

**Datas:** quarta 16/12/2026, quinta 17/12/2026
**Módulo:** 4, Tópicos Avançados e Projeto Final

### Objetivos de aprendizagem

1. Recompor o percurso completo, do HTML ao deploy, como um sistema único.
2. Explicar as decisões técnicas tomadas ao longo do projeto.
3. Identificar e corrigir as falhas mais comuns encontradas nos projetos.
4. Apresentar o próprio trabalho de forma objetiva, em tempo limitado.
5. Entregar o projeto final conforme os critérios de avaliação.

### Recapitulação da Aula 19

A aplicação publicada e acessível, fechando a trajetória do case.

### Ciclo 1, 19h30 às 20h05

**Conceito:** revisão da espiral inteira em uma linha do tempo: requisição HTTP,
HTML semântico, CSS responsivo, JavaScript no navegador, C# e MVC, Models e
validação, EF Core e MySQL, sessão, AJAX, autenticação, API REST,
relacionamentos, layout e deploy. Para cada etapa, o problema que ela resolveu no
case. Erros mais comuns e como depurar cada um.
**Demonstração:** percorrer a aplicação completa apontando, tela a tela, em qual
aula cada peça foi construída.
**Exercício curto:** cada aluno escreve o mapa do próprio projeto, ligando cada
funcionalidade à aula em que ela nasceu.

### Ciclo 2, 20h05 às 20h40

**Conceito:** revisão dirigida para a prova objetiva, com questões comentadas dos
quatro módulos. Detalhamento dos critérios do projeto final: funcionalidade 30%,
código 25%, banco de dados 20%, interface 15% e apresentação 10%. O que a banca
vai olhar em cada critério. Formato da apresentação e o roteiro sugerido:
problema, demonstração, arquitetura, decisão técnica mais difícil e o que faria
diferente.
**Demonstração:** apresentação modelo de cinco minutos, feita pelo professor,
sobre um projeto de referência.
**Exercício curto:** cada aluno escreve o roteiro da própria apresentação em
cinco tópicos.

### Quiz de fixação, 20h40 às 20h50

**Enunciado:** Em uma aplicação ASP.NET Core MVC com EF Core, onde deve ficar a
regra que impede agendar duas consultas para o mesmo médico no mesmo horário?

- (a) Somente no JavaScript da página de agendamento, que bloqueia o envio do
  formulário antes de a requisição sair do navegador.
- (b) Somente na View, escondendo da lista os horários que já estão ocupados por
  outra consulta marcada com o mesmo médico.
- (c) Somente no banco de dados, com uma restrição de unicidade que rejeita a
  segunda tentativa de gravar o mesmo horário.
- (d) No servidor, na lógica da aplicação e com apoio de restrição no banco, porque
  a validação feita no navegador pode ser contornada.

**Resposta correta: (d).**

### Ciclo 3, 20h50 às 21h25: laboratório guiado, parte 1

**Missão no case:** entregar e apresentar a Clínica Vida+.

Parte guiada: rodar com o professor o checklist final de entrega, aplicação
publicada respondendo, repositório com histórico de commits do aluno,
`README.md` com descrição, instruções de execução e URL do deploy, e banco com
dados de demonstração; corrigir as pendências encontradas; e integrar as branches
remanescentes à `main`.

### Ciclo 4, 21h25 às 21h50: laboratório, parte 2, e entregável

Apresentar o projeto em cinco minutos, com dois minutos de arguição, seguindo o
roteiro montado no Ciclo 2. Enquanto uma equipe apresenta, as demais preenchem a
ficha de observação por critério.

**Entregável:** apresentação realizada, mais o link do repositório no GitHub e a
URL do deploy funcional, postados no Google Classroom.

### Fechamento, 21h50 às 22h00

Devolutiva geral das apresentações, orientações finais sobre a AV2 institucional
e encerramento da disciplina, com os caminhos de continuidade para quem quiser
seguir na área.

---

Prof. José Romualdo, Uninove, 2026.2.
