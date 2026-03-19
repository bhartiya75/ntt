# Multi-Layer Memory Architecture for Persistent AI Coding Agents: A Practical Framework

**Chandra Shekhar Bhartiya**

*Independent Researcher*

**Date:** March 2026

**Keywords:** AI coding agents, memory persistence, knowledge graphs, vector search, Model Context Protocol, software engineering

---

## Abstract

AI-powered coding agents such as Claude Code, Cursor, GitHub Copilot, and OpenAI Codex CLI have transformed software development by providing intelligent code generation, debugging, and architectural guidance. However, these agents suffer from a fundamental limitation: **session amnesia**. Each interaction begins from a blank slate, forcing developers to repeatedly re-explain project context, architectural decisions, coding conventions, and debugging history. This paper presents a **multi-layer memory architecture** that addresses this limitation through five complementary persistence layers: static file memory, structured event memory, vector-semantic memory with knowledge graphs, reinforcement learning memory, and code structural memory. Each layer targets a distinct category of knowledge loss and operates independently, ensuring graceful degradation. We describe the design principles, implementation details, and practical deployment of this framework across real-world software engineering projects. Our architecture leverages the Model Context Protocol (MCP) as an integration substrate, SQLite with vector extensions for offline semantic search, and session lifecycle hooks for automatic knowledge capture. Qualitative evaluation across multiple projects demonstrates reduced context re-explanation, more consistent decision-making, and faster agent onboarding. To our knowledge, this work presents the first comprehensive taxonomy of memory persistence approaches for AI coding agents and proposes a unified architecture that synthesizes insights from twenty-two open-source memory solutions.

---

## 1. Introduction

### 1.1 The Rise of AI-Assisted Software Development

The landscape of software development has undergone a paradigm shift with the introduction of AI coding agents. Tools such as Anthropic's Claude Code, Cursor, GitHub Copilot, and OpenAI's Codex CLI have moved beyond simple code completion to serve as interactive collaborators capable of understanding codebases, generating complex implementations, debugging issues, and providing architectural guidance. These agents operate within developer environments---terminals, IDEs, and browsers---and interact with codebases through sophisticated tooling that includes file reading, code search, command execution, and browser automation.

The capability of these agents is remarkable: they can navigate unfamiliar codebases, understand complex dependency graphs, generate test suites, refactor legacy code, and even manage deployment workflows. However, beneath this impressive functionality lies a fundamental architectural limitation that significantly undermines their utility in sustained software engineering work.

### 1.2 The "Groundhog Day" Problem

We term this limitation the **"Groundhog Day" problem**, after the 1993 film in which the protagonist relives the same day repeatedly without memory of previous iterations. AI coding agents, regardless of their sophistication, typically begin each session with no memory of prior interactions. The agent that spent two hours yesterday understanding a project's authentication architecture, identifying a subtle race condition, and establishing a debugging strategy will, upon the next invocation, have no recollection of any of this work.

This amnesia manifests in several costly ways:

1. **Repeated explanations**: Developers must re-describe project structure, conventions, and goals at the start of each session.
2. **Inconsistent decisions**: Without memory of prior architectural choices and their rationale, agents may propose conflicting approaches across sessions.
3. **Lost debugging context**: Insights gained during troubleshooting---which code paths were explored, which hypotheses were eliminated---vanish entirely.
4. **Abandoned progress**: Multi-session tasks require the developer to manually reconstruct the agent's previous state, negating much of the productivity benefit.
5. **Erosion of trust**: Developers lose confidence in agents that cannot maintain continuity, reverting to manual work for complex tasks.

### 1.3 The Cost of Lost Context

The economic and cognitive cost of session amnesia is substantial. Consider a developer working with an AI agent on a medium-complexity microservices project over thirty sessions. If each session requires ten minutes of context re-establishment, the cumulative overhead is five hours---time spent not on productive work but on teaching the agent what it already knew. More insidiously, the qualitative cost of inconsistent decisions and forgotten conventions compounds over time, potentially introducing architectural drift and technical debt.

### 1.4 Our Contribution

This paper makes the following contributions:

1. **Problem taxonomy**: We systematically categorize the types of knowledge lost between agent sessions and establish requirements for effective agent memory systems.
2. **Multi-layer architecture**: We propose a five-layer memory architecture in which each layer addresses distinct memory needs while operating independently.
3. **Practical implementation**: We describe a working implementation built on the Model Context Protocol (MCP), SQLite, and offline embedding models, requiring no cloud dependencies.
4. **Ecosystem analysis**: We survey and taxonomize twenty-two open-source memory solutions for AI agents, positioning our work within this landscape.
5. **Qualitative evaluation**: We report on the practical deployment of this architecture across real-world software engineering projects.

---

## 2. Related Work

### 2.1 Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation (Lewis et al., 2020) established the foundational pattern of augmenting language model generation with retrieved external knowledge. RAG systems index a corpus of documents, retrieve relevant passages at inference time based on query similarity, and inject them into the model's context window. While RAG addresses the knowledge limitation of static training data, standard RAG implementations are designed for document retrieval rather than the dynamic, session-aware memory requirements of coding agents. The knowledge base is typically static, the retrieval is query-driven rather than event-driven, and there is no mechanism for the agent to write back learned information.

### 2.2 MemGPT / Letta

Packer et al. (2023) introduced MemGPT, later developed into the Letta framework, which applies operating system concepts of virtual memory management to large language models. MemGPT maintains a hierarchy of memory---a limited "main context" analogous to RAM and an unbounded "external context" analogous to disk---with the LLM itself managing page-in and page-out operations. This work is seminal in recognizing that LLMs need memory management abstractions, but MemGPT focuses primarily on managing a single extended conversation rather than persisting knowledge across independent sessions. Furthermore, its self-managed paging approach introduces latency and token overhead that may be prohibitive in the interactive coding agent context.

### 2.3 Mem0

Mem0 (formerly EmbedChain) provides a memory layer for AI applications, offering APIs for storing, searching, and managing memories with automatic extraction from conversations. Mem0 supports multiple vector store backends and provides both cloud-hosted and self-hosted deployment options. While Mem0 addresses the general problem of AI application memory, it operates primarily as a single-layer solution focused on vector-semantic search and lacks the multi-layer architecture we propose. Its cloud-hosted model also introduces latency and privacy considerations relevant to coding agents that process proprietary codebases.

