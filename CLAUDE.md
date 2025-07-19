### 🧪 Test-Driven Development (TDD) - MANDATORY
- **Red-Green-Refactor**: Write failing test → Make it pass → Refactor. NO EXCEPTIONS.
- **Test First, Always**: Every feature, every bug fix, every refactor starts with a test.
- **Chicago School TDD**: Test behavior, not implementation
  - Focus on public APIs and outcomes
  - Use real objects when possible, mock only external dependencies
- **London School TDD**: Isolate units with mocks/stubs
  - Test interactions between objects
  - Mock all dependencies for true isolation
- **Coverage Requirements**: Minimum 80%, target 95%
- **Every task iteration MUST have tests** before implementation

### 🔌 MCP Server Integration - MANDATORY
- **Memory Bank MCP**: Maintain cross-session project context and progress tracking
  - Use `mcp__memory-bank__read_memory_bank_file` to access: product-context, active-context, progress, decision-log, system-patterns
  - Use `mcp__memory-bank__track_progress` after completing significant work
  - Use `mcp__memory-bank__update_active_context` to sync tasks and next steps
  - Use `mcp__memory-bank__log_decision` for architectural and design choices
- **Knowledge Graph MCP**: Build persistent knowledge repositories for complex projects
  - Use `mcp__knowledge-graph__create_entities` to capture key concepts, components, and relationships
  - Use `mcp__knowledge-graph__search_nodes` to find relevant information across sessions
  - Use `mcp__knowledge-graph__add_observations` to update understanding over time
- **Playwright MCP**: Automate web interactions and testing
  - Use `mcp__playwright__browser_navigate` + `mcp__playwright__browser_snapshot` for web testing
  - Use `mcp__playwright__browser_click` + `mcp__playwright__browser_type` for form automation
  - Always take snapshots before interactions to understand page state
- **Perplexity MCP**: Access real-time information and research
  - Use `mcp__perplexity-ask__perplexity_ask` for current events, latest documentation, and research
  - Particularly valuable for checking latest framework versions and API changes
- **IDE MCP**: Enhance code analysis and execution
  - Use `mcp__ide__getDiagnostics` to identify code issues before running tests
  - Use `mcp__ide__executeCode` for Jupyter notebook interactions and data analysis

### 🔄 Project Awareness & Context
- **Always read `PLANNING.md`** at the start to understand architecture and constraints.
- **Check `TASK.md`** before starting any work. Add tasks with dependencies and test requirements.
- **Use Memory Bank MCP** to maintain context across sessions - read active-context at start, update progress at end.
- **Use venv_linux** for all Python commands.

### 📁 Use-Case Project Location - MANDATORY
- **ALL use-case projects MUST be created within `/workspaces/hackathon_demo/use-case`** folder.
- **NEVER create project files outside this directory** - this includes:
  - Source code (`src/`, `backend/`, `frontend/`)
  - Test files (`tests/`, `test/`, `__tests__/`)
  - Configuration files (`package.json`, `requirements.txt`, etc.)
  - Documentation (`README.md`, `docs/`)
  - Build artifacts (`dist/`, `build/`, `.next/`)
  - Examples and demos (`examples/`, `demo/`)
  - Any other project-related files or folders
- **Full project tree structure** must be contained within `/workspaces/hackathon_demo/use-case`
- **Absolute path enforcement**: Always use the full path when creating directories or files

### 🧹 Preventing Context Rot
- **MCP-Enhanced Context Management**: 
  - **Session Start**: Read Memory Bank active-context, check Knowledge Graph for relevant entities
  - **During Work**: Update Memory Bank progress, create Knowledge Graph entities for new concepts
  - **Session End**: Update Memory Bank with next steps, log key decisions
- **Frequent State Checks**: Re-read key files periodically, verify before editing, use git status/diff
- **Explicit Documentation**: Update PLANNING.md/TASK.md immediately, add inline comments for decisions
- **Modular Context**: Keep files focused, maintain structure diagram, use full paths in docs
- **Verification Pattern**: Read → Understand → Plan → Execute → Verify → Test → Document → Update MCP
- **Session Boundaries**: Start with PLANNING/TASK review, end with summary, never assume old context
- **Search Before Assuming**: Use grep/search tools, cross-reference dependencies, verify imports exist

### 🧱 Code Structure & Modularity
- **500 line limit per file** - refactor if approaching.
- **Module organization** by feature:
  - `agent.py` - Main logic
  - `tools.py` - Tool functions
  - `prompts.py` - System prompts
- **Use relative imports** within packages.
- **Use python_dotenv** for environment variables.

