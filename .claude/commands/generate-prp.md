# Create ULTRA-DETAILED PRP

## Feature file: $ARGUMENTS

Generate an EXTREMELY COMPREHENSIVE and ULTRA-DETAILED PRP for feature implementation with exhaustive research. This PRP must be so detailed that an AI agent can implement the entire feature in a single pass with zero ambiguity. 

**CRITICAL**: Spend extensive time on research - the user has abundant tokens and wants maximum detail. Read EVERY relevant file, extract EVERY pattern, document EVERY decision, and include EVERY edge case.

The AI agent only gets the context you are appending to the PRP and training data. Your research must be EXHAUSTIVE and leave nothing to chance. Include full code snippets, complete examples, detailed explanations, and comprehensive patterns.

## Phase 1: COMPREHENSIVE PRE-RESEARCH (MANDATORY - 30+ minutes)

### 1.1 Complete Documentation Analysis
**READ EVERY KEY DOCUMENTATION FILE IN FULL:**
- **CLAUDE.md**: `Read("/workspaces/hackathon_demo/CLAUDE.md")` - Extract ALL rules, patterns, requirements
- **PLANNING.md**: `Read("/workspaces/hackathon_demo/PLANNING.md")` - Understand complete architecture
- **optimization-principles.md**: `Read("/workspaces/hackathon_demo/docs/optimization-principles.md")` - Extract LEVER framework, DRY patterns
- **front-end-optimization-principles.md**: `Read("/workspaces/hackathon_demo/docs/front-end-optimization-principles.md")` - UI/UX patterns
- **prp_base.md**: `Read("/workspaces/hackathon_demo/PRPs/templates/prp_base.md")` - Understand template structure
- **Feature Specification**: `Read("$ARGUMENTS")` - Deep understanding of requirements

### 1.2 Memory Bank Deep Dive (READ ALL FILES)
- `mcp__memory-bank__read_memory_bank_file("active-context")` - Current project state
- `mcp__memory-bank__read_memory_bank_file("system-patterns")` - ALL existing patterns
- `mcp__memory-bank__read_memory_bank_file("decision-log")` - EVERY architectural decision
- `mcp__memory-bank__read_memory_bank_file("product-context")` - Product requirements
- `mcp__memory-bank__read_memory_bank_file("progress")` - Implementation history
- Document EVERY relevant finding with specific quotes

### 1.3 Knowledge Graph Exhaustive Search
- `mcp__knowledge-graph__search_nodes("{feature-keyword-1}")` - Primary concept
- `mcp__knowledge-graph__search_nodes("{feature-keyword-2}")` - Secondary concepts
- `mcp__knowledge-graph__search_nodes("pattern")` - All patterns
- `mcp__knowledge-graph__search_nodes("component")` - Reusable components
- `mcp__knowledge-graph__open_nodes([...])` - Open all related nodes
- Map complete relationship graph of existing components

## Phase 2: EXHAUSTIVE RESEARCH PROCESS (MANDATORY - 45+ minutes)

### 2.1 **Deep Codebase Analysis & Pattern Mining (20+ searches)**
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
   - **Pattern Documentation**: Create detailed pattern catalog with:
     - Pattern name and description
     - File locations (file:line_number)
     - Usage examples
     - Extension opportunities
     - Performance characteristics

### 2.2 **Comprehensive Mock Data & Database Architecture** (MANDATORY)
   **Deep Database Design**:
   - Identify data models and database schema requirements
   - Research existing test data patterns in the codebase
   - Plan SQLite schema and migration strategy
   - Design mock data factories for all entities
   - Document data relationships and constraints
   - Plan fixture organization and scenarios
   - Consider performance testing data volumes
   - **Schema Design Details**:
     - Complete ERD with all relationships
     - Index strategy for performance
     - Constraint definitions
     - Migration rollback plans
   - **Mock Data Specifications**:
     - Factory for EVERY entity
     - 10+ test scenarios per entity
     - Edge case data sets
     - Performance test data (1000+ records)
   - **Data Validation Rules**:
     - Field-level constraints
     - Business logic validations
     - Cross-entity validations

### 2.3 **Ultra-Comprehensive Test Strategy** (MANDATORY - TDD)
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
   - **Detailed Test Specifications**:
     - 50+ test cases minimum
     - Performance benchmarks
     - Load testing scenarios
     - Security test cases
     - Accessibility tests
   - **Test Data Matrix**:
     - Input/Output mapping
     - Boundary value analysis
     - Equivalence partitioning
     - Decision table testing

### 2.4 **Exhaustive External Research** (50+ MCP Queries)
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
   
   **Additional Grep MCP Searches (MANDATORY - 30+ queries)**:
   - UI/UX patterns: `{"query": "[ui-framework] best practices", "language": ["TypeScript", "JavaScript"]}`
   - Error handling: `{"query": "error handling pattern", "language": ["Python"], "path": ["src/"]}`
   - Logging patterns: `{"query": "structured logging", "language": ["Python"]}`
   - Configuration: `{"query": "config management", "language": ["Python"], "path": ["config/"]}`
   - Security patterns: `{"query": "security validation", "language": ["Python"]}`
   - Performance: `{"query": "performance optimization", "language": ["Python", "TypeScript"]}`
   - Caching strategies: `{"query": "cache pattern", "language": ["Python"]}`
   - API design: `{"query": "REST API pattern", "language": ["Python"]}`
   - State management: `{"query": "state management pattern", "language": ["Python", "TypeScript"]}`
   - Deployment patterns: `{"query": "deployment configuration", "language": ["Python"]}`