### 2.4 Knowledge Graphs for AI Agents

Knowledge graph approaches (Hogan et al., 2021) represent information as entities, attributes, and relations, enabling structured reasoning over connected data. Systems such as Graphiti (Zep AI) and Neo4j-backed MCP servers bring knowledge graph capabilities to AI agents, supporting temporal queries and relationship traversal. Knowledge graphs excel at representing structured relationships---such as "module A depends on module B" or "decision X was made because of constraint Y"---but are less suited to storing unstructured observations or performing fuzzy semantic matching on natural language descriptions.

### 2.5 Vector Databases in AI Applications

Purpose-built vector databases such as ChromaDB, Pinecone, Weaviate, and Qdrant have become standard infrastructure for AI applications requiring similarity search. In the agent memory context, vector databases enable semantic recall: finding memories that are conceptually similar to a query even when they share no keywords. However, vector-only approaches lack the structured reasoning capabilities of knowledge graphs and the explicit categorization of typed memory systems. Recent work on hybrid search---combining vector similarity with traditional full-text search---has shown improved retrieval quality (Ma et al., 2024).

### 2.6 Session Persistence in Conversational AI

Commercial conversational AI platforms (e.g., ChatGPT with memory, Google Gemini with context caching) have begun introducing session persistence features, typically storing user preferences and interaction history. These implementations are generally opaque, cloud-dependent, and not designed for the specialized requirements of software engineering workflows. They also raise privacy concerns when applied to proprietary codebases.

### 2.7 Model Context Protocol (MCP)

Anthropic's Model Context Protocol (2024) provides a standardized interface for connecting AI models to external tools and data sources. MCP defines a client-server architecture in which MCP servers expose capabilities (tools, resources, prompts) that AI agents can invoke. This protocol has emerged as a critical integration layer for agent memory systems, enabling memory servers to be composed alongside other development tools without tight coupling. Our architecture leverages MCP as the substrate through which all memory layers are accessed.

---

## 3. Problem Analysis

### 3.1 Types of Knowledge Lost Between Sessions

Through systematic observation of AI coding agent usage across multiple software engineering projects, we identify six categories of knowledge that are lost between sessions:

**Category 1: Architectural Decisions and Rationale.** When an agent recommends a particular architectural pattern---such as choosing event sourcing over CRUD, selecting a specific database, or designing an API boundary---the decision and its rationale are lost. Subsequent sessions may propose contradictory architectures because the constraints and trade-offs that informed the original decision are no longer available.

**Category 2: User Preferences and Coding Style.** Developers have strong preferences regarding code formatting, naming conventions, error handling patterns, testing approaches, and documentation style. An agent that has been corrected to use `snake_case` instead of `camelCase`, to prefer explicit error handling over exceptions, or to write integration tests before unit tests will forget all such preferences in the next session.

**Category 3: Project Conventions and Patterns.** Beyond individual preferences, projects develop conventions: specific directory structures, import ordering rules, logging patterns, configuration management approaches, and deployment procedures. These conventions are often implicit, documented incompletely (if at all), and critical for maintaining codebase consistency.

**Category 4: Debugging Insights and Gotchas.** Some of the most valuable knowledge generated during agent-assisted development comes from debugging sessions. Understanding that "the authentication middleware silently swallows 401 errors in test mode" or "the database connection pool exhausts after 50 concurrent requests" represents hard-won insight that is extremely costly to rediscover.

**Category 5: Task Progress and Context.** Multi-session tasks---implementing a feature, performing a large refactoring, or migrating a system---require continuity. Knowledge of what has been completed, what remains, what blockers were encountered, and what approach is being followed must persist across sessions.

**Category 6: Relationships Between Code Components.** Understanding how components interact---which services call which, which modules share data structures, which tests cover which functionality---is essential for effective code modification. While this information is theoretically derivable from the codebase itself, the cost of re-deriving it each session is significant.

### 3.2 Requirements for Effective Agent Memory

Based on the knowledge categories above and the operational constraints of coding agents, we establish the following requirements for an effective memory system:

**R1: Low Latency.** Memory operations must not introduce perceptible delays in the coding workflow. Developers using AI agents expect near-instantaneous responses; a memory system that adds seconds of latency to each interaction will be abandoned. We target sub-200ms for memory retrieval operations.

**R2: Semantic Recall.** The memory system must support retrieval based on semantic similarity, not merely keyword matching. A query about "handling user authentication failures" should retrieve memories about "login error management" even though the terminology differs.

**R3: Structured and Unstructured Storage.** Different knowledge categories demand different storage models. Architectural decisions benefit from structured representation (decision, alternatives considered, rationale, date). Debugging insights are better captured as unstructured natural language observations. The memory system must accommodate both.

**R4: Session-Aware Lifecycle Hooks.** Memory capture and retrieval should be triggered automatically by session lifecycle events (start, end, task completion) rather than requiring explicit user commands. This reduces the cognitive overhead of memory management.

**R5: Offline Operation.** Coding agents frequently operate on proprietary codebases in environments with restricted network access. The memory system must function entirely offline, with no dependency on cloud services for core operations.

**R6: Graceful Degradation.** The failure or unavailability of any single memory component must not compromise the agent's ability to function. Each memory layer should operate independently, with the overall system degrading gracefully as layers become unavailable.

**R7: Privacy and Isolation.** Memories from one project must not leak into another. The memory system must support project-level isolation to prevent cross-contamination of context and to protect proprietary information.

---

## 4. Multi-Layer Memory Architecture

### 4.1 Architecture Overview

We propose a five-layer memory architecture in which each layer addresses distinct requirements and operates independently. The layers are ordered by increasing sophistication and decreasing ubiquity:

