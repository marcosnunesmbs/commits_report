# Commits Report

Este projeto consiste em uma ferramenta para gerar relatório de commits feitos em projetos para relatório.

## Como Rodar o Projeto

1. **Pré-requisitos**:
   - Certifique-se de ter o Python instalado em sua máquina. Você pode baixar e instalar o Python a partir do [site oficial](https://www.python.org/downloads/).
   - Renomeie os arquivos `entry_example.txt` e `repositories_example.txt` para `entry.txt` e `repositories.txt`

2. **Instalar Dependências**:
   - Instale as dependências do projeto usando o comando:
     ```
     pip install -r requirements.txt
     ```

3. **Configuração**:
   - No arquivo `entry.txt`, forneça as informações necessárias para o projeto:
     - `author`: O autor dos commits que deseja analisar.
     - `since_date`: A data a partir da qual deseja extrair os commits.
   - No arquivo `repositories.txt`, liste os repositórios que deseja analisar. Cada linha do arquivo deve conter o nome e o caminho do repositório separados por vírgula.

4. **Execução**:
   - Execute o script Python `main.py` para iniciar a análise dos commits. Certifique-se de estar no diretório onde o script está localizado.
   ~~~shell
   python main.py
   ~~~
    Ou
   ~~~shell
   python3 main.py
   ~~~
   - Durante a execução, o script irá fornecer informações sobre cada etapa do processo e em qual repositório está trabalhando.

4. **Resultados**:
   - Os resultados da análise serão salvos no arquivo `all_repositories_commits.xlsx` no formato Excel. Este arquivo conterá duas planilhas: "Modifications" e "Additions", que mostrarão as modificações e adições de arquivos, respectivamente.

## Estrutura dos Arquivos de Configuração

### entry.txt

Este arquivo contém as informações necessárias para o projeto, conforme descrito abaixo:

```
author=SEU_AUTOR
since_date=DATA_DESDE
```

- `author`: O autor dos commits que deseja analisar.
- `since_date`: A data a partir da qual deseja extrair os commits.

### repositories.txt

Este arquivo contém a lista de repositórios que deseja analisar, no formato a seguir:

```
NOME-REPOSITORIO1,C:\CAMINHO\REPOSITORI\O1
NOME-REPOSITORIO2,C:\CAMINHO\REPOSITORI\O2
```

Cada linha deve conter o nome e o caminho do repositório, separados por vírgula.
