<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./banner.svg?v=2">
  <source media="(prefers-color-scheme: light)" srcset="./banner-light.svg?v=2">
  <img src="./banner.svg?v=2" alt="Puneet Sharma — Lead Architect · AI Systems · Tokyo" width="100%">
</picture>

</div>

<br>

Thirteen years on the systems capital markets actually run on — trade pipelines,
reconciliation engines, and regulatory reporting across **JFSA, MAS, ASIC and HKMA**.
Most of my time now goes to the other side of that problem: **agentic infrastructure
that writes, tests and governs software**, and what it takes to make that trustworthy
enough to put near regulated systems.

I lead architecture for Asia RegTech out of Tokyo, where the work is mostly modular
monoliths, high-throughput trade pipelines and compliance automation. Alongside it I
build and open-source the tooling I wish existed: agent orchestration that holds a
spec, LLM gateways that enforce policy, lineage tracers that survive a codebase
nobody fully remembers writing.

AI tooling has taken **20–30% off delivery effort** on the teams I've rolled it out to.
I've mentored **15+ engineers** into senior and architect roles. Both numbers are mine
to defend, and I'd rather you judge me on the repositories below.

<br>

---

## Now

<table>
<tr>
<td width="50%" valign="top">

### Asia RegTech · Tokyo

High-stakes regulatory transformation across four APAC jurisdictions, on systems
where a bad reconciliation is a reportable event.

- Modular monolith architecture
- Real-time reconciliation engines
- Compliance automation
- Distributed processing at trade volume
- High-throughput trade pipelines

**Jurisdictions** `JFSA` `MAS` `ASIC` `HKMA`

**Stack** `Java` `Spring Boot` `Kafka` `PostgreSQL`

</td>
<td width="50%" valign="top">

### Agentic AI Systems

Autonomous systems that do the engineering work, and the guardrails that make
that a defensible thing to do.

- Multi-agent orchestration
- Autonomous delivery pipelines
- RAG knowledge systems
- AI-driven QA and validation
- Context engineering

**Concerns** `Governance` `Cost` `Traceability`

**Stack** `Python` `LangChain` `FastAPI` `LLMs`

</td>
</tr>
</table>

---

## The work

### AI &amp; agentic systems

