#!/bin/bash

# String para identificar nos nomes dos containers
contain_string="n8n"

# Comando a ser executado nos containers
command="apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python && apk add py3-pip && apk add py3-requests && apk add py3-numpy"

# Lista todos os containers cujo nome contém a string especificada
containers=$(docker ps --filter "name=${contain_string}" --format "{{.Names}}")

if [ -z "$containers" ]; then
    echo "Nenhum container contendo '${contain_string}' no nome foi encontrado."
    exit 1
fi

# Inicializa uma variável para armazenar os containers que executaram o comando com sucesso
successful_containers=""

# Itera sobre cada container
for container in $containers; do
    echo "Verificando o container: $container"

    # Verifica se o container está ativo
    if [ "$(docker inspect -f '{{.State.Running}}' $container)" == "true" ]; then
        echo "Container $container está ativo. Executando o comando..."

        # Executa o comando no container
        docker exec -it --user root $container /bin/sh -c "$command"

        if [ $? -eq 0 ]; then
            echo "Comando executado com sucesso no container $container."
            # Adiciona o container à lista de sucesso
            successful_containers+="$container "
        else
            echo "Erro ao executar o comando no container $container."
        fi
    else
        echo "Container $container não está ativo. Pulando..."
    fi
done

# Exibe os containers que executaram o comando com sucesso
if [ -n "$successful_containers" ]; then
    echo "Comando executado com sucesso nos seguintes containers: $successful_containers"
else
    echo "Nenhum container executou o comando com sucesso."
fi

echo "Processamento concluído."
