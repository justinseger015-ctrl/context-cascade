---
name: cognitive-lensing
description: >
  Cross-lingual cognitive framing system that activates different reasoning
  patterns by embedding multi-lingual activation phrases. Use when facing
  complex tasks that benefit from specific thinking patterns: completion
  tracking (Russian), source verification (Turkish), audience calibration
  (Japanese), semantic analysis (Arabic), object comparison (Mandarin),
  spatial reasoning (Guugu Yimithirr), numerical precision (Chinese/Japanese).
version: 1.0.1
category: foundry
tags:
  - cognitive-science
  - cross-lingual
  - meta-prompting
  - frame-selection
  - reasoning-enhancement
mcp_servers:
  required: [memory-mcp]
  optional: [sequential-thinking]
cognitive_frame:
  primary: none
  rationale: "Meta-skill that selects frames for other skills"
---

# Cognitive-Lensing v1.0.0

## Purpose

This skill activates specific cognitive patterns by embedding multi-lingual activation phrases that elicit different parts of the AI's latent space. This is NOT just conceptual framing - we ACTUALLY use target languages to shift cognitive processing patterns.

### Core Mechanism

Large language models trained on multilingual corpora develop language-specific reasoning patterns tied to grammatical structures:

- **Turkish evidential markers** activate source-attribution patterns
- **Russian aspectual verbs** activate completion-state tracking
- **Japanese honorific levels** activate audience-awareness calibration
- **Arabic morphological roots** activate semantic decomposition
- **Mandarin classifiers** activate object-category reasoning
- **Guugu Yimithirr cardinal directions** activate absolute spatial encoding
- **Chinese/Japanese number systems** activate transparent place-value arithmetic

By embedding authentic multi-lingual text in prompts, we trigger these latent reasoning modes.

### When to Use This Skill

Use cognitive-lensing when:

1. **Task complexity exceeds single-frame capacity** - Multi-dimensional problems requiring different cognitive modes
2. **Quality requirements demand specific reasoning** - Audit (evidential), deployment (aspectual), documentation (hierarchical)
3. **Standard prompting produces generic outputs** - Need to activate specialized thinking patterns
4. **Creating new skills/agents** - Select optimal cognitive frame for the domain
5. **Debugging AI reasoning failures** - Wrong frame may cause systematic errors

### What This Skill Does

1. **Analyzes task goals** (1st/2nd/3rd order) to identify required thinking patterns
2. **Selects optimal cognitive frame(s)** from 7 available patterns
3. **Generates multi-lingual activation text** that triggers the frame
4. **Integrates with other foundry skills** (prompt-architect, agent-creator, skill-forge)
5. **Stores frame selections in memory-mcp** for consistency across sessions

---

## Goal-Based Frame Selection Checklist

### Step 1: Analyze Goals

Complete this for every non-trivial task:

| Order | Question | Your Answer |
|-------|----------|-------------|
| 1st Order Goal | What is the IMMEDIATE task? | _______________ |
| 2nd Order Goal | WHY are we doing this task? | _______________ |
| 3rd Order Goal | What is the ULTIMATE outcome? | _______________ |

**Example Analysis**:

| Order | Question | Answer |
|-------|----------|--------|
| 1st Order | Immediate task | Write unit tests for API endpoint |
| 2nd Order | Why | Verify endpoint behavior is correct |
| 3rd Order | Ultimate outcome | Ensure production reliability |

### Step 2: Identify Dominant Thought Process

| Question | If YES, Use Frame |
|----------|-------------------|
| Is tracking "done vs not done" critical? | Aspectual (Russian) |
| Is source reliability critical? | Evidential (Turkish) |
| Is audience/formality critical? | Hierarchical (Japanese) |
| Is semantic decomposition needed? | Morphological (Arabic/Hebrew) |
| Is physical/visual comparison needed? | Classifier (Mandarin) |
| Is spatial navigation needed? | Spatial-Absolute (Guugu Yimithirr) |
| Is mathematical precision needed? | Numerical-Transparent (Chinese/Japanese) |

**Example Selection**:

For "Write unit tests for API endpoint":
- Tracking done/not done: YES (need to track test coverage completion)
- Source reliability: YES (need to verify test assertions match specs)

Selected Frames:
- Primary: Aspectual (Russian) - for completion tracking
- Secondary: Evidential (Turkish) - for assertion verification

### Step 3: Select Primary Frame

Based on analysis, select:
- **Primary Frame**: _______________
- **Secondary Frame (optional)**: _______________
- **Rationale**: _______________

---

## Seven Frame Activation Protocols

### Frame 1: Evidential (Turkish - Kanitsal Cerceve)

**When to Use**:
- Research and fact-checking tasks
- Audit and compliance work
- Source verification
- Claim validation
- Documentation review
- Code review (verifying claims about behavior)

**Linguistic Basis**:

