# Trabalho em Grupo de Integração de Sistemas: Agenda de Contatos

## Visão Geral

Este projeto demonstra a integração de múltiplos serviços web utilizando diversas tecnologias, incluindo SOAP, REST, GraphQL, gRPC e WebSockets, com autenticação JWT, mensageria assíncrona (RabbitMQ) e armazenamento NoSQL (MongoDB). O objetivo principal é criar um sistema cliente-servidor distribuído que permita a gestão de contatos, com funcionalidades de exportação e importação de dados em formatos XML e JSON.

## Membros do Grupo

*   Guilherme Barbosa - 230000002@esg.ipsantarem.pt
*   Irisnédio Imbar - 220000882@esg.ipsantarem.pt
*   Laysa Siqueira - 220000005@esg.ipsantarem.pt

## Estrutura do Projeto

O projeto está distribuído em três servidores, cada um com responsabilidades específicas:

*   **192.168.246.26 (Guilherme):** Hospeda os serviços SOAP, GraphQL e gRPC.
*   **192.168.246.62 (Irisnédio):** Hospeda os serviços REST, de Autenticação (JWT), RabbitMQ e MongoDB.
*   **192.168.246.60 (Laysa):** Hospeda o cliente web (Node.js + Express + Static HTML) e a funcionalidade de WebSocket.

## Propósito Principal

O propósito principal deste projeto é demonstrar a integração de diferentes tecnologias e protocolos de comunicação em um sistema distribuído. Ele aborda desafios como autenticação centralizada, comunicação assíncrona, persistência de dados e interação em tempo real, fornecendo uma solução completa para a gestão de contatos.

## Arquivos de Configuração

Os principais arquivos de configuração incluem:

*   **docker-compose.yml (servidor .62):** Define os serviços Docker para MongoDB, RabbitMQ, Autenticação e REST.
*   **docker-compose2.yml (servidor .26):** Define os serviços Docker para SOAP, GraphQL e gRPC, dependendo dos serviços definidos no servidor .62.
*   **Dockerfile (em cada diretório de serviço):** Contém as instruções para construir as imagens Docker de cada serviço.
*   **app.py (em cada diretório de serviço):** Arquivo principal de cada serviço, contendo a lógica de negócio e a configuração dos endpoints.
*   **app.js (client):** Arquivo principal do cliente web, responsável por inicializar o servidor Express e servir os arquivos estáticos.

## Resumo da Documentação

A documentação do projeto está distribuída nos arquivos README.md de cada serviço e nos comentários no código. Aqui está um resumo dos principais pontos:

*   **Autenticação (JWT):** O serviço de autenticação em `.62` gera e valida tokens JWT. Os demais serviços validam os tokens chamando o endpoint `/verificar` remotamente.
*   **REST:** O serviço REST em `.62` expõe endpoints CRUD para a gestão de contatos, utilizando MongoDB para persistência e RabbitMQ para comunicação assíncrona.
*   **SOAP:** O serviço SOAP em `.26` utiliza Spyne para definir os serviços web, validando os tokens JWT remotamente e enviando eventos HTTP para o serviço de mensageria.
*   **GraphQL:** O serviço GraphQL em `.26` utiliza Flask-GraphQL para expor uma API GraphQL, validando os tokens JWT remotamente e disparando eventos HTTP a cada query/mutation.
*   **gRPC:** O serviço gRPC em `.26` utiliza gRPC-Python para definir os serviços gRPC, validando os tokens JWT remotamente via metadados e disparando eventos HTTP para o serviço de mensageria.
*   **Cliente Web:** O cliente web em `.60` utiliza Node.js, Express e React/Vanilla JS para interagir com os serviços REST, SOAP, GraphQL e gRPC, além de se comunicar com o servidor via WebSockets.

## Instruções de Execução

Para executar o projeto, siga os seguintes passos:

1.  **Clonar o repositório:**

    ```bash
    git clone https://github.com/laysasiqueira/tp2grupo/
    cd tp2grupo
    ```

2.  **Configurar a rede Docker:**

    ```bash
    docker network create agenda-net
    ```

3.  **Executar os serviços no servidor .62:**

    ```bash
    cd tp2grupo
    docker-compose up -d --build
    ```

4.  **Executar os serviços no servidor .26:**

    ```bash
    cd tp2grupo
    docker-compose -f docker-compose2.yml up -d --build
    ```

5.  **Executar o cliente web no servidor .60:**

    ```bash
    cd client
    npm install # ou yarn install
    node app.js
    ```

    O cliente web estará disponível em `http://<ip_do_servidor_60>:3000`.

**Observações:**

*   Certifique-se de que as variáveis de ambiente (URLs, credenciais, etc.) estejam corretamente configuradas nos arquivos `docker-compose.yml` e nos arquivos de configuração dos serviços.
*   O cliente web não está dockerizado e precisa ser executado diretamente com `node app.js`.
*   O WebSocket não está 100% funcional.

## Tecnologias Utilizadas

*   **Servidor:** Python, Node.js, Spyne, Flask, Graphene, gRPC-Python, Express
*   **Cliente:** React/Vanilla JS, Axios, gRPC-JS, WebSockets
*   **Banco de Dados:** MongoDB (Docker)
*   **Mensageria:** RabbitMQ (Docker)
*   **Autenticação:** JWT
*   **Orquestração:** Docker, Docker Compose

## Boas Práticas e Lições Aprendidas

1.  **Centralizar Autenticação:** Evitar duplicar a lógica JWT em cada serviço, utilizando um serviço centralizado para validação.
2.  **Rede Docker:** Criar uma rede Docker externa e referenciá-la nos arquivos `docker-compose.yml` de ambos os servidores para facilitar a comunicação entre os containers.
3.  **Ambientes Limpos:** Utilizar `docker compose down && docker compose up -d --build` para reconstruir os containers e garantir um ambiente limpo.
4.  **Mensageria:** Utilizar HTTP para o serviço de "messaging" que envia eventos para o RabbitMQ, desacoplando produtores e consumidores.

## Próximos Passos

*   **Documentação de API:** Gerar Swagger/OpenAPI para REST e GraphQL (SDL), e arquivos `.proto` versionados para gRPC.
*   **Monitoramento & Logs:** Integrar ELK/Prometheus para observabilidade.
*   **Scripts de CI/CD:** Automatizar o Docker Push e os testes de integração em um pipeline de CI/CD.
*   **Segurança:** Habilitar TLS nos serviços HTTP/gRPC e configurar usuários dedicados no RabbitMQ/MongoDB.
*   **Escalabilidade:** Considerar o uso de um orquestrador como Kubernetes para replicação de pods e auto-scaling.
