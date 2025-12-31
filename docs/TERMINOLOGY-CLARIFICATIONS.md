# Terminology Clarifications

**Version**: 1.0.0
**Created**: 2025-12-31
**Purpose**: Clarify potentially misleading terminology in Context Cascade

---

## Overview

This document clarifies terminology that may be misinterpreted. The goal is transparency about what features actually do vs. what their names might imply.

---

## Protocol Terminology

### Byzantine Fault Tolerance (BFT)

**What the name implies**: Implementation of academic BFT protocols (PBFT, HotStuff) with cryptographic verification, quorum voting, and malicious node detection.

**What Context Cascade actually provides** (CONCEPTUAL patterns only):
- Conceptual coordination patterns inspired by BFT principles
- Multi-agent redundancy with majority voting
- No cryptographic message authentication between agents
- No formal Byzantine consensus protocol implementation
- LLM-based "consensus" through response aggregation

**Recommendation**: Treat as "redundant agent coordination" not "Byzantine fault tolerance."

---

### Raft Consensus

**What the name implies**: Implementation of the Raft consensus algorithm with leader election, log replication, and term-based voting.

**What Context Cascade actually provides**:
- Conceptual leader-follower agent patterns
- Task distribution from coordinator to worker agents
- No actual Raft log replication
- No term-based leader election
- No formal membership changes protocol

**Recommendation**: Treat as "hierarchical agent coordination" not "Raft consensus."

---

### Gossip Protocol

**What the name implies**: Implementation of gossip/epidemic protocols for peer-to-peer state propagation.

**What Context Cascade actually provides**:
- Conceptual peer-to-peer agent communication patterns
- Shared memory via Memory MCP (not gossip)
- No probabilistic message propagation
- No anti-entropy synchronization

**Recommendation**: Treat as "shared memory coordination" not "gossip protocol."

---

## Verification Terminology

### VeriX / VERIX

**What the name implies**: Formal verification system using SMT solvers (Z3, Marabou) to prove properties about code or neural networks.

**What Context Cascade actually provides**:
- Structured epistemic notation for claims
- Regex-based parsing of notation syntax
- Confidence scoring (0.0-1.0)
- Source grounding requirements
- NO SMT solver integration
- NO formal proof generation
- NO mathematical verification

**Recommendation**: Treat as "epistemic notation system" not "formal verification."

---

### VeriLingua

**What the name implies**: Verified natural language processing or formal language verification.

**What Context Cascade actually provides**:
- Cognitive framing prompts based on linguistic research
- 7 cognitive frames (evidential, aspectual, morphological, etc.)
- Prompt engineering patterns
- NO formal language verification
- NO NLP model verification

**Recommendation**: Treat as "cognitive prompting framework" not "language verification."

---

## Safety Terminology

### Frozen Eval Harness

**What the name implies**: Cryptographically immutable evaluation code that cannot be modified.

**What Context Cascade actually provides** (after Phase 2):
- SHA-256 hash verification of eval harness files
- Hash seal stored in `safety/constitution/hash-seal.json`
- Safety Guardian blocks writes to sealed paths
- Git history provides rollback capability
- Still modifiable by humans with signed commits

**Recommendation**: Treat as "hash-verified evaluation code" - modifications are detected, not prevented at filesystem level.

---

### Immutable Constitution

**What the name implies**: Files that literally cannot be changed.

**What Context Cascade actually provides**:
- Policy-level immutability enforced by Safety Guardian
- Hash verification detects tampering
- Automated processes blocked from modifying
- Human modifications still possible (with approval)

**Recommendation**: Treat as "protected files with tamper detection" not "physically immutable."

---

## Architecture Terminology

### Infinite Context

**What the name implies**: Unlimited context window with perfect recall.

**What Context Cascade actually provides**:
- Automatic summarization for long conversations
- Memory MCP for persistent storage
- Vector search for retrieval
- Still subject to retrieval errors
- Summarization may lose details

**Recommendation**: Treat as "extended context with summarization" not "infinite context."

---

### Agent Registry (211 Agents)

**What the name implies**: 211 distinct, specialized AI agents.

**What Context Cascade actually provides**:
- 211 agent definition files (markdown)
- Agents are prompt templates, not separate AI instances
- Many agents have overlapping capabilities
- Could be consolidated to ~20 archetypes

**Recommendation**: Treat as "211 agent templates" that map to ~20 functional archetypes.

---

## Recommended Reading

For accurate understanding of the distributed systems concepts referenced:

1. **Byzantine Fault Tolerance**: Castro & Liskov, "Practical Byzantine Fault Tolerance" (OSDI 1999)
2. **Raft**: Ongaro & Ousterhout, "In Search of an Understandable Consensus Algorithm" (USENIX ATC 2014)
3. **Gossip Protocols**: Demers et al., "Epidemic Algorithms for Replicated Database Maintenance" (PODC 1987)
4. **Formal Verification**: Introduction to SMT solving and tools like Z3

---

## Changelog

| Date | Change |
|------|--------|
| 2025-12-31 | Initial clarifications document created |