**[awesome-prompts](https://github.com/sharmapuneet1510/awesome-prompts)** — A spec-driven engineering system for AI coding assistants.
Five role-based agents, 42 callable functions, 35 reusable skills, and gates that stop
an assistant from confidently building the wrong thing. Exports to Claude, Copilot,
Cursor, Windsurf, Gemini, Continue, OpenAI and Aider.
`Python` `LangChain` `RAG`

**[Aether Guard](https://github.com/sharmapuneet1510/promptshield)** — An LLM governance and query gateway that sits in front of your
providers: pre-query token and cost estimation, prompt classification, policy
enforcement, intelligent routing, and behaviour analytics. The control layer teams
need before they let an LLM near production.
`Python` `FastAPI`

**[ContextBridge](https://github.com/sharmapuneet1510/ai-context-bridge)** — Move an AI coding session from one model to another without
starting over. Captures, organises and exports context so work survives a context
window, a token budget, or a change of assistant.
`TypeScript` `VS Code`

**[Agentic AI Lab](https://github.com/sharmapuneet1510/agentic-ai-lab)** — Where the ideas above get tried before they earn a repository
of their own: multi-agent coordination, autonomous decision systems, prompt
engineering frameworks.
`Python` `LangChain`

### Lineage &amp; regulated data

**[Synapse Trace](https://github.com/sharmapuneet1510/synapse-trace)** — Data lineage for Java and XSLT codebases. Parses source to find
field mappings, constant references, DTO unmarshalling and method calls, then
stitches them into one lineage graph — across repository boundaries.
`Python` `Graph stores`

**[ai-lineage](https://github.com/sharmapuneet1510/ai-lineage)** — Enterprise platform for regulatory data lineage: visualising and
analysing how data moves through complex systems, for compliance and governance.
`React` `FastAPI` `Neo4j` `MSSQL`

**[Doc-Based RAG](https://github.com/sharmapuneet1510/doc-based-rag)** — Turning enterprise documentation into something you can
actually query: semantic search and vector retrieval over the pile of PDFs every
institution runs on.
`FastAPI` `Vector DB`

### Platforms &amp; tooling

**[ExecOS](https://github.com/sharmapuneet1510/exec-os)** — A zero-dependency execution system for engineering leadership:
task capture, project health scoring, commitment tracking, alerts and layered
dashboards. Runs entirely locally, which is the point.
`Python` `FastAPI`

**[Guardian](https://github.com/sharmapuneet1510/guardian)** — AI-powered multi-camera safety monitoring built for secure local
deployment, with incident-driven workflows rather than a wall of live feeds.
`Computer vision` `Python`

**[Workstream](https://github.com/sharmapuneet1510/workstream)** — Desktop workflow orchestration and release management.
`Electron` `TypeScript` `Node.js`

---

## Domains

<table>
<tr>
<td width="33%" valign="top">

### Architecture

- Modular monolith architecture
- Domain-driven design
- CQRS &amp; event sourcing
- Distributed systems
- Event-driven architecture
- API gateway patterns
- Resilience engineering

</td>
<td width="33%" valign="top">

### FinTech &amp; RegTech

- Regulatory reporting
- Capital markets infrastructure
- Reconciliation engines
- Trade lifecycle systems
- Settlement &amp; clearing
- Risk management
- Market data systems

</td>
<td width="33%" valign="top">

### Agentic AI

- Multi-agent patterns
- Workflow orchestration
- Autonomous feature delivery
- Context-aware RAG
- AI validation pipelines
- Test automation intelligence
- Governance &amp; cost control

</td>
</tr>
</table>

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./stack.svg?v=1">
  <source media="(prefers-color-scheme: light)" srcset="./stack-light.svg?v=1">
  <img src="./stack.svg?v=1" alt="Tools and platforms I work in" width="96%">
</picture>

</div>

---

## Trajectory

```
2015 ──── 2018    enterprise monoliths          mastered, then outgrown
2018 ──── 2022    microservices                 distributed systems, the hard way
2022 ──── 2024    modular monolith synthesis    the good parts of both
2024 ──── now     agentic infrastructure        systems that build systems
```

> The interesting problem stopped being how to write more code.
> It became how to design systems that can safely change themselves.

---

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./stats.svg?v=2">
  <source media="(prefers-color-scheme: light)" srcset="./stats-light.svg?v=2">
  <img src="./stats.svg?v=2" alt="Activity" width="47%">
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./langs.svg?v=2">
  <source media="(prefers-color-scheme: light)" srcset="./langs-light.svg?v=2">
  <img src="./langs.svg?v=2" alt="Languages by share of code" width="47%">
</picture>

<br><br>

<img src="https://github-readme-activity-graph.vercel.app/graph?username=sharmapuneet1510&bg_color=00000000&color=6b6259&title_color=6b6259&line=D4AF37&point=D4AF37&area=true&area_color=D4AF37&hide_border=true&custom_title=Contributions" alt="Contribution graph" width="96%">

<br><br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/sharmapuneet1510/sharmapuneet1510/output/snake.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/sharmapuneet1510/sharmapuneet1510/output/snake-light.svg">
  <img src="https://raw.githubusercontent.com/sharmapuneet1510/sharmapuneet1510/output/snake.svg" alt="Contribution snake" width="96%">
</picture>

</div>

---

## Writing

**[Tech Mavericks](https://github.com/sharmapuneet1510/tech-mavericks)** — High-scale architecture, distributed systems, AI engineering and
FinTech transformation, written for people who have to ship the thing.

**Nexus Threads** — Where mathematics, AI and architecture intersect.

**Capital markets deep dives** — Trading infrastructure, regulatory reporting, market
reconciliation and the distributed systems underneath them, taken apart slowly.

---

## Beyond the code

| | |
|:--|:--|
| **Cricket** | Leadership and pressure-handling, learned somewhere lower-stakes than production |
| **Japanese** | Putting down real roots in Tokyo's engineering community |
| **Mathematics** | Applied optimisation, and why distributed systems behave the way they do |
| **Mentorship** | Helping engineers make the jump from writing code to designing systems |

---

## Elsewhere

[LinkedIn](https://www.linkedin.com/in/sharmapuneet1510/) · [puneet@techmavericks.dev](mailto:puneet@techmavericks.dev) · [Tech Mavericks](https://github.com/sharmapuneet1510/tech-mavericks)

<sub>Every card on this page is drawn by [`tools/render.py`](./tools/render.py) and refreshed nightly — no badge services involved.</sub>
