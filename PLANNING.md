## FEATURE:

**HSA Contribution Planner Agent Flow**

* **UserInputAgent**: Collects user responses for:
  - Coverage type (self-only or family)
  - Current year-to-date (YTD) contribution amount
  - Age 55+ status (optional, for catch-up contribution eligibility)
  - Number of pay periods remaining in the year

* **LimitCalcAgent**: Applies IRS contribution limits based on:
  - 2025 limits: $4,300 (self-only) / $8,550 (family)
  - Additional $1,000 catch-up contribution if age 55+
  - Proration calculations if plan type changed mid-year
  - Validates against IRS rules per [Fidelity][1] guidelines

* **PlannerAgent**: Performs calculations to:
  - Determine remaining allowable contribution amount
  - Suggest per-paycheck contribution to maximize annual HSA
  - Provide actionable guidance to reach contribution cap by year-end

**Frontend Chat UI**

* Form-based conversational prompts:
  - "Are you on self-only or family coverage?"
  - "How much have you already contributed this year?"
  - "Are you 55 or older? (eligible for catch-up contributions)"
  - "How many pay periods remain in the year?"
* Interactive summary card displaying:
  - *Remaining annual contribution allowance*
  - *Suggested per-paycheck contribution amount*
  - Visual indicators (green if on track, yellow if close, red if over limit)

## EXAMPLES:

In the `examples/` folder:

* `examples/planner_flow.json`: A LangGraph test flow demonstrating:
  - Complete user-agent interaction sequences
  - Expected intermediate agent messages and state transitions
  - Sample conversation flows for different user scenarios
  - Agent handoffs and data passing between UserInputAgent → LimitCalcAgent → PlannerAgent

* `examples/ui_mockup.png`: Screenshot of the chat UI featuring:
  - Conversational interface with agent responses
  - Summary card showing "You can contribute $2,150 more — that's about $90 over your 24 remaining paychecks."
  - Visual design and UX flow

These examples demonstrate expected agent choreography and UI output for implementation reference.

## DOCUMENTATION:

### IRS Resources
* **IRS HSA contribution limits (Rev. Proc. 2024-25)** – Official 2025 limits and catch-up contribution rules ([IRS][2])
* **IRS Publication 969** – Comprehensive guide on HSA rules including:
  - Last-month rule for mid-year enrollments
  - Proration logic for plan changes
  - Testing period requirements ([IRS][3])

### Financial Provider References
* **Fidelity HSA Guidelines** – Practical implementation of IRS rules and catch-up contributions ([Fidelity][1])
* **OptumBank HSA Resources** – Plan type specifications and contribution tracking ([Optum Bank][4])

### LangGraph Agent Architecture
* **Agent Communication Protocols**
  - Message passing specifications between agents
  - State management patterns for multi-agent systems
  - Event-driven architecture for agent coordination

* **State Management**
  - Conversation state persistence across agent handoffs
  - User session management and context preservation
  - Checkpointing for long-running conversations

* **Agent Workflow Orchestration**
  - Sequential flow: UserInput → LimitCalc → Planner
  - Conditional branching based on user responses
  - Error recovery and fallback paths

* **Message Schemas**
  - Input/output type definitions for each agent
  - Standardized error message formats
  - Inter-agent communication contracts

### API Specifications
* **Agent Interface Definitions**
  - UserInputAgent API: question prompts, response validation
  - LimitCalcAgent API: calculation inputs, limit outputs
  - PlannerAgent API: planning parameters, recommendation outputs

* **Backend Integration** (if applicable)
  - RESTful API endpoints for HSA data
  - Authentication and authorization flows
  - Data persistence layer specifications

### GitHub Pattern Research (Grep MCP)

**HSA & Financial Calculation Patterns**
* Search for existing HSA implementations: `{"query": "HSA calculation OR health savings", "language": ["Python", "JavaScript"]}`
* Find IRS compliance patterns: `{"query": "IRS calculation OR tax calculation", "language": ["Python"]}`
* Research proration logic: `{"query": "proration OR pro-rata calculation", "language": ["Python", "JavaScript"]}`
* Discover financial validation patterns: `{"query": "financial validation OR money calculation", "language": ["Python"]}`

