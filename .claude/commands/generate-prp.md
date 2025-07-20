# Create PRP

## Feature file: $ARGUMENTS

Generate a complete PRP for general feature implementation with thorough research. Ensure context is passed to the AI agent to enable self-validation and iterative refinement. Read the feature file first to understand what needs to be created, how the examples provided help, and any other considerations.

The AI agent only gets the context you are appending to the PRP and training data. Assume the AI agent has access to the codebase and the same knowledge cutoff as you, so its important that your research findings are included or referenced in the PRP. The Agent has Websearch capabilities, so pass urls to documentation and examples.

## Pre-Research: MCP Context Loading

1. **Memory Bank Check**
   - Use `mcp__memory-bank__read_memory_bank_file("active-context")` to understand current project state
   - Check `mcp__memory-bank__read_memory_bank_file("system-patterns")` for existing patterns
   - Review `mcp__memory-bank__read_memory_bank_file("decision-log")` for architectural decisions

2. **Knowledge Graph Search**
   - Use `mcp__knowledge-graph__search_nodes("{feature-keywords}")` to find related concepts
   - Check for existing components that could be extended

## Research Process

1. **Codebase Analysis & DRY Pattern Discovery**
   - **DRY Search Strategy**: Before designing new code, search for reusable patterns
     - Local pattern search: `rg "[functionality] OR [pattern]" src/ --type py`
     - External pattern mining: `{"query": "[feature] implementation", "language": ["Python", "TypeScript"]}`
     - Utility pattern discovery: `{"query": "utility OR helper", "language": ["Python"], "path": ["utils/", "lib/"]}`
   - **Code Reuse Opportunity Assessment**:
     - Search for similar business logic that can be extended
     - Identify common validation patterns that can be shared
     - Find database operations that can use repository pattern
     - Locate configuration patterns for centralization
   - **Anti-Duplication Analysis**:
     - Document existing patterns to prevent recreation
     - Note configuration sources to avoid duplication
     - Identify test utilities that can be reused
     - Map shared functionality for extension opportunities
   - Compare local vs external patterns for optimization opportunities
   - Identify files to reference in PRP (include file:line_number format)
   - Note existing conventions to follow and external best practices discovered
   - Check test patterns for validation approach using both local and Grep MCP searches
   - **CRITICAL**: Verify code optimization opportunities per CLAUDE.md using LEVER framework with external validation

2. **Mock Data & Database Research** (MANDATORY)
   - Identify data models and database schema requirements
   - Research existing test data patterns in the codebase
   - Plan SQLite schema and migration strategy
   - Design mock data factories for all entities
   - Document data relationships and constraints
   - Plan fixture organization and scenarios
   - Consider performance testing data volumes

3. **Test Strategy Research** (MANDATORY - TDD)
   - Identify existing test patterns in `/tests` or relevant test directories
   - **Use Grep MCP to discover external testing patterns**:
     - TDD examples: `{"query": "test-driven OR tdd", "language": ["Python"], "path": ["tests/", "test/"]}`
     - Database testing: `{"query": "pytest database OR sqlalchemy test", "language": ["Python"]}`
     - Mock strategies: `{"query": "mock OR fixture OR factory", "language": ["Python"], "path": ["tests/"]}`
     - Agent testing: `{"query": "agent test OR langgraph test", "language": ["Python"]}`
   - Document test structure that mirrors app structure (validate with external examples)
   - Plan for: Happy path, Edge cases, Failure cases, Property-based tests
   - Include specific test examples with expected outcomes (from both local and external research)
   - Design database fixtures and test data scenarios using discovered best practices
   - Plan test isolation strategy (transactions, cleanup) based on proven patterns
   - Mock external dependencies and services following industry standards

4. **External Research with MCP Tools**
   - Use `mcp__perplexity-ask__perplexity_ask` for latest documentation and best practices
   - **Use Grep MCP for GitHub pattern mining**:
     - Architecture research: `{"query": "langgraph OR multi-agent", "language": ["Python"], "path": ["src/", "lib/"]}`
     - Database patterns: `{"query": "sqlalchemy alembic", "language": ["Python"], "path": ["models/", "db/"]}`
     - Testing strategies: `{"query": "pytest factory-boy", "language": ["Python"], "path": ["tests/", "test/"]}`
     - Mock data patterns: `{"query": "faker factory", "language": ["Python"], "useRegexp": true}`
     - Performance optimizations: `{"query": "optimization OR performance", "language": ["Python"]}`
   - Search for implementation examples with specific version compatibility
   - Document library quirks, version issues, and gotchas from both Perplexity and Grep research
   - Include specific URLs with section anchors (e.g., `#configuration`)
   - Cross-reference Perplexity documentation with Grep implementation examples
   - Find SQLAlchemy/Alembic patterns for the specific use case using both research methods
   - Look up Factory Boy or similar library documentation and real-world usage patterns

5. **User Clarification** (if needed)
   - Specific patterns to mirror and where to find them?
   - Integration requirements and where to find them?
   - Performance requirements or constraints?
   - Data volume expectations for testing?
   - Specific compliance requirements for test data?

## PRP Generation

Using PRPs/templates/prp_base.md as template:

