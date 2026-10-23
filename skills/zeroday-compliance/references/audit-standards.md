# Standards — Control Catalogs

## SOC 2 — AICPA Trust Services Criteria

# SOC 2 Type II Standards Reference

## Primary Standards

### AICPA Trust Services Criteria (TSC) 2017 (Revised 2022)
- **Governing Body**: American Institute of Certified Public Accountants (AICPA)
- **Basis**: Built on COSO 2013 Internal Control Framework
- **Revision**: Points of Focus updated in 2022 to address cloud, supply chain, and evolving technology risks
- **Description Criteria**: Updated July 2025

### SSAE 18 (Statement on Standards for Attestation Engagements No. 18)
- **Standard**: AT-C Section 105, 205, and 320
- **Purpose**: Governs the attestation engagement performed by the CPA firm
- **Effective**: May 1, 2017 (replaced SSAE 16)

## Trust Services Criteria Detail

### Security (Common Criteria) - MANDATORY
CC1: Control Environment
- CC1.1: COSO Principle 1 - Demonstrates commitment to integrity and ethical values
- CC1.2: COSO Principle 2 - Board exercises oversight responsibility
- CC1.3: COSO Principle 3 - Management establishes structures, reporting lines, authorities
- CC1.4: COSO Principle 4 - Demonstrates commitment to attract, develop, retain competent individuals
- CC1.5: COSO Principle 5 - Holds individuals accountable for internal control responsibilities

CC2: Communication and Information
- CC2.1: COSO Principle 13 - Uses relevant, quality information to support internal control
- CC2.2: COSO Principle 14 - Internally communicates information supporting internal control
- CC2.3: COSO Principle 15 - Communicates with external parties regarding internal control

CC3: Risk Assessment
- CC3.1: COSO Principle 6 - Specifies objectives with sufficient clarity
- CC3.2: COSO Principle 7 - Identifies risks to achievement of objectives
- CC3.3: COSO Principle 8 - Considers potential for fraud
- CC3.4: COSO Principle 9 - Identifies and assesses changes that could impact internal control

CC4: Monitoring Activities
- CC4.1: COSO Principle 16 - Selects, develops, performs ongoing and separate evaluations
- CC4.2: COSO Principle 17 - Evaluates and communicates internal control deficiencies

CC5: Control Activities
- CC5.1: COSO Principle 10 - Selects and develops control activities
- CC5.2: COSO Principle 11 - Selects and develops general controls over technology
- CC5.3: COSO Principle 12 - Deploys through policies and procedures

CC6: Logical and Physical Access Controls
- CC6.1: Logical access security software, infrastructure, and architectures
- CC6.2: Prior to credential issuance, registration and authorization processes
- CC6.3: Access removal, modification upon changes to roles
- CC6.4: Physical access restrictions to facilities and protected information assets
- CC6.5: Changes in physical access restrictions are managed
- CC6.6: Logical access security measures against threats from external sources
- CC6.7: Restricts transmission, movement, and removal of information
- CC6.8: Controls against threats from deployment of unauthorized or malicious code

CC7: System Operations
- CC7.1: Detection and monitoring for anomalies and events
- CC7.2: Activities monitored against security event criteria
- CC7.3: Procedures exist to evaluate security events
- CC7.4: Response to identified security incidents
- CC7.5: Identification and remediation of identified vulnerabilities

CC8: Change Management
- CC8.1: Changes to infrastructure, data, software, and procedures are authorized, designed, developed, tested, approved, and implemented

CC9: Risk Mitigation
- CC9.1: Risk mitigation activities are considered through risk assessment
- CC9.2: Assesses and manages risks through vendor/business partner activities

### Availability (Optional)
- A1.1: Performance and capacity maintenance
- A1.2: Environmental protections, software, data backup and recovery
- A1.3: Recovery plan testing

### Processing Integrity (Optional)
- PI1.1: Obtains or generates, uses, and communicates relevant quality information
- PI1.2: System inputs are complete, accurate, and timely
- PI1.3: Processing is complete, valid, accurate, timely, and authorized
- PI1.4: System output is complete, valid, accurate, timely, and authorized
- PI1.5: Data stored is complete, valid, accurate, timely, and authorized

### Confidentiality (Optional)
- C1.1: Identifies and maintains confidential information
- C1.2: Disposes of confidential information

### Privacy (Optional)
- P1.0-P8.0: Covers notice, choice, collection, use, retention, disclosure, access, quality, and monitoring/enforcement

## SOC 2 Report Structure

### Section I: Independent Service Auditor's Report
- Auditor opinion on control design and operating effectiveness
- Scope of examination and applicable criteria

### Section II: Management's Assertion
- Management's representation regarding system description and control effectiveness

### Section III: Description of the System
- Nature of services, principal service commitments, system requirements
- Components: infrastructure, software, people, procedures, data
- Boundaries and subservice organizations

### Section IV: Description of Criteria, Controls, Tests, and Results
- Each TSC criterion with mapped controls
- Test procedures performed by auditor
- Results of testing (no exceptions / exception noted)

### Section V: Other Information (Optional)
- Complementary User Entity Controls (CUECs)
- Complementary Subservice Organization Controls (CSOCs)

## Related Standards
- SOC 1 (SSAE 18/ISAE 3402): Financial reporting controls
- SOC 3 (Trust Services Criteria): Public-facing summary report
- ISO 27001: Information Security Management System
- NIST CSF: Cybersecurity Framework (mappings available)

---

## GDPR — Regulation 2016/679

# Standards and References — Conducting GDPR Compliance Assessment

## NIST Cybersecurity Framework 2.0

