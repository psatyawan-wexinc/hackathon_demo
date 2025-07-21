---
name: "LangGraph HSA Contribution Planner PRP"
description: This template provides a production-ready implementation blueprint for building an HSA Contribution Planner using LangGraph's multi-agent orchestration framework with proven conversational AI patterns.
---

## Purpose

Template optimized for AI agents to implement a production-ready HSA (Health Savings Account) contribution planning system using LangGraph's multi-agent architecture, with conversational UI, IRS compliance logic, and enterprise-grade error handling.

## Core Principles

1. **Agent Orchestration First**: Design clear agent boundaries with well-defined inputs, outputs, and state transitions
2. **IRS Compliance Built-In**: Embed 2025 contribution limits, proration rules, and catch-up provisions in agent logic
3. **Conversation Flow Management**: Implement robust state persistence and error recovery for multi-turn conversations
4. **Test-Driven Agent Development**: Build comprehensive test suites for individual agents and orchestration flows
5. **User Experience Focus**: Provide clear, actionable guidance with visual feedback throughout the planning process

## Data Management & Testing Infrastructure

### Mock Data Generation Standards
1. **Factory Pattern Implementation**: Use Factory Boy (Python) or equivalent for consistent test object creation
2. **Fixture Management**: Implement pytest fixtures or similar for reusable test data scenarios
3. **Realistic Data Generation**: Leverage Faker library for generating realistic user profiles, dates, and financial data
4. **Deterministic Seeding**: Use fixed random seeds for reproducible test runs
5. **Data Builders**: Implement test data builders for complex HSA scenarios

### Database Strategy
1. **SQLite for Development**: Local SQLite databases for development and testing
2. **In-Memory Testing**: Use `:memory:` SQLite databases for fast unit tests
3. **Schema Migrations**: Implement Alembic or similar for version-controlled database changes
4. **Test Isolation**: Transaction rollback or database recreation between test runs
5. **Repository Pattern**: Abstract data access for clean separation of concerns

### Data Hydration Patterns
1. **Scenario-Based Fixtures**: Pre-defined data sets for common HSA scenarios:
   - New enrollment (no YTD contributions)
   - Mid-year job change
   - Approaching contribution limits
   - Over-contribution scenarios
   - Catch-up eligible users
2. **Performance Data Sets**: Large-scale data for load testing (1000+ user profiles)
3. **Edge Case Collections**: Unusual but valid scenarios for comprehensive testing
4. **GDPR Compliance**: No real PII in test data, use realistic but fake data

### Claude Code Hooks Integration

**Automated Development Workflow Enhancement**

This PRP implementation benefits from Claude Code Hooks that provide automated development workflow support:

1. **TDD Enforcement** (`ensure_test_file.py`):
   - Automatically creates test files when implementing agents
   - Generates HSA-specific test templates for LangGraph agents
   - Pre-configures Factory Boy integration for test data
   - Example: Creating `src/agents/user_input_agent.py` automatically generates `tests/test_user_input_agent.py` with HSA conversation flow tests

2. **Database Preparation** (`prepare_test_db.py`):
   - Automatically clears and seeds test SQLite database before pytest runs
   - Pre-populates with HSA-specific factory data (user profiles, contribution scenarios)
   - Ensures consistent test environment for agent interactions
   - Supports IRS limit test data and edge case scenarios

3. **Factory Generation** (`generate_factory.py`):
   - Detects HSA model files and generates Factory Boy factories automatically
   - Creates HSA-specific traits (catch-up eligible, near limits, family coverage)
   - Includes builder patterns for complex test scenarios
   - Example: Detects `UserProfile` model and generates `UserProfileFactory` with HSA business logic

4. **Continuous Testing** (`run_tests_and_feedback.py`):
   - Runs pytest automatically after agent implementation
   - Provides TDD guidance for Red-Green-Refactor cycles
   - Focuses on financial calculation accuracy and IRS compliance
   - Blocks completion if critical HSA calculation tests fail

5. **DRY Analysis** (`check_duplication.py`):
   - Identifies duplicated IRS calculation logic across agents
   - Suggests extraction of common HSA utilities
   - Prevents redundant limit calculation implementations
   - Promotes shared utilities for financial validations

6. **Code Quality** (`format_and_lint.py`):
   - Automatically formats agent code with consistent style
   - Identifies critical issues in financial calculations
   - Ensures production-ready code quality for HSA compliance

**Hook Integration with PRP Workflow:**

The hooks enhance each PRP implementation task:
- **Task 2 (Models)**: Auto-generates factories when creating HSA models
- **Task 3 (Agents)**: Creates comprehensive test suites for each agent
- **Task 4 (Orchestration)**: Tests LangGraph integration automatically
- **Task 6 (Testing)**: Maintains test database and provides TDD feedback
- **Task 7 (Production)**: Ensures code quality and DRY compliance

**HSA-Specific Hook Benefits:**
- Enforces IRS calculation accuracy through automated testing
- Maintains consistent test data across agent development
- Prevents financial logic duplication across agents
- Ensures comprehensive coverage of HSA edge cases
- Provides real-time feedback on calculation errors

---

## Goal

Build a production-ready HSA Contribution Planner with:

- **Three specialized LangGraph agents**: UserInputAgent, LimitCalcAgent, and PlannerAgent working in orchestrated sequence
- **Conversational interface** that guides users through HSA planning with contextual prompts
- **IRS-compliant calculations** including 2025 limits, catch-up contributions, and proration logic
- **Visual progress tracking** with color-coded status indicators and summary cards
- **Enterprise features**: State persistence, error recovery, audit logging, and performance monitoring

## Why

- **Maximize Tax Benefits**: Help users optimize HSA contributions to reduce taxable income
- **Prevent Over-contributions**: Avoid IRS penalties through accurate limit calculations
- **Simplify Complex Rules**: Navigate proration, catch-up, and mid-year changes automatically
- **Improve Financial Wellness**: Enable better healthcare savings planning
- **Reduce HR Burden**: Automate common HSA questions and calculations

## What

### LangGraph Agent System

**Core Agents:**

1. **UserInputAgent**
   - Manages conversational flow for data collection
   - Validates user inputs in real-time
   - Handles re-prompting for corrections
   - Maintains conversation context

2. **LimitCalcAgent**
   - Applies 2025 IRS contribution limits
   - Calculates catch-up eligibility
   - Handles proration for mid-year changes
   - Validates against IRS Publication 969 rules

3. **PlannerAgent**
   - Generates per-paycheck recommendations
   - Creates contribution schedules
   - Provides actionable guidance
   - Handles edge cases gracefully

**System Features:**

- **State Management**: Persistent conversation state across agent handoffs
- **Error Recovery**: Graceful handling of invalid inputs and calculation errors
- **Audit Trail**: Complete logging of user interactions and calculations
- **Performance Monitoring**: Agent response time and success rate tracking
- **Security**: PII encryption and secure session management

### Success Criteria

- [ ] All three agents successfully initialized and registered in LangGraph
- [ ] Agent handoffs work seamlessly with proper state transfer
- [ ] User inputs validated according to IRS rules
- [ ] Calculations match manual verification for all test scenarios
- [ ] Error messages provide clear, actionable guidance
- [ ] Conversation state persists across session interruptions
- [ ] UI displays real-time agent status and results
- [ ] Performance meets < 2 second response time per agent
- [ ] All unit and integration tests pass
- [ ] Load testing confirms 1000+ concurrent users supported

## All Needed Context

### Documentation & References (MUST READ)

```yaml
# CORE LANGGRAPH DOCUMENTATION
- url: https://langchain-ai.github.io/langgraph/
  why: Official LangGraph documentation for multi-agent orchestration patterns

- url: https://langchain-ai.github.io/langgraph/tutorials/
  why: Step-by-step tutorials for building agent systems - START HERE

- url: https://langchain-ai.github.io/langgraph/how-tos/
  why: Practical guides for state management, persistence, and error handling

# AGENT DESIGN PATTERNS
- url: https://langchain-ai.github.io/langgraph/concepts/
  why: Core concepts including nodes, edges, state, and checkpointing

- url: https://langchain-ai.github.io/langgraph/reference/
  why: API reference for StateGraph, Node, and Edge implementations

# PROJECT-SPECIFIC DOCUMENTATION
- file: /workspaces/hackathon_demo/PLANNING.md
  why: Complete project specifications with agent details and IRS rules

- file: examples/planner_flow.json
  why: Expected agent interaction sequences and state transitions

# IRS REGULATIONS
- url: https://www.irs.gov/pub/irs-drop/rp-24-25.pdf
  why: Official 2025 HSA contribution limits and rules

- url: https://www.irs.gov/publications/p969
  why: IRS Publication 969 - HSA rules including proration logic

# FRONTEND INTEGRATION
- url: https://streamlit.io/
  why: Potential UI framework for conversational interface

- url: https://gradio.app/
  why: Alternative UI framework with chat components

# GITHUB PATTERN MINING (Grep MCP)
- search: {"query": "langgraph multi-agent", "language": ["Python"], "path": ["src/", "lib/"]}
  why: Real-world LangGraph agent orchestration patterns and architectures

- search: {"query": "HSA calculation OR IRS limits", "language": ["Python", "JavaScript"]}
  why: Financial compliance implementations and calculation patterns

- search: {"query": "pytest factory-boy faker", "language": ["Python"], "path": ["tests/"]}
  why: Comprehensive testing patterns with mock data generation

- search: {"query": "sqlalchemy alembic migration", "language": ["Python"], "path": ["models/", "db/"]}
  why: Database schema management and migration patterns

- search: {"query": "streamlit gradio conversational", "language": ["Python"]}
  why: Conversational UI implementation patterns and best practices
```

### Current Codebase Tree (Initial state)

```bash
/workspaces/hackathon_demo/
├── PLANNING.md                 # Project specifications ← PRIMARY REFERENCE
├── PRPs/
│   └── templates/
│       └── prp_base.md        # This template
├── examples/
│   ├── planner_flow.json      # Agent interaction examples
│   └── ui_mockup.png          # UI design reference
└── README.md                  # Project overview
```

### Desired Codebase Tree (Target structure)

