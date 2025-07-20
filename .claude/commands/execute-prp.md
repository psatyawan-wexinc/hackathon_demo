# Execute ULTRA-DETAILED PRP

Implement a feature using the PRP file with EXHAUSTIVE validation, CONTINUOUS verification, and ZERO ambiguity. Every step must be executed with maximum detail and comprehensive checking.

**CRITICAL**: This execution process is designed for PERFECT implementation. Follow EVERY step, validate EVERYTHING, and leave NOTHING to chance.

## PRP File: $ARGUMENTS

## Phase 1: EXHAUSTIVE PRE-EXECUTION VALIDATION

### 1.1 Deep PRP Analysis (MANDATORY)
**Read the PRP THREE times with different focus:**
1. **First Read**: Overall architecture and requirements
2. **Second Read**: Extract EVERY pattern, example, and code snippet
3. **Third Read**: Map all tasks and dependencies

**Document Understanding:**
```markdown
# PRP Comprehension Checklist
- [ ] All 15+ sections understood?
- [ ] All 100+ tasks mapped?
- [ ] All 50+ patterns extracted?
- [ ] All 100+ test cases documented?
- [ ] All code examples saved?
- [ ] All edge cases identified?
- [ ] Zero ambiguity remaining?
```

### 1.2 Complete Environment Verification
```bash
# Tool Availability Check (ALL must pass)
python --version && echo "✓ Python available"
sqlite3 --version && echo "✓ SQLite available"
pytest --version && echo "✓ Pytest available"
ruff --version && echo "✓ Ruff available"
mypy --version && echo "✓ Mypy available"
black --version && echo "✓ Black available"
alembic --version && echo "✓ Alembic available"

# Python environment
source venv_linux/bin/activate
pip list | grep -E "factory-boy|faker|sqlalchemy|pydantic" || pip install factory-boy faker sqlalchemy pydantic
```

### 1.3 Comprehensive MCP Context Loading
**Load ALL context files and document findings:**

1. **Memory Bank Deep Dive**:
   ```python
   # Read EVERY context file
   contexts = [
       "active-context", "system-patterns", "decision-log",
       "product-context", "progress"
   ]
   for context in contexts:
       content = mcp__memory-bank__read_memory_bank_file(context)
       # Document all relevant patterns and decisions
   ```

2. **Knowledge Graph Exhaustive Search**:
   ```python
   # Search for ALL related concepts
   searches = [
       "{feature}", "pattern", "component", "utility",
       "repository", "validator", "test", "mock"
   ]
   for term in searches:
       results = mcp__knowledge-graph__search_nodes(term)
       # Map all relationships and existing components
   ```

3. **Pattern Validation with Grep MCP** (20+ searches):
   ```python
   # Validate architecture patterns
   patterns_to_validate = [
       {"query": "repository pattern", "language": ["Python"]},
       {"query": "factory pattern", "language": ["Python"]},
       {"query": "validator pattern", "language": ["Python"]},
       {"query": "test fixture", "language": ["Python"]},
       # ... 20+ more pattern searches
   ]
   ```

### 1.4 Directory Structure Preparation
```bash
# Create complete directory structure
mkdir -p /workspaces/hackathon_demo/use-case/{src,tests,db,docs,scripts}
mkdir -p /workspaces/hackathon_demo/use-case/src/{agents,models,repositories,utils,validators,config}
mkdir -p /workspaces/hackathon_demo/use-case/tests/{unit,integration,fixtures,mocks}

# Verify structure
tree /workspaces/hackathon_demo/use-case

# Create __init__.py files
find /workspaces/hackathon_demo/use-case -type d -name "*" -exec touch {}/__init__.py \;
```

## Phase 2: ULTRA-DETAILED EXECUTION PROCESS

### 2.0 **Comprehensive Database & Mock Data Architecture** (MANDATORY FIRST STEP)

