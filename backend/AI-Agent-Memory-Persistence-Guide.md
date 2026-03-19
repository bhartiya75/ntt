# The Complete Guide to Persistent Memory for AI Coding Agents (Claude Code)

> **TL;DR:** AI coding agents forget everything between sessions. This guide walks you through a production-tested, multi-layer memory architecture that gives your AI agent persistent context -- from simple markdown files to vector-semantic search and self-improving intelligence layers.

---

## Table of Contents

1. [The Problem](#1-the-problem)
2. [The Solution: Multi-Layer Memory Architecture](#2-the-solution-multi-layer-memory-architecture)
3. [Step-by-Step Setup Guide](#3-step-by-step-setup-guide)
4. [How the Layers Work Together](#4-how-the-layers-work-together)
5. [Best Practices](#5-best-practices)
6. [Comparison Table](#6-comparison-table)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. The Problem

Every developer who has used an AI coding agent has experienced this frustration:

**Session 1:** "We use a monorepo with pnpm workspaces. The API is in `packages/api`, the frontend is in `packages/web`. We use Drizzle ORM with PostgreSQL. Our naming convention is camelCase for variables, PascalCase for components, and we always co-locate tests next to source files..."

**Session 2:** "...Yes, we use pnpm. Yes, it's a monorepo. No, not npm. The API is in `packages/api`... I told you this yesterday."

**Session 47:** *Developer slowly loses will to live.*

This is not a minor inconvenience. It is a fundamental limitation that undermines the promise of AI-assisted development. The problem exists across all major AI coding agents:

| Agent | Memory Mechanism | Persistent? | Limitations |
|-------|-----------------|-------------|-------------|
| **Claude Code** | `CLAUDE.md`, session context | Partial | Static files, no semantic search, size-limited |
| **Cursor** | `.cursorrules`, codebase indexing | Partial | Rules are static, no learning |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Partial | Single file, no structure |
| **Codex** | `AGENTS.md` | Partial | Static instructions only |

Current workarounds share common weaknesses:

- **Static:** They do not learn or evolve with your project
- **Unsearchable:** No semantic understanding, just text matching
- **Manual:** You must write and maintain them yourself
- **Size-limited:** Context windows cannot absorb entire project histories
- **Session-blind:** No concept of "what happened last time"

We can do significantly better.

---

## 2. The Solution: Multi-Layer Memory Architecture

The answer is not a single tool -- it is a layered architecture where each layer handles a different type of memory at a different level of sophistication.

Think of it like the memory hierarchy in a CPU:

```
Layer 5: Code Index (JCodeMunch)         -- "What does my code look like?"
Layer 4: Intelligence Layer (Ruflo)       -- "What worked before?"
Layer 3: Vector-Semantic Memory (Memento) -- "What do I know about X?"
Layer 2: Structured Memory (MCP Memory)   -- "What decisions were made?"
Layer 1: File-Based Memory (CLAUDE.md)    -- "What are the basics?"
```

Each layer is independently useful. You can adopt one, three, or all five. They compose naturally -- each layer fills gaps the others leave.

---

### Layer 1: File-Based Memory (CLAUDE.md / Auto-Memory)

**How it works:** Static markdown files are loaded into the system prompt at the start of every session. This is the simplest form of persistence -- a text file the agent always reads.

**Location:**
```
# Project-level (checked into git, shared with team)
./CLAUDE.md

# User-level project memory (personal preferences per project)
~/.claude/projects/<project-hash>/CLAUDE.md

# Global user memory (applies to all projects)
~/.claude/CLAUDE.md
```

**What goes in CLAUDE.md:**
```markdown
# Project: my-saas-app

## Architecture
- Monorepo managed with pnpm workspaces
- packages/api: Express + Drizzle ORM + PostgreSQL
- packages/web: Next.js 14 (App Router) + Tailwind CSS
- packages/shared: Shared types and utilities

## Conventions
- Use camelCase for variables and functions
- Use PascalCase for React components and types
- Co-locate tests: `MyComponent.test.tsx` next to `MyComponent.tsx`
- Use barrel exports (index.ts) for public module APIs

## Common Commands
- `pnpm dev` -- start all packages in dev mode
- `pnpm test` -- run all tests
- `pnpm db:migrate` -- run database migrations

## Gotchas
- The `users` table has a soft-delete pattern: always filter by `deleted_at IS NULL`
- Environment variables must be prefixed with `NEXT_PUBLIC_` for client-side access
- The CI pipeline requires all tests to pass before merge
```

**Pros:**
- Zero setup -- works out of the box
- Always loaded -- guaranteed to be in context
- Version-controllable -- commit it to git
- Shareable -- team members benefit too

**Cons:**
- Static -- does not update itself
- No search -- just linear text in the prompt
- Manual management -- you write and maintain it
- Size-limited -- roughly 200 lines before it starts consuming too much context
- No structure -- flat text, no types or categories

**When to use:** Always. This is your foundation. Even if you set up every other layer, keep a CLAUDE.md with the essentials.

---

### Layer 2: MCP-Based Structured Memory (claude-code-memory)

**How it works:** This layer uses Claude Code's hooks system to automatically extract learnings at the end of each session and store them as typed, searchable entries. It adds MCP tools that the agent can call to save and retrieve memories.

**Memory Types:**

| Type | Purpose | Example |
|------|---------|---------|
| `decision` | Why X was chosen over Y | "Chose Drizzle over Prisma for edge runtime support" |
| `pattern` | Recurring conventions | "All API routes follow RESTful naming with `/api/v1/` prefix" |
| `gotcha` | Pitfalls and warnings | "The Stripe webhook handler must return 200 within 5 seconds" |
| `architecture` | System structure | "Auth uses JWT with refresh tokens stored in httpOnly cookies" |
| `progress` | What is done / in-flight | "User dashboard: complete. Settings page: in progress" |
| `context` | Business context | "The app serves healthcare providers; HIPAA compliance is required" |

**Available Tools:**

| Tool | Purpose |
|------|---------|
| `memory_save` | Store a new memory with type, content, and tags |
| `memory_recall` | Retrieve all active memories, optionally filtered |
| `memory_search` | Keyword search across memories |
| `memory_ask` | Ask a natural language question, get a synthesized answer |
| `memory_consolidate` | Merge duplicates, remove outdated entries |
| `memory_consciousness` | Generate a full context document from all memories |

**How memories are created:**

Memories can be created in two ways:

1. **Manually by the agent** during a session:
   ```
   Agent calls memory_save({
     type: "decision",
     content: "Switched from REST to tRPC for type-safe API calls between frontend and backend",
     tags: ["api", "architecture", "trpc"]
   })
   ```

2. **Automatically via hooks** at session end:
   The hooks system can trigger memory extraction when a session ends (via `Stop` or `Ctrl+C`), analyzing the conversation for decisions, patterns, and gotchas worth remembering.

**Pros:**
- Structured and typed -- not just raw text
- Searchable by type, tags, and keywords
- Session-aware through hooks
- Consolidation prevents memory bloat
- The `memory_ask` tool provides RAG-like Q&A over your memories

**Cons:**
- No vector/semantic search -- keyword matching only
- Requires MCP server setup
- Memories are per-project (which is often what you want)

---

### Layer 3: Vector-Semantic Memory (Memento MCP)

**How it works:** Memento provides a knowledge graph backed by SQLite, sqlite-vec (vector search), and FTS5 (full-text search). It uses BGE-M3 embeddings to enable true semantic search -- finding related memories even when the exact words differ.

**Core Concepts:**

- **Entities:** Named things (a person, a module, a concept)
- **Observations:** Facts about entities (strings of text attached to an entity)
- **Relations:** Connections between entities ("UserService" --depends_on--> "DatabaseModule")

**Search Architecture:**

Memento uses a hybrid search strategy:

```
Final Score = (0.7 x Vector Similarity) + (0.3 x BM25 Keyword Score)
```

This means:
- Searching for "authentication" will find memories about "login", "auth", "JWT", and "session management"
- Exact keyword matches still get a boost
- You get the best of both worlds

**Example Usage:**

```
# The agent can create entities
create_entities([{
  name: "AuthModule",
  entityType: "module",
  observations: [
    "Handles JWT-based authentication",
    "Uses refresh tokens stored in httpOnly cookies",
    "Located in packages/api/src/auth/"
  ]
}])

# And create relationships
create_relations([{
  from: "AuthModule",
  to: "UserService",
  relationType: "depends_on"
}])

# Later, semantic search finds relevant context
search_nodes("how does login work?")
# Returns: AuthModule with all its observations
```

**Configuration for Claude Code:**

Add to `~/.claude.json` under `mcpServers`:

```json
{
  "mcpServers": {
    "memento": {
      "type": "stdio",
      "command": "npx",
      "args": ["@iachilles/memento@latest"],
      "env": {
        "MEMORY_DB_PATH": "/Users/yourname/.claude/memory-db/memento.db"
      }
    }
  }
}
```

**Pros:**
- True semantic search -- finds related concepts, not just keyword matches
- Knowledge graph -- captures relationships between concepts
- Fully offline -- no API calls, no cloud dependency
- Single-file database -- easy to back up (`cp memento.db memento.db.bak`)
- Hybrid search -- combines vector similarity with keyword matching

**Cons:**
- First load downloads the BGE-M3 embedding model (~400MB)
- Heavier than simple text files
- Requires Node.js 18+
- Knowledge graph requires the agent to create meaningful entities

---

### Layer 4: Intelligence Layer (Ruflo)

**How it works:** Ruflo adds a self-improving intelligence layer on top of memory. It uses HNSW-indexed semantic memory combined with SONA (Self-Organizing Neural Architecture) reinforcement learning to not just remember things, but learn from them.

**Key Components:**

| Component | Purpose |
|-----------|---------|
| `memory_store/retrieve/search` | Semantic memory with HNSW vector index |
| `hooks pre-task/post-task` | Learn from task outcomes (what worked, what failed) |
| `hooks session-start/session-end` | Save and restore full session state |
| `hooks route` | Route tasks to optimal strategies based on learned patterns |
| `hooks intelligence` | SONA reinforcement learning, pattern consolidation |

**How it learns:**

```
1. Pre-task:  "You're about to work on a React component refactor"
              -> Ruflo searches for past patterns, suggests approaches

2. During:    Agent works on the task

3. Post-task: "The refactor succeeded/failed, quality: 0.9"
              -> Ruflo records the outcome, updates its patterns

4. Next time: "Another React refactor? Last time approach X worked well."
              -> Ruflo suggests the proven approach
```

**Session Continuity:**

```
Session End:
  -> Ruflo saves: active tasks, agent states, learned patterns
  -> Everything persists to disk

Next Session Start:
  -> Ruflo restores: picks up where you left off
  -> Tasks, context, patterns all available
```

**Pros:**
- Self-improving -- gets better at routing and suggestions over time
- Session continuity -- full state save/restore
- Pattern learning -- remembers what worked and what did not
- Semantic search with HNSW indexing (fast, even with thousands of entries)
- Agent coordination support (for multi-agent workflows)

**Cons:**
- More complex setup than simpler layers
- Heavier runtime footprint
- Learning requires consistent use to build meaningful patterns
- Best suited for power users and complex projects

---

### Layer 5: Code Index (JCodeMunch)

**How it works:** JCodeMunch parses your codebase using language-specific AST parsers, extracts symbols (functions, classes, methods, types), and creates a searchable index with optional AI-generated summaries.

**This is not memory in the traditional sense** -- it does not remember conversations or decisions. Instead, it gives the agent instant, structured access to your codebase without reading every file.

**Capabilities:**

| Tool | Purpose |
|------|---------|
| `index_folder` / `index_repo` | Parse and index a codebase |
| `search_symbols` | Find functions, classes, methods by name or description |
| `get_file_outline` | See all symbols in a file with signatures |
| `get_symbol` | Get the full source code of a specific symbol |
| `find_references` | Find where a symbol is used across the codebase |
| `find_importers` | Find all files that import from a given file |
| `search_text` | Full-text search across indexed file contents |

**Why it matters for memory:**

Without a code index, the agent must re-discover your codebase structure every session. With JCodeMunch, it can instantly ask "Where is the authentication middleware?" and get a precise answer with file paths and line numbers.

**Pros:**
- Instant codebase knowledge -- no re-exploration needed
- AST-aware -- understands code structure, not just text
- Supports 30+ languages
- Persistent index -- survives between sessions
- AI-generated summaries for each symbol

**Cons:**
- Not a general-purpose memory -- only knows about code
- Index must be refreshed when code changes significantly
- Initial indexing takes time for large codebases

---

## 3. Step-by-Step Setup Guide

### Prerequisites

```bash
# Required
node --version    # Must be 18.0.0 or higher
npm --version     # Comes with Node.js

# Optional (for some MCP servers)
python3 --version # 3.10+ recommended

# Claude Code CLI
claude --version  # Should be installed already
```

---

### Step 1: File-Based Memory (Built-in -- No Setup Needed)

CLAUDE.md is built into Claude Code. No installation required.

**Create your project-level CLAUDE.md:**

```bash
# Navigate to your project root
cd /path/to/your/project

# Create CLAUDE.md
touch CLAUDE.md
```

**Populate it with project essentials:**

```markdown
# Project: [Your Project Name]

## Tech Stack
- [List your primary technologies]

## Architecture
- [Describe your project structure]

## Conventions
- [Your coding conventions]

## Common Commands
- [Key development commands]

## Known Gotchas
- [Things that trip people up]
```

**Create your global CLAUDE.md (optional):**

```bash
# This applies to ALL your projects
mkdir -p ~/.claude
touch ~/.claude/CLAUDE.md
```

```markdown
# Global Preferences

## Coding Style
- I prefer functional programming patterns where practical
- Always use TypeScript strict mode
- Write tests for all public functions

## Communication
- Be concise in explanations
- Show code examples rather than lengthy descriptions
- Ask before making large refactors
```

**Verification:**

Start a new Claude Code session in your project and ask: "What do you know about this project?" The agent should reference information from your CLAUDE.md.

---

### Step 2: Install claude-code-memory

**Install the MCP server:**

```bash
npm install -g claude-code-memory
```

**Configure Claude Code to use it:**

Edit (or create) `~/.claude.json`:

```json
{
  "mcpServers": {
    "memory": {
      "type": "stdio",
      "command": "claude-code-memory",
      "args": ["--memory-dir", "/Users/yourname/.claude/memory"]
    }
  }
}
```

> **Note:** Replace `/Users/yourname` with your actual home directory path.

**Set up hooks for automatic memory extraction:**

Edit `~/.claude/settings.json` to add hooks that trigger memory operations:

```json
{
  "hooks": {
    "SessionStop": [
      {
        "command": "claude-code-memory extract-session",
        "description": "Extract learnings from the completed session"
      }
    ]
  }
}
```

**Verification:**

```
# In a Claude Code session, try:
"Save a memory: We decided to use PostgreSQL instead of MySQL for JSON column support"

# Then in a new session:
"What database are we using and why?"
```

The agent should use `memory_save` and `memory_recall` tools to persist and retrieve this information.

---

### Step 3: Install Memento (Semantic Memory)

**Test that it works:**

```bash
npx @iachilles/memento@latest --help
```

> The first run will download the BGE-M3 embedding model (~400MB). This is a one-time download.

**Create a persistent database directory:**

```bash
mkdir -p ~/.claude/memory-db
```

**Add to your Claude Code MCP configuration:**

Edit `~/.claude.json` and add Memento to `mcpServers`:

```json
{
  "mcpServers": {
    "memory": {
      "type": "stdio",
      "command": "claude-code-memory",
      "args": ["--memory-dir", "/Users/yourname/.claude/memory"]
    },
    "memento": {
      "type": "stdio",
      "command": "npx",
      "args": ["@iachilles/memento@latest"],
      "env": {
        "MEMORY_DB_PATH": "/Users/yourname/.claude/memory-db/memento.db"
      }
    }
  }
}
```

**Verification:**

```
# In a Claude Code session:
"Create a knowledge entity for our AuthModule.
 It handles JWT authentication, uses refresh tokens in httpOnly cookies,
 and is located in packages/api/src/auth/"

# Then search for it:
"What do you know about how login works?"
```

The agent should create an entity via Memento and later find it through semantic search, even though you said "login" and the memory says "authentication."

---

### Step 4: Install Ruflo (Optional -- Advanced)

Ruflo is best suited for power users who work on complex projects daily and want their agent to learn and improve over time.

**Install:**

```bash
npm install -g ruflo
```

**Add to your Claude Code MCP configuration:**

```json
{
  "mcpServers": {
    "ruflo": {
      "type": "stdio",
      "command": "ruflo",
      "args": ["mcp"]
    }
  }
}
```

**Initialize in your project:**

```
# In a Claude Code session:
"Initialize Ruflo for this project with standard hooks"
```

**Verification:**

```
# Start a session
"Start a Ruflo session for this project"

# Work on a task
"Refactor the UserService to use dependency injection"

# End session
"End the Ruflo session, saving all state"

# Next session
"Restore the latest Ruflo session"
# -> Should restore context from the previous session
```

---

### Step 5: Set Up JCodeMunch (Code Index)

**JCodeMunch typically runs as an MCP server. Add it to your configuration:**

```json
{
  "mcpServers": {
    "jcodemunch": {
      "type": "stdio",
      "command": "npx",
      "args": ["jcodemunch-mcp"]
    }
  }
}
```

**Index your project:**

```
# In a Claude Code session:
"Index the current project folder with JCodeMunch"
```

**Verification:**

```
# Search for symbols
"Find all functions related to authentication in the codebase"

# Get file structure
"Show me the file tree of the project"

# Find references
"Where is the validateToken function used?"
```

---

### Step 5 (Alternate): Verify All Layers

After setting up your chosen layers, verify everything works together:

```
# 1. Check CLAUDE.md is loaded
"What project conventions do you know about?"

# 2. Check structured memory
"Recall all memories about architecture decisions"

# 3. Check semantic search (Memento)
"Search your knowledge graph for anything about database design"

# 4. Check intelligence layer (Ruflo)
"What patterns have you learned from previous sessions?"

# 5. Check code index (JCodeMunch)
"Search for all exported functions in the api package"
```

---

## 4. How the Layers Work Together

Here is how a typical session flows with all layers active:

```
SESSION START
  |
  |-- Layer 1: CLAUDE.md loaded into system prompt
  |     "I know this is a pnpm monorepo with Express + Next.js"
  |
  |-- Layer 2: memory_recall loads structured memories
  |     "Previous decisions: chose tRPC, switched to Drizzle ORM"
  |
  |-- Layer 4: Ruflo restores session state
  |     "Last session was working on user dashboard, 70% complete"
  |
  v
DURING WORK
  |
  |-- Layer 3: Memento semantic search for relevant context
  |     User asks about auth -> finds AuthModule entity with relations
  |
  |-- Layer 5: JCodeMunch provides code context
  |     "The validateToken function is in packages/api/src/auth/jwt.ts"
  |
  |-- Layer 4: Ruflo routes tasks based on learned patterns
  |     "This looks like a React refactor. Last time, approach X worked."
  |
  v
TASK COMPLETION
  |
  |-- Layer 4: Ruflo records outcome (success/failure, quality score)
  |     "React refactor succeeded, quality: 0.9, approach: X"
  |
  v
SESSION END
  |
  |-- Layer 2: claude-code-memory extracts session learnings
  |     Saves: decisions, patterns, gotchas discovered during session
  |
  |-- Layer 4: Ruflo saves full session state
  |     Tasks, agent states, patterns all persisted
  |
  |-- Layer 1: Developer updates CLAUDE.md if needed
  |     (manual, but informed by what the agent learned)
  |
  v
NEXT SESSION
  |
  All layers contribute context from the start.
  The agent picks up where it left off.
```

**The key insight:** Each layer handles a different concern:

| Layer | Concern | Question it Answers |
|-------|---------|-------------------|
| CLAUDE.md | Static project facts | "What are the basics?" |
| claude-code-memory | Structured decisions | "What was decided and why?" |
| Memento | Semantic knowledge | "What do I know about topic X?" |
| Ruflo | Learned patterns | "What approach works best for this type of task?" |
| JCodeMunch | Code structure | "Where is this function and who uses it?" |

---

## 5. Best Practices

### What to Store in Each Layer

**CLAUDE.md (Layer 1):**
- Project structure and tech stack
- Coding conventions and style guides
- Common commands and workflows
- Team agreements and standards
- Things that NEVER change or change very rarely

**claude-code-memory (Layer 2):**
- Architecture decisions with reasoning ("chose X because Y")
- Discovered gotchas and pitfalls
- Progress on ongoing work
- Patterns specific to your project
- Business context and domain knowledge

**Memento (Layer 3):**
- Detailed technical knowledge (module responsibilities, API contracts)
- Relationships between system components
- Complex domain concepts that benefit from semantic search
- Information you might search for using different terminology

**Ruflo (Layer 4):**
- Task outcomes and quality assessments
- Session state for continuity
- Routing preferences (which approaches work for which problems)
- Let it learn organically -- do not over-engineer the input

### Preventing Memory Bloat

Memory systems that grow without bounds become useless. Here is how to keep them sharp:

1. **Consolidate regularly:**
   ```
   "Consolidate and deduplicate my memories"
   ```
   This merges duplicate entries, removes outdated information, and keeps memory lean.

2. **Use superseding:**
   When a decision changes, supersede the old memory rather than creating a new one:
   ```
   memory_save({
     type: "decision",
     content: "Switched from REST to tRPC for end-to-end type safety",
     supersedes: "mem_abc123"  // ID of the old "we use REST" memory
   })
   ```

3. **Review periodically:**
   Every few weeks, ask the agent to list all memories and remove anything stale:
   ```
   "List all active memories and flag any that seem outdated"
   ```

4. **Keep CLAUDE.md concise:**
   If your CLAUDE.md exceeds 150 lines, it is too long. Move detailed information to structured memory (Layer 2) or Memento (Layer 3).

### Backup Recommendations

All memory data is stored in local files. Backing up is straightforward:

```bash
# Back up everything
cp -r ~/.claude/memory ~/.claude/memory-backup-$(date +%Y%m%d)
cp ~/.claude/memory-db/memento.db ~/.claude/memory-db/memento.db.bak

# Or add to your dotfiles backup script
rsync -av ~/.claude/ /path/to/backup/claude/
```

For team projects, consider:
- Committing `CLAUDE.md` to git (it is meant to be shared)
- Keeping personal memories in `~/.claude/` (not in git)
- Sharing a team `CLAUDE.md` with project-wide conventions

---

## 6. Comparison Table

| Feature | CLAUDE.md | claude-code-memory | Memento | Ruflo | JCodeMunch |
|---------|-----------|-------------------|---------|-------|------------|
| **Setup Complexity** | None | Low | Medium | High | Medium |
| **Persistence** | File | File | SQLite DB | File + DB | File + DB |
| **Search Type** | None (linear read) | Keyword | Semantic + Keyword | Semantic (HNSW) | AST + Keyword |
| **Auto-learning** | No | Via hooks | No (agent-driven) | Yes (SONA RL) | No |
| **Semantic Search** | No | No | Yes (BGE-M3) | Yes (HNSW) | Partial |
| **Knowledge Graph** | No | No | Yes | No | Yes (AST) |
| **Session Continuity** | No | Partial | No | Yes | No |
| **Self-improving** | No | No | No | Yes | No |
| **Offline** | Yes | Yes | Yes | Yes | Yes |
| **Team Shareable** | Yes (git) | No (personal) | No (personal) | No (personal) | Yes (index) |
| **Size Limit** | ~200 lines | Unlimited | Unlimited | Unlimited | Codebase-sized |
| **Best For** | Basics, conventions | Decisions, progress | Deep knowledge | Learning, routing | Code navigation |

### Recommended Configurations by Use Case

**Solo developer, simple projects:**
- Layer 1 (CLAUDE.md) + Layer 2 (claude-code-memory)
- Low overhead, covers 80% of needs

**Solo developer, complex projects:**
- Layer 1 + Layer 2 + Layer 3 (Memento) + Layer 5 (JCodeMunch)
- Semantic search becomes valuable when projects grow

**Power user / daily AI-assisted development:**
- All five layers
- The investment in Ruflo pays off with consistent daily use

**Team environment:**
- Layer 1 (shared CLAUDE.md in git) + Layer 2 (personal memories)
- Each developer maintains their own structured memories

---

## 7. Troubleshooting

### Common Issues

#### "MCP server failed to start"

**Symptom:** Claude Code shows an error about failing to connect to an MCP server.

**Fix:**
```bash
# Check that the command works directly
npx @iachilles/memento@latest --help

# Check Node.js version
node --version  # Must be 18+

# Check the path in your config
cat ~/.claude.json | python3 -m json.tool

# Common issue: wrong path separator on Windows
# Use forward slashes or double backslashes in JSON paths
```

#### "Memento is slow on first load"

**Symptom:** The first time you use Memento, it takes 30-60 seconds to respond.

**Explanation:** Memento downloads the BGE-M3 embedding model (~400MB) on first use. Subsequent loads use the cached model.

**Fix:** Run `npx @iachilles/memento@latest --help` once before your first real session to trigger the download.

#### "Memories are not persisting between sessions"

**Symptom:** Memories saved in one session are not available in the next.

**Fix:**
```bash
# Check that the memory directory exists
ls -la ~/.claude/memory/

# Check that the Memento DB exists and has data
ls -la ~/.claude/memory-db/memento.db

# Verify your claude.json points to the right paths
cat ~/.claude.json
```

#### "Too many memories -- agent is slow"

**Symptom:** The agent takes a long time to start or respond because it is loading too many memories.

**Fix:**
```
# In a Claude Code session:
"Consolidate my memories, removing duplicates and outdated entries"

# Or manually review:
"List all memories sorted by date, oldest first"
# Then delete stale ones
```

#### "Semantic search returns irrelevant results"

**Symptom:** Memento or Ruflo returns memories that are not related to your query.

**Fix:**
- Be more specific in your queries
- Add more observations to your entities (more context = better embeddings)
- Check that your memories have meaningful content (short, vague memories produce poor embeddings)

#### "Hooks are not triggering"

**Symptom:** Session-end hooks do not extract memories.

**Fix:**
```bash
# Check hooks configuration
cat ~/.claude/settings.json | python3 -m json.tool

# Make sure the hook command is executable
which claude-code-memory

# Check for hook errors in Claude Code logs
# (Hook failures are usually silent)
```

#### "JCodeMunch index is stale"

**Symptom:** Code search returns results that reference deleted or moved files.

**Fix:**
```
# Re-index with incremental mode (only re-indexes changed files)
"Re-index the project folder with JCodeMunch"

# Or force a full re-index
"Invalidate the JCodeMunch cache and re-index from scratch"
```

### Getting Help

- **Claude Code documentation:** https://docs.anthropic.com/en/docs/claude-code
- **MCP specification:** https://modelcontextprotocol.io
- **Memento:** https://github.com/iachilles/memento
- **Ruflo:** Check the npm package page for documentation
- **JCodeMunch:** Check the npm package page for documentation

---

## Final Thoughts

Persistent memory transforms AI coding agents from forgetful assistants into knowledgeable collaborators. The multi-layer approach described here is not theoretical -- it is a practical architecture that you can adopt incrementally.

Start with CLAUDE.md. It costs nothing and provides immediate value. Add structured memory when you find yourself repeating decisions. Layer in semantic search when your project knowledge becomes too complex for keyword matching. And if you are pushing the boundaries of AI-assisted development daily, the intelligence layer will reward your investment.

The gap between "AI that forgets" and "AI that remembers" is the gap between a tool and a partner. Close it.

---

*This guide was written from hands-on experience setting up and using multi-layer memory systems with Claude Code. Contributions, corrections, and improvements are welcome.*

*Last updated: March 2026*
