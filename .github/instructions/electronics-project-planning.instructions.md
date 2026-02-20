---
applyTo: '**/electronics-project-plan-*/**'
description: Standards for planning electronics/embedded systems projects for junior developers
name: Electronics Project Planning Standards
---

# Electronics Project Planning Standards

## Purpose

These standards guide the creation of comprehensive implementation plans for electronics and embedded systems projects. Plans must be detailed enough for a junior developer to follow from start to finish, covering hardware, firmware, and software integration.

## Target Audience

All plans assume the implementing developer is **junior-level**. This means:

- No assumed prior knowledge of electronics, protocols, or embedded development
- Every task must include prerequisite concepts with learning resources
- Jargon must be explained in a glossary
- Tasks must be decomposed to atomic level (one clear action per task)

## Technology Stack Defaults

Unless the project specifies otherwise, prefer:

| Layer                 | Default              | Alternatives                    |
| --------------------- | -------------------- | ------------------------------- |
| Microcontroller       | ESP32 (DevKit v1)    | Arduino Mega, Raspberry Pi Pico |
| Single-board computer | Raspberry Pi 4/5     | Raspberry Pi Zero 2W            |
| IDE                   | PlatformIO (VS Code) | Arduino IDE                     |
| Communication         | MQTT over WiFi       | Serial, BLE, OSC                |
| PCB Design            | KiCad                | EasyEDA                         |
| Version Control       | Git                  | —                               |

## Plan Output Structure

Every plan must be a **single markdown file** with the following sections in order:

### 1. Executive Summary

- Project name and date
- Brief description (2-3 sentences)
- Overall complexity rating: 🟢 Simple / 🟡 Moderate / 🔴 Complex
- Estimated total duration
- Key risks summary

### 2. System Architecture

- High-level block diagram (ASCII or Mermaid)
- Communication protocols between subsystems
- Power distribution overview
- Data flow description

### 3. Challenge Breakdown

For **each challenge/subsystem**, include:

#### 3.1. Overview

- Objective (what does it do?)
- Difficulty: 🟢 Easy / 🟡 Medium / 🔴 Advanced
- Estimated duration

#### 3.2. Requirements

- Functional requirements (what it must do)
- Non-functional requirements (performance, safety, noise tolerance)
- Constraints and restrictions

#### 3.3. Component Selection

| Component       | Model/Part Number | Qty | Est. Cost (€) | Datasheet Link | Purpose         |
| --------------- | ----------------- | --- | ------------- | -------------- | --------------- |
| Microcontroller | ESP32 DevKit v1   | 1   | ~8€           | [link]         | Main controller |

- Justification for each key component choice
- Alternative components if primary is unavailable

#### 3.4. Circuit/Wiring Notes

- Pin mapping table (GPIO → Component)
- Wiring considerations (pull-ups, decoupling capacitors, etc.)
- Safety notes (max voltage, current limits)
- Reference schematic description or link

#### 3.5. Firmware Tasks

Each task must follow this format:

```markdown
- [ ] **Task Title** 🟢/🟡/🔴
  - **What**: Clear description of what to implement
  - **Why**: Purpose and context
  - **Prerequisites**: Concepts to understand first
  - **Resources**: Links to tutorials, docs, examples
  - **Steps**:
    1. Step-by-step instructions
    2. With specific file names, function names, pin numbers
    3. Including expected output/behavior
  - **Definition of Done**: Exact criteria to verify completion
  - **Estimated time**: X hours
```

#### 3.6. Software Integration Tasks

Same format as firmware tasks, for the host/server side.

#### 3.7. Risks & Mitigations

| Risk                            | Probability | Impact | Mitigation                                  |
| ------------------------------- | ----------- | ------ | ------------------------------------------- |
| False touch readings due to EMI | Medium      | High   | Add filtering capacitors, software debounce |

### 4. Technology Decision Matrix

When multiple technologies could solve the same problem, present a comparison:

```markdown
| Criteria            | Option A | Option B | Option C |
| ------------------- | -------- | -------- | -------- |
| Cost                | €X       | €Y       | €Z       |
| Complexity          | 🟢       | 🟡       | 🔴       |
| Performance         | Good     | Better   | Best     |
| Junior-friendliness | High     | Medium   | Low      |
| **Recommendation**  | ✅       |          |          |
```