**Deep Database Design Implementation:**
   - Create database directory: `mkdir -p /workspaces/hackathon_demo/use-case/db`
   - Initialize SQLite database:
     ```bash
     cd /workspaces/hackathon_demo/use-case
     # Create database schema file
     cat > db/schema.sql << 'EOF'
     CREATE TABLE IF NOT EXISTS user_profiles (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         user_id TEXT UNIQUE NOT NULL,
         coverage_type TEXT NOT NULL,
         ytd_contribution REAL NOT NULL,
         is_55_plus BOOLEAN NOT NULL,
         remaining_pay_periods INTEGER NOT NULL,
         pay_frequency TEXT,
         employer_contribution REAL,
         plan_start_date DATE,
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
     );
     
     CREATE TABLE IF NOT EXISTS contribution_calculations (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         user_id TEXT NOT NULL,
         calculation_date DATE NOT NULL,
         annual_limit REAL NOT NULL,
         remaining_allowed REAL NOT NULL,
         per_period_amount REAL NOT NULL,
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
         FOREIGN KEY (user_id) REFERENCES user_profiles (user_id)
     );
     EOF
     
     # Initialize development database
     sqlite3 db/dev_hsa.db < db/schema.sql
     
     # Create Alembic configuration
     alembic init db/migrations
     ```
   - Setup mock data factories in `src/test_utils/factories.py`
   - Create fixture loader in `tests/fixtures/loader.py`
   - Initialize test database: `sqlite3 db/test_hsa.db < db/schema.sql`
   - Track: `mcp__memory-bank__track_progress("Database Setup", "Created SQLite schema and test database")`
   
   **Extensive Mock Data Setup**:
   ```python
   # src/test_utils/factories.py - Create comprehensive factories
   import factory
   from factory import Faker, Factory, Sequence, Trait
   from datetime import datetime, date
   import random
   
   class UserProfileFactory(Factory):
       class Meta:
           model = dict
       
       user_id = Sequence(lambda n: f"user_{n:05d}")
       first_name = Faker('first_name')
       last_name = Faker('last_name')
       email = Faker('email')
       coverage_type = factory.Iterator(['self-only', 'family'])
       ytd_contribution = factory.LazyFunction(lambda: round(random.uniform(0, 8000), 2))
       is_55_plus = factory.LazyFunction(lambda: random.choice([True, False]))
       remaining_pay_periods = factory.LazyFunction(lambda: random.randint(1, 26))
       
       # Traits for specific scenarios
       class Params:
           near_limit = Trait(
               coverage_type='family',
               ytd_contribution=8400.00
           )
           over_limit = Trait(
               coverage_type='family',
               ytd_contribution=9000.00
           )
           catch_up_eligible = Trait(
               is_55_plus=True
           )
   
   # Create 50+ test scenarios
   TEST_SCENARIOS = {
       'standard': {...},
       'edge_cases': {...},
       'error_cases': {...},
       # ... 50+ scenarios
   }
   ```
   
   **Validate Mock Data Generation**:
   ```bash
   # Test all factories
   python -m pytest tests/test_factories.py -v
   
   # Generate sample data
   python scripts/generate_test_data.py --scenarios 50
   
   # Verify data integrity
   sqlite3 db/test_hsa.db "SELECT COUNT(*) FROM user_profiles;"
   ```

### 2.1 **Deep PRP Loading and Pattern Extraction**
   - Read the specified PRP file
   - Verify TDD task ordering (tests before implementation)
   - Ensure all paths use `/workspaces/hackathon_demo/use-case`
   - Understand all context and requirements
   - **Validate with Grep MCP pattern research**:
     - Verify architecture approach: `{"query": "[domain] [framework]", "language": ["Python"]}`
     - Check testing strategies: `{"query": "pytest OR testing", "language": ["Python"], "path": ["tests/"]}`
     - Validate database patterns: `{"query": "sqlalchemy OR database", "language": ["Python"]}`
   - Use `mcp__perplexity-ask__perplexity_ask` for any missing documentation
   - Cross-reference Perplexity documentation with Grep pattern discoveries
   
   **Pattern Extraction and Documentation**:
   ```python
   # Extract and document EVERY pattern from PRP
   patterns = {
       'architecture': [],
       'code': [],
       'test': [],
       'database': [],
       'validation': [],
       'error_handling': []
   }
   
   # Document each pattern with:
   # - Pattern name
   # - Description
   # - Code example
   # - Usage context
   # - File location in PRP
   ```
   
   **Task Dependency Mapping**:
   ```python
   # Create complete task dependency graph
   task_graph = {
       'task_001': {'deps': [], 'status': 'pending'},
       'task_002': {'deps': ['task_001'], 'status': 'pending'},
       # ... map all 100+ tasks
   }
   ```