### Project Structure Requirements (MANDATORY)
- **ALL code MUST be created within `/workspaces/hackathon_demo/use-case`**
- Include explicit directory structure in the PRP showing full paths
- Remind in each task that files go in the use-case directory

### Critical Context to Include and pass to the AI agent as part of the PRP
- **Documentation**: URLs with specific sections and anchors
- **Code Examples**: Real snippets from codebase with file:line_number references
- **Gotchas**: Library quirks, version issues in problem-solution format
- **Patterns**: Existing approaches to follow with explicit file references
- **CLAUDE.md Rules**: Explicitly reference which rules apply to this feature
- **Database Setup**: SQLite configuration, migration scripts, schema definitions
- **Mock Data Patterns**: Factory definitions, fixture files, data builders
- **Test Data Scenarios**: Comprehensive list of test cases with expected data

### Test-First Implementation Blueprint (TDD MANDATORY)
- **Task ordering MUST follow**: Database setup → Mock data → Write test → Run (fail) → Implement → Run (pass) → Refactor
- Start with database schema and migration setup
- Create mock data factories before writing tests
- Include test database fixtures and scenarios
- Start with test file creation for each component
- Include specific test examples with assertions
- Reference real test patterns from the codebase
- Include error handling test cases
- List tasks in TDD order (test tasks before implementation tasks)
- Ensure test data cleanup and isolation

### MCP Integration During Implementation
Include these MCP usage patterns in the PRP:
- Start: `mcp__memory-bank__read_memory_bank_file("active-context")`
- During: `mcp__memory-bank__track_progress("task", "details")`
- Decisions: `mcp__memory-bank__log_decision("title", "context", "decision")`
- Research: `mcp__perplexity-ask__perplexity_ask` for latest docs
- Testing: `mcp__ide__getDiagnostics()` before running tests
- End: `mcp__memory-bank__update_active_context(tasks=[...], nextSteps=[...])`

### Validation Gates (Must be Executable)
```bash
# For Python projects:
# Database Setup Validation
python -m alembic upgrade head
pytest tests/test_database_setup.py -v

# Mock Data Validation
pytest tests/test_mock_data_generation.py -v
pytest tests/test_fixtures.py -v

# Syntax/Style
ruff check src/ tests/ --fix
mypy src/ tests/

# Unit Tests with coverage
pytest tests/unit/ -v --cov=src --cov-report=term-missing

# Integration Tests
pytest tests/integration/ -v

# Database Cleanup
pytest tests/test_cleanup.py -v

# For JavaScript/TypeScript projects:
# npm run lint
# npm run type-check
# npm test
```

*** CRITICAL AFTER YOU ARE DONE RESEARCHING AND EXPLORING THE CODEBASE BEFORE YOU START WRITING THE PRP ***

*** ULTRATHINK ABOUT THE PRP AND PLAN YOUR APPROACH THEN START WRITING THE PRP ***

## PRP Validation (Before Saving)

### CLAUDE.md Compliance Check
- [ ] TDD approach enforced (tests before implementation)
- [ ] MCP tools integrated throughout the workflow
- [ ] Code location set to `/workspaces/hackathon_demo/use-case`
- [ ] Module organization follows project standards
- [ ] Testing requirements meet coverage targets (80% min)
- [ ] Frontend/optimization principles referenced if applicable
- [ ] Mock data generation implemented with factories
- [ ] SQLite database configured for development/testing
- [ ] Test isolation and cleanup strategies defined
- [ ] No real PII in test data (GDPR compliance)
- [ ] **DRY Principles Applied**: All repeated code patterns identified and utilities planned
- [ ] **Code Reuse Strategy**: Existing patterns extended instead of creating new code
- [ ] **Single Source of Truth**: Configuration and constants centralized
- [ ] **Shared Utilities**: Common functionality extracted to reusable modules

### Context Completeness
- [ ] All research findings included or referenced
- [ ] Test examples with expected outcomes provided
- [ ] Error handling patterns documented
- [ ] Performance requirements specified
- [ ] Gotchas documented in problem-solution format
- [ ] Database schema and migrations defined
- [ ] Mock data factories and builders specified
- [ ] Test data scenarios comprehensively listed
- [ ] Data cleanup and isolation strategies documented

## Output
Save as: `PRPs/{feature-name}.md`

## Quality Metrics

### Scoring Rubric (1-10)
- **10**: All checklists complete, comprehensive test coverage planned, clear TDD task ordering
- **8-9**: Minor gaps in context, but core implementation path clear
- **6-7**: Some research needed during implementation, but feasible
- **4-5**: Significant gaps requiring AI to search/research during implementation
- **1-3**: Insufficient context for one-pass implementation

### Final Checklist
- [ ] All necessary context included with specific references
- [ ] Validation gates are executable by AI
- [ ] Test-first approach clearly defined
- [ ] References existing patterns with file:line format
- [ ] Clear implementation path with TDD ordering
- [ ] Error handling and edge cases documented
- [ ] MCP usage integrated throughout
- [ ] Project structure rules enforced

Score: [X/10] - Justify your score based on the rubric above

Remember: The goal is one-pass implementation success through comprehensive context. A PRP scoring below 7 should be enhanced with more research before saving.