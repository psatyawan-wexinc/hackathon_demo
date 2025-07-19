# Execute BASE PRP

Implement a feature using the PRP file while following all CLAUDE.md rules.

## PRP File: $ARGUMENTS

## Pre-Execution Checklist

1. **Directory Structure Validation**
   - Verify `/workspaces/hackathon_demo/use-case` directory exists
   - Confirm PRP specifies all files go in use-case directory
   - **CRITICAL**: NO files should be created outside `/workspaces/hackathon_demo/use-case`

2. **MCP Context Loading**
   - `mcp__memory-bank__read_memory_bank_file("active-context")` - Load current state
   - `mcp__memory-bank__read_memory_bank_file("system-patterns")` - Review patterns
   - `mcp__knowledge-graph__search_nodes("{feature}")` - Find related components

3. **Environment Setup**
   - For Python: Activate `venv_linux` for all commands
   - Verify all required tools are available (ruff, mypy, pytest, etc.)

## Execution Process

1. **Load and Validate PRP**
   - Read the specified PRP file
   - Verify TDD task ordering (tests before implementation)
   - Ensure all paths use `/workspaces/hackathon_demo/use-case`
   - Understand all context and requirements
   - Use `mcp__perplexity-ask__perplexity_ask` for any missing documentation

2. **ULTRATHINK & Plan with TodoWrite**
   - Create comprehensive plan following TDD: Test → Implement → Refactor
   - Use TodoWrite to track: test creation, implementation, validation
   - Ensure EVERY task creates files in `/workspaces/hackathon_demo/use-case`
   - Track progress: `mcp__memory-bank__track_progress("Planning", "Created TDD task list")`
   - Identify patterns from existing code to follow

3. **Execute TDD Cycle** (MANDATORY Order)
   
   For each component:
   
   a) **Write Failing Tests First**
      - Create test file in `/workspaces/hackathon_demo/use-case/tests/`
      - Write comprehensive test cases (happy path, edge cases, errors)
      - Run tests to ensure they fail: `pytest {test_file} -v`
      - Track: `mcp__memory-bank__track_progress("TDD", "Created failing tests for {component}")`
   
   b) **Implement Code**
      - Create implementation in `/workspaces/hackathon_demo/use-case/src/`
      - Follow patterns identified in PRP
      - Use `mcp__ide__getDiagnostics()` to catch issues early
      - Make tests pass with minimal code
   
   c) **Refactor**
      - Improve code quality while keeping tests green
      - Apply CLAUDE.md optimization principles
      - Log decisions: `mcp__memory-bank__log_decision("Design Choice", "context", "decision")`

4. **Progressive Validation**
   
   a) **Syntax & Style** (Run first)
      ```bash
      # Python
      cd /workspaces/hackathon_demo/use-case
      ruff check src/ tests/ --fix
      mypy src/ tests/
      
      # JavaScript/TypeScript
      npm run lint
      npm run type-check
      ```
   
   b) **Unit Tests with Coverage**
      ```bash
      pytest tests/unit/ -v --cov=src --cov-report=term-missing
      # Ensure minimum 80% coverage
      ```
   
   c) **Integration Tests**
      ```bash
      pytest tests/integration/ -v
      ```
   
   d) **Fix Any Failures**
      - Read error messages carefully
      - Apply fixes following TDD cycle
      - Re-run validation until all pass

5. **Completion & Context Update**
   - Verify all PRP requirements implemented
   - Ensure all files are in `/workspaces/hackathon_demo/use-case`
   - Run final validation suite across all tests
   - Update MCP context:
     ```
     mcp__memory-bank__update_active_context(
         tasks=["Completed: {feature}"],
         nextSteps=["Document API", "Add integration tests", etc.],
         issues=["Any known limitations"]
     )
     ```
   - Create Knowledge Graph entities for new components:
     ```
     mcp__knowledge-graph__create_entities([{
         name: "{ComponentName}",
         entityType: "component",
         observations: ["Purpose", "Dependencies", "Key methods"]
     }])
     ```
   - Final progress track: `mcp__memory-bank__track_progress("Complete", "Feature implemented with X% coverage")`

## Error Recovery Patterns

### Common Issues & Solutions

1. **Files Created Outside use-case Directory**
   - STOP immediately
   - Move files to correct location under `/workspaces/hackathon_demo/use-case`
   - Update all imports and paths
   - Re-run validation

2. **Test Failures**
   - Review test expectations vs implementation
   - Check for missing edge cases
   - Verify test setup/teardown
   - Use `mcp__ide__getDiagnostics()` for code issues

3. **Coverage Below 80%**
   - Identify uncovered lines: `pytest --cov-report=html`
   - Add missing test cases
   - Focus on error paths and edge cases

4. **Import/Module Errors**
   - Verify all paths relative to `/workspaces/hackathon_demo/use-case`
   - Check `__init__.py` files exist
   - For Python: Ensure using `venv_linux`

5. **MCP Connection Issues**
   - Continue with implementation
   - Log decisions manually
   - Update context when connection restored

Remember: Always reference the PRP for specific patterns and requirements. The PRP is your source of truth for implementation details.