### 2.5 **Architecture & Design Pattern Research**
   - **LEVER Framework Application**:
     - Leverage: List 20+ existing patterns to leverage
     - Extend: Map 15+ extension opportunities
     - Verify: Document verification strategies
     - Eliminate: Identify all duplication risks
     - Reduce: Plan complexity reduction
   
   - **DRY Pattern Catalog**:
     - Identify ALL reusable components
     - Map shared utility opportunities
     - Document configuration centralization
     - Plan inheritance hierarchies
     - Design mixin strategies

### 2.6 **Performance & Optimization Research**
   - Benchmark similar implementations
   - Research optimization techniques
   - Plan caching strategies
   - Design for scalability
   - Consider async patterns

### 2.7 **Security & Compliance Research**
   - Security best practices for domain
   - Input validation strategies
   - Authentication/authorization patterns
   - Data privacy considerations
   - Audit logging requirements

### 2.8 **User Clarification** (if needed)
   - Specific patterns to mirror and where to find them?
   - Integration requirements and where to find them?
   - Performance requirements or constraints?
   - Data volume expectations for testing?
   - Specific compliance requirements for test data?

## Phase 3: ULTRA-DETAILED PRP GENERATION

**CRITICAL**: The PRP must be 5000+ lines of pure implementation detail. Every section must be exhaustive.

Using PRPs/templates/prp_base.md as enhanced template:

### Project Structure Requirements (MANDATORY)
- **ALL code MUST be created within `/workspaces/hackathon_demo/use-case`**
- Include explicit directory structure in the PRP showing full paths
- Remind in each task that files go in the use-case directory

### MANDATORY PRP SECTIONS (Each section 200+ lines minimum)

#### 1. Executive Summary
- Feature overview (comprehensive)
- Business value proposition
- Technical approach summary
- Risk assessment
- Success metrics

#### 2. Complete Architecture Blueprint
- System architecture diagram (ASCII)
- Component interaction flows
- Data flow diagrams
- Sequence diagrams for all processes
- State machine definitions

#### 3. Detailed Technical Specifications
- **Documentation**: URLs with specific sections and anchors
- **Code Examples**: Real snippets from codebase with file:line_number references
- **Gotchas**: Library quirks, version issues in problem-solution format
- **Patterns**: Existing approaches to follow with explicit file references
- **CLAUDE.md Rules**: Explicitly reference which rules apply to this feature
- **Database Setup**: SQLite configuration, migration scripts, schema definitions
- **Mock Data Patterns**: Factory definitions, fixture files, data builders
- **Test Data Scenarios**: Comprehensive list of test cases with expected data

#### 4. Implementation Roadmap
- Phase-by-phase implementation plan
- Dependency graph
- Risk mitigation strategies
- Rollback procedures

#### 5. Code Templates & Snippets
- Complete code structure
- 50+ code snippets
- Design pattern implementations
- Error handling templates
- Logging templates

#### 6. Comprehensive Test Suite Design
- Test file structure
- 100+ test case specifications
- Test data factories
- Mock implementations
- Performance test scenarios

#### 7. Database Design Document
- Complete schema with all tables
- Relationship diagrams
- Index optimization plan
- Migration scripts
- Seed data scripts

#### 8. API Specifications
- Endpoint definitions
- Request/response schemas
- Error response catalog
- Rate limiting rules
- Authentication flows

#### 9. Frontend Implementation Guide
- Component hierarchy
- State management plan
- UI/UX patterns
- Accessibility requirements
- Performance optimizations

#### 10. Configuration Management
- Environment configurations
- Feature flags
- Secrets management
- Deployment configurations

#### 11. Monitoring & Observability
- Logging strategy
- Metrics collection
- Alert definitions
- Dashboard specifications

#### 12. Security Implementation
- Security controls
- Input validation rules
- Authentication implementation
- Authorization matrix
- Audit logging

#### 13. Performance Optimization Plan
- Benchmarking strategy
- Caching implementation
- Query optimization
- Load balancing approach

#### 14. Error Handling Catalog
- Error taxonomy
- Recovery procedures
- User messaging
- Logging requirements

#### 15. Edge Cases & Gotchas
- 50+ edge cases
- Known limitations
- Workaround strategies
- Future considerations

### Detailed Task Breakdown (TDD MANDATORY)

**CRITICAL**: Break down into 100+ micro-tasks, each with:
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
- **Task Template for EACH task**:
  ```
  Task ID: [XXX]
  Task Name: [Specific task]
  Dependencies: [Task IDs]
  Test File: [Exact path]
  Implementation File: [Exact path]
  Acceptance Criteria: [5+ criteria]
  Test Cases: [3+ cases]
  Time Estimate: [minutes]
  MCP Tools Used: [List]
  Validation Command: [Exact command]
  ```