```bash
/workspaces/hackathon_demo/
├── src/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── user_input_agent.py    # Conversation management
│   │   ├── limit_calc_agent.py    # IRS limit calculations
│   │   └── planner_agent.py       # Recommendation engine
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user_profile.py        # Pydantic models for user data
│   │   ├── contribution_limits.py # IRS limit models
│   │   └── contribution_plan.py   # Output models
│   ├── orchestration/
│   │   ├── __init__.py
│   │   ├── graph_builder.py       # LangGraph setup
│   │   ├── state_manager.py       # Conversation state
│   │   └── error_handlers.py      # Recovery strategies
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── irs_rules.py           # IRS calculation logic
│   │   ├── validators.py          # Input validation
│   │   └── formatters.py          # Output formatting
│   └── ui/
│       ├── __init__.py
│       ├── app.py                 # Streamlit/Gradio app
│       └── components.py          # UI components
├── tests/
│   ├── unit/
│   │   ├── test_user_input_agent.py
│   │   ├── test_limit_calc_agent.py
│   │   ├── test_planner_agent.py
│   │   └── test_irs_rules.py
│   ├── integration/
│   │   ├── test_agent_handoffs.py
│   │   └── test_conversation_flow.py
│   └── e2e/
│       └── test_full_planning_flow.py
├── config/
│   ├── agent_config.yaml          # Agent parameters
│   └── irs_limits_2025.yaml       # IRS contribution limits
├── scripts/
│   ├── run_local.py               # Local development
│   └── deploy.py                  # Deployment script
├── requirements.txt               # Python dependencies
├── pyproject.toml                # Project configuration
└── .env.example                  # Environment variables
```

### Data Models & Types

```python
# Mock Data Factory Patterns
from factory import Factory, Faker, SubFactory, LazyAttribute
from factory.alchemy import SQLAlchemyModelFactory
import factory
from datetime import date, timedelta
import random

# Database Models
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class UserProfileDB(Base):
    __tablename__ = 'user_profiles'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True)
    coverage_type = Column(String)
    ytd_contribution = Column(Float)
    is_55_plus = Column(Boolean)
    remaining_pay_periods = Column(Integer)
    pay_frequency = Column(String)
    employer_contribution = Column(Float)
    plan_start_date = Column(Date)
    created_at = Column(Date)

# Factory for generating test data
class UserProfileFactory(SQLAlchemyModelFactory):
    class Meta:
        model = UserProfileDB
        sqlalchemy_session_persistence = 'commit'
    
    user_id = Faker('uuid4')
    coverage_type = factory.LazyFunction(lambda: random.choice(['self-only', 'family']))
    ytd_contribution = factory.LazyFunction(lambda: round(random.uniform(0, 7000), 2))
    is_55_plus = factory.LazyFunction(lambda: random.choice([True, False]))
    remaining_pay_periods = factory.LazyFunction(lambda: random.randint(1, 26))
    pay_frequency = factory.LazyFunction(lambda: random.choice(['biweekly', 'semi-monthly']))
    employer_contribution = factory.LazyFunction(lambda: round(random.uniform(0, 2000), 2))
    plan_start_date = factory.LazyFunction(lambda: date.today() - timedelta(days=random.randint(1, 300)))
    created_at = factory.LazyFunction(date.today)

# Scenario-based factories
class NewEnrollmentFactory(UserProfileFactory):
    """User just enrolled - no YTD contributions"""
    ytd_contribution = 0.0
    plan_start_date = factory.LazyFunction(date.today)
    remaining_pay_periods = factory.LazyFunction(lambda: random.randint(20, 26))

class ApproachingLimitFactory(UserProfileFactory):
    """User approaching contribution limit"""
    @factory.lazy_attribute
    def ytd_contribution(self):
        limit = 4300 if self.coverage_type == 'self-only' else 8550
        return round(limit * 0.85, 2)  # 85% of limit
    
    remaining_pay_periods = factory.LazyFunction(lambda: random.randint(3, 8))

class OverContributionFactory(UserProfileFactory):
    """User has over-contributed"""
    @factory.lazy_attribute
    def ytd_contribution(self):
        limit = 4300 if self.coverage_type == 'self-only' else 8550
        return round(limit * 1.1, 2)  # 110% of limit

# Test Data Builder Pattern
class HSATestDataBuilder:
    def __init__(self, session):
        self.session = session
        UserProfileFactory._meta.sqlalchemy_session = session
    
    def create_test_scenario(self, scenario: str):
        """Create predefined test scenarios"""
        scenarios = {
            'new_enrollment': NewEnrollmentFactory,
            'approaching_limit': ApproachingLimitFactory,
            'over_contribution': OverContributionFactory,
            'catch_up_eligible': lambda: UserProfileFactory(is_55_plus=True),
            'mid_year_change': lambda: UserProfileFactory(
                plan_start_date=date.today() - timedelta(days=180)
            )
        }
        
        factory = scenarios.get(scenario, UserProfileFactory)
        return factory() if callable(factory) else factory.create()
    
    def create_performance_dataset(self, count: int = 1000):
        """Create large dataset for performance testing"""
        return UserProfileFactory.create_batch(count)
    
    def reset_database(self):
        """Clean all test data"""
        self.session.query(UserProfileDB).delete()
        self.session.commit()

# SQLite Setup for Testing
def setup_test_database(in_memory: bool = True):
    """Setup SQLite database for testing"""
    if in_memory:
        engine = create_engine('sqlite:///:memory:')
    else:
        engine = create_engine('sqlite:///test_hsa.db')
    
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session(), engine

# Pytest Fixtures
import pytest

@pytest.fixture
def db_session():
    """Provide a transactional database session for tests"""
    session, engine = setup_test_database(in_memory=True)
    yield session
    session.close()
    engine.dispose()

@pytest.fixture
def test_data_builder(db_session):
    """Provide test data builder for tests"""
    return HSATestDataBuilder(db_session)

@pytest.fixture
def sample_users(test_data_builder):
    """Create a set of sample users for testing"""
    return {
        'new_user': test_data_builder.create_test_scenario('new_enrollment'),
        'near_limit': test_data_builder.create_test_scenario('approaching_limit'),
        'over_limit': test_data_builder.create_test_scenario('over_contribution'),
        'catch_up': test_data_builder.create_test_scenario('catch_up_eligible')
    }
```