### 2.2 **Comprehensive Planning with TodoWrite**

**Create Ultra-Detailed Task List:**
   - Create comprehensive plan following TDD: Test → Implement → Refactor
   - Use TodoWrite to track: test creation, implementation, validation
   - Ensure EVERY task creates files in `/workspaces/hackathon_demo/use-case`
   - Track progress: `mcp__memory-bank__track_progress("Planning", "Created TDD task list")`
   - Identify patterns from existing code to follow

### 2.3 **Ultra-Detailed TDD Execution** (MANDATORY Order)

**CRITICAL**: For EACH component, follow this exhaustive process:
   
   For each component:
   
   a) **Setup Test Data & Write Failing Tests**
      - Create test fixtures with mock data:
        ```python
        # tests/conftest.py
        import pytest
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from src.test_utils.factories import UserProfileFactory, HSATestDataBuilder
        
        @pytest.fixture
        def test_db():
            engine = create_engine('sqlite:///:memory:')
            # Create tables
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            session = Session()
            yield session
            session.close()
        
        @pytest.fixture
        def test_data_builder(test_db):
            return HSATestDataBuilder(test_db)
        
        @pytest.fixture
        def sample_users(test_data_builder):
            return {
                'standard': test_data_builder.create_test_scenario('standard'),
                'near_limit': test_data_builder.create_test_scenario('approaching_limit'),
                'over_limit': test_data_builder.create_test_scenario('over_contribution')
            }
        ```
      - Create test file in `/workspaces/hackathon_demo/use-case/tests/`
      - Write comprehensive test cases using mock data fixtures
      - Run tests to ensure they fail: `pytest {test_file} -v`
      - Track: `mcp__memory-bank__track_progress("TDD", "Created failing tests with mock data for {component}")`
   
   b) **Implement Code with DRY Validation & Pattern Reuse**
      - **Before writing any code**: Search for existing patterns to extend
        ```bash
        # Search for similar functionality
        rg "similar_functionality" src/ --type py
        grep -r "pattern_name" src/
        ```
      - **DRY Implementation Strategy**:
        - Extend existing utilities instead of creating new ones
        - Use shared validators for common input validation
        - Implement repository pattern for data access (if not existing)
        - Reuse configuration from centralized sources
      - Create implementation in `/workspaces/hackathon_demo/use-case/src/`
      - **DRY Repository Pattern Implementation**:
        ```python
        # src/repositories/base_repository.py (DRY: Create once, extend everywhere)
        from abc import ABC, abstractmethod
        from sqlalchemy.orm import Session
        
        class BaseRepository(ABC):
            def __init__(self, session: Session):
                self.session = session
            
            def create(self, entity_data: dict):
                entity = self.model_class(**entity_data)
                self.session.add(entity)
                self.session.commit()
                return entity
            
            def get_by_id(self, entity_id: str):
                return self.session.query(self.model_class).filter_by(id=entity_id).first()
        
        # src/repositories/user_profile_repository.py (DRY: Extends base)
        from src.models import UserProfile
        from .base_repository import BaseRepository
        
        class UserProfileRepository(BaseRepository):
            model_class = UserProfile
            
            def get_by_user_id(self, user_id: str) -> UserProfile:
                return self.session.query(UserProfile).filter_by(user_id=user_id).first()
        ```
      - **DRY Utility Usage**:
        ```python
        # Use shared utilities instead of duplicating logic
        from src.utils.calculations import calculate_remaining_contribution
        from src.validators.hsa_validators import validate_coverage_type
        from src.config.hsa_limits import HSA_LIMITS_2025
        ```
      - Follow patterns identified in PRP
      - Use `mcp__ide__getDiagnostics()` to catch issues early
      - Make tests pass with minimal code
      - Ensure proper database transaction handling
   
   c) **Refactor with DRY Principles**
      - **DRY Refactoring Checklist**:
        - [ ] Extract any repeated code blocks (>3 lines) into utilities
        - [ ] Consolidate duplicate validation logic
        - [ ] Move hard-coded values to configuration files
        - [ ] Create shared base classes for similar components
        - [ ] Abstract common patterns into decorators/mixins
      - **Anti-Duplication Validation**:
        ```bash
        # Find potential duplications
        rg -A 3 -B 3 "duplicate_pattern" src/
        rg "TODO.*DRY" src/ # Find DRY improvement opportunities
        ```
      - Improve code quality while keeping tests green
      - Apply CLAUDE.md optimization principles  
      - Log decisions: `mcp__memory-bank__log_decision("Design Choice", "context", "decision")`