**LangGraph & Multi-Agent Implementation Research**  
* Find LangGraph agent examples: `{"query": "langgraph OR langchain agent", "language": ["Python"], "path": ["src/", "agents/"]}`
* Research multi-agent orchestration: `{"query": "multi-agent OR agent workflow", "language": ["Python"], "useRegexp": true}`
* Discover state management patterns: `{"query": "state management OR conversation state", "language": ["Python"]}`
* Find agent communication protocols: `{"query": "agent communication OR message passing", "language": ["Python"]}`

**Conversational UI & Chat Implementation**
* Research Streamlit chat patterns: `{"query": "streamlit chat OR conversational", "language": ["Python"], "path": ["ui/", "app/"]}`
* Find form-based conversation flows: `{"query": "form conversation OR step-by-step", "language": ["Python", "JavaScript"]}`
* Discover user input validation: `{"query": "user input validation", "language": ["Python", "TypeScript"]}`

**Testing & Quality Assurance Patterns**
* Find agent testing strategies: `{"query": "agent test OR langgraph test", "language": ["Python"], "path": ["tests/"]}`
* Research financial calculation testing: `{"query": "financial test OR calculation test", "language": ["Python"]}`
* Discover mock data for financial apps: `{"query": "financial mock OR financial fixture", "language": ["Python"]}`

## DRY ARCHITECTURE CONSIDERATIONS:

### Pattern Library & Reusable Components
**HSA Calculation Pattern Reuse**
* **Common IRS Logic**: Create shared utility for standard calculations:
  - `hsa_limits.py` - Centralized 2025 limits and validation
  - `proration_calculator.py` - Reusable mid-year calculations  
  - `catch_up_validator.py` - Age-based eligibility logic
* **Database Pattern Reuse**: 
  - Repository pattern for all data access
  - Shared SQLAlchemy models across agents
  - Common transaction management utilities
* **Agent Communication DRY**: 
  - Standardized message schemas
  - Shared state validation functions
  - Common error handling patterns

**External Pattern Mining for DRY (Grep MCP)**
* **HSA Implementation Patterns**: `{"query": "HSA contribution calculation", "language": ["Python"], "path": ["src/", "lib/"]}`
* **Agent Communication DRY**: `{"query": "langgraph state management", "language": ["Python"], "useRegexp": true}`
* **Financial Validation Reuse**: `{"query": "financial validation utility", "language": ["Python"], "path": ["utils/"]}`
* **Database Pattern Library**: `{"query": "repository pattern sqlalchemy", "language": ["Python"], "path": ["models/", "db/"]}`

### Anti-Duplication Strategy
**Centralized Configuration**
* Single `config.py` for all IRS limits, dates, and constants
* Shared environment variable management
* Common logging configuration across all agents

**Shared Business Logic**
* Extract common validation rules into `validators/` module
* Create shared exception classes in `exceptions.py`
* Implement common audit logging patterns

**Template and Factory Patterns**
* Agent response templates to ensure consistent format
* Data factory patterns for test fixture generation
* Message builder utilities for inter-agent communication

## OTHER CONSIDERATIONS:

### Business Logic Considerations
* **Proration logic**: When users switch plan type mid-year, apply last-month rule based on IRS Pub 969—AI tools often miss this critical detail
* **Catch-up eligibility**: Only apply $1,000 extra if user is 55 or older by year-end; include explicit UI prompt or default to "no" with user override option
* **Pay period handling**: 
  - Clarify payment frequency (weekly/biweekly/semi-monthly/monthly)
  - Handle non-standard scenarios (e.g., 27 pay periods in a year)
  - Account for final paycheck timing vs. December 31 deadline

### Edge Cases
* **Over-contribution scenarios**: If user's YTD contribution ≥ limit, show clear warning and provide corrective action guidance
* **Negative contributions**: Handle payroll errors or HSA corrections gracefully
* **Mid-year changes**: Account for employment changes, coverage switches, or HSA provider changes
* **Employer contributions**: Option to include employer contributions in calculations

