# Utilitarios EDAT
Classes utilitarias utilizadas pelo EDAT.
---- 

## - Passos para deploy
Primeiro, é necessário alterar a versão do projeto no arquivo [setup.py](./setup.py), após, seguir os comandos abaixo para gerar o pacote.


#### Configuração
Antes de realizar o deploy, deve-se configurar o arquivo de acesso ao [pypi.org](https://pypi.org).

Mais informações acessar [docs pypirc](https://packaging.python.org/en/latest/specifications/pypirc/)

- Criar arquivo com o nome .pypirc em:
  - linux: `/home/$USER/` 
  - windows: `C:\Users\$USER\`
- Salvar o seguinte conteúdo dentro do arquivo:
```toml
[distutils]
index-servers =
    pypi
    edat_utils

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = <token_acesso> 

[edat_utils]
repository = https://test.pypi.org/edat_utils/
username = __token__
password = <token_acesso> 

```

#### Ativar o ambiente virtual
```sh
source venv/bin/activate
```

#### Instalar as dependências
```sh 
pip install wheel twine
```


#### Gerar os pacotes necessários
```sh 
python setup.py sdist bdist_wheel
```

#### Verificar os pacotes
```sh
twine check dist/*
```

#### Realizar deploy dos pacotes
```sh
twine upload dist/*
```
---

# Possíveis erros

#### Erro de reuso de nome 
- Verificar se a versão já foi utilizada. 
Apagar a pasta dist e gerar novamente os pacotes