4. **Progressive Validation**
   
   a) **Database & Mock Data Validation** (Run first)
      ```bash
      cd /workspaces/hackathon_demo/use-case
      
      # Verify database setup
      sqlite3 db/test_hsa.db ".tables"
      
      # Test mock data generation
      python -c "from src.test_utils.factories import UserProfileFactory; print(UserProfileFactory.build())"
      
      # Validate fixtures
      pytest tests/test_fixtures.py -v
      ```
   
   b) **Syntax & Style**
      ```bash
      # Python
      cd /workspaces/hackathon_demo/use-case
      ruff check src/ tests/ --fix
      mypy src/ tests/
      
      # JavaScript/TypeScript
      npm run lint
      npm run type-check
      ```
   
   c) **Unit Tests with Coverage**
      ```bash
      # Run with test database
      pytest tests/unit/ -v --cov=src --cov-report=term-missing
      # Ensure minimum 80% coverage
      ```
   
   d) **Integration Tests with Database**
      ```bash
      # Test with full database integration
      pytest tests/integration/ -v --db=test
      ```
   
   e) **Data Cleanup Validation**
      ```bash
      # Verify test isolation
      pytest tests/test_cleanup.py -v
      ```
   
   f) **DRY Compliance Validation**
      ```bash
      cd /workspaces/hackathon_demo/use-case
      
      # Check for code duplication
      rg -C 3 "def.*calculate.*contribution" src/ # Find calculation duplicates
      rg -C 3 "validate.*" src/ # Find validation duplicates
      rg "import.*config" src/ # Verify centralized config usage
      
      # Validate single source of truth
      find src/ -name "*.py" -exec grep -l "HSA_LIMIT\|4300\|8550" {} \;
      # Should only return config files
      
      # Check utility usage
      rg "from.*utils" src/ # Verify utilities are being used
      rg "class.*Repository" src/ # Verify repository pattern consistency
      ```
   
   g) **External Pattern Validation** (Grep MCP)
      - Verify implementation follows discovered patterns
      - Compare architecture decisions with external research
      - Validate testing approach against best practices found
      - Check for missed optimization opportunities from pattern research
      - Document any deviations from discovered patterns with justification
   
   h) **Fix Any Failures**
      - Read error messages carefully
      - Apply fixes following TDD cycle
      - Re-run validation until all pass

5. **Completion & Context Update**
   - Verify all PRP requirements implemented
   - Ensure all files are in `/workspaces/hackathon_demo/use-case`
   - Clean up test databases:
     ```bash
     # Archive test data for future reference
     cp db/test_hsa.db db/test_hsa_$(date +%Y%m%d).db.backup
     
     # Clean test database
     sqlite3 db/test_hsa.db "DELETE FROM contribution_calculations; DELETE FROM user_profiles;"
     ```
   - Run final validation suite across all tests
   - Document mock data patterns used:
     ```
     mcp__knowledge-graph__create_entities([{
         name: "MockDataPatterns",
         entityType: "test-infrastructure",
         observations: [
             "Factory pattern used for user profile generation",
             "SQLite in-memory databases for unit tests",
             "Transactional fixtures for test isolation",
             "Scenario-based test data builders implemented"
         ]
     }])
     ```
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