### Technical Considerations
* **Locale/date sensitivity**: 
  - Assume calendar year (Jan-Dec) for contribution limits
  - Handle fiscal year employers with clear messaging
  - Date format localization for international users

* **Frontend UX enhancements**:
  - Real-time validation of user inputs
  - Progress indicators during agent processing
  - Color-coded status indicators (green: on track, yellow: close to limit, red: over limit)
  - Mobile-responsive design for on-the-go planning

### LangGraph-Specific Considerations
* **Agent State Persistence**: Implement conversation checkpointing for resumable sessions
* **Async Communication**: Handle agent timeouts and long-running calculations
* **Retry Strategies**: Implement exponential backoff for failed agent calls
* **Monitoring**: Add telemetry for agent performance and error tracking
* **Testing Multi-Agent Systems**: 
  - Unit tests for individual agents
  - Integration tests for agent handoffs
  - End-to-end conversation flow tests
  - Load testing for concurrent user sessions

## AGENT SPECIFICATIONS:

### UserInputAgent
* **Purpose**: Gather required information from users through conversational interface
* **Inputs**: User messages, conversation history
* **Outputs**: Structured user data object containing:
  - coverage_type: "self-only" | "family"
  - ytd_contribution: number
  - is_55_plus: boolean
  - remaining_pay_periods: number
* **State Management**: Tracks which questions have been asked and validates responses
* **Error Handling**: Re-prompts for invalid inputs with helpful guidance

### LimitCalcAgent
* **Purpose**: Calculate HSA contribution limits based on IRS rules
* **Inputs**: User data from UserInputAgent
* **Outputs**: Limit calculation object containing:
  - annual_limit: number
  - catch_up_amount: number (if applicable)
  - total_allowed: number
  - remaining_contribution: number
* **State Management**: Caches IRS limit data, tracks calculation history
* **Error Handling**: Validates inputs against IRS rules, handles edge cases

### PlannerAgent
* **Purpose**: Generate actionable contribution recommendations
* **Inputs**: User data and limit calculations
* **Outputs**: Contribution plan containing:
  - per_paycheck_amount: number
  - total_remaining: number
  - contribution_schedule: array of payment dates and amounts
  - warnings: array of any concerns or limitations
* **State Management**: Maintains planning history for user
* **Error Handling**: Provides fallback recommendations for edge cases

## TEST DATA & DATABASE STRATEGY:

### Database Architecture

**SQLite Configuration:**
- **Development**: Local SQLite file (`dev_hsa.db`) with persistent test data
- **Testing**: In-memory SQLite (`:memory:`) for fast, isolated test runs
- **CI/CD**: Ephemeral SQLite instances with fixture data
- **Migration Tool**: Alembic for schema version control

### Mock Data Specifications by Agent

#### UserInputAgent Test Data
```python
# Mock conversation scenarios
USER_INPUT_SCENARIOS = {
    'happy_path': [
        {'coverage_type': 'family', 'ytd_contribution': 3000, 'is_55_plus': False, 'remaining_pay_periods': 12},
        {'coverage_type': 'self-only', 'ytd_contribution': 0, 'is_55_plus': True, 'remaining_pay_periods': 26}
    ],
    'edge_cases': [
        {'coverage_type': 'family', 'ytd_contribution': 8600, 'is_55_plus': True, 'remaining_pay_periods': 1},  # Over limit
        {'coverage_type': 'self-only', 'ytd_contribution': -100, 'is_55_plus': False, 'remaining_pay_periods': 0}  # Invalid
    ],
    'validation_tests': [
        {'coverage_type': 'invalid', 'ytd_contribution': 'abc', 'is_55_plus': 'maybe', 'remaining_pay_periods': 53}
    ]
}
```

