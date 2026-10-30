---
name: minimalist-ui
description: Design and build clean, minimalist interfaces with strong hierarchy and generous whitespace. Use when the user asks for a minimal, clean, simple, or Apple/Notion-like UI, or wants to simplify a cluttered screen.
---

# Minimalist UI

## Principles
- One primary action per screen. Everything else is secondary or hidden.
- Remove before adding: borders, shadows, colors and icons need a reason.
- Hierarchy through size, weight and space, not decoration.
- Content is the interface.

## System
- **Spacing**: 8 px scale (8, 16, 24, 32, 48, 64). Prefer larger gaps over dividers.
- **Type**: one family, 2 to 3 weights, a scale like 12/14/16/20/28/40. Body at least 16 px.
- **Color**: neutral base, a single accent for actions and focus. Text contrast at least 4.5:1.
- **Shape**: one radius value, subtle or no shadows, 1 px hairlines only where needed.
- **Components**: simple buttons (filled primary, text or outline secondary), inputs with clear labels and visible focus, lists instead of cards when possible.
- **Motion**: 150 to 250 ms ease-out on state changes only; respect `prefers-reduced-motion`.

## Process
1. List what the user must do on the screen; delete everything else.
2. Sketch hierarchy: title, primary action, supporting content.
3. Implement with CSS variables for color, spacing, radius, type.
4. Verify responsive behavior (360 px up), keyboard focus and empty/error states.

Minimal does not mean empty: keep affordances obvious and labels explicit.