1. **Database Connection Errors**
   - Verify SQLite is installed: `sqlite3 --version`
   - Check database file permissions
   - Ensure database path is absolute in connection string
   - For in-memory databases, verify syntax: `sqlite:///:memory:`

2. **Mock Data Generation Failures**
   - Check Factory Boy installation: `pip install factory-boy faker`
   - Verify all required fields in factories
   - Ensure proper faker providers are used
   - Check for circular dependencies in factories

3. **Test Data Contamination**
   - Verify transaction rollback in fixtures
   - Check for shared database connections
   - Ensure proper teardown methods
   - Use separate databases for different test types

4. **Files Created Outside use-case Directory**
   - STOP immediately
   - Move files to correct location under `/workspaces/hackathon_demo/use-case`
   - Update all imports and paths
   - Re-run validation

5. **Test Failures**
   - Review test expectations vs implementation
   - Check for missing edge cases
   - Verify test setup/teardown
   - Validate mock data matches test expectations
   - Check database state before/after tests
   - Use `mcp__ide__getDiagnostics()` for code issues

6. **Coverage Below 80%**
   - Identify uncovered lines: `pytest --cov-report=html`
   - Add missing test cases with appropriate mock data
   - Focus on error paths and edge cases
   - Test database error scenarios

7. **Import/Module Errors**
   - Verify all paths relative to `/workspaces/hackathon_demo/use-case`
   - Check `__init__.py` files exist
   - For Python: Ensure using `venv_linux`
   - Verify SQLAlchemy models are properly imported

8. **MCP Connection Issues**
   - Continue with implementation
   - Log decisions manually
   - Update context when connection restored

9. **Data Migration Issues**
   - Check Alembic configuration
   - Verify migration scripts syntax
   - Test migrations on copy of database first
   - Keep migration rollback scripts

## Phase 3: EXHAUSTIVE PROGRESSIVE VALIDATION

### 3.1 Continuous Validation Loop (Run after EVERY file creation)

**CRITICAL**: Run validation after EVERY single change, not just at the end.

#### Real-time Syntax Validation
```bash
# After EVERY Python file edit
cd /workspaces/hackathon_demo/use-case
ruff check {file} --fix
mypy {file}

# After EVERY test file creation
pytest {test_file} -v --no-header

# IDE diagnostics after EVERY change
mcp__ide__getDiagnostics(uri="{file_path}")
```

#### Incremental Test Execution
```bash
# Run related tests immediately
pytest tests/test_{component}.py -v

# Check coverage incrementally
pytest tests/test_{component}.py --cov=src/{module} --cov-report=term-missing
```

### 3.2 Deep Test Validation (50+ validation points)

**Test Quality Metrics**:
- [ ] Test isolation verified (no shared state)
- [ ] Mock data properly scoped
- [ ] Database transactions rolled back
- [ ] All fixtures properly torn down
- [ ] No test order dependencies
- [ ] Edge cases covered (nulls, empty, overflow)
- [ ] Error paths tested
- [ ] Performance benchmarks included
- [ ] Concurrency scenarios tested
- [ ] Security validations included

**Test Data Validation**:
```python
# Verify test data quality
def validate_test_data():
    # Check for PII
    assert not contains_real_pii(test_data)
    
    # Verify deterministic generation
    data1 = UserProfileFactory.build()
    data2 = UserProfileFactory.build()
    assert data1 != data2  # Unique data
    
    # Validate scenario coverage
    scenarios = generate_all_test_scenarios()
    assert len(scenarios) >= 50
    
    # Check edge case representation
    edge_cases = filter_edge_cases(scenarios)
    assert len(edge_cases) >= 20
```

### 3.3 DRY Compliance Deep Validation

