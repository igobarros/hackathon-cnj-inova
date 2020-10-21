# Hackathon CNJ Inova 2020

Para melhorar e automatizar o processo de leitura e tratamento dos arquivos em formato ```.json``` foi-se criado um script para essa tarefa. Como também a facilidade de subir a base de dados em algum SGBD (Sistema Gerenciador de Banco de Dados), para esse projeto trabalhos com o PostgreSQL.

### Configurando o ambiente

Linux ou Mac

```bash
$ git clone https://github.com/igobarros/hackathon-cnj-inova
$ cd cnj
$ pip install virtualenv
$ virtualenv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

Windows

```bash
> git clone https://github.com/igobarros/hackathon-cnj-inova
> cd cnj
> pip install virtualenv
> virtualenv .venv
> venv\Scripts\activate
> pip install -r requirements.txt
```

Após todos os passos anterioes realizados com êxito, descompacte todas as bases dos tribuinais da justica dentro da pasta ``` hackathon-cnj-inova/base```.

Com tudo bem sucedido, agora vamos configurar o ambiente de banco de dados. Na pasta ```cnj/config``` no arquivo ```.env``` preencha suas credencias para se conectar ao seu banco de dados postgreSQL.

```
DB_USER=seu_usuario
DB_PASS=sua_senha
DB_NAME=nome_do_banco_de_dados
DB_PORT=porta_do_postgresql
DB_IP=ip_de_conexao_do_postgresql
```

### Executando o projeto

Depois de todos os passos e configurações efetuadas com sucesso, podemos executar o projeto e salvar os dados no banco de dados.

```
--segmento', '-sj' --> Segmento da justica
--eleitoral', '-tre' --> Tribunal Eleitoral
--estadual', '-tje' --> Tribunal Estaduaç
--federal', '-trf' --> Tribunal Federal
--militar', '-tjm' --> Tribunal Militar
--'--tribunal_superior', '-ts' --> Tribunal Superior
--salvar', '-s' --> Salva os arquivo no banco de dados
```

Ex.: ```python main.py -sj estadual -tje pi --salvar```

O resultado da execução da linha de comando a cima está "dizendo" o seguinte: Para o python executar o script python pega o primeiro arquivo da pasta que contém os arquivos referente ao segmento da justica estadual do Estado do Piauí, e salve em um banco de dados.

Após a execução, podemos verificar o banco de dados com os dados persistidos.

#### Model das tabelas

**tb_processo_tj**

```
id
siglaTribunal
grau
numero
dataAjuizamento
classeProcessual
codigoOrgao
codigoMunicipioIBGE
instancia
codigoLocalidade
```

**tb_movimento_tj**
```
id
codigoNacional
dataHora
id_processo
```

### Issues

1. Caso nossa equipe seguir  para a próxima etapa, temos como tarefa a melhoria da modelagem do banco de dados. Pois contivemos algumas inconsistências ao subir os dados no banco, problema no qual com maior quantidade de tempo pode ser resolver.