### Known Gotchas & Critical LangGraph Patterns

```python
# CRITICAL: LangGraph State Management Patterns

# 1. ALWAYS define clear state schemas
from typing import TypedDict, List
from langgraph.graph import StateGraph

class ConversationState(TypedDict):
    user_profile: dict
    contribution_limits: dict
    contribution_plan: dict
    conversation_history: List[dict]
    current_agent: str
    error_state: dict

# 2. ALWAYS implement proper agent handoffs
def create_hsa_graph():
    graph = StateGraph(ConversationState)
    
    # Add nodes for each agent
    graph.add_node("user_input", user_input_agent)
    graph.add_node("limit_calc", limit_calc_agent)
    graph.add_node("planner", planner_agent)
    
    # Define edges with conditional logic
    graph.add_edge("user_input", "limit_calc")
    graph.add_edge("limit_calc", "planner")
    
    # Set entry point
    graph.set_entry_point("user_input")
    
    return graph.compile()

# 3. ALWAYS handle state persistence
from langgraph.checkpoint import MemorySaver

memory = MemorySaver()
graph = create_hsa_graph()
config = {"configurable": {"thread_id": "user-session-123"}}

# 4. ALWAYS validate state transitions
def user_input_agent(state: ConversationState):
    # Validate required fields before proceeding
    required_fields = ["coverage_type", "ytd_contribution", "remaining_pay_periods"]
    
    for field in required_fields:
        if field not in state["user_profile"]:
            return {"error_state": {"missing_field": field}}
    
    return {"current_agent": "limit_calc"}

# 5. ALWAYS implement error recovery
def limit_calc_agent(state: ConversationState):
    try:
        # Calculation logic
        limits = calculate_limits(state["user_profile"])
        return {"contribution_limits": limits, "current_agent": "planner"}
    except Exception as e:
        return {
            "error_state": {"error": str(e), "recovery_action": "retry"},
            "current_agent": "user_input"  # Fall back to data collection
        }
```

### DRY Pattern Validation & Code Reuse Strategy

**Pre-Implementation DRY Analysis:**
```markdown
# DRY Opportunity Assessment
- [ ] Search for similar HSA logic: `{"query": "HSA contribution calculation", "language": ["Python"], "path": ["src/", "lib/"]}`
- [ ] Find reusable financial utilities: `{"query": "financial calculation utility", "language": ["Python"], "path": ["utils/", "helpers/"]}`
- [ ] Identify common validation patterns: `{"query": "input validation OR user validation", "language": ["Python"]}`
- [ ] Check for existing agent patterns: `{"query": "langgraph agent pattern", "language": ["Python"], "path": ["agents/", "src/"]}`
- [ ] Locate shared database utilities: `{"query": "repository pattern OR database utility", "language": ["Python"]}`
```

**Code Reuse Requirements:**
1. **Before creating new functions**: Search for existing implementations that can be extended
2. **Extract common patterns**: Any logic used 3+ times must be extracted to utilities
3. **Single source configuration**: All IRS limits, dates, and constants in one place
4. **Shared validation logic**: Common input validation extracted to validators module
5. **Template reuse**: Agent response templates to ensure consistency

**DRY Implementation Checklist:**
- [ ] All IRS limits centralized in `config/hsa_limits.py`
- [ ] Common calculation logic extracted to `utils/calculations.py`
- [ ] Shared validation functions in `validators/hsa_validators.py`
- [ ] Repository pattern for all database access
- [ ] Agent message templates for consistent responses
- [ ] Test utilities and fixtures shared across test files

### External Pattern Validation (Grep MCP)

Before implementing any components, validate architectural decisions against proven patterns from millions of GitHub repositories:

#### Pre-Implementation Research Checklist
```markdown
# Agent Architecture Validation
- [ ] Search for similar LangGraph implementations: `{"query": "langgraph OR multi-agent system", "language": ["Python"], "path": ["src/"]}`
- [ ] Find agent orchestration patterns: `{"query": "agent OR workflow", "language": ["Python"], "useRegexp": true}`
- [ ] Research state management approaches: `{"query": "state management OR context", "language": ["Python"]}`

# Financial Domain Research  
- [ ] Find HSA/financial calculation patterns: `{"query": "HSA OR financial calculation", "language": ["Python", "JavaScript"]}`
- [ ] Research IRS compliance implementations: `{"query": "IRS OR tax calculation", "language": ["Python"]}`
- [ ] Discover proration logic examples: `{"query": "proration OR pro-rata", "language": ["Python"]}`

# Testing Strategy Validation
- [ ] Find comprehensive testing patterns: `{"query": "pytest OR testing", "language": ["Python"], "path": ["tests/", "test/"]}`
- [ ] Research mock data strategies: `{"query": "factory OR faker OR mock", "language": ["Python"]}`
- [ ] Discover database testing approaches: `{"query": "database test OR sqlalchemy test", "language": ["Python"]}`

# Performance & Optimization
- [ ] Research optimization techniques: `{"query": "performance optimization", "language": ["Python", "JavaScript"]}`
- [ ] Find caching strategies: `{"query": "cache OR memoization", "language": ["Python"]}`
- [ ] Discover async patterns: `{"query": "async OR asyncio", "language": ["Python"]}`
```

