#!/bin/bash

# Exemplo de requisição correta para /register
# Os campos devem estar diretamente no body, não dentro de "value"

curl -X 'POST' \
  'http://localhost:8084/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "tipo_usuario": "produtor",
  "subtipo_usuario": "fornecedor_individual",
  "name": "João Silva",
  "email": "joao@example.com",
  "senha": "senha123",
  "cpf": "123.456.789-10"
}'

