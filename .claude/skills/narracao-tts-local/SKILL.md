---
name: narracao-tts-local
description: Gera narração em português do Brasil a partir de texto, localmente, com o Kokoro TTS (vozes pf_dora, pm_alex e pm_santa), e prepara o texto para soar natural. Use quando o usuário pedir "narração", "locução", "voz para o vídeo", "texto para fala" ou "TTS" sem querer enviar o texto a um serviço externo.
---

# Narração local em português (Kokoro)

Se o usuário já usa o VoiceStudio (skill `voicestudio`), prefira ele. Esta skill é para quando não há um app de voz rodando.

## 1. Prepare o ambiente

```sh
pip install kokoro soundfile
apt-get install -y espeak-ng   # necessário para a pronúncia; no macOS: brew install espeak-ng
which ffmpeg ffprobe
```

A primeira execução baixa o modelo do Kokoro; avise o usuário antes. Se a instalação ou o download falharem, diga o erro e pare: não finja ter gerado áudio.

## 2. Prepare o texto (o que mais melhora o resultado)

- Escreva números, valores e siglas como se fala: "R$ 39,90" vira "trinta e nove reais e noventa centavos"; "3x" vira "três vezes".
- Troque abreviações por palavras inteiras ("pág." → "página").
- Use ponto e vírgula para pausas, ponto final para pausas longas, e frases de até ~25 palavras.
- Nomes estrangeiros: escreva como se pronuncia, se a primeira tentativa soar errada.
- Divida em parágrafos curtos; gere um arquivo por parágrafo se quiser ajustar o ritmo.

## 3. Gere o áudio

```python
import numpy as np, soundfile as sf
from kokoro import KPipeline

pipeline = KPipeline(lang_code="p")   # português do Brasil
texto = open("roteiro.txt", encoding="utf-8").read()

pedacos = []
for _, _, audio in pipeline(texto, voice="pf_dora", speed=1.0):
    pedacos.append(audio)

sf.write("narracao.wav", np.concatenate(pedacos), 24000)
```

Vozes em português do Brasil: `pf_dora` (feminina), `pm_alex` e `pm_santa` (masculinas). Gere uma amostra curta de cada e deixe o usuário escolher. `speed` entre 0,9 e 1,1 costuma soar natural.

## 4. Confira e converta

```sh
ffprobe -v error -show_entries format=duration -of csv=p=0 narracao.wav
ffmpeg -y -i narracao.wav -ac 1 -b:a 128k narracao.mp3
```

Diga a duração real. Ouça ou ao menos confira que o arquivo não está vazio ou mudo (`ffmpeg -i narracao.wav -af volumedetect -f null -` mostra o volume médio).

## 5. Cuidados

- É uma voz sintética: avise o usuário que Instagram, TikTok e YouTube pedem o rótulo de conteúdo gerado por IA em alguns casos.
- Não use para imitar a voz de uma pessoa real. Clonagem de voz só com autorização da pessoa e por uma ferramenta própria para isso.
- Para colocar a narração em um vídeo: `ffmpeg -i video.mp4 -i narracao.mp3 -map 0:v -map 1:a -c:v copy -shortest saida.mp4`.