Turkish requires grammatical evidential markers on every verb:
- **-DI** (direct): Speaker witnessed the event firsthand
- **-mIs** (indirect): Speaker inferred or was told about the event

This grammatical requirement trains speakers to constantly track information sources.

**Activation Protocol**:

```markdown
## Kanitsal Cerceve Aktivasyonu

Bu gorev icin her iddia kaynaklandirilmalidir:

Kaynak Turleri:
- DOGRUDAN (-DI): Ben bizzat gordum/test ettim
- CIKARIM (-mIs): Kanitlardan cikarim yaptim
- BILDIRILEN (-mIs): Dokumantasyon/baskasi soyledi

Her iddia icin sunu belirtin:
1. Iddia nedir?
2. Kaynak turu nedir? (DOGRUDAN/CIKARIM/BILDIRILEN)
3. Kanitlar nelerdir?

English Markers:
- [DIRECT]: "I tested this myself"
- [INFERRED]: "Evidence suggests..."
- [REPORTED]: "Documentation states..."
```

**Example Usage**:

```markdown
## Code Review with Evidential Frame

## Kanitsal Cerceve Aktivasyonu

Bu kod incelemesi icin her iddia kaynaklandirilmalidir.

Review the authentication middleware:

1. **Claim**: "This middleware validates JWT tokens"
   - **Source Type**: [DIRECT] - I read the code and tested the function
   - **Evidence**: Lines 23-45 show jwt.verify() call with error handling

2. **Claim**: "This follows OAuth 2.0 spec"
   - **Source Type**: [INFERRED] - Code structure matches RFC patterns
   - **Evidence**: Token validation, scope checking, expiry verification align with RFC 6749

3. **Claim**: "This handles refresh tokens"
   - **Source Type**: [REPORTED] - Documentation states this feature exists
   - **Evidence**: README.md line 67, but NO CODE FOUND - DISCREPANCY DETECTED
```

**Integration Points**:
- Use with `code-review-assistant` agent
- Use with `security-audit` skill
- Use with `documentation-validator` skill

---

### Frame 2: Aspectual (Russian - Aspektual'naya Ramka)

**When to Use**:
- Build and deployment pipelines
- Task tracking and progress reporting
- Completion verification
- State management
- CI/CD workflows
- Multi-step processes

**Linguistic Basis**:

Russian verbs have two forms for every action:
- **Sovershennyy Vid (SV)**: Perfective - action is COMPLETED, focus on result
- **Nesovershennyy Vid (NSV)**: Imperfective - action is ONGOING, focus on process

This grammatical distinction trains speakers to constantly track completion states.

**Activation Protocol**:

```markdown
## Aspektual'naya Ramka Aktivatsiya

Etot zadacha trebuyet otslezhivaniya zavershennosti:

Tipy Aspekta:
- SV (Sovershennyy Vid): Polnost'yu zaversheno, mozhno prodolzhat'
- NSV (Nesovershennyy Vid): V protsesse, ne zaversheno
- BLOCKED: Ozhidayet zavisimosti

Dlya kazhdogo shaga ukazhite:
1. Shag nomer
2. Aspekt (SV/NSV/BLOCKED)
3. Usloviya zavershennosti

English Markers:
- [SV:COMPLETED]: Task fully done, move on
- [NSV:IN_PROGRESS]: Task ongoing, not finished
- [BLOCKED]: Waiting on dependencies
```

**Example Usage**:

```markdown
## Deployment Pipeline with Aspectual Frame

## Aspektual'naya Ramka Aktivatsiya

Etot deployment trebuyet chetkoye otslezhivaniye zavershennosti.

Pipeline Status:

1. **Build Docker Image**
   - Aspect: [SV:COMPLETED]
   - Completion Criteria: Image tagged and pushed to registry
   - Evidence: docker-image-id: sha256:abc123...

2. **Run Integration Tests**
   - Aspect: [NSV:IN_PROGRESS]
   - Completion Criteria: All tests pass with >80% coverage
   - Current State: 45/60 tests passed, running...

3. **Deploy to Staging**
   - Aspect: [BLOCKED]
   - Completion Criteria: Integration tests pass AND security scan complete
   - Blocker: Waiting on Step 2 completion

4. **Security Scan**
   - Aspect: [NSV:IN_PROGRESS]
   - Completion Criteria: No HIGH vulnerabilities, <5 MEDIUM
   - Current State: Scanning dependencies...
```

**Integration Points**:
- Use with `ci-cd-orchestrator` agent
- Use with `deployment-manager` skill
- Use with TodoWrite tool (maps to pending/in_progress/completed)

---

### Frame 3: Hierarchical (Japanese - Keigo Wakugumi)

**When to Use**:
- Stakeholder communication
- Formal documentation
- Audience-calibrated output
- Executive summaries
- User-facing content
- Cross-functional collaboration

**Linguistic Basis**:

Japanese has three grammatical levels of formality:
- **Sonkeigo**: Respectful language (elevates listener)
- **Kenjougo**: Humble language (lowers speaker)
- **Teineigo**: Polite language (neutral professional)

This grammatical requirement trains speakers to constantly model the audience's social position.

**Activation Protocol**:

```markdown
## Keigo Wakugumi Aktiveshon

Kono tasuku wa taishouzentai ni awaseta rejisutaa wo hitsuyou to shimasu:

Rejisutaa Shurui:
- Sonkeigo: Keiei-sha, gaibu patonaazu (executives, external partners)
- Kenjougo: Jibun no koudou (humble self-reference)
- Teineigo: Hyoujun bijinesu (standard professional)

Kakutei subeki koto:
1. Taishouzentai wa dare desu ka?
2. Kankeishi wa nan desu ka?
3. Mokuteki wa nan desu ka?

English Markers:
- [SONKEIGO]: Formal, respectful (executives, clients)
- [TEINEIGO]: Professional, polite (colleagues)
- [CASUAL]: Informal (personal notes, internal tools)
```

**Example Usage**:

```markdown
## API Documentation with Hierarchical Frame

## Keigo Wakugumi Aktiveshon

Kono dokumento wa betsu no taishouzentai ni muketeirukara, rejisutaa wo chosei shimasu.

### For Executive Summary (SONKEIGO)

**Overview of Authentication System**

This system will provide secure access control for your organization's resources. The architecture has been designed with scalability and compliance in mind, ensuring alignment with your strategic objectives.

**Key Benefits**:
- Enhanced security posture through multi-factor authentication
- Compliance with SOC2 and ISO27001 requirements
- Seamless integration with existing infrastructure

### For Developer Documentation (TEINEIGO)

**Authentication Middleware Setup**

This middleware validates JWT tokens for protected routes. Please follow these steps:

1. Install the package: `npm install @org/auth-middleware`
2. Configure environment variables
3. Add middleware to your Express app

**Configuration Options**:
- `tokenSecret`: Your JWT signing secret
- `tokenExpiry`: Token lifetime in seconds
- `refreshEnabled`: Enable refresh token flow

### For Internal Notes (CASUAL)

**Auth Middleware TODO**

- Fix that weird edge case with expired tokens
- Need to add rate limiting
- Remember to update tests when we ship v2
```

**Integration Points**:
- Use with `documentation-generator` skill
- Use with `stakeholder-communicator` agent
- Use with `content-writer` skill

---

### Frame 4: Morphological (Arabic - Al-Itar al-Sarfi)

**When to Use**:
- Concept mapping and taxonomy
- Semantic analysis
- Etymology tracing
- Terminology development
- Domain modeling
- Ontology construction

**Linguistic Basis**:

Arabic words are constructed from 3-letter roots with patterns applied:
- **Root K-T-B** (writing): kitab (book), katib (writer), maktub (written), maktaba (library)
- **Root '-L-M** (knowledge): 'ilm (knowledge), 'alim (scholar), mu'allim (teacher)

This morphological system trains speakers to see semantic relationships through shared roots.

**Activation Protocol**:

```markdown
## Al-Itar al-Sarfi al-Tanshit

Hadhihi al-mahimma tatatallab tahlil al-judur:

Anmat al-Judur:
- Kull kalima min jadhr thalathi (every word from 3-letter root)
- Al-jadhr yarbut al-ma'ani al-murtabita (root connects related meanings)
- Tahlil al-namt yakshif al-'alaqat (pattern analysis reveals relationships)

Mithal (Example):
- K-T-B: kitab (book), katib (writer), maktub (written), maktaba (library)
- '-L-M: 'ilm (knowledge), 'alim (scholar), mu'allim (teacher), ta'lim (education)

Lil-tatbiq:
1. Hadd al-jadhr lil-mafhum (Identify root of concept)
2. Ijad al-kalimat al-muratabita (Find related terms from same root)
3. Rasm al-'alaqat al-daliliya (Map semantic relationships)

English Application:
- Identify root pattern in concept
- Map related terms from same root
- Reveal hidden semantic connections
```

**Example Usage**:

```markdown
## Domain Modeling with Morphological Frame

## Al-Itar al-Sarfi al-Tanshit

Hadhihi al-mahimma tatatallab tahlil al-judur lil-nizam al-authentication.

### Authentication Domain - Root Analysis

**Root AUTH (authority, author)**:
- **authenticate**: Verify authority/authorship
- **authorization**: Grant authority
- **author**: Original creator (authority over content)
- **authority**: Power to enforce rules
- **authoritative**: Having definitive authority

**Semantic Relationships**:
```
       AUTH (root concept: rightful power)
          |
    +-----+-----+-----+
    |     |     |     |
  authenticate authorization author authority
    |           |          |         |
  "verify     "grant    "create   "enforce
   power"      power"    with      power"
                         power"