#### Pattern Integration Strategy
1. **Discovery Phase**: Use Grep MCP to find 3-5 similar implementations
2. **Analysis Phase**: Compare approaches and identify best practices
3. **Validation Phase**: Ensure chosen approach aligns with discovered patterns
4. **Implementation Phase**: Apply lessons learned from external research
5. **Optimization Phase**: Integrate performance patterns discovered

## Implementation Blueprint

### DRY Architecture Foundation

**Shared Utility Modules (Create First):**
```python
# config/hsa_limits.py - Single source of truth
HSA_LIMITS_2025 = {
    'self_only': 4300,
    'family': 8550,
    'catch_up': 1000,
    'age_threshold': 55
}

# utils/calculations.py - Reusable calculation logic
def calculate_remaining_contribution(ytd: float, annual_limit: float) -> float:
    """DRY: Used by all agents for remaining contribution calculation"""
    return max(0, annual_limit - ytd)

def calculate_per_period_amount(remaining: float, periods: int) -> float:
    """DRY: Used across multiple planning scenarios"""
    return remaining / periods if periods > 0 else 0

# validators/hsa_validators.py - Shared validation logic
def validate_coverage_type(coverage: str) -> bool:
    """DRY: Used by all agents for coverage validation"""
    return coverage in ['self-only', 'family']

def validate_contribution_amount(amount: float, limit: float) -> bool:
    """DRY: Used across input and calculation validation"""
    return 0 <= amount <= limit
```

**DRY Code Organization:**
```
src/
├── config/
│   ├── hsa_limits.py        # DRY: Single source IRS data
│   └── app_config.py        # DRY: Application constants
├── utils/
│   ├── calculations.py      # DRY: Shared calculation logic
│   ├── formatters.py        # DRY: Response formatting
│   └── date_utils.py        # DRY: Date handling utilities
├── validators/
│   └── hsa_validators.py    # DRY: Shared validation logic
├── repositories/
│   └── base_repository.py   # DRY: Common database operations
├── agents/
│   ├── base_agent.py        # DRY: Common agent functionality
│   ├── user_input_agent.py  # Extends base patterns
│   ├── limit_calc_agent.py  # Extends base patterns
│   └── planner_agent.py     # Extends base patterns
└── shared/
    ├── exceptions.py        # DRY: Common exception classes
    ├── message_types.py     # DRY: Agent communication schemas
    └── templates.py         # DRY: Response templates
```

### Data Models & Types

```python
# User Profile Models
from pydantic import BaseModel, Field, validator
from typing import Literal, Optional
from datetime import date

class UserProfile(BaseModel):
    coverage_type: Literal["self-only", "family"]
    ytd_contribution: float = Field(ge=0, description="Year-to-date HSA contributions")
    is_55_plus: bool = Field(default=False, description="Eligible for catch-up contributions")
    remaining_pay_periods: int = Field(ge=0, le=52, description="Pay periods left in year")
    pay_frequency: Literal["weekly", "biweekly", "semi-monthly", "monthly"]
    employer_contribution: Optional[float] = Field(default=0, ge=0)
    plan_start_date: Optional[date] = None
    
    @validator('ytd_contribution')
    def validate_contribution(cls, v):
        if v > 10000:  # Reasonable upper bound
            raise ValueError("YTD contribution seems unusually high")
        return v

# IRS Limit Models
class ContributionLimits(BaseModel):
    base_limit: float
    catch_up_amount: float = 0
    total_allowed: float
    remaining_contribution: float
    prorated: bool = False
    proration_months: Optional[int] = None
    warnings: List[str] = []

# Contribution Plan Models  
class PayPeriodContribution(BaseModel):
    period_number: int
    contribution_amount: float
    cumulative_total: float
    pay_date: Optional[date] = None

class ContributionPlan(BaseModel):
    per_paycheck_amount: float
    total_remaining: float
    contribution_schedule: List[PayPeriodContribution]
    recommendations: List[str]
    status: Literal["on-track", "at-risk", "over-limit"]
    
# Agent Message Models
class AgentMessage(BaseModel):
    agent_name: str
    message_type: Literal["question", "info", "error", "result"]
    content: str
    options: Optional[List[str]] = None
    metadata: dict = {}
```

### List of Tasks (Complete in order)