```
+------------------------------------------------------------------+
|                    AI Coding Agent Runtime                        |
|                                                                  |
|  +------------------------------------------------------------+  |
|  |                  MCP Integration Layer                      |  |
|  +------------------------------------------------------------+  |
|       |           |           |           |           |          |
|  +--------+  +--------+  +--------+  +--------+  +--------+    |
|  | Layer 1|  | Layer 2|  | Layer 3|  | Layer 4|  | Layer 5|    |
|  | Static |  |Struct. |  | Vector |  |  RL    |  | Code   |    |
|  | File   |  | Event  |  |Semantic|  | Memory |  |Struct. |    |
|  | Memory |  | Memory |  | Memory |  |        |  | Memory |    |
|  +--------+  +--------+  +--------+  +--------+  +--------+    |
|       |           |           |           |           |          |
|  CLAUDE.md   Hooks +     SQLite +      SONA +      AST +       |
|  .cursorrules typed     sqlite-vec    HNSW       Symbol        |
|              entries    + FTS5     trajectories   Index         |
+------------------------------------------------------------------+
```

*Figure 1: Multi-Layer Memory Architecture. Each layer communicates with the agent runtime through the MCP integration layer and maintains independent storage.*

#### Layer 1: Static File Memory

The simplest and most widely adopted form of agent memory is the **static file**, exemplified by Anthropic's `CLAUDE.md` and Cursor's `.cursorrules`. These files are loaded into the agent's system prompt at the beginning of every session, providing a guaranteed baseline of project context.

**Characteristics:**
- **Storage format:** Plain Markdown files in the project root
- **Capacity:** Limited to approximately 200 lines (~4,000 tokens) to avoid consuming excessive context window space
- **Management:** Manual; the developer or agent explicitly updates the file
- **Retrieval:** Automatic; loaded at session initialization
- **Best for:** Stable conventions, project structure overviews, critical constraints

**Advantages:** Zero infrastructure requirements, version-controlled alongside code, universally supported by modern AI coding tools.

**Limitations:** Severe capacity constraints, no semantic search capability, manual maintenance burden, no temporal awareness (no concept of when information was added or whether it remains current).

#### Layer 2: Structured Event Memory

The second layer captures knowledge as **typed, categorized entries** triggered by session lifecycle events. Unlike static files, this layer supports multiple memory types and keyword-based search.

**Characteristics:**
- **Storage format:** JSON entries with typed schemas
- **Memory types:** `decision`, `pattern`, `gotcha`, `architecture`, `progress`, `context`
- **Triggers:** Session start (recall), session end (extract learnings), explicit save
- **Retrieval:** Keyword search, type filtering, tag-based queries
- **Best for:** Discrete, categorizable knowledge units

**Schema example:**
```json
{
  "id": "mem_a1b2c3",
  "type": "decision",
  "content": "Chose PostgreSQL over MongoDB for the analytics service because
              the query patterns are predominantly relational joins across
              time-series data. MongoDB's document model would require
              denormalization that complicates the aggregation pipeline.",
  "tags": ["database", "analytics", "architecture"],
  "created": "2026-02-15T10:30:00Z",
  "supersedes": null
}
```

**Advantages:** Structured data enables precise queries ("show me all decisions tagged 'database'"), types enable role-specific retrieval, supersession chains maintain decision history.

**Limitations:** Keyword search misses semantic relationships, manual tagging introduces inconsistency, no vector similarity matching.

#### Layer 3: Vector-Semantic Memory

The third layer provides the richest memory capabilities through a **knowledge graph backed by hybrid vector-semantic search**. This layer, exemplified by implementations such as Memento MCP, combines the structured reasoning of knowledge graphs with the fuzzy matching capability of vector embeddings.

**Characteristics:**
- **Storage format:** SQLite database with sqlite-vec extension
- **Data model:** Knowledge graph (entities, observations, relations)
- **Search:** Hybrid---vector similarity (BGE-M3, 1024 dimensions) combined with BM25 full-text search
- **Embeddings:** Offline generation via `@xenova/transformers` (ONNX runtime)
- **Infrastructure:** Single SQLite file, zero external dependencies
- **Best for:** Nuanced recall, connecting related concepts, semantic search

**Knowledge Graph Schema:**

```
+-------------+          +---------------+          +-------------+
|   Entity    |  1---*   | Observation   |          |  Relation   |
+-------------+          +---------------+          +-------------+
| id          |          | id            |          | id          |
| name        |          | entity_id  (FK)|         | source_id   |
| entity_type |          | content       |          | target_id   |
| created_at  |          | embedding (vec)|         | relation_type|
| updated_at  |          | created_at    |          | created_at  |
+-------------+          +---------------+          +-------------+
                                                         |
                              Entity ----< Relation >---- Entity
```

*Figure 2: Knowledge Graph Schema. Entities represent concepts (modules, decisions, people). Observations are factual statements about entities with associated embeddings. Relations connect entities with typed edges.*

**Hybrid Search Algorithm:**

The hybrid search combines vector similarity and BM25 full-text scores:

```
score(query, memory) = alpha * vector_similarity(embed(query), embed(memory))
                     + (1 - alpha) * bm25_score(query, memory)
```

where `alpha = 0.7`, reflecting the empirical observation that semantic similarity is generally more valuable than keyword overlap for coding agent memory retrieval, while BM25 provides important exact-match signals for technical terms such as function names, error codes, and library identifiers.

**Advantages:** Semantic search handles vocabulary variation, knowledge graph captures relationships, hybrid scoring balances precision and recall, single-file portability.

**Limitations:** Embedding model download size (~400MB for BGE-M3), first-query latency for model loading, storage growth requires periodic consolidation.

#### Layer 4: Reinforcement Learning Memory

The fourth layer introduces **learning from outcomes**, enabling the agent to improve its behavior over time based on the success or failure of previous actions.

**Characteristics:**
- **Storage format:** Trajectory records with outcome annotations
- **Learning mechanism:** SONA (Self-Organizing Neural Architecture) with EWC++ consolidation
- **Index:** HNSW (Hierarchical Navigable Small World) for fast pattern matching
- **Capabilities:** Task routing optimization, session state save/restore, pattern recognition
- **Best for:** Improving agent behavior over time, optimal tool/approach selection

**Trajectory Record:**
```
Trajectory {
  id: "traj_001",
  task: "Fix authentication middleware race condition",
  steps: [
    { action: "grep for auth middleware", result: "found 3 files", quality: 0.8 },
    { action: "read middleware source", result: "identified shared state", quality: 0.9 },
    { action: "apply mutex lock", result: "race condition resolved", quality: 1.0 }
  ],
  outcome: success,
  agent: "coder",
  duration: "12 minutes"
}
```

