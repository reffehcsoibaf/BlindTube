This is the official repository of Blind Tube, the free software to improve access to YouTube for blind people, developed by Blind Center and coordinated by Gabriel Haberkamp.

## Sobre este repositório

Este repositório contém modificações no Blind Tube original, criado por Gabriel Haberkamp (Blind Center), disponível em https://github.com/gabrielhhaber/Blind_Tube. O projeto continua licenciado sob a GPL-3.0.

### Modificações

- Escolha do idioma do áudio em vídeos com dublagens em vários idiomas (botão no player, atalho alt+i), com opção de idioma de áudio preferido nas configurações gerais e nas configurações de cada canal. As dublagens do YouTube vêm em um formato que a biblioteca de som usada pelo programa não consegue tocar direto da internet, então o Blind Tube baixa o áudio escolhido (com o yt-dlp) e guarda em blind_tube/data/audio_cache antes de tocar; os arquivos antigos desse cache são apagados automaticamente.
- O arquivo cookies.txt, gerado pelo yt-dlp durante o uso, deixou de ser versionado.