### Comprehensive MCP Integration Strategy
Include these MCP usage patterns in the PRP:
- Start: `mcp__memory-bank__read_memory_bank_file("active-context")`
- During: `mcp__memory-bank__track_progress("task", "details")`
- Decisions: `mcp__memory-bank__log_decision("title", "context", "decision")`
- Research: `mcp__perplexity-ask__perplexity_ask` for latest docs
- Testing: `mcp__ide__getDiagnostics()` before running tests
- End: `mcp__memory-bank__update_active_context(tasks=[...], nextSteps=[...])`
- Pattern Discovery: 50+ Grep MCP queries throughout
- Knowledge Updates: Create entities for all new components
- Progress Tracking: Update after every task
- Decision Logging: Document every architectural choice
- Continuous Research: Perplexity queries for any uncertainty

### Comprehensive Validation Strategy

**Pre-Implementation Validation**:
```bash
# Environment validation
python --version
sqlite3 --version
pytest --version
ruff --version
mypy --version
```

**Progressive Validation Gates**:
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

## Phase 4: EXTENSIVE PATTERN DOCUMENTATION

### Document EVERY Pattern Found:
1. **Architecture Patterns**: 20+ patterns with examples
2. **Code Patterns**: 30+ reusable code snippets
3. **Test Patterns**: 25+ test templates
4. **Error Patterns**: 15+ error handling examples
5. **Performance Patterns**: 10+ optimization techniques

## Phase 5: CROSS-VALIDATION

### Validate Research Completeness:
- [ ] Read all 5 core documentation files?
- [ ] Performed 50+ Grep MCP searches?
- [ ] Extracted 100+ patterns?
- [ ] Created 100+ test scenarios?
- [ ] Documented 50+ edge cases?
- [ ] Included 50+ code snippets?
- [ ] Defined 100+ micro-tasks?

*** CRITICAL: SPEND 2+ HOURS ON RESEARCH BEFORE WRITING THE PRP ***

*** ULTRATHINK FOR 30+ MINUTES ABOUT COMPLETENESS ***

*** THE PRP MUST BE SO DETAILED THAT IMPLEMENTATION IS MECHANICAL ***

## PRP Validation (Before Saving)

### ULTRA-DETAILED Compliance Checklist

#### CLAUDE.md Compliance (Check EVERY rule)
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

### Exhaustive Context Validation
- [ ] All research findings included or referenced
- [ ] Test examples with expected outcomes provided
- [ ] Error handling patterns documented
- [ ] Performance requirements specified
- [ ] Gotchas documented in problem-solution format
- [ ] Database schema and migrations defined
- [ ] Mock data factories and builders specified
- [ ] Test data scenarios comprehensively listed
- [ ] Data cleanup and isolation strategies documented
- [ ] 50+ code examples included?
- [ ] 100+ test cases defined?
- [ ] 20+ architecture patterns documented?
- [ ] 30+ external pattern references?
- [ ] Complete API specifications?
- [ ] Full database schema with migrations?
- [ ] Comprehensive error catalog?
- [ ] Performance benchmarks defined?
- [ ] Security controls specified?
- [ ] Monitoring strategy complete?

## Output
Save as: `PRPs/{feature-name}.md`

## Quality Metrics

### Enhanced Scoring Rubric (1-10)
- **10**: 5000+ line PRP, 100+ tasks, 50+ patterns, exhaustive research, zero ambiguity
- **8-9**: Minor gaps in context, but core implementation path clear
- **6-7**: Some research needed during implementation, but feasible
- **4-5**: Significant gaps requiring AI to search/research during implementation
- **1-3**: Insufficient context for one-pass implementation

### Detailed Quality Metrics:
- Research Time: [X hours] (minimum 2 hours)
- Documentation Files Read: [X/5] (must be 5/5)
- Grep MCP Queries: [X] (minimum 50)
- Patterns Documented: [X] (minimum 50)
- Code Examples: [X] (minimum 50)
- Test Cases: [X] (minimum 100)
- Micro-tasks: [X] (minimum 100)
- Edge Cases: [X] (minimum 50)
- Total PRP Length: [X lines] (minimum 5000)

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

### PRP Completeness Validation:

**MANDATORY CHECKS**:
1. Did you read ALL 5 core documentation files completely?
2. Did you perform 50+ Grep MCP searches?
3. Did you document 100+ patterns and examples?
4. Did you create 100+ detailed micro-tasks?
5. Is the PRP 5000+ lines of implementation detail?
6. Did you spend 2+ hours on research?
7. Did you include code for EVERY component?
8. Did you specify EVERY test case?
9. Did you document EVERY edge case?
10. Is there ZERO ambiguity in implementation?

**CRITICAL**: The goal is ZERO ambiguity, COMPLETE context, EXHAUSTIVE detail. A PRP scoring below 10 is UNACCEPTABLE - continue research until perfect.

**FINAL REMINDER**: The user has ABUNDANT tokens and wants MAXIMUM detail. Do NOT hold back on research or documentation. Make this the most comprehensive PRP ever created.