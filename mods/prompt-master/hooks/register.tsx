import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

const isOn = atom({ plugin: 'prompt-master', key: 'isOn' } as const, true)

const SYSTEM = `Você é o Prompt Master. Reescreva o prompt do usuário para um assistente de programação (Claude Code) deixando-o claro, específico e acionável.
Regras:
- Preserve a intenção, o idioma e todos os detalhes, nomes, caminhos e trechos de código do original. Não invente requisitos.
- Deixe explícitos: objetivo, contexto relevante, restrições e o resultado esperado. Se o pedido for grande, organize em passos curtos.
- Seja conciso: não infle o texto.
- Responda SOMENTE com o prompt reescrito, sem explicações, aspas ou cercas de código.`

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: 'prompt-master',
      description: 'Liga ou desliga o Prompt Master (reescreve seu prompt antes de enviar).',
    })
    return next(e)
  })

  on('command.run', { command: 'prompt-master' }, async $ => {
    const now = await update($, isOn, v => !v)
    return { text: `Prompt Master ${now ? 'ligado' : 'desligado'}.` }
  })

  on('prompt.submit', async ($, e, next) => {
    const text = e.text.trim()
    const skip = e.command || e.isMeta || text === '' || text.startsWith('!') || (e.origin.kind !== 'composer' && e.origin.kind !== 'bridge')
    if (skip || !(await read($, isOn))) return next(e)

    $.ui.status('Prompt Master reescrevendo…')
    try {
      const r = await $.model.complete({
        model: 'haiku',
        system: SYSTEM,
        prompt: text,
        maxTokens: 2000,
        effort: 'low',
        timeoutMs: 20000,
      })
      if (r.isAnswered && r.text.trim()) {
        $.ui.toast('Prompt Master: prompt reescrito')
        return next({ ...e, text: r.text.trim() })
      }
    } finally {
      $.ui.status(undefined)
    }
    return next(e)
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    if (e.props.hasSurvey) return next(e)
    const on_ = await read($, isOn)
    const { Box, Text, Button } = $.ui.resolve(e)
    return (
      <Box>
        <Button
          key="pm"
          label={on_ ? '✨ Prompt Master: ligado' : '✨ Prompt Master: desligado'}
          onPress={() => update($, isOn, v => !v)}
        />
        <Text dimColor> clique para {on_ ? 'desligar' : 'ligar'} · prefixe com ! para enviar sem reescrever</Text>
      </Box>
    )
  })
}
