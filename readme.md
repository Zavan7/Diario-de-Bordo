# Diário de Bordo Volkswagen

Automação para extração, tratamento e consolidação de informações de mailings do sistema HCosta para a Volkswagen.

## Descrição

Este projeto automatiza o processo de login, navegação, extração de dados de campanhas de mailing e tratamento dos dados, gerando relatórios em Excel para acompanhamento das campanhas.

## Funcionalidades

- Login automatizado no sistema HCosta
- Navegação automática até o menu de mailings
- Extração de informações de campanhas para arquivo Excel
- Tratamento e filtragem dos dados extraídos
- Geração de relatório final consolidado
- Utilização do padrão de projeto Page Objects para melhor organização e manutenção do código.
- Configuração de logging para rastreamento e diagnóstico.

## Estrutura do Projeto

O projeto segue o padrão de projeto Page Objects para melhor organização e manutenibilidade.

- `main.py`: Script principal de automação.
- `pages/`: Classes de automação de páginas (login, navegação, mailing).
- `base_tratament.py`: Processamento e limpeza dos dados extraídos.
- `config/logging_config.py`: Configuração de logging.
- `.env`: Variáveis de ambiente (credenciais e token do GitHub).
- `mailing_info_raw.xlsx`: Arquivo gerado com dados brutos extraídos.
- `Diario de Bordo.xlsx`: Arquivo final tratado.

## Pré-requisitos

- Python 3.8+
- Firefox instalado
- [Selenium](https://pypi.org/project/selenium/)
- [webdriver-manager](https://pypi.org/project/webdriver-manager/)
- [pandas](https://pypi.org/project/pandas/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## Instalação

1. Clone este repositório.
2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```
3. Crie um arquivo `.env` na raiz do projeto e configure as variáveis de ambiente:

   ```
   USER=seu_usuario
   PASSWORD=sua_senha
   GITHUB_TOKEN=seu_token_github
   ```

## Uso

1.  Certifique-se de que todos os pré-requisitos estão instalados e configurados.
2.  Execute o script principal:

    ```bash
    python main.py
    ```

O processo irá:

- Abrir o navegador Firefox.
- Realizar login e navegação automática.
- Extrair e salvar os dados brutos em `mailing_info_raw.xlsx`.
- Processar os dados extraídos e salvar o resultado final em `Diario de Bordo.xlsx`.

## Observações

- O token do GitHub é opcional, mas recomendado para evitar limites de requisições à API do GitHub ao baixar o driver do Firefox.
- Os logs do processo são exibidos no console e também são salvos no arquivo `automation.log`, configurado em `config/logging_config.py`.

## Licença

Uso interno. Consulte o responsável pelo projeto, Vitor Zavan, para mais informações.