| ID | Category | Rationale |
|----|----------|-----------|
| GV.OC-02 | Organizational Context: Legal, regulatory, and contractual requirements regarding cybersecurity are understood and managed | GDPR is a primary legal/regulatory requirement for organizations processing EU resident data; understanding its applicability (Article 3) and requirements is foundational to governance. |
| GV.PO-01 | Policy: Organizational cybersecurity policy is established, communicated, and enforced | GDPR Article 5 accountability principle and Article 24 controller responsibilities require documented data protection policies aligned with GDPR principles. |
| GV.RM-04 | Risk Management Strategy: Strategic direction that describes appropriate risk response options is established and communicated | DPIAs (Article 35) and controller accountability (Article 24) mandate risk-based approaches to data protection; risk tolerance must be documented and communicated. |
| PR.DS-01 | Data Security: Data-at-rest is protected | Article 32 requires encryption and pseudonymization as technical measures appropriate to the risk; data-at-rest encryption directly implements this. |
| PR.DS-02 | Data Security: Data-in-transit is protected | Article 32 confidentiality/integrity; TLS 1.2+ for all personal data transmission implements this security baseline. |
| ID.AM-05 | Asset Management: Resources are prioritized based on classification, criticality, and business value | Article 30 records of processing categorize personal data by sensitivity (special category under Article 9 vs. general); this informs security prioritization. |

## MITRE ATT&CK

| Technique ID | Name | Tactic | Rationale |
|--------------|------|--------|-----------|
| T1530 | Data from Cloud Storage Object | Collection | Unauthorized access to cloud-stored personal data represents a data breach under GDPR Article 4(12); assessing cloud security controls (access logs, IAM) validates Article 32 compliance. |
| T1567 | Exfiltration Over Web Service | Exfiltration | Data exfiltration scenarios (T1567.002 to cloud, T1567.004 over encrypted channel) constitute personal data breaches; GDPR Article 33 breach notification and Article 32 exfiltration prevention controls directly address this. |

## GDPR Articles Mapped

| Article | Title | Assessment Focus |
|---------|-------|------------------|
| Article 3 | Territorial Scope | Determine applicability: establishment, offering goods/services, monitoring |
| Article 4 | Definitions | Controller, processor, personal data, special category data, consent |
| Article 5 | Principles | Lawfulness, fairness, transparency, purpose limitation, data minimization, accuracy, storage limitation, integrity/confidentiality, accountability |
| Article 6 | Lawfulness of Processing | Identify lawful basis for each processing activity (consent, contract, legal obligation, vital interests, public task, legitimate interest) |
| Article 7 | Conditions for Consent | Verify consent is freely given, specific, informed, unambiguous; withdrawal mechanism |
| Article 9 | Special Categories | Additional conditions for processing health, biometric, genetic, racial, political, religious, trade union, sex life data |
| Article 12-23 | Data Subject Rights | Access (15), rectification (16), erasure (17), restriction (18), portability (20), objection (21), automated decision-making (22) |
| Article 24 | Controller Responsibility | Implement technical/organizational measures demonstrating compliance; accountability |
| Article 25 | Privacy by Design | Data protection by design and by default |
| Article 28 | Processor Obligations | Data Processing Agreement requirements, sub-processor rules |
| Article 30 | Records of Processing | Written register of all processing activities (mandatory for orgs 250+ employees or high-risk) |
| Article 32 | Security of Processing | Encryption, pseudonymization, confidentiality, integrity, availability, resilience, regular testing |
| Article 33 | Breach Notification (Authority) | Notify supervisory authority within 72 hours unless unlikely to risk rights |
| Article 34 | Breach Notification (Data Subject) | Notify individuals without undue delay if high risk to rights |
| Article 35 | Data Protection Impact Assessment | Mandatory for systematic large-scale processing, special categories, monitoring public areas |
| Article 37-39 | Data Protection Officer | Designation criteria, tasks, independence |
| Articles 44-50 | International Transfers | Chapter V: adequacy decisions, SCCs, BCRs, derogations |

## Supporting Standards

- **ISO/IEC 27701:2019** — Privacy Information Management System (PIMS); extension to ISO 27001 for GDPR-style privacy
- **ISO/IEC 29134:2017** — Privacy Impact Assessment (PIA) methodology; aligns with GDPR Article 35 DPIA
- **NIST Privacy Framework 1.0** — Risk-based approach to privacy; complements GDPR compliance programs
- **EDPB Guidelines** — European Data Protection Board authoritative guidance on GDPR interpretation

## Official Resources

- **GDPR Full Text**: https://gdpr.eu/tag/gdpr/
- **ICO GDPR Guidance** (UK Supervisory Authority): https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/
- **EDPB Guidelines**: https://edpb.europa.eu/our-work-tools/general-guidance_en
- **Standard Contractual Clauses (2021)**: https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/standard-contractual-clauses-scc_en
- **Article 29 Working Party Opinions** (superseded by EDPB but still referenced): https://ec.europa.eu/justice/article-29/documentation/opinion-recommendation/index_en.htm
- **Data (Use and Access) Act 2025** (UK, Royal Assent 19 June 2025): https://www.legislation.gov.uk/ukpga/2025/18

## Enforcement Statistics (2024-2026)

- **Total fines issued**: €4.8 billion (2024-2025 period)
- **Largest fine**: €1.2 billion (Meta Ireland, data transfer violations)
- **Most common violations**: Insufficient legal basis (28%), inadequate security (Article 32, 22%), failure to implement data subject rights (18%)
- **Average DSAR response time**: 18 days (requirement: within 1 month, Article 15)
- **Breach notification compliance**: 41% of controllers notified ICO within 72 hours (2025 ICO report)

