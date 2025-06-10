Serviço REST

Esta seção descreve a implementação da interface REST do sistema de agenda de contatos. A API REST permite listar, adicionar e remover contatos através de endpoints HTTP. A comunicação entre o cliente e o servidor utiliza o formato JSON. Abaixo estão a estrutura do código, instruções de execução e exemplos de uso.

Estrutura de Pastas

/servidor/rest/api.py                  Servidor Flask com API REST

/cliente/routes/rest.js          Cliente Node.js que consome a API REST

/public/rest.html                Interface web REST (HTML, JS e CSS)



Como Executar o Servidor REST

1.	Acede à pasta do servidor:

cd servidor/rest

2.	Inicia o servidor:

python api.py


OBS: O servidor ficará disponível em: http://localhost:5000



Como Testar (Postman)

 Listar contatos

•	Método: GET

•	URL: http://localhost:5000/contatos

 Adicionar contato

•	Método: POST

•	URL: http://localhost:5000/contatos

•	Body (JSON):


{

  "nome": "Ana",

  "email": "ana@email.com",

  "telefone": "911234567"

}




Interface Web (rest.html)

Para utilizar a interface web:

1.	Acede à pasta raiz do cliente:

cd cliente

2.	Inicia o servidor Node.js:

node app.js

OBS: Abre no navegador http://localhost:3000/rest.html


A interface permite:

•	Listar todos os contatos

•	Adicionar um novo contato

•	Apagar um contato existente







Serviço SOAP

Este serviço permite listar, exportar e importar contatos via protocolo SOAP, com suporte a ficheiros JSON e XML codificados em base64.



 Tecnologias utilizadas:

•	Python + Spyne no servidor (porta 8000)

•	Node.js + Express + soap no cliente

•	Interface gráfica em HTML + JavaScript




Como executar

Servidor SOAP:

python -m servidor.soap.soap_service


Acede a: http://localhost:3000/soap.html


 Funcionalidades

 Listar contatos

•	WSDL: http://localhost:8000/?wsdl

•	Função: listar_contatos

•	Exibe todos os contatos formatados na interface.

 Exportar contatos (JSON/XML)

•	Botões disponíveis na interface:

o	Exportar JSON

o	 Exportar XML

•	Permite fazer download do ficheiro diretamente para o utilizador.

 Importar contatos (JSON/XML)

•	O ficheiro é enviado em formato base64 via SOAP.

•	As funções importar_json_base64 e importar_xml_base64 processam o conteúdo e atualizam o contatos.json.


Exemplo de chamada SOAP no Postman

•	Endpoint:

POST http://localhost:8000/


•	Headers:

Content-Type: text/xml

•	Corpo (exemplo de chamada listar):

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="agenda.contatos">

   <soapenv:Body>

      <tns:listar_contatos/>

   </soapenv:Body>
  
</soapenv:Envelope>



GraphQL

O serviço GraphQL permite consultar todos os contatos e também pesquisar por um contato específico com base no nome.~


Endpoints disponíveis

•	POST /graphql

o	Utilizado para enviar queries GraphQL.

o	Interface gráfica (graphiql) ativada em: http://localhost:5000/graphql

🔎 Queries implementadas

•	Consultar todos os contatos:

query {

  contatos {

    id

    nome

    email

    telefone

  }

}

•	Buscar contato por nome:


query {

  buscarContatoPorNome(nome: "João") {

    id

    nome

    email

    telefone

  }

}


Exemplo de chamada GraphQL no Postman

•	URL: http://localhost:5000/graphql

•	Método: POST

•	Headers:

o	Content-Type: application/json

•	Body (raw JSON):

{

  "query": "query { buscarContatoPorNome(nome: \"João\") { id nome email telefone } }"

}

Cliente Web

Foi desenvolvido um cliente web com HTML/CSS/JavaScript que permite pesquisar contatos por nome usando o serviço GraphQL.

•	Interface simples com campo de pesquisa e botão "Buscar".

•	Ao encontrar o contato, os dados são exibidos de forma organizada no navegador.

▶️ Execução do servidor GraphQL

1.	Executar o servidor:

python servidor/graphql/graphql_service.py

2.	 Aceder à interface: http://localhost:5000/graphql

3.	  Abrir o ficheiro graphql.html no navegador para utilizar o cliente web.