```yaml
Task 0 - Database & Mock Data Setup:
  Initialize Testing Infrastructure:
    - CREATE SQLite database schema in use-case/db/
    - IMPLEMENT database models with SQLAlchemy
    - CREATE Alembic migration scripts
    - SETUP test database factories
    - IMPLEMENT mock data generation utilities
    
  Create Mock Data Factories:
    - IMPLEMENT UserProfileFactory with Faker
    - CREATE scenario-based factories (new user, near limit, etc.)
    - ADD test data builder for complex scenarios
    - IMPLEMENT deterministic data generation (fixed seeds)
    - CREATE performance testing data generators
    
  Setup Test Fixtures:
    - CREATE pytest fixtures for database sessions
    - IMPLEMENT transactional test isolation
    - ADD fixture for common test scenarios
    - CREATE data cleanup utilities
    - IMPLEMENT fixture dependencies

Task 1 - Project Setup:
  Initialize Python Project:
    - CREATE virtual environment: python -m venv venv_linux
    - ACTIVATE environment: source venv_linux/bin/activate
    - CREATE requirements.txt with core dependencies:
      - langgraph>=0.2.0
      - langchain>=0.2.0
      - pydantic>=2.0
      - streamlit>=1.28.0 (or gradio>=4.0)
      - pytest>=7.0
      - python-dotenv
    - INSTALL dependencies: pip install -r requirements.txt
    - CREATE .env.example with required variables

  Setup Project Structure:
    - CREATE src/ directory tree as specified
    - CREATE __init__.py files in all packages
    - CREATE config files with 2025 IRS limits
    - SETUP logging configuration

Task 2 - Core Models Implementation:
  Create Pydantic Models:
    - IMPLEMENT UserProfile with validation
    - IMPLEMENT ContributionLimits with IRS rules
    - IMPLEMENT ContributionPlan with scheduling logic
    - ADD comprehensive validators for all fields
    - CREATE model factories for testing

  Create IRS Rules Engine:
    - IMPLEMENT 2025 contribution limit lookups
    - ADD catch-up contribution logic
    - IMPLEMENT proration calculations
    - ADD last-month rule handling
    - CREATE validation for edge cases

Task 3 - Agent Development:
  UserInputAgent Implementation:
    - CREATE conversational flow logic
    - IMPLEMENT question sequencing
    - ADD input validation and re-prompting
    - IMPLEMENT state updates
    - ADD conversation context tracking

  LimitCalcAgent Implementation:
    - CREATE limit calculation engine
    - IMPLEMENT IRS rule application
    - ADD proration logic
    - IMPLEMENT catch-up eligibility
    - ADD warning generation for edge cases

  PlannerAgent Implementation:
    - CREATE per-paycheck calculations
    - IMPLEMENT contribution scheduling
    - ADD recommendation engine
    - CREATE status determination logic
    - ADD visualization data preparation

Task 4 - LangGraph Orchestration:
  Create Graph Structure:
    - IMPLEMENT StateGraph with ConversationState
    - ADD all three agents as nodes
    - DEFINE edge logic and transitions
    - IMPLEMENT conditional routing
    - ADD state persistence with checkpointing

  Implement Error Handling:
    - CREATE fallback mechanisms
    - ADD retry logic with backoff
    - IMPLEMENT graceful degradation
    - ADD user-friendly error messages
    - CREATE recovery flows

Task 5 - Frontend Development:
  Create Streamlit/Gradio App:
    - IMPLEMENT chat interface
    - ADD agent status indicators
    - CREATE summary card component
    - ADD visual progress tracking
    - IMPLEMENT responsive design

  Connect to LangGraph:
    - CREATE session management
    - IMPLEMENT real-time updates
    - ADD state synchronization
    - CREATE conversation history display
    - ADD export functionality

Task 6 - Testing Suite:
  Unit Tests:
    - SETUP test database with mock data
    - TEST each agent independently with fixture data
    - TEST IRS calculation logic with edge case data
    - TEST input validation with invalid mock data
    - TEST error handling with database failures
    - TEST data persistence and retrieval
    - VERIFY mock data determinism
    - ACHIEVE 90%+ coverage

  Integration Tests:
    - TEST agent handoffs
    - TEST state persistence
    - TEST error recovery
    - TEST conversation flows
    - TEST edge cases

  End-to-End Tests:
    - TEST complete user journeys
    - TEST UI interactions
    - TEST performance under load
    - TEST session recovery
    - TEST data export

Task 7 - Production Readiness:
  Performance Optimization:
    - PROFILE agent response times
    - OPTIMIZE state operations
    - ADD caching where appropriate
    - IMPLEMENT connection pooling
    - MINIMIZE LLM calls

  Deployment Preparation:
    - CREATE Docker configuration
    - SETUP environment management
    - ADD health check endpoints
    - IMPLEMENT monitoring hooks
    - CREATE deployment scripts

  Documentation:
    - WRITE API documentation
    - CREATE user guides
    - ADD architecture diagrams
    - DOCUMENT deployment process
    - CREATE troubleshooting guide
```

### Per Task Implementation Details

