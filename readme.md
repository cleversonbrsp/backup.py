# Script de Backup e Compactação de Arquivos

Este script realiza o backup de arquivos novos ou modificados em um diretório, preservando a estrutura de pastas original, e em seguida compacta o diretório de destino em um arquivo ZIP. O estado dos arquivos é registrado em um arquivo JSON para comparação futura.

## Funcionalidades

1. **Listagem de Arquivos**: Lista todos os arquivos em um diretório e suas datas de modificação.
2. **Cópia de Arquivos**: Copia apenas arquivos novos ou modificados para um diretório de destino, mantendo a estrutura de pastas.
3. **Compactação**: Compacta o diretório de destino em um arquivo ZIP.
4. **Registro de Estado**: Salva o estado atual dos arquivos em um arquivo JSON para comparação futura.

## Estrutura do Script

O script é dividido em etapas que são executadas sequencialmente:

1. **Etapa 1**: Solicita ao usuário o diretório a ser analisado.
2. **Etapa 2**: Carrega o estado anterior dos arquivos e lista os arquivos novos ou modificados.
3. **Etapa 3**: Solicita ao usuário o diretório de destino e cria uma nova pasta para os arquivos copiados.
4. **Etapa 4**: Copia os arquivos novos ou modificados para o novo diretório de destino.
5. **Etapa 5**: Compacta o novo diretório de destino em um arquivo ZIP.
6. **Etapa 6**: Salva o estado atual dos arquivos no arquivo de registro JSON.