**Advantages:** Enables genuine learning, not just recall; optimizes agent routing over time; session state persistence enables multi-session task continuity.

**Limitations:** Requires sufficient trajectory data for meaningful learning; reinforcement signals are noisy in software engineering contexts; pattern overfitting risk.

#### Layer 5: Code Structural Memory

The fifth layer provides **symbol-level understanding** of the codebase through AST (Abstract Syntax Tree) parsing and indexing.

**Characteristics:**
- **Storage format:** Indexed symbol database with cached source
- **Capabilities:** Symbol search, file outline, import/reference graph, cross-file navigation
- **Languages:** Support for 40+ programming languages via tree-sitter parsers
- **Best for:** Codebase navigation, understanding component relationships, impact analysis

**Capabilities:**
- `get_file_outline`: List all functions, classes, and methods in a file with signatures
- `search_symbols`: Find symbols by name, signature, or summary across the codebase
- `find_references`: Locate all usages of a given identifier
- `find_importers`: Identify all files that import from a given module
- `get_context_bundle`: Retrieve a symbol's definition plus its import context

**Advantages:** Provides structural understanding that complements semantic memory; import graphs enable impact analysis; symbol-level indexing is more efficient than full-file reading.

**Limitations:** Requires indexing step; index staleness after code changes; language parser coverage varies.

### 4.2 Information Flow Between Layers

The layers interact through a defined information flow pattern aligned with the session lifecycle:

```
Session Start
    |
    +---> Layer 1: Load CLAUDE.md into system prompt
    +---> Layer 2: Recall recent memories (decisions, progress, gotchas)
    +---> Layer 4: Restore session state (if resuming)
    |
During Session
    |
    +---> Layer 3: Semantic search on user queries for relevant context
    +---> Layer 5: Code structure queries for navigation
    +---> Layer 3: Knowledge graph updates (new entities, observations)
    +---> Layer 2: Save discrete learnings as they emerge
    |
Task Completion
    |
    +---> Layer 4: Record trajectory with outcome for learning
    +---> Layer 2: Extract and save task-specific learnings
    |
Session End
    |
    +---> Layer 2: Consolidate session learnings
    +---> Layer 4: Save session state for future restoration
    +---> Layer 1: (Optionally) Update CLAUDE.md with stable insights
```

*Figure 3: Information flow across memory layers during a typical agent session.*

### 4.3 Design Principles

The architecture adheres to five design principles:

**Principle 1: Independence.** Each layer functions as a standalone system. Removing any single layer degrades capability but does not cause failure. A deployment with only Layer 1 (static files) still provides basic memory; adding Layer 3 (semantic search) provides a significant capability increase; the full five-layer stack provides maximum persistence.

**Principle 2: Complementarity.** The layers are designed to be complementary rather than redundant. Static files handle stable knowledge; structured memory handles categorized facts; semantic memory handles nuanced, connected knowledge; RL memory handles behavioral learning; code structural memory handles codebase understanding. Overlap is minimized.

**Principle 3: Low Overhead.** Memory operations are designed to be non-blocking and low-latency. Embedding generation is cached; database queries use indexed lookups; session hooks execute asynchronously where possible. The target is for memory operations to add less than 200ms to any agent interaction.

**Principle 4: Single-File Portability.** SQLite-based layers (Layers 3 and 4) store all data in single database files that can be trivially backed up, version-controlled, or transferred. This design decision prioritizes operational simplicity over the theoretical advantages of client-server database architectures.

**Principle 5: Privacy by Default.** Memory is project-scoped. Each project maintains its own memory stores, and there is no mechanism for cross-project memory leakage. This is a deliberate design choice: while cross-project memory transfer could be valuable, the privacy risks of inadvertent context leakage outweigh the benefits in most professional software engineering contexts.

---

## 5. Implementation

### 5.1 Technology Stack

The implementation leverages the following technology stack:

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Integration layer | Model Context Protocol (MCP) | Standardized tool interface between agent and memory servers |
| Vector storage | SQLite + sqlite-vec | Local vector similarity search with no external dependencies |
| Embeddings | BGE-M3 via @xenova/transformers | Offline 1024-dimensional embedding generation |
| Full-text search | SQLite FTS5 | BM25-based keyword search for hybrid retrieval |
| Structured storage | JSON files / SQLite | Typed memory entries with metadata |
| Code indexing | Tree-sitter parsers | AST-based symbol extraction across 40+ languages |
| Session hooks | MCP lifecycle events | Automatic memory capture at session boundaries |

### 5.2 Key Implementation Details

#### 5.2.1 Hybrid Search Scoring

The core retrieval mechanism combines vector similarity and BM25 full-text search. Given a query `q` and a candidate memory `m`:

```
score(q, m) = 0.7 * cosine_similarity(E(q), E(m)) + 0.3 * normalized_bm25(q, m)
```

where `E(x)` denotes the BGE-M3 embedding of text `x`. The weighting factor `alpha = 0.7` was determined empirically: pure vector search excels at capturing semantic relationships but misses exact technical terms; pure BM25 excels at exact matches but fails on paraphrase. The hybrid approach captures both.

**Normalization:** BM25 scores are normalized to the `[0, 1]` range using min-max normalization across the candidate set to ensure comparability with cosine similarity scores.

#### 5.2.2 Knowledge Graph Operations

The knowledge graph supports four primary operations:

1. **Create entities:** Register new concepts with typed classification.
   ```
   create_entities([{ name: "AuthMiddleware", entityType: "module" }])
   ```

2. **Add observations:** Attach factual statements to entities, with automatic embedding generation.
   ```
   add_observations([{
     entityName: "AuthMiddleware",
     contents: ["Uses JWT with RS256 signing", "Rate-limits to 100 req/min per IP"]
   }])
   ```

3. **Create relations:** Establish typed connections between entities.
   ```
   create_relations([{
     from: "AuthMiddleware",
     to: "UserService",
     relationType: "authenticates_requests_for"
   }])
   ```

4. **Search:** Hybrid vector + BM25 retrieval across all observations.
   ```
   search_nodes({ query: "authentication rate limiting" })
   ```

#### 5.2.3 Embedding Model Management

