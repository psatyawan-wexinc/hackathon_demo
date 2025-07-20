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

0. **Database & Mock Data Setup** (MANDATORY FIRST STEP)
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

1. **Load and Validate PRP**
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

2. **ULTRATHINK & Plan with TodoWrite**
   - Create comprehensive plan following TDD: Test → Implement → Refactor
   - Use TodoWrite to track: test creation, implementation, validation
   - Ensure EVERY task creates files in `/workspaces/hackathon_demo/use-case`
   - Track progress: `mcp__memory-bank__track_progress("Planning", "Created TDD task list")`
   - Identify patterns from existing code to follow

3. **Execute TDD Cycle** (MANDATORY Order)
   
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

Remember: Always reference the PRP for specific patterns and requirements. The PRP is your source of truth for implementation details.