```python
# Task 3 - UserInputAgent Implementation Pattern with Mock Data
from langgraph.graph import StateGraph
from typing import Dict, Any
from sqlalchemy.orm import Session

# Mock data integration for testing
def create_test_user_profiles(session: Session):
    """Create mock user profiles for testing agent interactions"""
    builder = HSATestDataBuilder(session)
    
    # Create diverse test scenarios
    test_users = [
        builder.create_test_scenario('new_enrollment'),
        builder.create_test_scenario('approaching_limit'),
        builder.create_test_scenario('mid_year_change'),
        builder.create_test_scenario('catch_up_eligible')
    ]
    
    return test_users

class UserInputAgent:
    def __init__(self):
        self.questions = [
            {
                "field": "coverage_type",
                "prompt": "Are you on self-only or family HSA coverage?",
                "options": ["self-only", "family"],
                "validator": lambda x: x in ["self-only", "family"]
            },
            {
                "field": "ytd_contribution",
                "prompt": "How much have you already contributed this year?",
                "validator": lambda x: float(x) >= 0
            },
            {
                "field": "is_55_plus", 
                "prompt": "Are you 55 or older? (eligible for catch-up contributions)",
                "options": ["yes", "no"],
                "validator": lambda x: x.lower() in ["yes", "no"]
            },
            {
                "field": "remaining_pay_periods",
                "prompt": "How many pay periods remain in the year?",
                "validator": lambda x: 0 <= int(x) <= 52
            }
        ]
        
    def __call__(self, state: ConversationState) -> Dict[str, Any]:
        user_profile = state.get("user_profile", {})
        conversation_history = state.get("conversation_history", [])
        
        # Find next unanswered question
        for question in self.questions:
            if question["field"] not in user_profile:
                # Add question to conversation
                conversation_history.append({
                    "role": "assistant",
                    "content": question["prompt"],
                    "options": question.get("options")
                })
                
                return {
                    "conversation_history": conversation_history,
                    "current_agent": "user_input",
                    "awaiting_input": question["field"]
                }
        
        # All questions answered, proceed to limit calculation
        return {
            "user_profile": user_profile,
            "current_agent": "limit_calc"
        }

# Task 3 - LimitCalcAgent Implementation Pattern
class LimitCalcAgent:
    def __init__(self):
        self.limits_2025 = {
            "self-only": 4300,
            "family": 8550,
            "catch_up": 1000
        }
        
    def calculate_proration(self, start_date: date, coverage_type: str) -> Dict[str, Any]:
        # Implement IRS last-month rule
        # Return prorated limits and warnings
        pass
        
    def __call__(self, state: ConversationState) -> Dict[str, Any]:
        user_profile = UserProfile(**state["user_profile"])
        
        # Calculate base limit
        base_limit = self.limits_2025[user_profile.coverage_type]
        
        # Add catch-up if eligible
        catch_up = self.limits_2025["catch_up"] if user_profile.is_55_plus else 0
        
        # Calculate total allowed
        total_allowed = base_limit + catch_up
        
        # Handle proration if needed
        if user_profile.plan_start_date:
            proration_result = self.calculate_proration(
                user_profile.plan_start_date,
                user_profile.coverage_type
            )
            total_allowed = proration_result["prorated_limit"]
        
        # Calculate remaining
        remaining = max(0, total_allowed - user_profile.ytd_contribution)
        
        limits = ContributionLimits(
            base_limit=base_limit,
            catch_up_amount=catch_up,
            total_allowed=total_allowed,
            remaining_contribution=remaining,
            warnings=[]
        )
        
        # Add warnings
        if user_profile.ytd_contribution > total_allowed:
            limits.warnings.append("You have already exceeded the annual limit!")
        
        return {
            "contribution_limits": limits.dict(),
            "current_agent": "planner"
        }

# Task 4 - Graph Creation Pattern
def create_hsa_planner_graph():
    # Initialize agents
    user_input = UserInputAgent()
    limit_calc = LimitCalcAgent()
    planner = PlannerAgent()
    
    # Create graph
    workflow = StateGraph(ConversationState)
    
    # Add nodes
    workflow.add_node("user_input", user_input)
    workflow.add_node("limit_calc", limit_calc)
    workflow.add_node("planner", planner)
    
    # Add edges
    workflow.add_conditional_edges(
        "user_input",
        lambda x: x["current_agent"],
        {
            "user_input": "user_input",  # Continue collecting input
            "limit_calc": "limit_calc"    # Move to calculation
        }
    )
    
    workflow.add_edge("limit_calc", "planner")
    workflow.add_edge("planner", END)
    
    # Set entry point
    workflow.set_entry_point("user_input")
    
    # Compile with checkpointing
    from langgraph.checkpoint.memory import MemorySaver
    memory = MemorySaver()
    
    return workflow.compile(checkpointer=memory)

# Task 5 - Streamlit UI Pattern
import streamlit as st
from streamlit_chat import message

def main():
    st.title("HSA Contribution Planner")
    
    # Initialize session state
    if "graph" not in st.session_state:
        st.session_state.graph = create_hsa_planner_graph()
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.messages = []
    
    # Display conversation
    for msg in st.session_state.messages:
        message(msg["content"], is_user=msg["role"] == "user")
    
    # Handle user input
    user_input = st.chat_input("Your response:")
    
    if user_input:
        # Add to messages
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Process with graph
        config = {"configurable": {"thread_id": st.session_state.thread_id}}
        result = st.session_state.graph.invoke(
            {"user_input": user_input},
            config
        )
        
        # Display agent response
        if "agent_message" in result:
            st.session_state.messages.append({
                "role": "assistant",
                "content": result["agent_message"]
            })
        
        # Display summary card if planning complete
        if result.get("current_agent") == "completed":
            display_summary_card(result["contribution_plan"])

def display_summary_card(plan: dict):
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Remaining Contribution",
            f"${plan['total_remaining']:,.2f}",
            delta=None
        )
    
    with col2:
        st.metric(
            "Per Paycheck",
            f"${plan['per_paycheck_amount']:,.2f}",
            delta=None
        )
    
    # Status indicator
    status_colors = {
        "on-track": "🟢",
        "at-risk": "🟡", 
        "over-limit": "🔴"
    }
    
    st.info(f"{status_colors[plan['status']]} Status: {plan['status'].title()}")
```