### 🚀 Code Optimization
- **Refer to `docs/optimization-principles.md`** for LEVER framework and optimization strategies
- **Before creating new code**: Check if existing code can be extended (>50% reduction target)
- **Three-Pass Approach**: Discovery → Design → Implementation
- **Extend don't create**: Add fields to existing tables, enhance queries, reuse components
- **Apply scoring system**: Use extend vs create decision matrix before implementation

### 🎨 Frontend Design & Architecture
- **Refer to `docs/front-end-optimization-principles.md`** for comprehensive frontend guidelines
- **Core principles**: 4 font sizes, 2 weights, 8pt grid, 60/30/10 color rule
- **Modern stack**: shadcn/ui, Tailwind v4, Radix UI, variable fonts (Inter/Geist)
- **Performance targets**: LCP < 2.5s, INP < 200ms, CLS < 0.1
- **Accessibility first**: WCAG 2.2 compliance, keyboard navigation, screen reader support

### ✅ Testing & Quality
- **MCP-Enhanced Testing Workflow**:
  - Use `mcp__ide__getDiagnostics` before writing tests to identify potential issues
  - Use `mcp__playwright__browser_snapshot` for visual regression testing of web components
  - Use `mcp__perplexity-ask__perplexity_ask` to research latest testing best practices
- **Test structure mirrors app structure** in `/tests`.
- **Minimum test coverage**:
  - Happy path test
  - Edge case test
  - Failure case test
  - Property-based tests for complex logic
- **Parameterized tests** for similar cases.
- **Run tests before every commit**.

### 🔒 Security & Error Handling
- **Never commit secrets** - use environment variables.
- **Validate all inputs** at boundaries.
- **Structured logging** with appropriate levels.
- **Never silence exceptions** without logging.
- **Handling .env files** Never edit or change the .env files yourself. Always prompt the user if you need to access .env files under very special circumstances, such as, when you need the secrets, api keys or passwords to create and test use cases, and even in this case, you are only permitted to read .env files, never edit or change. If you need to add additional secrets, pause, and prompt the user to add those for you before continuing. 

### 📎 Style & Conventions
- **Python with PEP8**, type hints, format with `black`.
- **Pydantic** for validation, **FastAPI** for APIs.
- **Google-style docstrings**:
  ```python
  def example(param: str) -> bool:
      """Brief summary.
      
      Args:
          param: Description.
          
      Returns:
          Description.
      """
  ```

### 🚀 Git & Deployment
- **Feature branches** with descriptive names.
- **Conventional commits**: `feat:`, `fix:`, `docs:`, etc.
- **No commits without passing tests**.
- **Update README.md** for new features or setup changes.

### 🧠 AI Behavior Rules
- **MCP-First Approach**: Always consider which MCP tools can enhance the current task
- **Ask questions** when context is missing.
- **Verify existence** of files/modules before use.
- **Never delete code** unless instructed or in TASK.md.
- **Comment complex logic** with `# Reason:` explanations.

### 💡 MCP Usage Examples & Best Practices

#### Memory Bank Workflow:
```
Session Start: mcp__memory-bank__read_memory_bank_file("active-context")
During Work: mcp__memory-bank__track_progress("Implemented user auth", "Added JWT validation and middleware")
Session End: mcp__memory-bank__update_active_context(tasks=["Fix auth tests"], nextSteps=["Add password reset"])
```

#### Knowledge Graph for Architecture:
```
New Feature: mcp__knowledge-graph__create_entities([{name: "UserService", entityType: "service", observations: ["Handles authentication", "Uses JWT tokens"]}])
Research: mcp__knowledge-graph__search_nodes("authentication")
Update: mcp__knowledge-graph__add_observations([{entityName: "UserService", contents: ["Added password hashing with bcrypt"]}])
```

#### Playwright for E2E Testing:
```
Test Setup: mcp__playwright__browser_navigate("http://localhost:3000/login")
Visual Check: mcp__playwright__browser_snapshot()
Interaction: mcp__playwright__browser_type("login form email field", ref="...", text="test@example.com")
Validation: mcp__playwright__browser_click("submit button", ref="...")
```

#### Perplexity for Research:
```
Framework Updates: mcp__perplexity-ask__perplexity_ask([{role: "user", content: "Latest Next.js 15 breaking changes and migration guide"}])
Best Practices: mcp__perplexity-ask__perplexity_ask([{role: "user", content: "React 19 concurrent features best practices 2024"}])
```

#### IDE Integration:
```
Code Health: mcp__ide__getDiagnostics() # Before implementing features
Jupyter Work: mcp__ide__executeCode("import pandas as pd; df.head()") # For data analysis tasks
```