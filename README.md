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

# Endpoints

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
| | | | | 
| api.orders.create_sale | POST | /api/orders |
| api.orders.delete_sale | DELETE | /api/orders/<int:id> |
| api.orders.get_all_sale_for_id_seller | GET | /api/orders/seller/<int:id> |
| api.orders.get_one_sale_for_id_order | GET | /api/orders/<int:id> |
| | | | |
| api.distribute.create_distribute_product | POST | /api/products/distribute |
| api.distribute.get_all_products_for_store | GET | /api/products/distribute/<int:id> |
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
  
 **Em construção**