**Comprehensive DRY Checks**:
```bash
# 1. Function duplication analysis
rg "def " src/ | awk -F: '{print $2}' | sort | uniq -c | sort -rn | head -20
# Any count > 1 needs investigation

# 2. Import pattern analysis
rg "^from|^import" src/ | grep -v "__" | sort | uniq -c | sort -rn
# Verify shared utilities are being used

# 3. Constant duplication check
rg "=\s*[0-9]+" src/ | grep -v "test" | grep -v "config"
# All numeric constants should be in config

# 4. String literal analysis
rg '"[^"]{10,}"' src/ | grep -v "test" | grep -v "doc"
# Long strings should be constants

# 5. Class hierarchy verification
rg "class.*\(.*\):" src/ | grep -v "Test"
# Check for proper inheritance usage

# 6. Repository pattern compliance
find src/ -name "*repository.py" -exec grep -L "BaseRepository" {} \;
# All repositories should extend base

# 7. Validation logic centralization
rg "validate|Validator" src/ | grep -v "validators.py"
# Validation should be centralized

# 8. Configuration usage audit
rg "HSA_LIMIT|4300|8550|1000" src/ | grep -v "config"
# Should return empty - all in config
```

**DRY Scoring Matrix**:
- 0 duplicate functions: +2 points
- <5% code duplication: +2 points
- 100% config centralization: +2 points
- >80% base class usage: +2 points
- All patterns documented: +2 points
Total: _/10 (Must achieve 8+)

### 3.4 Integration Test Suite Validation

```bash
# Full integration test suite
cd /workspaces/hackathon_demo/use-case

# 1. Database integration
pytest tests/integration/test_database_operations.py -v

# 2. Agent communication
pytest tests/integration/test_agent_flow.py -v

# 3. End-to-end scenarios
pytest tests/integration/test_e2e_scenarios.py -v

# 4. Performance benchmarks
pytest tests/performance/test_benchmarks.py -v

# 5. Concurrent operations
pytest tests/integration/test_concurrency.py -v
```

### 3.5 External Pattern Validation with Grep MCP

**Validate Implementation Against Research**:
```python
# Cross-reference implementation with discovered patterns
pattern_validations = [
    {"local": "repository pattern", "external": mcp_grep_results['repository']},
    {"local": "factory pattern", "external": mcp_grep_results['factory']},
    {"local": "validator pattern", "external": mcp_grep_results['validator']},
    # ... 20+ pattern validations
]

for validation in pattern_validations:
    # Compare local implementation with external best practices
    # Document any deviations with justification
    pass
```

## Phase 4: COMPREHENSIVE COMPLETION VERIFICATION

### 4.1 Exhaustive PRP Compliance Check

**Task Completion Audit**:
```python
# Verify EVERY task from PRP is complete
task_checklist = load_prp_tasks(prp_file)
completed_tasks = load_completed_from_todo()

for task in task_checklist:
    assert task['id'] in completed_tasks
    assert completed_tasks[task['id']]['status'] == 'completed'
    
    # Verify acceptance criteria
    for criteria in task['acceptance_criteria']:
        assert verify_criteria(criteria)
    
    # Verify test coverage
    assert get_test_coverage(task['component']) >= 80
```

### 4.2 Deep Code Quality Validation

```bash
# Comprehensive quality checks
cd /workspaces/hackathon_demo/use-case

# 1. Complexity analysis
radon cc src/ -a -nb
# Average complexity should be < 5

# 2. Maintainability index
radon mi src/ -nb
# Should be > 80

# 3. Documentation coverage
interrogate src/ -v
# Should be 100%

# 4. Security audit
bandit -r src/
# No high severity issues

# 5. Dead code detection
vulture src/
# No unused code

# 6. Import order
isort src/ --check-only --diff
# Properly organized imports
```

### 4.3 Database & Mock Data Final Validation