#### LimitCalcAgent Test Data
```python
# IRS limit calculation test cases
LIMIT_CALC_SCENARIOS = {
    'standard_limits': [
        {'input': {'coverage': 'self-only', 'age_55_plus': False}, 'expected': 4300},
        {'input': {'coverage': 'family', 'age_55_plus': False}, 'expected': 8550},
        {'input': {'coverage': 'self-only', 'age_55_plus': True}, 'expected': 5300},
        {'input': {'coverage': 'family', 'age_55_plus': True}, 'expected': 9550}
    ],
    'proration_cases': [
        {'start_date': '2025-07-01', 'coverage': 'self-only', 'expected_limit': 2150},  # 6 months
        {'start_date': '2025-10-01', 'coverage': 'family', 'expected_limit': 2137.50}  # 3 months
    ],
    'last_month_rule': [
        {'enrollment_date': '2025-12-01', 'full_year_eligible': True, 'testing_period': True}
    ]
}
```

#### PlannerAgent Test Data
```python
# Contribution planning scenarios
PLANNER_SCENARIOS = {
    'contribution_schedules': [
        {
            'remaining_allowed': 2400,
            'pay_periods': 12,
            'frequency': 'biweekly',
            'expected_per_period': 200
        },
        {
            'remaining_allowed': 1000,
            'pay_periods': 26,
            'frequency': 'weekly',
            'expected_per_period': 38.46
        }
    ],
    'warning_scenarios': [
        {'ytd': 4500, 'limit': 4300, 'expected_warning': 'Over-contribution detected'},
        {'ytd': 4250, 'limit': 4300, 'periods': 2, 'expected_warning': 'Approaching limit'}
    ]
}
```

### Data Factory Implementation

```python
# Factory pattern for test data generation
from factory import Factory, Faker, Trait
import factory

class HSAUserFactory(Factory):
    class Meta:
        model = dict
    
    user_id = Faker('uuid4')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('email')
    coverage_type = factory.Iterator(['self-only', 'family'])
    ytd_contribution = factory.Faker('pyfloat', min_value=0, max_value=8000, right_digits=2)
    birth_date = Faker('date_of_birth', minimum_age=25, maximum_age=70)
    
    class Params:
        catch_up_eligible = Trait(
            birth_date=factory.Faker('date_of_birth', minimum_age=55, maximum_age=70)
        )
        new_enrollment = Trait(
            ytd_contribution=0,
            enrollment_date=factory.Faker('date_this_year')
        )
```

### Test Data Management

**Fixture Organization:**
```
use-case/tests/fixtures/
├── users/
│   ├── standard_users.json      # Basic test users
│   ├── edge_case_users.json     # Boundary condition users
│   └── performance_users.sql    # Large dataset for load testing
├── conversations/
│   ├── happy_path.json          # Successful conversation flows
│   ├── error_scenarios.json     # Error handling test cases
│   └── incomplete_flows.json    # Partial conversation states
└── calculations/
    ├── irs_limits_2025.json     # IRS limit test data
    ├── proration_cases.json     # Mid-year enrollment tests
    └── contribution_plans.json  # Expected calculation results
```

**Data Isolation Strategy:**
1. **Unit Tests**: Fresh in-memory database per test
2. **Integration Tests**: Transactional rollback after each test
3. **E2E Tests**: Dedicated test database with known state
4. **Performance Tests**: Pre-populated database with 10K+ records

### Mock External Dependencies

```python
# Mock IRS API responses (if applicable)
class MockIRSService:
    @staticmethod
    def get_contribution_limits(year: int, coverage_type: str):
        limits = {
            2025: {'self-only': 4300, 'family': 8550, 'catch_up': 1000}
        }
        return limits.get(year, {})

# Mock employer contribution data
class MockEmployerService:
    @staticmethod
    def get_employer_contribution(employer_id: str):
        # Return deterministic mock data based on employer_id hash
        return (hash(employer_id) % 2000) + 500  # $500-$2500 range
```

## DATA FLOW:

```
User → UserInputAgent
         ↓ (structured user data)
    LimitCalcAgent
         ↓ (contribution limits)
    PlannerAgent
         ↓ (contribution plan)
    Frontend UI ← (formatted recommendation)
```

### Inter-Agent Data Contracts
1. **UserInputAgent → LimitCalcAgent**:
   - Passes validated user profile data
   - Includes conversation context for audit trail

