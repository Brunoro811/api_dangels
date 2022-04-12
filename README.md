# Controle de Estoque Api

### A Controle de Estoque Api faz o controle do estoque de produtos,vendas e lucros de várias lojas de uma mesma empresa. Possui três tipos de usuários administrador, gerente e vendedor. 

> Status: Em Desenvolvimento ⚠️
> [![NPM](https://img.shields.io/npm/l/react)](https://github.com/Brunoro811/api_dangels/blob/development/LICENSE)

# Sobre o Projeto

### Base url da api
 **Deploy pentente**

**Controle de Estoque Api** é uma aplicação de serviço construida para controle de estoque de uma micro empresa com uma ou vários lojas. Esta aplicação foi desenvolvida com o Python, Micro Framework Flask e Postgresql oyu Mysql.

# Tecnologias Utilizadas

- Python
- Micro Framework Flask
- DB PostgreSQL ou DB Mysql
- Deploy Heroku

# Bibliotecas Utilizadas

- Flask Migrate
- Flask SQLAlchemy
- Flask JWT Extended
- Postgresql
- Environs
- Python-dotenv ( para ambiente de Desenvolvimento)
- Psycopg2
- Pillow (Tratamento de imagens)
- Requests
- Gunicorn

# Como executar

Pré-requisitos : python 3.9, biblioteca pip.

Executa:
1 - Criar um ambiente vitual venv :

```bash
python -m venv venv
```

2 - Ativar um ambiente vitual venv :

```bash
source venv/bin/activate
```

3 - Instalar as bibliotecas que estão no arquivo requirements.txt:

```bash
pip install -r requirements.txt
```

4 - Criar um arquivo .env com os dados de .env.example e subistituie pelos seus dados os campos:

- Bando de dados
- usuário do banco
- senha do banco

5 - Rodar o servidor

```bash
flask run
```

## Author

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table textAlign="center" style="margin: 0 auto;">
  <tr>
    <td align="center" title="Bruno"><a href="https://github.com/Brunoro811"><img src="https://avatars.githubusercontent.com/u/82813383?v=4" width="100px;" alt=""/><br />
    </td>    
  </tr>
</table>
<hr/>

# Sumário dos Endpoints

| Endpoints | Methods | Rule |
| :--- | :--- | :--- |
| api.users.create_users | POST | /api/users |
| api.users.delete_users | DELETE | /api/users/<int:id> |
| api.users.get_one_users |GET | /api/users/<int:id> |
| api.users.get_users | GET | /api/users |
| api.users.update_users | PATCH | /api/users/<int:id> |
| | | | |
| api.login.create_login | POST | /api/users/login |
| | | | |
| api.stores.create_stores | POST | /api/stores |
| api.stores.delete_store | DELETE | /api/stores/<int:id> |
| api.stores.get_one_store | GET | /api/stores/<int:id> |
| api.stores.get_stores | GET | /api/stores |
| api.stores.update_store | PATCH | /api/stores/<int:id> |
| | | | |
| api.products.create_group_products | POST | /api/products/group |
| api.products.create_product | POST | /api/products |
| api.products.create_update_images_product | POST | /api/products/images/<int:id> |
| api.products.delete_product | DELETE |  /api/products/<int:id> |
| api.products.get_all_products_all_stores | GET | /api/products/completed |
| api.products.get_groups_products | GET |  /api/products/group |
| api.products.get_image_product | GET |  /api/products/images/<name> |
| api.products.get_one_product | GET |  /api/products/<int:id> |
| api.products.update_product | PATCH  |  /api/products/<int:id> |
| api.products.create_distribute_product | POST | /api/products/distribute |
| api.products.get_all_products_for_store | GET | /api/products/distribute/<int:id> |
| | | | | 
| api.orders.create_sale | POST | /api/orders |
| api.orders.delete_sale | DELETE | /api/orders/<int:id> |
| api.orders.get_all_sale_for_id_seller | GET | /api/orders/seller/<int:id> |
| api.orders.get_all_sale_finish_for_id_seller | GET | /api/orders/finish/seller/<int:id> |
| api.orders.get_all_sale_not_finish_for_id_seller | GET | /api/orders/not_finish/seller/<int:id> |
| api.orders.get_one_sale_for_id_order | GET | /api/orders/<int:id> |
| api.orders.get_orders_sale_for_store | GET | /api/orders/store/<int:id> |
| | | | |
| api.clients.create_client | POST | /api/clients |
| api.clients.delete_client | DELETE | /api/clients/<int:id> |
| api.clients.get_clients | GET | /api/clients |
| api.clients.get_one_client | GET | /api/clients/<int:id> |
| api.clients.update_client | PATCH | /api/clients/<int:id> |
| | | | | 
| api.category.create_category | POST | /api/products/category |
| api.category.delete_category | DELETE | /api/products/category/<int:id_category> |
| api.category.get_all_category | GET | /api/products/category |
| api.category.get_category | GET | /api/products/category/<int:id_category> |
| api.category.update_category | PATCH |/api/products/category/<int:id_category> |

  
 # **Endpoints**
 ## Rotas de Categorias

  
<details>
  <summary><b>POST /api/products/category - Essa rota permite o usuário logado cadastrar uma categoria de produto.</b></summary>

`POST /api/products/category - FORMATO DA REQUISIÇÃO`

```json
{
	"name": "jeans"
}
```

Caso dê tudo certo, a resposta será assim:

`POST /clients/login - FORMATO DA RESPOSTA - STATUS 201`

```json
{
  "id_category": 1,
  "name": "Jeans"
}
```

Erros :

Caso a Categoria já exista:
<span class="sumary sumary--orange">
`CONFLICT - FORMATO DA RESPOSTA - STATUS 409`
</span>
```JSON
{
  "error": "category already exist!"
}
```
</details>

<br/>

## Rotas de Clients

<details>
  <summary><b>GET /api/clients?search=string - Essa rota permite o usuário logado buscar todos os clients ou por um cliente especifico passando o parametro search na url.</b></summary>

`GET /api/clients?search=string - FORMATO DA REQUISIÇÃO`

** No body. **

Caso a requisição seja feita sem o parametro ```search```, a resposta será assim:
`GET /api/clients - FORMATO DA RESPOSTA - STATUS 201`

**A pesquisa não é case sensitive.**

Com Clientes cadastrados :

```json
[
  {
    "id_client": 2,
    "first_name": "Livia",
    "last_name": "Nobre",
    "street": "Rua tal",
    "number": 490,
    "zip_code": "60000-000",
    "country": "CE",
    "city": "Fortaleza",
    "phone": "(85)91234-4567",
    "email": "email@email.com.br",
    "birthdate": "Wed, 23 Oct 1996 00:00:00 GMT",
    "cpf": "123.456.789.01",
    "date_creation_user": "08/04/2022"
  },
  {
    "id_client": 6,
    "first_name": "Ilze",
    "last_name": "Nobre",
    "street": "Rua tal",
    "number": 490,
    "zip_code": "60000-000",
    "country": "CE",
    "city": "Fortaleza",
    "phone": "(85)91234-4567",
    "email": "email2@email.com.br",
    "birthdate": "Wed, 23 Oct 1996 00:00:00 GMT",
    "cpf": "123.456.789.03",
    "date_creation_user": "08/04/2022"
  }
]
```

Sem Clientes cadastrados :

```json
[]
```
Caso a requisição seja feita com o parametro ```search```, a resposta será assim:

`GET /api/clients?search=livia - FORMATO DA RESPOSTA - STATUS 201`

Caso encontre ```first_name``` iguais ou parecidos :
```json
[
  {
    "id_client": 2,
    "first_name": "Livia",
    "last_name": "Nobre",
    "street": "Rua tal",
    "number": 490,
    "zip_code": "60000-000",
    "country": "CE",
    "city": "Fortaleza",
    "phone": "(85)91234-4567",
    "email": "email@email.com.br",
    "birthdate": "Wed, 23 Oct 1996 00:00:00 GMT",
    "cpf": "123.456.789.01",
    "date_creation_user": "08/04/2022"
  }
]
```
Caso não encontre :

```json
[]
```

</details>
  
  
 **Possiveis erros de Token**
  Em construção
