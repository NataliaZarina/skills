# Example: GPUs and TPUs — Constraint-Driven Teaching

This is a real teaching conversation that represents the gold standard for how the /learn skill should teach. Study the patterns here: the depth, the pacing, the analogies, the real-world grounding, and the responsiveness to follow-up questions.

## What Made This Great

- **Started with clarifying questions** — "What's driving this question? What do you already know? How deep?"
- **Calibrated to the learner** — "I teach AI and need to intuit from first principles" shaped everything
- **Curriculum proposed first** with goal intuitions per section and a skipping table
- **Each section was essay-length** — full paragraphs building a causal chain, not bullet points
- **Terms defined through constraints** — CPU defined as "Central Processing Unit, the main chip, roughly postage-stamp sized, packed with billions of transistors"
- **Memorable analogies carried through** — "CPU as brilliant executive" referenced in multiple later sections
- **Real examples with real names** — Intel Core i7, Apple M1/M2/M3, AlexNet on GTX 580s, GPT-3's 175B parameters, NVIDIA's trillion-dollar market cap
- **Inevitability language throughout** — "had to", "forced by", "unavoidable", "the only viable path"
- **Responsive to gaps** — when user said "you never defined CPU," immediately filled it
- **Handled tangents gracefully** — "what are neural networks?" acknowledged as separate topic, gave minimum needed, offered future curriculum
- **Visuals arrived AFTER explanation** — scalar→vector→matrix→tensor visual created only after those terms were explained through constraints
- **Comparison tables** — CPU vs GPU vs TPU table crystallized the spectrum

## The Curriculum Structure

1. What a CPU Actually Does (constraint: general-purpose, unpredictable tasks)
2. Why AI Broke the CPU (constraint: matrix multiplication is embarrassingly parallel)
3. The GPU — Already Existed for Screens (accident of history: same math pattern)
4. The TPU — Hardware Shaped Like the Math (constraint: Google's scale economics)
5. Integration — The Landscape and Why It Matters (spectrum of generality vs efficiency)

Each section followed: Constraint → Design forced by constraint → Why it survived → Intuition to carry forward

## Key Teaching Moments

**The "had to" chain:**
> "Computers were built to handle unpredictable tasks → so CPUs were designed as sequential, general-purpose machines → then AI came along with the exact opposite workload → CPUs couldn't do this efficiently → the graphics industry had already solved this same pattern → GPUs were repurposed → but GPUs still carried baggage → Google asked 'what if we build hardware that does nothing except matrix multiplication?' → the TPU was born"

**The quotable insight:**
> "AI's core computation is millions of simple, independent math operations. CPUs are architecturally incapable of doing this efficiently — not because they're bad, but because they spent their transistor budget on handling complexity that AI doesn't have."

**The one sentence test:**
> "If a student asks 'why do we need GPUs and TPUs for AI?', you should be able to say: 'AI's core math is millions of simple, identical operations that can all happen at the same time. CPUs are designed for complex, unpredictable tasks — they're overqualified and slow for this job. GPUs have thousands of simple processors that accidentally match this pattern because screens needed the same thing. TPUs go even further — they're chips physically built in the shape of the math, sacrificing everything else for maximum efficiency at that one operation.'"
