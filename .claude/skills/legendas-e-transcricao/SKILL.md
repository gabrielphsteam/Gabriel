---
name: legendas-e-transcricao
description: Transcreve áudio ou vídeo em português no próprio computador (ffmpeg + Whisper), gera legendas SRT prontas para Reels, TikTok e Shorts, traduz legendas e embute a legenda no vídeo. Use quando o usuário pedir "transcreva este áudio", "gere legenda", "SRT", "legendar vídeo" ou "traduzir legenda".
---

# Legendas e transcrição (local)

Tudo roda na máquina do usuário ou no ambiente da sessão; nenhum áudio vai para serviços externos sem o usuário pedir.

## 1. Confira as ferramentas

```sh
which ffmpeg ffprobe
python3 -c "import faster_whisper" 2>&1 || which whisper
```

Se faltar o Whisper: `pip install faster-whisper` (preferido, mais leve) ou `pip install openai-whisper`. A primeira execução baixa o modelo; avise o usuário antes, pois pode passar de 1 GB nos modelos maiores.

## 2. Prepare o áudio

```sh
ffmpeg -y -i entrada.mp4 -vn -ac 1 -ar 16000 audio.wav
```

Arquivos longos (mais de ~30 min) ou máquinas com pouca memória: divida em blocos de 10 minutos e transcreva um a um, somando o deslocamento de tempo de cada bloco ao juntar:

```sh
ffmpeg -i audio.wav -f segment -segment_time 600 -c copy bloco_%03d.wav
```

## 3. Transcreva

Escolha o modelo pela memória disponível: `small` é um bom ponto de partida para português; `medium` ou `large-v3` ficam mais precisos, porém mais lentos e pesados.

```python
from faster_whisper import WhisperModel
model = WhisperModel("small", device="cpu", compute_type="int8")
segments, info = model.transcribe("audio.wav", language="pt", vad_filter=True)
for s in segments:
    print(f"{s.start:.2f} --> {s.end:.2f}  {s.text.strip()}")
```

Com o programa de linha de comando: `whisper audio.wav --language pt --model small --output_format srt`.

## 4. Monte a legenda SRT

Formato: número, `HH:MM:SS,mmm --> HH:MM:SS,mmm`, texto, linha em branco.

Regras para vídeo vertical (Reels, TikTok, Shorts):
- Até 2 linhas por legenda e cerca de 32 a 42 caracteres por linha.
- Cada legenda fica de 1 a 6 segundos na tela.
- Quebre por sentido, não no meio de uma expressão.
- Mantenha a pontuação e os acentos corretos do português.

## 5. Revise antes de entregar

A transcrição automática erra nomes próprios, siglas, números e gírias. Leia o texto inteiro, corrija o que estiver claramente errado e liste para o usuário os trechos em que ficou em dúvida, com o horário de cada um.

## 6. Embutir a legenda no vídeo (opcional)

```sh
ffmpeg -y -i entrada.mp4 -vf "subtitles=legenda.srt:force_style='FontName=DejaVu Sans,FontSize=14,Bold=1,Outline=2,Alignment=2,MarginV=60'" saida.mp4
```

Ajuste `MarginV` para a legenda não ficar escondida pelos botões do app. Confira o resultado extraindo um quadro: `ffmpeg -ss 5 -i saida.mp4 -frames:v 1 quadro.png`.

## 7. Traduzir legenda

Traduza só o texto, preservando numeração e horários. Faça em blocos de até ~50 legendas, mantenha cada legenda dentro do limite de caracteres e, ao final, confira que o número de legendas é o mesmo do original.

## 8. Entrega

Entregue o `.srt`, o texto corrido (se pedido) e, se embutiu, o vídeo final. Diga o modelo usado e os trechos duvidosos. Verifique que o arquivo abre e a duração bate com a do vídeo (`ffprobe`).
