#!/bin/sh

# Falha o script se qualquer comando falhar
set -e

echo "Rodando migrações..."
python manage.py migrate --noinput

echo "Iniciando o servidor..."
exec "$@"