### 5. Implementation Roadmap

Must be organized in **sequential phases** with explicit dependencies:

```markdown
## Phase 1: Environment Setup (Week 1)

**Dependencies**: None
**Goal**: Developer has working dev environment

- [ ] Task 1.1 ...
- [ ] Task 1.2 ...

## Phase 2: Prototyping (Week 2-3)

**Dependencies**: Phase 1 complete
**Goal**: Each subsystem working independently on breadboard

- [ ] Task 2.1 ...
```

Phases should follow this general progression:

1. **Environment Setup** — Tools, IDE, libraries, board testing
2. **Component Testing** — Individual component validation on breadboard
3. **Subsystem Prototyping** — Each challenge as standalone prototype
4. **Integration** — Subsystems communicating together
5. **Enclosure & Wiring** — Physical assembly, cable management
6. **Testing & Validation** — Full system testing, edge cases
7. **Documentation & Handover** — Code comments, user manual, maintenance guide

### 6. Testing & Validation Plan

For each subsystem:

```markdown
| Test            | Type | Input            | Expected Output                | Pass Criteria               |
| --------------- | ---- | ---------------- | ------------------------------ | --------------------------- |
| Touch detection | Unit | Finger on zone A | Serial prints "Zone A touched" | 95% accuracy over 20 trials |
```

### 7. Learning Path

Ordered list of topics the junior developer should study **before starting implementation**:

```markdown
### Week 0: Foundations (before Phase 1)

1. **Arduino/ESP32 Basics**
   - What to learn: Digital I/O, analogRead, Serial Monitor
   - Resource: [ESP32 Getting Started](url)
   - Practice: Blink LED, read potentiometer

2. **Basic Electronics**
   - What to learn: Ohm's law, voltage dividers, pull-up resistors
   - Resource: [Electronics Tutorial](url)
   - Practice: Build voltage divider on breadboard
```

### 8. Glossary

Alphabetical list of technical terms used in the plan:

```markdown
| Term | Definition                                                                                        |
| ---- | ------------------------------------------------------------------------------------------------- |
| ADC  | Analog-to-Digital Converter — converts analog voltage (0-3.3V) to digital value (0-4095 on ESP32) |
| BLE  | Bluetooth Low Energy — low-power wireless protocol for short-range communication                  |
```

## Difficulty Classification

Use consistent difficulty markers:

- 🟢 **Easy** — Standard library usage, well-documented, copy-paste examples available
- 🟡 **Medium** — Requires understanding of underlying concepts, some debugging expected
- 🔴 **Advanced** — Complex integration, limited documentation, requires electrical/signal knowledge

## Estimation Guidelines

| Task Type             | Junior Multiplier    |
| --------------------- | -------------------- |
| Environment setup     | 1.5x normal estimate |
| Library integration   | 2x normal estimate   |
| Custom firmware logic | 2.5x normal estimate |
| Hardware debugging    | 3x normal estimate   |
| System integration    | 2x normal estimate   |

Always add a **20% buffer** to total estimation for unexpected issues.

## Safety Standards

Every plan involving mains voltage (AC), motors, or high-current loads MUST include:

- ⚡ Clear safety warnings with specific voltages/currents
- Galvanic isolation requirements
- Fuse/overcurrent protection specifications
- Emergency stop (E-STOP) considerations for moving parts
- Thermal protection for power components
- Reference to applicable standards (CE, IEC 61010, etc.)

## Quality Checklist

Before delivering a plan, verify:

- [ ] Every task has a Definition of Done
- [ ] Every component has a datasheet link or reference
- [ ] Every advanced concept has a learning resource linked
- [ ] All tasks have difficulty ratings
- [ ] All tasks have time estimates
- [ ] Dependencies between phases are explicit
- [ ] Safety warnings are present for AC/high-current sections
- [ ] Glossary covers all technical terms used
- [ ] BOM is complete with estimated costs
- [ ] Architecture diagram is present