```bash
# Final database checks
cd /workspaces/hackathon_demo/use-case

# 1. Schema integrity
sqlite3 db/dev_hsa.db ".schema" > schema_actual.sql
diff db/schema.sql schema_actual.sql
# Should be identical

# 2. Migration history
alembic history -v
# All migrations applied

# 3. Test data quality
python scripts/validate_test_data.py
# 100% compliance

# 4. Performance benchmarks
python scripts/benchmark_queries.py
# All queries < 100ms

# 5. Data cleanup verification
pytest tests/test_data_cleanup.py -v
# No data leakage between tests
```

### 4.4 Final Test Suite Execution

```bash
# Complete test suite with all validations
cd /workspaces/hackathon_demo/use-case

# 1. Full test suite with coverage
pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing

# 2. Mutation testing
mutmut run --paths-to-mutate=src/

# 3. Property-based testing
pytest tests/property/ -v

# 4. Stress testing
pytest tests/stress/ -v -n 4

# 5. Generate final reports
pytest --html=reports/test_report.html --self-contained-html
```

### 4.5 MCP Context Finalization

```python
# Comprehensive context update
mcp__memory-bank__update_active_context(
    tasks=[
        "Completed: {feature} implementation with {coverage}% coverage",
        "All {num_tests} tests passing",
        "DRY compliance score: {dry_score}/10",
        "Performance benchmarks met"
    ],
    nextSteps=[
        "API documentation generation",
        "Deployment configuration",
        "Performance optimization opportunities",
        "Additional test scenarios"
    ],
    issues=[
        "Known limitations",
        "Future enhancement opportunities",
        "Technical debt items"
    ]
)

# Create comprehensive knowledge graph
entities = []
for component in implemented_components:
    entities.append({
        "name": component['name'],
        "entityType": component['type'],
        "observations": [
            f"Purpose: {component['purpose']}",
            f"Dependencies: {component['deps']}",
            f"Test coverage: {component['coverage']}%",
            f"Patterns used: {component['patterns']}",
            f"Performance: {component['metrics']}"
        ]
    })

mcp__knowledge-graph__create_entities(entities)

# Log all architectural decisions
for decision in architectural_decisions:
    mcp__memory-bank__log_decision(
        title=decision['title'],
        context=decision['context'],
        decision=decision['choice'],
        alternatives=decision['alternatives'],
        consequences=decision['impact']
    )
```

## Phase 5: EXHAUSTIVE ERROR HANDLING & RECOVERY

### 5.1 Comprehensive Error Recovery Patterns

#### Test Failure Recovery
```python
# Detailed test failure analysis
def analyze_test_failure(test_output):
    failure_patterns = {
        "AssertionError": check_assertion_details,
        "ValidationError": check_validation_logic,
        "DatabaseError": check_db_state,
        "ImportError": check_module_paths,
        "AttributeError": check_object_structure
    }
    
    for pattern, handler in failure_patterns.items():
        if pattern in test_output:
            recovery_steps = handler(test_output)
            apply_recovery(recovery_steps)
```

#### Database Recovery
```bash
# Database corruption recovery
if sqlite3 db/dev_hsa.db "PRAGMA integrity_check" | grep -v "ok"; then
    # Backup corrupted database
    cp db/dev_hsa.db db/corrupted_$(date +%s).db
    
    # Recreate from schema
    rm db/dev_hsa.db
    sqlite3 db/dev_hsa.db < db/schema.sql
    
    # Rerun migrations
    alembic upgrade head
    
    # Regenerate test data
    python scripts/generate_test_data.py
fi
```

#### Import Path Recovery
```python
# Fix common import issues
def fix_import_paths():
    # Add missing __init__.py files
    for root, dirs, files in os.walk('/workspaces/hackathon_demo/use-case'):
        if not '__init__.py' in files and any(f.endswith('.py') for f in files):
            Path(root, '__init__.py').touch()
    
    # Fix relative imports
    fix_relative_imports('src/')
    
    # Update PYTHONPATH
    sys.path.insert(0, '/workspaces/hackathon_demo/use-case')
```

### 5.2 Performance Issue Resolution

