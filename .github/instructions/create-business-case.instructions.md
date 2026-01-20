# Rule: Generating a Business Case Document

## Goal

To guide an AI assistant in creating a detailed Business Case document in Markdown format, based on an initial user prompt. The Business Case should be clear, compelling, and suitable for convincing key decision-makers of the merits of a particular course of action.

## What is a Business Case?

A decision-making tool used to determine the effects a particular decision will have on profitability and organizational success. It is intended to convince key decision-makers of the merits of a particular course of action before the project is started.

## Process

1. **Receive Initial Prompt:** The user provides a brief description of a problem, opportunity, or proposed project.
2. **Ask Clarifying Questions:** Before writing the Business Case, the AI _must_ ask clarifying questions following the 5 phases approach. Make sure to provide options in letter/number lists so the user can respond easily with their selections.
3. **Generate Business Case:** Based on the initial prompt and the user's answers, generate a Business Case using the structure outlined below.
4. **Save Business Case:** Save the generated document as `[n]-bc-[project-name].md` inside the `/business-cases` directory. (Where `n` is a zero-padded 4-digit sequence starting from 0001, e.g., `0001-bc-inventory-system.md`, `0002-bc-customer-portal.md`, etc.)

## The 5 Phases to an Effective Business Case

### Phase 1 - Initial Analysis

- Thoroughly understand the problem or opportunity
- Determine high level requirements
- Identify data needed to support the business case (ROI)
- Validate with decision makers if the high level return is worth the potential investment
- Analyze likelihood project will be approved

### Phase 2 - Determine Potential Solutions

- Identify all possible solutions to the problem (including doing nothing)
- For each solution, analyze:
  - Benefits
  - Costs
  - Timetable of project
  - Time before a return on investment is realized
  - Risks

### Phase 3 - Write the Business Case

- Create comprehensive document with all sections
- Ensure clarity and persuasiveness
- Support claims with data and analysis

### Phase 4 - Review Business Case

- Validate problem statement justifies a call to action
- Ensure all valid solutions are given
- Double check cost-benefit analysis calculations
- Objectively dissect your recommendation
- Correct any spelling or grammatical mistakes

### Phase 5 - Present the Business Case

- Clearly define the problem and business need to act
- Give your recommendation
- Explain the return on investment (ROI)
- Touch on each risk
- Summarize the benefits and ROI

## Clarifying Questions (Examples)

The AI should adapt its questions based on the prompt and follow the 5 phases approach:

### Understanding the Business Objective

- **Purpose:** "What is the purpose of this project? What problem are we trying to solve or what opportunity are we pursuing?"
- **Goals & Objectives:** "What are the specific goals and objectives of this project?"
- **Success Definition:** "In the eyes of this project, what is success, and how will it be measured?"

### Problem/Opportunity Analysis

- **Current State:** "What is the current situation? What pain points or inefficiencies exist?"
- **Impact:** "What is the business impact of not addressing this problem?"
- **Urgency:** "How urgent is this issue? What happens if we delay action?"

### Solution Options

- **Alternatives:** "What alternative solutions have been considered? (We should always include 'do nothing' as an option)"
- **Preferred Solution:** "Do you have a preferred solution? Why?"

### Financial Analysis

- **Costs:** "What are the estimated costs (initial investment, ongoing costs, resource requirements)?"
- **Benefits:** "What are the expected benefits (revenue increase, cost savings, efficiency gains)?"
- **Timeline:** "What is the expected timeline for implementation and for realizing ROI?"

### Stakeholders

- **Decision Makers:** "Who are the key decision-makers who need to approve this?"
- **Impacted Parties:** "Who will be affected by this project (team members, customers, suppliers, etc.)?"
- **Support:** "Do you have buy-in from any key stakeholders already?"

### Risks & Constraints

- **Risks:** "What are the main risks associated with this project?"
- **Constraints:** "Are there any technical, budgetary, or timeline constraints we should be aware of?"

## Business Case Structure

The generated Business Case should include the following sections:

### 1. Executive Summary

A concise overview (1-2 paragraphs) that captures:

- The problem or opportunity
- The recommended solution
- The expected ROI and key benefits
- Call to action

### 2. Problem Statement / Business Need

Clearly define:

- The current situation and its business impact
- Why action is needed now
- What happens if no action is taken

### 3. Business Objectives

List specific, measurable objectives such as:

- Increase revenue by X%
- Reduce costs by Y
- Improve efficiency/customer satisfaction
- Meet regulatory requirements

### 4. Analysis of Current Situation

Provide context including:

- Current processes and their limitations
- Market conditions or competitive pressures
- Data supporting the need for change

### 5. Solution Options

For each potential solution (including "do nothing"), describe:

- Overview of the solution
- Benefits
- Costs (initial and ongoing)
- Implementation timeline
- Time to ROI
- Risks and mitigation strategies

### 6. Cost-Benefit Analysis

Provide detailed financial analysis:

- Total cost of ownership
- Expected benefits (quantified)
- Break-even analysis
- ROI calculation
- Payback period

### 7. Recommendation

- Clearly state the recommended course of action
- Explain why this is the best option
- Reference key stakeholder support if available

### 8. Implementation Approach (High-Level)

- Major phases or milestones
- Key resources needed
- Critical success factors

### 9. Risk Assessment

- Identify major risks
- Likelihood and impact of each risk
- Mitigation strategies

### 10. Success Metrics

Define how success will be measured:

- Key Performance Indicators (KPIs)
- Measurement methods
- Target values and timeframes

### 11. Stakeholder Impact

Identify stakeholders using RACI concepts where relevant:

- Who will be **Responsible** for execution
- Who is **Accountable** for outcomes
- Who should be **Consulted**
- Who needs to be **Informed**

### 12. Next Steps & Timeline

- Immediate actions required
- Decision needed by (date)
- Proposed project start date

### 13. Appendices (Optional)

- Detailed financial models
- Market research
- Technical specifications
- Supporting documentation

## Target Audience

Assume the primary readers are **business executives and key decision-makers**. Therefore:

- Use clear, business-focused language
- Lead with benefits and ROI
- Support claims with data
- Be concise but thorough
- Avoid excessive technical jargon
- Focus on business value, not technical details

## Output

- **Format:** Markdown (`.md`)
- **Location:** `/business-cases/`
- **Filename:** `[n]-bc-[project-name].md`

## Key Principles

1. **Be Data-Driven:** Support all claims with data, metrics, and research
2. **Be Objective:** Present all viable options, even if you have a preference
3. **Focus on ROI:** Decision-makers care most about return on investment
4. **Address Risks:** Don't hide risks; show you've thought them through
5. **Get Buy-in:** Mention stakeholder support to build credibility
6. **Be Clear:** Write for busy executives who may only read the executive summary

## Final Instructions

1. Do NOT start implementing the project
2. Make sure to ask the user clarifying questions following the 5 phases
3. Take the user's answers to the clarifying questions and create a comprehensive, persuasive Business Case
4. Remember: One of the solution options should always be "do nothing" to provide a baseline for comparison
5. Focus on convincing decision-makers why this project deserves investment
