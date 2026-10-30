---
name: anti-ui-slop
description: Review or build interfaces while avoiding generic, AI-looking design. Use when the user says a UI looks generic, "AI slop", "vibe-coded", or asks to make a page look more original and professional.
---

# Anti UI Slop

## Telltale signs to remove
- Purple/blue gradients on white, glowing blobs, glassmorphism everywhere
- Default fonts (Inter, Roboto, system) with no hierarchy
- Every section as a centered card grid with an emoji or icon on top
- Generic copy: "Unlock the power of...", "Seamless", "Revolutionize"
- Uniform border radius and shadows on everything, low contrast gray text
- Stock hero: big headline, two buttons, mockup on the right
- Fake testimonials, lorem ipsum, placeholder logos, invented stats

## What to do instead
1. **Pick a point of view** before coding: audience, tone, one memorable idea. Write it in one line.
2. **Type**: choose a distinctive pairing, use a clear scale (at least 4 distinct sizes), tight headings, comfortable line length (60 to 75 characters).
3. **Color**: a limited palette (1 neutral base, 1 accent, 1 support) defined as tokens. Check contrast (WCAG AA).
4. **Layout**: vary rhythm and density, use asymmetry and real whitespace, align to a spacing scale (4 or 8 px).
5. **Content first**: real copy, real data, specific verbs. If content is missing, mark it clearly rather than faking it.
6. **Details**: consistent states (hover, focus, disabled, loading, empty, error), purposeful motion only.
7. **Restraint**: remove any element that has no job.

## Check before finishing
Squint test (is the hierarchy obvious?), contrast check, mobile width, keyboard focus visible, and ask "would a designer have chosen this, or was it the default?"