The BGE-M3 embedding model (approximately 400MB) is managed with the following strategy:

- **Lazy loading:** The model is loaded on first use rather than at server startup, avoiding unnecessary memory consumption when memory features are not invoked.
- **Caching:** Once loaded, the model remains in memory for the duration of the MCP server process.
- **Offline operation:** The `@xenova/transformers` library runs models locally via ONNX Runtime, requiring no network access after initial download.
- **Dimensionality:** BGE-M3 produces 1024-dimensional embeddings, providing a strong balance between representational capacity and storage efficiency.

#### 5.2.4 Session Lifecycle Hooks

Automatic memory capture is orchestrated through session lifecycle hooks:

```
hook: session-start
  triggers:
    - Load CLAUDE.md into context
    - Recall memories tagged with current project
    - Restore last session state (if available)
    - Search knowledge graph for entities related to user's first message

hook: pre-task
  triggers:
    - Search semantic memory for context relevant to the task description
    - Check for related past trajectories (successes and failures)

hook: post-task
  triggers:
    - Record task trajectory with outcome
    - Extract and save learnings (decisions, gotchas, patterns)

hook: session-end
  triggers:
    - Consolidate session memories
    - Save session state for future restoration
    - Update progress tracking
```

### 5.3 Production MCP Server Configuration

The following is the **exact production configuration** deployed and tested across multiple real-world projects. All MCP servers are defined in `~/.claude.json` under the `mcpServers` key, making them globally available across every Claude Code session regardless of project.

#### 5.3.1 MCP Server Definitions

```json
{
  "mcpServers": {
    "memento": {
      "type": "stdio",
      "command": "npx",
      "args": ["@iachilles/memento@latest"],
      "env": {
        "MEMORY_DB_PATH": "/Users/<username>/.claude/memory-db/memento.db"
      }
    },
    "ruflo": {
      "command": "ruflo",
      "args": ["mcp", "start"],
      "env": {}
    },
    "jcodemunch": {
      "type": "stdio",
      "command": "uvx",
      "args": ["jcodemunch-mcp"],
      "env": {}
    },
    "context-mode": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "context-mode@latest"],
      "env": {}
    }
  }
}
```

**Server roles:**
- **memento** (Layer 3): Knowledge graph + hybrid vector-semantic search. Uses `MEMORY_DB_PATH` to ensure the SQLite database persists in a known location rather than ephemeral npx cache directories.
- **ruflo** (Layer 4): Intelligence layer providing HNSW-indexed memory, SONA reinforcement learning, session save/restore, and agent orchestration. Exposes 80+ MCP tools spanning memory, hooks, agents, workflows, and neural subsystems.
- **jcodemunch** (Layer 5): AST-based code indexing with symbol search, import graph traversal, and file outline extraction across 40+ languages.
- **context-mode** (Context optimization): Sandbox execution environment that keeps large tool outputs out of the context window, with BM25-indexed knowledge base for on-demand retrieval.

#### 5.3.2 Session Lifecycle Hooks

Hooks are defined in `~/.claude/settings.json` and trigger shell commands at session lifecycle events. These hooks are the glue that orchestrates automatic memory capture without manual intervention.

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [{
          "type": "command",
          "command": "echo 'MEMORY RESTORE: Call the memory_recall tool now to restore project context from previous sessions before proceeding.'",
          "timeout": 10
        }]
      },
      {
        "hooks": [{
          "type": "command",
          "command": "ruflo hooks session-restore 2>/dev/null && echo 'RUFLO: Session intelligence restored.' || echo 'RUFLO: Fresh session.'",
          "timeout": 15
        }]
      }
    ],
    "Stop": [
      {
        "hooks": [{
          "type": "command",
          "command": "node \"/opt/homebrew/lib/node_modules/claude-code-memory/dist/extractor.js\"",
          "timeout": 30
        }]
      },
      {
        "hooks": [{
          "type": "command",
          "command": "ruflo hooks session-end 2>/dev/null || true",
          "timeout": 15
        }]
      }
    ],
    "PreCompact": [
      {
        "hooks": [{
          "type": "command",
          "command": "node \"/opt/homebrew/lib/node_modules/claude-code-memory/dist/extractor.js\"",
          "timeout": 30
        }]
      },
      {
        "hooks": [{
          "type": "command",
          "command": "ruflo hooks session-end 2>/dev/null || true",
          "timeout": 15
        }]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [{
          "type": "command",
          "command": "node \"/opt/homebrew/lib/node_modules/claude-code-memory/dist/extractor.js\"",
          "timeout": 30
        }]
      },
      {
        "hooks": [{
          "type": "command",
          "command": "ruflo hooks session-end 2>/dev/null || true",
          "timeout": 15
        }]
      }
    ]
  }
}
```

**Hook behavior explained:**

| Event | Layer 2 Action | Layer 4 Action |
|-------|---------------|---------------|
| **SessionStart** | Inject prompt to recall structured memories | Restore last session state from Ruflo |
| **Stop** | Extract learnings via `claude-code-memory` extractor | Save session state via `ruflo hooks session-end` |
| **PreCompact** | Extract learnings before context compression | Save state before compression discards context |
| **SessionEnd** | Final extraction of session learnings | Final session state persistence |

The `PreCompact` hook is particularly important: Claude Code compresses conversation history when approaching context limits, which would otherwise lose in-context learnings. By triggering extraction before compaction, we capture knowledge that would otherwise be discarded.

#### 5.3.3 Claude Code Plugins

The production setup also leverages Claude Code's plugin system for enhanced capabilities:

```json
{
  "enabledPlugins": {
    "claude-code-setup@claude-plugins-official": true,
    "code-review@claude-plugins-official": true,
    "code-simplifier@claude-plugins-official": true,
    "explanatory-output-style@claude-plugins-official": true,
    "feature-dev@claude-plugins-official": true,
    "frontend-design@claude-plugins-official": true,
    "figma@claude-plugins-official": true,
    "github@claude-plugins-official": true,
    "typescript-lsp@claude-plugins-official": true
  }
}
```

These plugins provide specialized skills (code review, feature development, frontend design) that benefit from persistent memory---the agent remembers project-specific review standards, design system tokens, and development patterns across sessions.

#### 5.3.4 Auto-Memory File Convention

Layer 1 uses Claude Code's built-in auto-memory directory at:
```
~/.claude/projects/<project-hash>/memory/MEMORY.md
```

This file is automatically loaded into the system prompt at session start. The first 200 lines are included; content beyond that is truncated. Best practice is to keep MEMORY.md concise and link to topic-specific files (e.g., `debugging.md`, `patterns.md`) for detailed notes.

#### 5.3.5 Complete Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     Claude Code Agent Runtime                    │
│                                                                  │
│  ┌──────────┐  ┌───────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ System   │  │  Context  │  │ Tool     │  │  Response     │  │
│  │ Prompt   │  │  Window   │  │ Router   │  │  Generator    │  │
│  │(MEMORY.md│  │           │  │  (MCP)   │  │               │  │
│  │ loaded)  │  │           │  │          │  │               │  │
│  └────┬─────┘  └─────┬─────┘  └────┬─────┘  └───────────────┘  │
│       │              │              │                            │
│  Layer 1             │         MCP Transport (stdio)             │
│  (Static)            │              │                            │
└──────────────────────┼──────────────┼────────────────────────────┘
                       │              │
       ┌───────────────┼──────────────┼───────────────────┐
       │               │              │                   │
  ┌────▼─────┐  ┌──────▼──────┐ ┌────▼──────┐  ┌────────▼────────┐
  │ claude-  │  │   memento   │ │   ruflo   │  │   jcodemunch    │
  │ code-    │  │  MCP Server │ │MCP Server │  │   MCP Server    │
  │ memory   │  │             │ │           │  │                 │
  │ (hook)   │  │ SQLite+vec  │ │ HNSW+SONA │  │ AST+TreeSitter  │
  │          │  │ +FTS5+BGE-M3│ │ +Sessions │  │ +SymbolIndex    │
  │ Layer 2  │  │  Layer 3    │ │  Layer 4  │  │    Layer 5      │
  └──────────┘  └─────────────┘ └───────────┘  └─────────────────┘
       │              │              │                   │
  ┌────▼─────┐  ┌─────▼──────┐ ┌────▼──────┐  ┌────────▼────────┐
  │  JSON    │  │ memento.db │ │ ruflo.db  │  │  index cache    │
  │ entries  │  │(single file│ │+ session  │  │  (per-repo)     │
  │          │  │ ~/.claude/  │ │  state    │  │                 │
  │          │  │ memory-db/) │ │           │  │                 │
  └──────────┘  └────────────┘ └───────────┘  └─────────────────┘
```

