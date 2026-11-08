---
name: texto-sobre-foto
description: Coloca título ou frase sobre uma foto, já no tamanho de post ou capa do Instagram (1080x1350, 1080x1080 ou 1080x1920), com corte automático, camada escura e contorno para o texto ficar legível. Use quando o usuário pedir "texto sobre a foto", "capa de carrossel", "post com título", "capa de reels" ou "arte simples para o feed".
---

# Texto sobre foto

Cria a imagem final com o script `scripts/texto_sobre_foto.py` (Pillow). Serve para capas, posts de frase e chamadas simples. Para um carrossel inteiro, planeje os slides com `ig-carousel` e use esta skill para gerar as capas.

## Passo a passo

1. **Combine com o usuário:** a foto (ele precisa ter os direitos de uso), o texto exato, o formato e onde o texto fica.
   - Feed vertical: `1080x1350`. Quadrado: `1080x1080`. Stories, Reels e TikTok: `1080x1920`.
   - Posição: `cima`, `centro` ou `baixo`. Em stories e reels, evite as bordas, onde ficam os botões do app.
2. **Escreva o texto curto:** até ~8 palavras funciona melhor; capas com mais de 12 palavras ficam ilegíveis no celular.
3. **Gere:**
   ```sh
   pip install pillow   # se ainda não estiver instalado
   python3 .claude/skills/texto-sobre-foto/scripts/texto_sobre_foto.py \
     --entrada foto.jpg --texto "Seu título aqui" --saida post.jpg \
     --tamanho 1080x1350 --posicao baixo
   ```
   Opções úteis: `--escurecer 0.6` (mais contraste), `--cor "#FFD400"`, `--fonte /caminho/fonte.ttf`, `--tamanho-fonte 90`.
4. **Olhe o resultado antes de entregar.** Abra a imagem e confira: o texto está inteiro, legível, sem cortar palavra, e o rosto ou o assunto da foto não ficou coberto. Se o texto estiver ilegível, aumente `--escurecer` ou mude a posição.
5. **Entregue** o arquivo ao usuário com o tamanho e a posição usados.

## Observações

- O script corta a foto para preencher o formato (sem esticar). Fotos muito diferentes do formato perdem as bordas.
- Acentos e cedilha funcionam com a fonte padrão. Se a fonte não for encontrada, o script avisa e pede o caminho de uma.
- Não use foto de pessoas que não autorizaram nem imagens de terceiros sem direito de uso.