```

**Root CRED (belief, trust)**:
- **credential**: Evidence worthy of belief
- **credibility**: Quality of being believable
- **credit**: Trust extended (financial)
- **creed**: System of beliefs

**Domain Model**:
- **Authentication** (AUTH root): Proving identity = verifying authority over account
- **Credentials** (CRED root): Evidence = trust-worthy proof
- **Authorization** (AUTH root): Granting access = delegating authority

**Insight**: Authentication and Authorization share AUTH root because both deal with rightful power - one verifies it, the other grants it.
```

**Integration Points**:
- Use with `domain-modeler` agent
- Use with `terminology-manager` skill
- Use with `ontology-builder` skill

---

### Frame 5: Classifier (Mandarin - Liangci Kuangjia)

**When to Use**:
- System design and architecture
- Object comparison
- Visual reasoning
- Categorization tasks
- Data modeling
- UI/UX design

**Linguistic Basis**:

Mandarin requires classifiers (measure words) between numbers/demonstratives and nouns:
- **Zhang** (flat things): yi zhang zhi (one sheet paper), san zhang zhao (three photos)
- **Ben** (bound volumes): liang ben shu (two books)
- **Tiao** (long things): yi tiao lu (one road), yi tiao he (one river)
- **Ge** (general): yi ge ren (one person)
- **Tai** (machines): yi tai diannao (one computer)

This grammatical requirement trains speakers to constantly categorize objects by physical properties.

**Activation Protocol**:

```markdown
## Liangci Kuangjia Jihuo

Zhe ge renwu xuyao anzhao xingzhuang/leibie fenlei:

Liangci Leixing:
- Zhang: Pingmian de (flat - documents, tables, images)
- Ben: Shuben leixing (bound - books, reports, notebooks)
- Tiao: Changxing de (long - paths, pipelines, rivers)
- Ge: Tongxing de (general - abstract concepts, entities)
- Tai: Jiqi de (machines - computers, servers, devices)
- Jian: Shiwu/xiangmu (items, projects, tasks)
- Zhi: Dongwu/shengwu (animals, agents, processes)

Duiyu mei ge duixiang:
1. Xingzhuang/xingzhi shi shenme?
2. Na ge liangci zui heshi?
3. Weishenme zhe ge fenlei you yongchu?

English Application:
- APIs are TIAO (path-like, route-based)
- Documents are ZHANG (flat, 2D)
- Databases are GE (abstract entities)
- Servers are TAI (machine-like)
- Services are ZHI (living processes)
- Features are JIAN (discrete items)
```

**Example Usage**:

```markdown
## System Architecture with Classifier Frame

## Liangci Kuangjia Jihuo

Zhe ge xitong sheji xuyao anzhao xingzhuang fenlei.

### System Components - Classifier Analysis

**API Gateway** (TIAO - path-like):
- Property: Routes requests like a road/river
- Classifier: Yi tiao API gateway
- Design Implication: Focus on flow, branching, throughput
- Metaphor: River with tributaries

**Database** (GE - abstract entity):
- Property: Abstract data container
- Classifier: Yi ge database
- Design Implication: Focus on relationships, constraints, integrity
- Metaphor: Container of structured information

**Servers** (TAI - machines):
- Property: Physical/virtual machines
- Classifier: San tai server
- Design Implication: Focus on capacity, redundancy, hardware
- Metaphor: Factory machines

**Authentication Service** (ZHI - living process):
- Property: Active, responsive, autonomous
- Classifier: Yi zhi authentication service
- Design Implication: Focus on behavior, lifecycle, health
- Metaphor: Guard dog or sentinel

**Documentation** (ZHANG - flat):
- Property: 2D, page-based
- Classifier: Wu zhang documentation
- Design Implication: Focus on layout, hierarchy, navigation
- Metaphor: Layered sheets

**Feature Requests** (JIAN - discrete items):
- Property: Countable, independent items
- Classifier: Shi jian feature request
- Design Implication: Focus on prioritization, completion, inventory
- Metaphor: Items on a conveyor belt

### Architectural Insight

The classifier analysis reveals:
- **TIAO components** (API Gateway) need flow optimization
- **TAI components** (Servers) need capacity planning
- **ZHI components** (Services) need health monitoring
- **ZHANG components** (Docs) need information architecture
- **JIAN components** (Features) need project management
```

**Integration Points**:
- Use with `system-architect` agent
- Use with `data-modeler` skill
- Use with `ui-designer` skill

---

### Frame 6: Spatial-Absolute (Guugu Yimithirr)

**When to Use**:
- Navigation and routing
- Orientation-independent memory
- Geographical reasoning
- Location-based systems
- Network topology
- Data flow analysis

**Linguistic Basis**:

Guugu Yimithirr (Australian Aboriginal language) has NO relative spatial terms (left/right/front/back). All spatial relationships use cardinal directions:
- "The cup is NORTH of the plate"
- "Move the file EAST on the desk"
- "My brother is standing SOUTH of the tree"

