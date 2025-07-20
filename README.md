# HSA Contribution Planner - Context Engineering Demo

A comprehensive demonstration of Context Engineering principles applied to building an HSA (Health Savings Account) Contribution Planner using LangGraph multi-agent orchestration, Test-Driven Development, DRY (Don't Repeat Yourself) methodology, and MCP (Model Context Protocol) integration.

> **This project showcases how Context Engineering with DRY principles and proper tooling enables AI assistants to build complex, production-ready applications in a single pass.**

## 🎯 Project Overview

The HSA Contribution Planner helps users optimize their Health Savings Account contributions for tax benefits. It features:

- **Three Specialized LangGraph Agents**:
  - `UserInputAgent`: Conversational data collection
  - `LimitCalcAgent`: IRS 2025 limit calculations with catch-up provisions
  - `PlannerAgent`: Per-paycheck contribution recommendations
  
- **IRS Compliance**: Implements 2025 contribution limits ($4,300 self-only / $8,550 family)
- **Smart Calculations**: Handles proration, catch-up contributions (55+), and mid-year changes
- **Conversational UI**: Natural language interface with visual progress indicators

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/psatyawan-wexinc/hackathon_demo.git
cd hackathon_demo

# 2. Verify MCP setup (required for Claude Code)
# The project includes 4 pre-configured MCP servers:
# - Memory Bank: Cross-session context persistence
# - Knowledge Graph: Architectural knowledge management  
# - Playwright: Web testing automation
# - Perplexity: Real-time documentation research
cat .mcp.json  # View MCP configuration

# 3. Set up Python environment
python -m venv venv_linux
source venv_linux/bin/activate

# 4. Create your feature specification
# Edit PLANNING.md with your requirements (HSA planner already configured)

# 5. Generate a comprehensive PRP (Product Requirements Prompt)
# In Claude Code, run:
/generate-prp PLANNING.md

# 6. Execute the PRP with TDD methodology
# In Claude Code, run:
/execute-prp PRPs/hsa-contribution-planner.md
```

## 📁 Project Structure

```
hackathon_demo/
├── .claude/                      # Claude Code configuration
│   ├── commands/
│   │   ├── generate-prp.md      # Enhanced PRP generation with MCP
│   │   └── execute-prp.md       # TDD execution with validation
│   ├── config.json              # MCP server configurations
│   └── settings.local.json      # Claude Code permissions
├── .mcp.json                    # MCP server definitions
├── CLAUDE.md                    # Global rules (TDD, MCP, structure)
├── PLANNING.md                  # HSA planner specifications
├── PRPs/                        # Product Requirements Prompts
│   └── templates/
│       └── prp_base.md          # LangGraph HSA template
├── docs/                        # Architecture documentation
├── examples/                    # Reference implementations
├── mcp-integration/             # MCP setup and tools
│   ├── memory-bank/             # Persistent context storage
│   └── scripts/                 # MCP utilities
└── use-case/                    # ⚠️ ALL CODE GOES HERE ⚠️
    ├── src/                     # Implementation code
    ├── tests/                   # Test files (TDD mandatory)
    └── config/                  # Configuration files
```

### ⚠️ Critical Directory Rule

**ALL project code MUST be created within `/workspaces/hackathon_demo/use-case/`**

This includes:
- Source code (`src/`)
- Test files (`tests/`)
- Configuration files
- Documentation
- Any project-related files

## 🔄 Development Workflow

### 1. Understand the Rules (CLAUDE.md)

The project enforces strict guidelines:

- **Test-Driven Development**: Write tests first, always
- **DRY Principles**: Don't Repeat Yourself - comprehensive code reuse strategy
- **MCP Integration**: Use Memory Bank and Knowledge Graph throughout
- **Directory Structure**: All code in `/use-case` folder
- **Coverage Requirements**: Minimum 80%, target 95%
- **Python Environment**: Use `venv_linux` for all commands

### 2. Create Feature Specification (PLANNING.md)

The HSA planner specification includes:

```markdown
## FEATURE:
**HSA Contribution Planner Agent Flow**
- UserInputAgent: Collects coverage type, YTD contributions, age, pay periods
- LimitCalcAgent: Applies IRS 2025 limits with catch-up calculations
- PlannerAgent: Generates per-paycheck recommendations

## EXAMPLES:
- examples/planner_flow.json: LangGraph agent orchestration
- examples/ui_mockup.png: Conversational UI design

## DOCUMENTATION:
- IRS resources for 2025 limits
- LangGraph multi-agent patterns
- State management specifications
```

### 3. Generate PRP (Product Requirements Prompt)

The `/generate-prp` command:
1. Loads MCP context (Memory Bank, Knowledge Graph)
2. Researches codebase patterns and documentation
3. Creates comprehensive implementation blueprint
4. Enforces TDD task ordering
5. Validates against all project rules
6. Scores confidence (1-10) for one-pass success

### 4. Execute with TDD Cycle

The `/execute-prp` command follows strict TDD:

```
For each component:
1. Write failing tests → 2. Run tests (RED) → 3. Implement code → 
4. Run tests (GREEN) → 5. Refactor → 6. Validate coverage
```

Validation includes:
- Syntax checking (ruff, mypy)
- Unit tests with coverage
- Integration tests
- Performance validation

## 🔌 MCP Integration

### Memory Bank
- Maintains context across Claude Code sessions
- Tracks progress and decisions
- Updates active context with next steps

```python
# Start of session
mcp__memory-bank__read_memory_bank_file("active-context")

# During work
mcp__memory-bank__track_progress("Implemented UserInputAgent", "All tests passing")

# End of session
mcp__memory-bank__update_active_context(tasks=["..."], nextSteps=["..."])
```

### Knowledge Graph
- Captures architectural decisions
- Links components and relationships
- Enables knowledge queries

```python
mcp__knowledge-graph__create_entities([{
    name: "UserInputAgent",
    entityType: "agent",
    observations: ["Handles conversation flow", "Validates user inputs"]
}])
```

### Additional MCP Tools
- **Playwright**: Automated testing of conversational UI
- **Perplexity**: Latest LangGraph documentation and patterns
- **Grep MCP**: GitHub pattern mining for code reuse discovery
- **IDE**: Code diagnostics before test execution

## 🔄 DRY (Don't Repeat Yourself) Principles

### Core DRY Philosophy

The project implements comprehensive DRY principles to eliminate code duplication and promote pattern reuse:

- **Pattern Recognition First**: Search existing patterns before writing new code
- **Code Reuse Over Creation**: Extend existing functions/classes instead of duplicates
- **Single Source of Truth**: Centralize configurations, constants, and repeated logic
- **Shared Utilities**: Extract common functionality to reusable modules

### DRY Implementation Strategy

#### 1. Pattern Discovery Workflow
```bash
# Before coding, search for existing patterns
rg "[functionality]" src/ --type py
grep -r "pattern_name" src/

# External pattern validation via Grep MCP
{"query": "[feature] implementation", "language": ["Python"], "path": ["src/", "utils/"]}
```

#### 2. Anti-Duplication Architecture
```python
# ✅ DO: Centralized configuration
# config/hsa_limits.py
HSA_LIMITS_2025 = {
    'self_only': 4300,
    'family': 8550,
    'catch_up': 1000
}

# ✅ DO: Shared utility functions
# utils/calculations.py
def calculate_remaining_contribution(ytd: float, annual_limit: float) -> float:
    """DRY: Used by all agents for remaining contribution calculation"""
    return max(0, annual_limit - ytd)

# ✅ DO: Repository pattern inheritance
class BaseRepository(ABC):
    # Common database operations
    
class UserProfileRepository(BaseRepository):
    # Specific user operations extending base
```

#### 3. DRY Validation Gates

The project includes automated DRY compliance checking:

```bash
# Check for code duplication
rg -C 3 "def.*calculate.*contribution" src/
rg "import.*config" src/

# Validate single source of truth
find src/ -name "*.py" -exec grep -l "HSA_LIMIT\|4300\|8550" {} \;
# Should only return config files
```

### DRY Quality Metrics

- **Code reuse ratio**: >70% of functionality extends existing patterns
- **Duplication detection**: <5% duplicate code blocks >3 lines
- **Configuration centralization**: 100% of config values in single source
- **Pattern consistency**: >90% adherence to established patterns

### DRY in Frontend Components

```typescript
// ✅ DO: Compound component pattern
const Form = ({ children, onSubmit }) => (
  <form onSubmit={onSubmit} className="space-y-6">{children}</form>
)

Form.Field = ({ label, error, children }) => (
  <div className="space-y-2">
    <Label>{label}</Label>
    {children}
    {error && <p className="text-destructive">{error}</p>}
  </div>
)

// Usage across multiple forms (DRY)
<Form onSubmit={handleSubmit}>
  <Form.Field label="Email" error={errors.email}>
    <Input {...emailProps} />
  </Form.Field>
</Form>
```

## 🧪 Test-Driven Development

### The TDD Cycle (Mandatory)

1. **Red Phase**: Write failing tests first
   ```python
   def test_user_input_agent_validates_coverage_type():
       agent = UserInputAgent()
       with pytest.raises(ValidationError):
           agent.validate_coverage("invalid")
   ```

2. **Green Phase**: Minimal code to pass
   ```python
   def validate_coverage(self, coverage_type: str):
       if coverage_type not in ["self-only", "family"]:
           raise ValidationError("Invalid coverage type")
   ```

3. **Refactor Phase**: Improve while keeping tests green

### Coverage Requirements
- Minimum: 80% (enforced)
- Target: 95% (recommended)
- Focus on: Happy paths, edge cases, error handling

## 📋 Best Practices

### Context Engineering Principles

1. **Comprehensive Context**: Include all documentation, examples, and patterns
2. **DRY-First Development**: Search and reuse before creating new code
3. **Validation Gates**: Automated checks at each step including DRY compliance
4. **Self-Correcting**: Error patterns guide fixes and refactoring opportunities
5. **One-Pass Success**: Complete context enables single-pass implementation

### PRP Quality Metrics

- **Score 10**: All context included, clear TDD path, comprehensive tests
- **Score 7-9**: Minor gaps but implementable
- **Score <7**: Needs more research before execution

### Common Patterns

1. **DRY Agent Architecture**
   ```python
   # Base agent with shared functionality
   class BaseAgent(ABC):
       def __init__(self, config: HSAConfig):
           self.config = config
           self.validator = HSAValidator()
       
       @abstractmethod
       def process(self, state: ConversationState) -> dict:
           pass
   
   # Specific agents extending base
   class UserInputAgent(BaseAgent):
       def process(self, state: ConversationState) -> dict:
           # Agent-specific logic using shared utilities
           pass
   ```

2. **Agent State Management**
   ```python
   class ConversationState(TypedDict):
       user_profile: dict
       contribution_limits: dict
       current_agent: str
   ```

3. **Shared Utilities Pattern**
   ```python
   # Single source of truth for calculations
   from src.utils.calculations import calculate_remaining_contribution
   from src.config.hsa_limits import HSA_LIMITS_2025
   from src.validators.hsa_validators import validate_coverage_type
   ```

4. **Error Recovery**
   - Path errors: Move files to `/use-case`
   - Test failures: Review expectations
   - Coverage gaps: Add edge case tests
   - DRY violations: Extract duplicated code to utilities

## 🔗 Resources

### Project Documentation
- [CLAUDE.md](/CLAUDE.md) - Global project rules with DRY principles
- [PLANNING.md](/PLANNING.md) - HSA planner specifications with DRY architecture
- [Optimization Principles](/docs/optimization-principles.md) - LEVER framework with DRY methodology
- [Frontend DRY Guidelines](/docs/front-end-optimization-principles.md) - Component reuse patterns
- [MCP Setup Guide](/mcp-integration/docs/mcp-setup.md)

### External Resources
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [IRS Publication 969](https://www.irs.gov/publications/p969) - HSA Rules
- [IRS Rev. Proc. 2024-25](https://www.irs.gov/pub/irs-drop/rp-24-25.pdf) - 2025 Limits
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)

### Example Implementations
- `/examples/planner_flow.json` - Agent orchestration patterns
- `/examples/ui_mockup.png` - UI/UX reference design
- `/PRPs/templates/prp_base.md` - LangGraph-specific PRP template

---

*This project demonstrates the power of Context Engineering: providing AI assistants with comprehensive context, clear rules, and validation gates to build production-ready applications efficiently.*