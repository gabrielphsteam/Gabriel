---
name: voz-da-marca
description: Define, guarda e aplica a voz da marca ou do perfil (tom, palavras que usa e evita, nível de formalidade, emojis, chamada para ação padrão) para que todo texto saia com a mesma personalidade. Use quando o usuário pedir "defina minha voz", "tom de voz da marca", "escreva no meu estilo" ou quando for escrever legendas, roteiros e mensagens de um perfil.
---

# Voz da marca

A voz fica guardada em um arquivo para ser reaproveitada: `voz-da-marca.md`, na raiz do projeto (ou na pasta que o usuário indicar). Um arquivo por marca ou perfil; use `voz-<nome>.md` quando houver mais de um.

## Fluxo

1. **Procure o arquivo.** Se `voz-da-marca.md` existe, leia e aplique sem perguntar de novo.
2. **Se não existe, entreviste.** Faça as perguntas abaixo de uma vez só, em lista curta, e aceite respostas parciais:
   - Para quem você fala e o que essa pessoa quer?
   - Em 3 palavras, como o perfil deve soar? (ex.: direto, acolhedor, bem-humorado)
   - Formal ou conversa de amigo? Usa "você", "tu" ou "vocês"?
   - Palavras, gírias ou expressões que você usa sempre.
   - Palavras ou jeitos que você nunca usaria.
   - Emojis: quais e com que frequência (ou nenhum).
   - Como terminam os seus textos? (chamada para ação padrão)
   - Cole 2 ou 3 textos seus de que você gostou, se tiver.
3. **Escreva o arquivo** com o modelo abaixo, só com o que o usuário disse ou o que os exemplos mostram com clareza. Marque o que for dedução como "(a confirmar)".
4. **Aplique.** Escreva o próximo texto pedido seguindo a voz e diga em uma linha que escolhas de voz você usou.
5. **Ajuste com o uso.** Quando o usuário corrigir um texto ("isso não é a minha cara"), pergunte se quer registrar a correção e, se sim, atualize o arquivo.

## Modelo do arquivo

```markdown
# Voz da marca: <nome>

## Quem fala e com quem
<perfil, público, o que o público quer>

## Personalidade (3 palavras)
<palavra 1>, <palavra 2>, <palavra 3>

## Tratamento e formalidade
<você / tu / vocês; formal ou conversa; frases curtas ou longas>

## Palavras e expressões que usa
- ...

## O que nunca usa
- ...

## Emojis
<quais, quantos, onde>

## Fechamento padrão
<chamada para ação>

## Exemplos de textos aprovados
<2 ou 3 textos colados pelo usuário>

## Regras aprendidas
- <correções registradas ao longo do uso>
```

## Cuidados

- Não invente traços de personalidade que o usuário não descreveu nem mostrou nos exemplos.
- Voz não é desculpa para afirmar o que não é verdade: afirmações sobre preço, resultado e garantia continuam precisando ser reais.
- Para textos de venda, combine com `copywriting-vendas`; para legendas de Instagram, com `ig-caption`.