*Figure 5: Production deployment architecture showing the complete stack from agent runtime through MCP servers to persistent storage. All data stores are local files with zero external service dependencies.*

Each MCP server runs as an independent process, communicating with the agent runtime through the standardized MCP stdio transport. This configuration provides the full five-layer memory architecture with zero cloud dependencies, zero Docker requirements, and a total setup time of approximately 30 minutes.

---

## 6. Evaluation

### 6.1 Qualitative Assessment

We deployed the multi-layer memory architecture across four software engineering projects over a period of eight weeks. The projects ranged from a greenfield web application to a legacy system migration. While we did not conduct controlled experiments with statistical significance testing---such experiments are challenging in the inherently variable domain of software engineering---we report qualitative observations.

**Reduced Context Re-explanation.** The most immediately apparent benefit was a dramatic reduction in the need to re-explain project context at the start of sessions. With Layer 2 (structured memory) automatically recalling recent decisions and progress, and Layer 3 (semantic memory) retrieving relevant context based on the user's initial query, sessions began productively rather than with orientation.

**Consistent Decision-Making.** Architectural decisions persisted across sessions through Layer 2's decision-type memories. When the agent encountered a choice point similar to a previous decision, it could retrieve the prior rationale and either follow the established pattern or explicitly articulate why a different approach was warranted. This consistency is particularly valuable in multi-week projects where architectural drift is a common problem.

**Faster Agent Onboarding.** Layer 5 (code structural memory) significantly reduced the time required for the agent to understand a codebase. Rather than reading files sequentially to build understanding, the agent could query the symbol index for specific functions, trace import graphs, and identify component relationships. Combined with Layer 3's knowledge graph of project-specific concepts, the agent could achieve working understanding of a complex codebase within the first interaction.

**Better Code Quality Through Remembered Conventions.** Layer 1 (static file) and Layer 2 (structured memory) worked together to maintain coding conventions. Project-specific patterns---error handling approaches, logging formats, test structure---persisted across sessions, resulting in more consistent code generation.

### 6.2 Comparison with Alternatives

| Approach | Semantic Search | Knowledge Graph | Offline | Setup Complexity | Memory Types Supported |
|----------|:-:|:-:|:-:|:-:|:-:|
| No memory | No | No | N/A | None | None |
| CLAUDE.md only | No | No | Yes | Minimal | Static conventions |
| Single vector MCP | Yes | No | Varies | Low | Unstructured text |
| Single graph MCP | No | Yes | Varies | Medium | Structured relations |
| Mem0 | Yes | No | Optional | Medium | Unstructured + metadata |
| **Our multi-layer** | **Yes** | **Yes** | **Yes** | **Medium-High** | **All six categories** |

*Table 1: Comparison of memory approaches for AI coding agents. Our multi-layer architecture is the only approach that provides semantic search, knowledge graph capabilities, full offline operation, and coverage of all six knowledge categories identified in Section 3.1.*

### 6.3 Limitations

We acknowledge several limitations of our current architecture:

**Cold Start.** The first session with a new project has no memories to retrieve. The agent must build its memory from scratch, with Layer 5 (code structural memory) providing the only head start through codebase indexing. Strategies for cold start mitigation---such as automatic memory population from README files, commit history, and existing documentation---are discussed in Section 8.

**Embedding Model Size.** The BGE-M3 embedding model requires approximately 400MB of disk space and significant memory when loaded. While this is acceptable on development workstations, it may be prohibitive in resource-constrained environments. Smaller models (e.g., all-MiniLM-L6-v2 at ~80MB) trade dimensionality for reduced resource requirements.

**Memory Bloat.** Without active management, the knowledge graph and structured memory can accumulate stale or redundant entries. While Layer 2 supports supersession chains (a new memory can explicitly replace an older one), automated consolidation---merging duplicate memories, pruning outdated entries, compressing low-value observations---requires further development.