2. **LimitCalcAgent → PlannerAgent**:
   - Passes calculated limits and remaining allowance
   - Includes any warnings or special considerations

3. **PlannerAgent → Frontend**:
   - Passes formatted recommendation
   - Includes visualization data for UI components

## ERROR SCENARIOS:

### Common Failure Modes
1. **Invalid User Input**
   - Negative contribution amounts
   - Pay periods exceeding reasonable bounds
   - Non-numeric inputs where numbers expected

2. **Calculation Errors**
   - Division by zero (no remaining pay periods)
   - Overflow scenarios for large contributions
   - Proration calculation edge cases

3. **Agent Communication Failures**
   - Timeout between agent calls
   - Malformed message passing
   - State corruption during handoffs

### Recovery Strategies
* **Graceful Degradation**: Provide partial recommendations when full calculation impossible
* **User Guidance**: Clear error messages with actionable next steps
* **Fallback Flows**: Alternative calculation methods for edge cases
* **Audit Logging**: Track all errors for debugging and improvement

## DEPLOYMENT CONSIDERATIONS:

### Scalability
* **Horizontal Scaling**: Stateless agents allow easy scaling
* **Load Balancing**: Distribute user sessions across agent instances
* **Caching Strategy**: Cache IRS limits and common calculations

### Performance
* **Response Time Targets**: < 2 seconds for each agent response
* **Concurrent Users**: Support 1000+ simultaneous conversations
* **Resource Optimization**: Minimize LLM calls through smart prompting

### Monitoring & Observability
* **Metrics to Track**:
  - Agent response times
  - Conversation completion rates
  - Error rates by agent and error type
  - User satisfaction metrics

* **Logging Strategy**:
  - Structured logs for each agent interaction
  - Conversation flow tracking
  - Performance profiling data

### Security & Compliance
* **Data Protection**: Encrypt PII in transit and at rest
* **Audit Trail**: Maintain conversation history for compliance
* **Access Control**: Role-based permissions for admin functions
* **HIPAA Considerations**: If applicable, ensure PHI handling compliance
* **Test Data Compliance**: 
  - No real user data in test environments
  - Use Faker library for realistic but fake PII
  - Implement data anonymization for production data copies
  - Regular audit of test databases for PII leakage

### Database Performance Optimization

**Indexing Strategy:**
```sql
-- Critical indexes for HSA application
CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_user_profiles_coverage_type ON user_profiles(coverage_type);
CREATE INDEX idx_contributions_user_date ON contributions(user_id, contribution_date);
CREATE INDEX idx_calculations_created_at ON calculations(created_at DESC);
```

**Query Optimization:**
- Use prepared statements for repeated queries
- Implement query result caching for IRS limits
- Batch insert for performance test data
- Connection pooling for concurrent access

### Test Data Lifecycle

1. **Setup Phase**:
   - Run Alembic migrations
   - Load base fixture data
   - Generate scenario-specific data
   - Verify data integrity

2. **Test Execution**:
   - Isolate test data per test case
   - Use database transactions
   - Mock external service calls
   - Capture data state for debugging

3. **Cleanup Phase**:
   - Rollback transactions
   - Clear temporary data
   - Reset sequences/auto-increments
   - Verify no data leakage

4. **Maintenance**:
   - Version control fixture files
   - Update mock data for new features
   - Archive old test scenarios
   - Monitor test data growth

[1]: https://www.fidelity.com/learning-center/smart-money/hsa-contribution-limits?utm_source=chatgpt.com "HSA contribution limits and eligibility rules for 2025 and 2026"
[2]: https://www.irs.gov/pub/irs-drop/rp-24-25.pdf?utm_source=chatgpt.com "Rev. Proc. 2024-25"
[3]: https://www.irs.gov/publications/p969?utm_source=chatgpt.com "Publication 969 (2024), Health Savings Accounts and ..."
[4]: https://www.optumbank.com/resources/library/contribution-limits.html?utm_source=chatgpt.com "HSA Contribution Limits"