### Integration Points

```yaml
LANGGRAPH_CORE:
  - StateGraph: Central orchestration mechanism
  - Checkpointer: Conversation persistence across sessions
  - Conditional Edges: Dynamic routing based on state
  - Memory Management: Thread-based conversation isolation

LANGCHAIN_INTEGRATION:
  - LLM Integration: Optional for natural language processing
  - Prompt Templates: Structured agent responses
  - Output Parsers: Consistent message formatting
  - Callbacks: Monitoring and debugging

FRONTEND_FRAMEWORKS:
  - Streamlit: Rapid prototyping with chat components
  - Gradio: Alternative with built-in chat interface
  - FastAPI: Backend API for production deployment
  - WebSockets: Real-time conversation updates

DATA_PERSISTENCE:
  - PostgreSQL: User profiles and conversation history
  - SQLite: Local development and testing
  - File System: Checkpoint storage for development

```

## Validation Gate

### Level 0: Database & Mock Data Validation

```bash
# Verify database setup
python -c "from src.db.models import Base, engine; Base.metadata.create_all(engine)"

# Test mock data generation
pytest tests/test_mock_data.py -v

# Validate fixtures
pytest tests/test_fixtures.py -v

# Check data determinism
pytest tests/test_data_determinism.py -v --seed=42

# Expected: All database tables created, mock data generates consistently
# If errors: Check SQLAlchemy models, factory definitions
```

### Level 1: Code Quality & Type Safety

```bash
# Python type checking
mypy src/ --strict

# Code formatting
black src/ tests/
isort src/ tests/

# Linting
ruff check src/ tests/

# Expected: No type errors, consistent formatting
# If errors: Fix type annotations, resolve import issues
```

### Level 2: Unit Testing

```bash
# Run unit tests with coverage
pytest tests/unit/ -v --cov=src --cov-report=html

# Test individual agents
pytest tests/unit/test_user_input_agent.py -v
pytest tests/unit/test_limit_calc_agent.py -v
pytest tests/unit/test_planner_agent.py -v

# Expected: All tests pass, >90% coverage
# If failures: Fix agent logic, add missing test cases
```

### Level 3: Integration Testing

```bash
# Test agent orchestration
pytest tests/integration/test_agent_handoffs.py -v

# Test conversation flows
pytest tests/integration/test_conversation_flow.py -v

# Test state persistence
pytest tests/integration/test_state_persistence.py -v

# Expected: Smooth agent transitions, state consistency
# If failures: Check graph configuration, state schema
```

### Level 4: End-to-End Testing

```bash
# Run full conversation scenarios
pytest tests/e2e/ -v

# Test with example flows
python scripts/test_example_flows.py

# Manual UI testing
streamlit run src/ui/app.py

# Expected: Complete conversations work, UI responsive
# If issues: Debug conversation flow, fix UI updates
```

### Level 5: Performance Testing

```bash
# Load testing
locust -f tests/performance/locustfile.py --headless -u 100 -r 10 -t 60s

# Response time analysis
python scripts/analyze_performance.py

# Expected: <2s agent response, 1000+ concurrent users
# If slow: Optimize state operations, add caching
```

## Final Validation Checklist

### Core Functionality
- [ ] All three agents properly initialized and registered
- [ ] Agent handoffs work with state preservation
- [ ] IRS calculations accurate for all test cases
- [ ] Error messages clear and actionable
- [ ] UI displays real-time agent responses

### Testing & Quality
- [ ] Type checking passes: `mypy src/ --strict`
- [ ] Unit test coverage >90%: `pytest --cov`
- [ ] Integration tests pass: All agent interactions verified
- [ ] E2E scenarios complete successfully
- [ ] Performance meets <2s response requirement

### Production Readiness
- [ ] Logging configured for all agents
- [ ] Error tracking integrated
- [ ] Deployment scripts tested
- [ ] Documentation complete
- [ ] Security review passed

---

## Anti-Patterns to Avoid

### LangGraph-Specific
- ❌ Don't create circular dependencies between agents
- ❌ Don't modify state outside of agent functions
- ❌ Don't forget to handle partial state updates
- ❌ Don't skip state validation between agents
- ❌ Don't ignore checkpoint/persistence errors

### Agent Design
- ❌ Don't combine unrelated responsibilities in one agent
- ❌ Don't make agents dependent on specific UI implementations
- ❌ Don't hardcode IRS limits - use configuration files
- ❌ Don't skip input validation at agent boundaries
- ❌ Don't forget conversation context in error messages

### Testing & Development
- ❌ Don't test agents only in isolation - test orchestration
- ❌ Don't skip edge case testing (negative values, extreme inputs)
- ❌ Don't deploy without load testing conversation flows
- ❌ Don't ignore conversation state cleanup
- ❌ Don't forget to test session recovery scenarios