**No Cross-Project Memory.** By design, project memory is isolated. A developer who learns that "library X has a subtle bug in version 2.3" through one project cannot automatically benefit from this knowledge in another project. While this isolation protects privacy, it prevents valuable cross-project learning.

**Evaluation Limitations.** Our evaluation is qualitative and based on a limited number of projects and a single developer. Controlled experiments with multiple developers, standardized tasks, and quantitative metrics would strengthen the evidence for the architecture's benefits.

---

## 7. Open-Source Ecosystem Analysis

Through a systematic survey of the AI agent memory landscape, we identified twenty-two open-source solutions, which we organize into a taxonomy based on their primary storage and retrieval approach.

### 7.1 SQLite-Based Solutions

These solutions leverage SQLite's ubiquity and zero-configuration deployment:

- **Memento MCP** (iAchilles/memento, npm: `@iachilles/memento`): Knowledge graph with hybrid vector (sqlite-vec, BGE-M3) and BM25 search. Our Layer 3 reference implementation.
- **Dead Simple Memory** (manuel-materazzo/dead-simple-memory-mcp): Minimal SQLite-backed memory with sqlite-vec vector search and duplicate detection. Optimized for simplicity.
- **claude-code-memory** (npm: `claude-code-memory`): Typed memory entries with keyword search, session lifecycle hooks, and consciousness document generation.
- **SQLite Memory Server**: General-purpose SQLite storage exposed via MCP, supporting custom schemas.

### 7.2 Document-Based Solutions

- **Basic Memory** (basicmemory): Markdown file-based memory with bidirectional links, emphasizing human-readable storage.
- **File-based Memory**: Various implementations that persist memories as structured text files, prioritizing simplicity and editability.

### 7.3 Platform-Based Solutions

- **Mem0 / OpenMemory** (mem0ai): Comprehensive memory platform with cloud and self-hosted options, automatic memory extraction, and multi-model support.
- **Zep**: Session memory for AI assistants with built-in summarization and fact extraction.

### 7.4 Graph-Based Solutions

- **Graphiti** (zep-ai): Temporal knowledge graph for AI agents, supporting time-aware queries and relationship evolution.
- **Neo4j MCP**: Exposes Neo4j graph database capabilities through MCP, enabling Cypher queries from AI agents.
- **FalkorDB MCP**: Graph database with MCP integration, supporting property graphs and graph queries.

### 7.5 Vector Database Solutions

- **ChromaDB MCP**: Lightweight vector database with MCP integration, supporting in-memory and persistent storage.
- **LanceDB MCP**: Columnar vector database with MCP integration, optimized for multi-modal data.
- **Qdrant MCP**: High-performance vector database exposed via MCP.
- **Pinecone MCP**: Cloud-native vector database with MCP integration.

### 7.6 Specialized Solutions

- **Knowledge Graph Memory** (modelcontextprotocol): Reference implementation of entity-observation-relation knowledge graphs via MCP.
- **Cline Memory Bank**: Project-specific memory designed for the Cline coding assistant, using structured Markdown documents.
- **RuFlo/RuVector**: Multi-capability MCP server combining memory, agent orchestration, neural patterns, and reinforcement learning.
- **Context7**: Documentation indexing and retrieval service, providing up-to-date library documentation as memory.

### 7.7 Taxonomy Summary

```
Memory Solutions (22 identified)
|
+-- By Storage Model
|   +-- SQLite-based (4): Memento, Dead Simple, claude-memory, SQLite Memory
|   +-- Document-based (2): Basic Memory, File-based
|   +-- Graph-based (3): Graphiti, Neo4j MCP, FalkorDB MCP
|   +-- Vector DB (4): ChromaDB, LanceDB, Qdrant, Pinecone
|   +-- Platform (2): Mem0, Zep
|   +-- Specialized (7): KG Memory, Cline, RuFlo, Context7, others
|
+-- By Deployment Model
|   +-- Local/Offline (14): SQLite-based, document-based, some vector DBs
|   +-- Cloud-required (5): Pinecone, some Mem0 configurations
|   +-- Hybrid (3): Mem0, Zep, Qdrant
|
+-- By Search Capability
    +-- Keyword only (4)
    +-- Vector only (6)
    +-- Hybrid (5)
    +-- Graph traversal (3)
    +-- No search / CRUD only (4)
```

*Figure 4: Taxonomy of open-source memory solutions for AI coding agents.*

---

## 8. Future Work

### 8.1 Cross-Project Memory Transfer with Privacy Controls

The strict project isolation in our current architecture prevents valuable cross-project learning. Future work should explore controlled memory transfer mechanisms that allow a developer to selectively share memories across projects. A privacy-preserving approach might involve:

- Explicit opt-in for cross-project memories
- Automatic redaction of project-specific identifiers
- Memory generalization (e.g., "PostgreSQL connection pools should be sized at 2x CPU cores" rather than "Project X's database uses a pool of 16 connections")

### 8.2 Automated Memory Consolidation

As the knowledge graph grows, automated consolidation becomes essential. We envision a multi-stage consolidation pipeline:

1. **Deduplication:** Identify and merge semantically equivalent memories using embedding similarity.
2. **Pruning:** Remove memories that have not been accessed within a configurable time window.
3. **Summarization:** Compress multiple related observations into concise summaries.
4. **Promotion:** Move frequently accessed Layer 2 memories into Layer 1 (static files) for guaranteed availability.

### 8.3 Memory Importance Scoring

Not all memories are equally valuable. An importance scoring mechanism based on access frequency, recency, and outcome correlation could prioritize memory retrieval and guide consolidation decisions. Memories that are frequently retrieved and associated with successful task outcomes should receive higher importance scores and be preserved longer.

### 8.4 Collaborative Team Memory

Extending the architecture to support team-shared memories---coding conventions, architectural decisions, incident post-mortems---would amplify the benefits across development teams. This requires addressing access control, conflict resolution (when team members record contradictory decisions), and consensus mechanisms.

### 8.5 Benchmarking Framework

The field lacks standardized benchmarks for evaluating agent memory quality. We propose the development of a benchmarking framework that measures:

- **Recall accuracy:** Can the agent retrieve the correct memory given a natural language query?
- **Decision consistency:** Does the agent make consistent decisions across sessions?
- **Context efficiency:** How much developer re-explanation is required per session?
- **Staleness detection:** Can the system identify and flag outdated memories?

### 8.6 Integration with Emerging Standards

As AI coding standards evolve---including developments in MCP, agent-to-agent communication protocols, and standardized tool interfaces---the memory architecture should adapt to leverage new capabilities for richer memory operations.

---

## 9. Conclusion

This paper has presented a multi-layer memory architecture for persistent AI coding agents that addresses the fundamental limitation of session amnesia. By decomposing the memory problem into five complementary layers---static file, structured event, vector-semantic, reinforcement learning, and code structural---we provide a practical framework that covers the full spectrum of knowledge types lost between sessions.

Our architecture is grounded in several key design decisions. First, **layer independence** ensures graceful degradation: each layer functions standalone, and deployments can adopt layers incrementally based on their needs and infrastructure constraints. Second, **offline operation** through SQLite-based storage and local embedding models ensures the architecture is viable in the privacy-sensitive, network-restricted environments common in professional software development. Third, **MCP-based integration** leverages an emerging standard for AI tool communication, ensuring interoperability with the broader ecosystem of development tools.

The practical deployment of this architecture across real-world software engineering projects has demonstrated meaningful improvements in session continuity, decision consistency, and developer experience. While quantitative evaluation remains an area for future work, the qualitative evidence supports the value of multi-layer memory persistence.

The open-source ecosystem analysis reveals a rapidly maturing landscape of memory solutions, with twenty-two identified implementations spanning diverse architectural approaches. Our multi-layer framework synthesizes insights from across this ecosystem, providing a unified architecture that is greater than the sum of its parts.

We believe that memory persistence will become a standard capability of AI coding agents within the next development cycle, much as code completion and inline suggestions became standard in the previous cycle. The framework presented here offers a practical path toward that future---one in which AI agents are true long-term collaborators rather than amnesia-bound assistants that must be re-introduced to the project with each new session.

---

## References

1. Anthropic. (2024). *Model Context Protocol Specification*. https://modelcontextprotocol.io/specification

2. Chen, J., Xiao, S., Zhang, P., Luo, K., Lian, D., & Liu, Z. (2024). BGE M3-Embedding: Multi-Lingual, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation. *arXiv preprint arXiv:2402.03216*.

3. Hogan, A., Blomqvist, E., Cochez, M., d'Amato, C., Melo, G. D., Gutierrez, C., ... & Zimmermann, A. (2021). Knowledge Graphs. *ACM Computing Surveys*, 54(4), 1-37.

4. Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., ... & Kiela, D. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. *Advances in Neural Information Processing Systems*, 33, 9459-9474.

5. Ma, X., Gong, Y., He, P., Zhao, H., & Duan, N. (2024). Query Rewriting in Retrieval-Augmented Large Language Models. *arXiv preprint arXiv:2305.14283*.

6. Packer, C., Wooders, S., Lin, K., Fang, V., Patil, S. G., Stoica, I., & Gonzalez, J. E. (2023). MemGPT: Towards LLMs as Operating Systems. *arXiv preprint arXiv:2310.08560*.

7. sqlite-vec. (2024). A SQLite extension for vector search. https://github.com/asg017/sqlite-vec

8. Mem0. (2024). The Memory Layer for AI Applications. https://github.com/mem0ai/mem0

9. Graphiti. (2024). Build and query dynamic, temporally-aware Knowledge Graphs. https://github.com/getzep/graphiti

10. Xenova/Transformers. (2024). Run Hugging Face Transformers in JavaScript. https://github.com/xenova/transformers.js

11. Malkov, Y. A., & Yashunin, D. A. (2020). Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs. *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 42(4), 824-836.

12. Robertson, S. E., & Zaragoza, H. (2009). The Probabilistic Relevance Framework: BM25 and Beyond. *Foundations and Trends in Information Retrieval*, 3(4), 333-389.

13. Borgeaud, S., Mensch, A., Hoffmann, J., Cai, T., Rutherford, E., Millican, K., ... & Sifre, L. (2022). Improving Language Models by Retrieving from Trillions of Tokens. *International Conference on Machine Learning*, 2206-2240.

14. OpenAI. (2024). Codex CLI. https://github.com/openai/codex

15. Anthropic. (2025). Claude Code: An Agentic Coding Tool. https://docs.anthropic.com/en/docs/claude-code

---

## Appendix A: Memory Layer Selection Guide

For practitioners adopting this framework, we recommend an incremental deployment strategy:

| Stage | Layers | Setup Time | Benefit Level |
|-------|--------|-----------|---------------|
| **Minimal** | Layer 1 only | 5 minutes | Basic: stable conventions persist |
| **Standard** | Layers 1 + 2 | 15 minutes | Good: categorized knowledge persists |
| **Advanced** | Layers 1 + 2 + 3 | 30 minutes | Excellent: semantic recall + knowledge graph |
| **Full** | All 5 layers | 1 hour | Maximum: complete memory persistence |

*Table 2: Incremental deployment stages for the multi-layer memory architecture.*

## Appendix B: Glossary

- **AST**: Abstract Syntax Tree---a tree representation of the syntactic structure of source code
- **BGE-M3**: BAAI General Embedding M3---a multilingual, multi-granularity embedding model
- **BM25**: Best Matching 25---a ranking function used in information retrieval
- **EWC++**: Elastic Weight Consolidation (enhanced)---a continual learning technique
- **FTS5**: Full-Text Search 5---SQLite's full-text search extension
- **HNSW**: Hierarchical Navigable Small World---an algorithm for approximate nearest neighbor search
- **MCP**: Model Context Protocol---Anthropic's standard for AI-tool communication
- **ONNX**: Open Neural Network Exchange---a format for ML model interoperability
- **RAG**: Retrieval-Augmented Generation---augmenting LLM generation with retrieved context
- **SONA**: Self-Organizing Neural Architecture---a pattern learning framework
- **sqlite-vec**: A SQLite extension providing vector similarity search capabilities

---

*Manuscript prepared March 2026. The authors welcome feedback and collaboration at the intersection of AI agent architecture and software engineering practice.*