```python
# Performance bottleneck detection and resolution
def diagnose_performance_issues():
    # Profile code execution
    profiler = cProfile.Profile()
    profiler.enable()
    run_performance_tests()
    profiler.disable()
    
    # Analyze results
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    
    # Identify bottlenecks
    bottlenecks = identify_slow_functions(stats)
    
    # Apply optimizations
    for bottleneck in bottlenecks:
        if bottleneck['type'] == 'database':
            add_database_index(bottleneck['query'])
        elif bottleneck['type'] == 'algorithm':
            optimize_algorithm(bottleneck['function'])
        elif bottleneck['type'] == 'io':
            implement_caching(bottleneck['operation'])
```

### 5.3 Coverage Gap Resolution

```python
# Automated coverage improvement
def improve_test_coverage():
    # Get uncovered lines
    coverage_report = run_coverage_analysis()
    uncovered = extract_uncovered_lines(coverage_report)
    
    for file, lines in uncovered.items():
        # Analyze uncovered code
        code_blocks = analyze_code_blocks(file, lines)
        
        for block in code_blocks:
            if block['type'] == 'error_handler':
                generate_error_test(block)
            elif block['type'] == 'edge_case':
                generate_edge_case_test(block)
            elif block['type'] == 'conditional':
                generate_conditional_test(block)
```

### 5.4 DRY Violation Resolution

```python
# Automated DRY refactoring
def resolve_dry_violations():
    # Find duplications
    duplications = find_code_duplications('src/')
    
    for duplication in duplications:
        if duplication['type'] == 'function':
            # Extract to shared utility
            create_shared_utility(duplication)
        elif duplication['type'] == 'validation':
            # Move to validator
            move_to_validator(duplication)
        elif duplication['type'] == 'constant':
            # Centralize in config
            add_to_config(duplication)
        
        # Update all references
        update_references(duplication)
```

## CRITICAL FINAL REMINDERS

### 🚨 MANDATORY CHECKS BEFORE MARKING COMPLETE

1. **Directory Compliance**
   ```bash
   # ALL files must be in use-case directory
   find . -name "*.py" -o -name "*.ts" -o -name "*.js" | grep -v "use-case"
   # Should return NOTHING
   ```

2. **Test Coverage**
   ```bash
   # Must exceed 80%
   pytest --cov=src --cov-report=term | grep TOTAL
   ```

3. **DRY Compliance**
   ```bash
   # No magic numbers outside config
   rg "=\s*[0-9]+" src/ | grep -v config | wc -l
   # Should be 0
   ```

4. **All Tests Passing**
   ```bash
   # Zero failures
   pytest tests/ -v | grep -E "FAILED|ERROR"
   # Should return nothing
   ```

5. **MCP Context Updated**
   ```python
   # Verify context saved
   assert mcp__memory-bank__read_memory_bank_file("active-context")
   assert mcp__knowledge-graph__search_nodes("{feature}")
   ```

### 🎯 SUCCESS CRITERIA

✅ **Implementation is COMPLETE when**:
- [ ] 100% of PRP tasks completed
- [ ] Test coverage ≥ 80%
- [ ] All tests passing (0 failures)
- [ ] DRY compliance score ≥ 8/10
- [ ] All files in `/workspaces/hackathon_demo/use-case`
- [ ] MCP context fully updated
- [ ] No linting errors
- [ ] No type checking errors
- [ ] Database migrations applied
- [ ] Mock data factories working
- [ ] Integration tests passing
- [ ] Performance benchmarks met
- [ ] Documentation complete
- [ ] Knowledge graph updated
- [ ] Decision log current

### 💡 REMEMBER

- **Research First**: Use all MCP tools for context
- **Test First**: Never write code without a failing test
- **DRY Always**: Search before creating, extend before duplicating
- **Validate Continuously**: Run checks after every change
- **Document Everything**: Update MCP with all decisions
- **Quality Over Speed**: Better to be thorough than fast

**THE GOAL**: ZERO defects, COMPLETE implementation, PERFECT adherence to all principles.

Remember: Always reference the PRP for specific patterns and requirements. The PRP is your source of truth for implementation details.