This linguistic constraint trains speakers to maintain constant cardinal orientation awareness.

**Activation Protocol**:

```markdown
## Spatial-Absolute Activation

This task requires cardinal-only encoding (no relative directions):

Position Markers:
- NORTH: Absolute north direction
- SOUTH: Absolute south direction
- EAST: Absolute east direction
- WEST: Absolute west direction

NEVER use:
- "left/right" (relative to observer)
- "in front/behind" (relative to facing)
- "up/down" in horizontal contexts

For every spatial relationship:
1. What is the absolute direction?
2. What is the reference frame?
3. How does this persist across viewpoints?

English Application:
- "The API endpoint is NORTH of the authentication layer"
- "Data flows EAST from input to output"
- "The error originates SOUTH in the stack"
```

**Example Usage**:

```markdown
## Network Topology with Spatial-Absolute Frame

## Spatial-Absolute Activation

This network topology requires cardinal-only encoding.

### System Layout (Cardinal Frame)

```
                    NORTH
                      |
            +-------------------+
            |   Load Balancer   |
            +-------------------+
                      |
        WEST --------+ +-------- EAST
                      |
        +-------------+-------------+
        |                           |
   +---------+               +---------+
   | Server1 |               | Server2 |
   +---------+               +---------+
        |                           |
        +-------------+-------------+
                      |
                 +----------+
                 | Database |
                 +----------+
                      |
                    SOUTH
```

**Component Relationships**:

1. **Load Balancer** is NORTH of both servers
2. **Server1** is WEST of Server2
3. **Server2** is EAST of Server1
4. **Database** is SOUTH of both servers
5. **Data flows SOUTH** from Load Balancer through servers to database
6. **Response flows NORTH** from database through servers to Load Balancer

**Routing Rules** (Cardinal-Based):

- Requests enter from NORTH (Load Balancer)
- Traffic splits EAST-WEST (Server1 vs Server2)
- Persistence layer is SOUTH (Database)
- Errors propagate NORTH (up the stack)

**Navigation Instructions**:

"To debug authentication failure:
1. Start at Load Balancer (NORTH)
2. Trace SOUTH to Server1 or Server2
3. Continue SOUTH to Database connection
4. Error is SOUTH of the JWT validation layer"

**Benefit**: This cardinal encoding is observer-independent. No matter which component you're "looking from", the directions remain consistent.
```

**Integration Points**:
- Use with `network-architect` agent
- Use with `routing-optimizer` skill
- Use with `topology-mapper` skill

---

### Frame 7: Numerical-Transparent (Chinese/Japanese)

**When to Use**:
- Mathematical calculations
- Quantitative analysis
- Metrics and statistics
- Financial computations
- Performance optimization
- Algorithmic complexity analysis

**Linguistic Basis**:

Chinese and Japanese number systems are base-10 transparent:
- English: "eleven" (opaque, doesn't mean "ten-one")
- Chinese: "shi yi" (literally "ten one")
- English: "twenty-three" (semi-opaque)
- Chinese: "er shi san" (literally "two ten three")

This transparent structure makes place value explicit at every step.

**Activation Protocol**:

```markdown
## Numerical-Transparent Activation (Suuji Toumei Wakugumi)

Kono keisan wa meikakuna ichi-keta hyouji wo hitsuyou to shimasu:

Structure:
- Explicit place value at every step
- No hidden carries or borrows
- Show intermediate calculations
- Verify by digit position

Example (32 x 15):
32 x 15 = 32 x (10 + 5)
       = 32 x 10 + 32 x 5
       = 3 x 10 x 10 + 2 x 10 + 3 x 10 x 5 + 2 x 5
       = 300 + 20 + 150 + 10
       = 480

English Application:
- Make place values explicit (ones, tens, hundreds)
- Show all intermediate steps
- Verify by column/position
- No mental arithmetic shortcuts
```

**Example Usage**:

```markdown
## Performance Metrics with Numerical-Transparent Frame

## Suuji Toumei Wakugumi Aktiveshon

Kono performance bunseki wa meikakuna keta-betsu keisan wo hitsuyou to shimasu.

### Latency Calculation

**Scenario**: API handles 1,250 requests/minute, average processing time 45ms

**Calculate total processing time per minute**:

```
Total Time = Requests x Time per Request
           = 1,250 x 45ms

Step 1: Break into place values
1,250 = 1,000 + 200 + 50
45    = 40 + 5

Step 2: Distribute multiplication
= (1,000 + 200 + 50) x (40 + 5)
= (1,000 x 40) + (1,000 x 5) + (200 x 40) + (200 x 5) + (50 x 40) + (50 x 5)
= 40,000 + 5,000 + 8,000 + 1,000 + 2,000 + 250
= 56,250ms
= 56.25s

Step 3: Verify by position
Ones place: 0 + 0 + 0 + 0 + 0 + 0 = 0
Tens place: 0 + 0 + 0 + 0 + 0 + 5 = 5
Hundreds place: 0 + 0 + 0 + 0 + 0 + 2 = 2
Thousands place: 0 + 5 + 8 + 1 + 2 + 0 = 16 (carry 1)
Ten-thousands place: 4 + 0 + 0 + 0 + 0 + 0 + 1 = 5
Result: 56,250ms VERIFIED
```

**Insight**: 56.25s of processing in 60s window = 93.75% CPU utilization (near capacity)

### Big-O Complexity Analysis

**Algorithm**: Nested loop processing N items

```
for i in range(N):          # N iterations
    for j in range(N):      # N iterations per i
        process(i, j)       # constant time

Total Operations = N x N
                 = N^2

For N = 100:
= 100 x 100
= (100) x (100)
= (10 x 10) x (10 x 10)
= 10^2 x 10^2
= 10^4
= 10,000 operations

For N = 1,000:
= 1,000 x 1,000
= (10 x 10 x 10) x (10 x 10 x 10)
= 10^3 x 10^3
= 10^6
= 1,000,000 operations (100x increase for 10x data)
```

**Benefit**: Explicit place-value calculation reveals scaling properties clearly.
```

**Integration Points**:
- Use with `performance-analyzer` agent
- Use with `metrics-calculator` skill
- Use with `algorithm-optimizer` skill

---

## Integration with Foundry Skills

### Integration with intent-analyzer (Phase 1)

The intent-analyzer should invoke cognitive-lensing when:

1. **Goal complexity detected** - User request has multiple implicit objectives
2. **Quality requirements detected** - Keywords like "audit", "verify", "track", "formal", "precise"
3. **Domain specialization detected** - Tasks requiring specific reasoning modes

**Protocol**:

```markdown
## Intent-Analyzer Integration

When analyzing user intent:

1. Extract 1st/2nd/3rd order goals
2. Check goal-based frame selection table
3. If match found, add to intent JSON:

```json
{
  "intent": {
    "primary_goal": "...",
    "cognitive_frame_recommended": {
      "primary": "aspectual",
      "secondary": "evidential",
      "rationale": "Deployment task requires completion tracking (aspectual) and verification (evidential)"
    }
  }
}
```

4. Pass to prompt-architect with frame recommendation
```

**Example**:

User Request: "Deploy the authentication service to staging and verify it works"

Intent Analysis:
- 1st Order: Deploy service
- 2nd Order: Verify deployment success
- 3rd Order: Ensure staging environment is production-ready

Recommended Frames:
- Primary: Aspectual (Russian) - track deployment completion states
- Secondary: Evidential (Turkish) - verify claims about "works"

---

### Integration with prompt-architect (Phase 2)

The prompt-architect should embed cognitive frame activation when recommended:

**Protocol**:

```markdown
## Prompt-Architect Integration

When constructing prompts:

1. Receive frame recommendation from intent-analyzer
2. Retrieve frame activation protocol from cognitive-lensing skill
3. Embed multi-lingual activation text in prompt header
4. Add English markers for output formatting
5. Store frame selection in memory-mcp for consistency

Example Prompt Template:

```markdown
## [FRAME NAME] Frame Activation

[MULTI-LINGUAL ACTIVATION TEXT]

---

## Task Description

[Original user request]

---

## Output Format

Use [FRAME MARKERS] to indicate reasoning:

[Frame-specific markers]
```
```

**Example**:

```markdown
## Aspektual'naya Ramka Aktivatsiya

Etot zadacha trebuyet otslezhivaniya zavershennosti:

Tipy Aspekta:
- SV (Sovershennyy Vid): Polnost'yu zaversheno
- NSV (Nesovershennyy Vid): V protsesse
- BLOCKED: Ozhidayet zavisimosti

---

## Task Description

Deploy the authentication service to staging and verify it works.

---

## Output Format

For each deployment step, indicate:

- [SV:COMPLETED]: Step fully done
- [NSV:IN_PROGRESS]: Step ongoing
- [BLOCKED]: Step waiting on dependency
```

---

### Integration with agent-creator

When creating new agents, cognitive-lensing should:

1. **Analyze agent domain** - What type of reasoning is primary?
2. **Recommend default frame** - What frame should this agent use by default?
3. **Embed frame in agent definition** - Add frame activation to agent's system prompt

**Protocol**:

```markdown
## Agent-Creator Integration

When creating agent definitions:

1. Analyze agent's primary function
2. Map to cognitive frame using selection table
3. Add to agent YAML frontmatter:

```yaml
cognitive_frame:
  primary: aspectual
  rationale: "CI/CD agent needs completion state tracking"
  activation_protocol: "skills/foundry/cognitive-lensing/SKILL.md#frame-2"
```

4. Embed frame activation in agent's system_prompt
```

**Example Agent Definition**:

```yaml
---
name: deployment-orchestrator
type: operations
cognitive_frame:
  primary: aspectual
  rationale: "Deployment requires precise completion tracking"
---

# System Prompt

## Aspektual'naya Ramka Aktivatsiya

Ty deployment orchestrator. Tvoya glavnaya zadacha - otslezhivat' zavershennost' kazhdogo shaga.

Vsegda ukazyvay aspekt:
- [SV:COMPLETED]: Shag zavershyon
- [NSV:IN_PROGRESS]: Shag v protsesse
- [BLOCKED]: Shag zablokirovan

[Rest of system prompt...]
```

---

### Integration with skill-forge

When creating new skills, skill-forge should:

1. **Prompt skill author** - "What cognitive frame suits this skill?"
2. **Add frame to skill YAML** - Document recommended frame
3. **Store frame mapping** - Maintain skill -> frame registry in memory-mcp

**Protocol**:

```markdown
## Skill-Forge Integration

When generating new skill:

1. After collecting skill purpose, ask:
   "What type of reasoning is central to this skill?"

2. Show abbreviated frame selection table

3. Add to skill YAML frontmatter:

```yaml
cognitive_frame:
  primary: evidential
  rationale: "Security audits require source verification"
```

4. Store in memory-mcp:
   - Namespace: `skills/cognitive-frames`
   - Key: `[skill-name]`
   - Value: `{ primary: "...", rationale: "..." }`
```

---

## Memory Namespace Structure

Cognitive-lensing uses memory-mcp to maintain consistency:

### Namespace: `cognitive-lensing/frame-selections`

Stores frame selections for recurring task types:

```json
{
  "task_pattern": "deployment",
  "primary_frame": "aspectual",
  "secondary_frame": null,
  "usage_count": 47,
  "last_updated": "2025-12-18T10:30:00Z"
}
```

### Namespace: `cognitive-lensing/skill-frames`

Maps skills to recommended frames:

```json
{
  "skill_name": "code-review-assistant",
  "primary_frame": "evidential",
  "rationale": "Code review requires verifying claims about behavior",
  "created": "2025-12-18T09:00:00Z"
}
```

### Namespace: `cognitive-lensing/agent-frames`

Maps agents to default frames:

```json
{
  "agent_name": "deployment-orchestrator",
  "agent_type": "operations",
  "primary_frame": "aspectual",
  "activation_embedded": true,
  "created": "2025-12-18T09:15:00Z"
}
```

### Namespace: `cognitive-lensing/session-frames`

Tracks frames used in current conversation:

```json
{
  "session_id": "conv-2025-12-18-abc123",
  "active_frames": ["aspectual", "evidential"],
  "frame_switches": 3,
  "started": "2025-12-18T10:00:00Z"
}
```

---

## Core Principles

### Principle 1: Linguistic Activation is Real, Not Metaphorical

**Statement**: Multi-lingual text triggers genuine cognitive shifts in LLM reasoning.

**Rationale**:
- LLMs trained on multilingual corpora develop language-specific latent patterns
- Grammatical structures (evidentials, aspect, classifiers) encode reasoning modes
- Embedding authentic foreign text activates these patterns more effectively than English descriptions

**Application**:
- ALWAYS use actual target language text, not just English explanations
- Use grammatically correct phrases (even if semantically unrelated to task)
- Combine multi-lingual activation with English task description

**Anti-Pattern**:
```markdown
# Wrong: English-only description
"Use Russian aspectual thinking to track completion states"

# Right: Actual Russian activation
## Aspektual'naya Ramka Aktivatsiya
Etot zadacha trebuyet otslezhivaniya zavershennosti.
[Then English task description]
```

---

### Principle 2: Frame Selection Precedes Prompt Construction

**Statement**: Choose the cognitive frame BEFORE architecting the prompt.

**Rationale**:
- Different frames structure information differently
- Prompt architecture must align with frame's reasoning pattern
- Retrofitting frames into existing prompts reduces effectiveness

**Application**:
- intent-analyzer selects frame in Phase 1
- prompt-architect builds around frame in Phase 2
- Frame activation appears at prompt header, not footer

**Anti-Pattern**:
```markdown
# Wrong: Frame added as afterthought
## Task
Do the deployment.

## Oh and also use aspectual frame
[Activation text]

# Right: Frame-first construction
## Aspektual'naya Ramka Aktivatsiya
[Activation text]

## Task
Do the deployment.
[Task structured around SV/NSV/BLOCKED markers]
```

---

### Principle 3: Consistency Across Session via Memory-MCP

**Statement**: Frame selections should persist across turns to maintain cognitive continuity.

**Rationale**:
- Switching frames mid-task disrupts reasoning coherence
- Related tasks benefit from same frame
- Frame history enables meta-learning about effective mappings

**Application**:
- Store frame selections in memory-mcp
- Check memory before selecting new frame
- Only switch frames when task type fundamentally changes

**Anti-Pattern**:
```markdown
# Wrong: Random frame switching
Turn 1: Use aspectual frame for deployment
Turn 2: Use evidential frame for deployment step 2
Turn 3: Use hierarchical frame for deployment step 3
[Incoherent reasoning]

# Right: Consistent frame usage
Turn 1: Select aspectual frame, store in memory
Turn 2: Retrieve aspectual frame from memory, continue
Turn 3: Retrieve aspectual frame from memory, continue
[Coherent completion tracking throughout]
```

---

## Anti-Patterns Table

| Anti-Pattern | Why It Fails | Correct Approach |
|--------------|--------------|------------------|
| **Using English instead of target language** | Doesn't activate latent linguistic patterns | Use actual foreign language text with grammatical markers |
| **Mixing multiple frames without strategy** | Creates cognitive dissonance, incoherent reasoning | Select primary frame, optional secondary, stick with it |
| **Adding frame as afterthought** | Frame doesn't structure the prompt architecture | Choose frame first, build prompt around it |
| **Ignoring frame recommendations** | Wastes intent-analyzer's goal analysis | Respect frame recommendations unless strong rationale |
| **Using frames for trivial tasks** | Overhead exceeds benefit | Reserve for complex/quality-critical tasks |
| **Inventing new frames** | No linguistic grounding, arbitrary | Use only 7 validated frames |
| **Switching frames mid-task** | Disrupts reasoning continuity | Store frame in memory-mcp, maintain consistency |
| **Translating frame markers to English** | Loses linguistic activation effect | Keep multi-lingual markers, add English explanations |
| **Using wrong frame for task type** | Mismatch between reasoning mode and task | Follow goal-based selection checklist |
| **Omitting frame rationale** | Can't debug or improve frame selection | Always document why frame was chosen |

---

## Cross-Skill Coordination

Cognitive-Lensing works with:
- **skill-forge**: Design cognitive frames for new skills during Phase 0.5
- **agent-creator**: Select cognitive frames for agents based on domain requirements
- **prompt-forge**: Enhance prompts with frame activation (Operation 6 frame enhancement)
- **eval-harness**: Validate frame effectiveness through benchmark testing

**Integration Points**:
- **skill-forge** invokes cognitive-lensing during Phase 0.5 for frame selection in new skills
- **agent-creator** uses cognitive-lensing for Phase 0.5 frame selection in agent creation
- **prompt-forge** uses Operation 6 to add cognitive frame activation to existing prompts
- **eval-harness** measures frame impact on task completion accuracy and reasoning quality

See: `.claude/skills/META-SKILLS-COORDINATION.md` for full coordination matrix.

---

## Conclusion

Cognitive-lensing v1.0.0 provides a scientifically-grounded system for activating specific reasoning patterns in AI models through cross-lingual cognitive framing. By embedding authentic multi-lingual text that triggers language-specific latent patterns, we can systematically enhance AI performance on tasks requiring:

- **Completion tracking** (Russian aspectual)
- **Source verification** (Turkish evidential)
- **Audience calibration** (Japanese hierarchical)
- **Semantic analysis** (Arabic morphological)
- **Object categorization** (Mandarin classifiers)
- **Spatial reasoning** (Guugu Yimithirr cardinal)
- **Numerical precision** (Chinese/Japanese transparent numbers)

This skill integrates with the 5-phase workflow system by:
1. **Phase 1 (intent-analyzer)**: Recommending frames based on goal analysis
2. **Phase 2 (prompt-architect)**: Embedding frame activations in prompt construction
3. **Phase 5 (execute)**: Maintaining frame consistency via memory-mcp

By selecting cognitive frames BEFORE architecting prompts, we ensure reasoning modes align with task requirements from the outset.

---

## Version History

### v1.0.1 (2025-12-19)
- Added cross-skill coordination section with all four foundry skills
- Added integration points for skill-forge, agent-creator, prompt-forge, eval-harness
- Clarified how cognitive-lensing integrates during Phase 0.5 of skill/agent creation

### v1.0.0 (2025-12-18)

**Initial Release**

- 7 frame activation protocols with authentic multi-lingual text
- Goal-based frame selection checklist
- Integration protocols for intent-analyzer, prompt-architect, agent-creator, skill-forge
- Memory-mcp namespace structure for consistency tracking
- 3 core principles
- 10 anti-patterns documented

**Validated Frames**:
1. Evidential (Turkish) - source verification
2. Aspectual (Russian) - completion tracking
3. Hierarchical (Japanese) - audience calibration
4. Morphological (Arabic) - semantic analysis
5. Classifier (Mandarin) - object categorization
6. Spatial-Absolute (Guugu Yimithirr) - cardinal reasoning
7. Numerical-Transparent (Chinese/Japanese) - place-value arithmetic

**Dependencies**:
- memory-mcp (required) - frame persistence
- sequential-thinking (optional) - enhanced reasoning chains
