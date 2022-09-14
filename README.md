# Tutorial-GIT

Tutorial de uso para Git e GitHub.

## Links para download

Para baixar o *git* use esse [link](https://git-scm.com/downloads).

## Criar um novo projeto Git

* Abra o `Git Bash`, você pode inicia-lo diretamente no local com o botão direito do mouse na pasta escolhida.

* `git init` para inicializar o repositório. Uma pasta é criada nesse momento `.git` (se não visualisa-la, no "Explorador de arquivos, vá em "Exibir" e marque a opção para habilitar "Itens Ocultos").
* `git add .` para colocar o arquivo na área de *staging*. Ele é necessário antes de executar o *commit*.
* `git commit -m "First commit"` para realizar o *commit* no repositório.
<!-- * `git branch -M "main"` é usado para alterar o nome da *branch* principal de *master* para *main* (isso é uma boa prática atualmente recomendada). -->

## Usando o GitHub

Agora entrando no site [GitHub](www.github.com), vá na página do seu *profile* e clique em ***New*** para criar um repositório. Após criado o próprio site irá indicar os passos para incializar o diretório em sua máquina.

:::image type="content" source="img/img_newCode.png" alt-text=" ":::

* Preencha os campos de ***Repository name*** e ***Description***.

Voltando ao ***git bash*** crie o link entre o *git* e *GitHub*:

* `git remote add origin <link>`, o termo *remote* cria a conexão entre a pasta no computador e o link do *GitHub*, o termo *add* serve para adicionar o arquivo e *origin* é uma nomenclatura (apelido) padrão usado para identificar o arquivo.

* `git push -u origin main`, envia os arquivos para o *GitHub*.

Após criar/alterar arquivos no seu desenvolvimento, para aplicar o versionamento utilize:

* `git add .`, para colocar em *stadding*.
* `git status`, para ver se existe alguma alteração noo sistema.
* `git commit -m "mensagem do commit"`
* `git push origin main`, para publicar no repositório.  Note que agora não é mais necessário usar o comando *remote* pois a conexão já foi feita.

### Usando *Branch*

Uma *branch* pode ser criada para alterar/criar/excluir um arquivo sem alterar a linha cronológica da linha principal (*main/master*).

:::image type="content" source="img/img_branch.png" alt-text=" ":::

Para isso, deve-se executar:

* `git checkout -b "nome-branch`", que irá criar a ramificação e gerar todo o ambiente. Esta *branch* ficará evidente no *Git bash*, substituido o ambiente *main/master*.

Utilize os comandos para adicionar e publicar:

* `git add .`, para colocar em *stadding*.
* `git status`, para ver se existe alguma alteração noo sistema.
* `git commit -m "mensagem do commit"`

Para publicar no repositório utilize o ***nome-branch*** deste vez:

* `git push origin nome-branch`

Para voltar ao *main/master*:

* `git checkout main`, podendo alterar a qualquer momento entre a linha principal e *branch*.

### Clone repositório

Em projeto do dia-a-dia será necessário trabalhar com repositórios de terceiro, para isso:

* Inicialmente crie uma pasta que irá receber os arquivos em seu computador (Ex. pasta Git).
* Com o botão direito abra o *Git Bash*.
* No *GitHub* do repositório que queira trabalhar, clique em **Code* e copie o endereço HTTPS.

:::image type="content" source="img/img_code_clone.png" alt-text=" ":::

* De volta ao *Git bash*, insira: `git clone <link do repositório>`.
* `git pull`, para atualizar os arquivos do repositório caso em algum momento tenha sido atualizado.

### Fork para repositório

Quando você "clona" o repositório, ele não irá diretamente para seu *GitHub*, necessariamente, precisa realizar um ***Fork*** no *GitHub* que deseja trabalhar. Para isso, clique no botão *Fork* localizado na direita superior do *GitHub* que deseja contribuir.

:::image type="content" source="img/img_fork.png" alt-text=" ":::

Preencha os campos de inicialização e ele já estará em seu repositório.
Agora basta seguir os passos anteriores como, clonar o repositório para seu computador, criar um *branch*, adicionar documentos e etc.

Para contribuir com para o repositório original, você deve realizar um ***PULL REQUEST***. Será necessário, ir até seu *GitHub* e lá terá a opção de realizar o *Pull Request*.

:::image type="content" source="img/img_pull_request.png" alt-text=" ":::

Enviando uma contribuição para o autor original, onde ele poderá acertar ou recusar a atualização.

----
Existem doutras funcionalidades do Git e do Github, aqui foram passadas as principais utilizadas no dia-a-dia.
Recomendo sempre ler a documentação do Git.
