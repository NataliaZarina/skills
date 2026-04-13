# Slide Data Schema

The `generate_deck.py` script reads JSON from stdin with this structure:

```json
{
  "title": "Topic Title",
  "subtitle": "One-line framing — the constraint or question this topic answers",
  "sections": [
    {
      "title": "Section Title",
      "goalIntuition": "One sentence mental model this section builds",
      "slides": [ ... ]
    }
  ]
}
```

## Slide Types

### section-title
Opening slide for a chapter. Dark background, prominent title, goal intuition as subtitle.
```json
{
  "type": "section-title",
  "section_label": "Chapter 1 of 5",
  "title": "What a CPU Actually Does",
  "subtitle": "A CPU is a genius working alone — optimized for doing one complex thing after another, very fast."
}
```

### constraint
Presents the problem that forced a design. Red accent. Optional progressive detail.
```json
{
  "type": "constraint",
  "title": "IP Addresses Are Unmemorizable",
  "body": "Every device has a numeric address. Humans can't remember 142.250.80.46.",
  "detail": "Even in the early ARPANET with only a few hundred hosts, people needed names."
}
```

### tradeoff
Two-column layout: green = optimized, red = sacrificed. Why below as fragment.
```json
{
  "type": "tradeoff",
  "title": "The Design Choice",
  "optimized": "Speed and simplicity — 3-5 second settlement",
  "sacrificed": "Full decentralization — relies on trusted validators",
  "why": "Banks need speed more than they need trustlessness."
}
```

### insight
The "aha" slide. Gold accent, dark background. This is the slide they'll screenshot.
```json
{
  "type": "insight",
  "body": "DNS is a hierarchical database — not because it's elegant, but because no single machine could hold all the world's name mappings.",
  "implication": "Every time you see hierarchy in infrastructure, ask: what couldn't fit in one place?"
}
```

### narrative
Essay-style content for deeper explanations. Supports multiple paragraphs.
```json
{
  "type": "narrative",
  "title": "How Money Actually Moves Between Countries",
  "body": "When you send money internationally, your bank doesn't actually send money. There's no pipe or wire that carries dollars from Miami to Tokyo.\\n\\nInstead, banks use a messaging system called SWIFT — the Society for Worldwide Interbank Financial Telecommunication. SWIFT is essentially a fax machine for banks."
}
```

### analogy
Memorable comparison that carries through the curriculum. Blue accent.
```json
{
  "type": "analogy",
  "body": "A CPU is like a brilliant executive. They can handle any problem — legal, financial, strategic. But hand them 10,000 envelopes to open, and they open them one at a time.",
  "connection": "They're overqualified for repetitive work — and that's exactly what AI needs."
}
```

### example
Real-world grounding with specific products, events, numbers. Blue accent.
```json
{
  "type": "example",
  "title": "AlexNet — The Moment GPUs Changed AI",
  "body": "In 2012, a neural network trained on two NVIDIA GTX 580 consumer gaming cards won a major image recognition competition by a huge margin. Without GPUs, this result might never have happened."
}
```

### comparison
Table for side-by-side comparisons (e.g., CPU vs GPU vs TPU).
```json
{
  "type": "comparison",
  "title": "The Hardware Spectrum",
  "headers": ["", "CPU", "GPU", "TPU"],
  "rows": [
    ["Designed for", "Anything", "Parallel tasks", "Matrix math only"],
    ["Cores", "4-24 complex", "Thousands simple", "Systolic array"],
    ["Flexibility", "Maximum", "High", "Minimal"]
  ]
}
```

### definition
Key term defined through the constraint that created it. Purple accent.
```json
{
  "type": "definition",
  "term": "Tensor",
  "definition": "A multi-dimensional grid of numbers. Neural networks store everything — inputs, weights, outputs — as tensors.",
  "context": "Google named their chip 'Tensor Processing Unit' because it processes these data structures and nothing else."
}
```

### image
Visual slide — either a web URL or embedded SVG markup.
```json
{
  "type": "image",
  "title": "The CPU Architecture",
  "url": "https://example.com/cpu-diagram.png",
  "alt": "Diagram showing CPU core architecture",
  "caption": "Notice how most of the chip area is dedicated to cache and control logic — not arithmetic."
}
```
Or with SVG:
```json
{
  "type": "image",
  "title": "Scalar → Vector → Matrix → Tensor",
  "svg": "<svg>...</svg>",
  "caption": "Each level adds a dimension. Neural networks work primarily with tensors."
}
```

### html
Custom HTML for complex visuals that don't fit other types. Use sparingly.
```json
{
  "type": "html",
  "html_content": "<h3>Custom Visual</h3><div>...</div>"
}
```

### bigpicture
Curriculum map showing progress. Green = done, gold = current, gray = upcoming.
```json
{
  "type": "bigpicture",
  "title": "Where We Are",
  "covered": ["The Naming Problem", "Why Hierarchy"],
  "current": "How Resolution Works",
  "upcoming": ["Caching", "Integration"],
  "skipped": ["DNSSEC — security extension, not needed for your goals"]
}
```

### summary
End-of-section or end-of-deck takeaways. Fragments build one at a time.
```json
{
  "type": "summary",
  "title": "What You Can Now Reason About",
  "takeaways": [
    "Why CPUs can't do AI efficiently — they spent their transistors on decision-making",
    "Why GPUs accidentally match AI's math — screens and neural networks need the same pattern",
    "Why TPUs exist — when you stop compromising, you build hardware shaped like the math"
  ]
}
```

### quote
Highlighted quote or key statement with attribution.
```json
{
  "type": "quote",
  "body": "Bitcoin was built to replace banks. Ripple was built to work with them.",
  "attribution": "The core identity split in crypto"
}
```

### content
General-purpose bullet slide. Use as fallback when no other type fits.
```json
{
  "type": "content",
  "title": "Ripple by the Numbers (2025)",
  "bullets": [
    "Valued at ~$40 billion",
    "Operating across 70+ markets",
    "3-5 second settlement times",
    "XRP is 3rd largest crypto by market cap"
  ],
  "fragments": true
}
```

## Design Guidelines

- **Narrative slides** are the workhorse — use them for the deep explanations
- **Constraint → Tradeoff → Insight** is the core pattern for each concept
- **Analogies** should be memorable enough to reference in later slides
- **Examples** with real names, dates, and numbers make abstract ideas concrete
- **Comparison tables** are essential for any "X vs Y" content
- **Definitions** should appear when jargon is first introduced — defined through constraint
- **Images** ground abstract concepts visually — always after explanation, never decorative
- Each chapter should have 5-10 slides that tell a complete story
- The deck should be readable as a standalone study guide on a phone
