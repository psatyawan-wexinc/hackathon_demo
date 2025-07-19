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

[1]: https://www.fidelity.com/learning-center/smart-money/hsa-contribution-limits?utm_source=chatgpt.com "HSA contribution limits and eligibility rules for 2025 and 2026"
[2]: https://www.irs.gov/pub/irs-drop/rp-24-25.pdf?utm_source=chatgpt.com "Rev. Proc. 2024-25"
[3]: https://www.irs.gov/publications/p969?utm_source=chatgpt.com "Publication 969 (2024), Health Savings Accounts and ..."
[4]: https://www.optumbank.com/resources/library/contribution-limits.html?utm_source=chatgpt.com "HSA Contribution Limits"