# 🗺️ US Oncology Market Map — RISA Labs Strategic Ecosystem Guide

> **Purpose:** Comprehensive stakeholder map for RISA Labs (healthcare AI / oncology RCM)
> **Last Updated:** February 2026

---

## 1. 🏥 CARE DELIVERY (Providers)

### 1.1 NCI-Designated Comprehensive Cancer Centers
- **Examples:** MD Anderson, Memorial Sloan Kettering, Dana-Farber, Fred Hutch, Moffitt, City of Hope
- **Role:** Research + clinical care, clinical trials, complex/rare cases
- **Revenue Model:** Grants (NCI/NIH), patient revenue, philanthropy, IP licensing
- **Scale:** ~72 NCI-designated centers (53 comprehensive)
- **Pain Points:** Grant funding uncertainty, EHR fragmentation, trial enrollment bottlenecks, complex multi-payer billing
- **RISA Opportunity:** Complex claim adjudication (multi-payer, trial vs. standard care billing), denial management for novel therapies
- **Money Flow:** ← NCI grants, patient revenue (commercial + Medicare), philanthropy → staff, research, drugs
- **Data Flow:** Generates → clinical trial data, genomic data, treatment outcomes; Consumes ← guidelines, payer policies

### 1.2 Academic Medical Center Cancer Programs
- **Examples:** Stanford Cancer Center, UCSF, Johns Hopkins, Mayo Clinic, Cleveland Clinic
- **Role:** Teaching + research + clinical care, tertiary/quaternary referrals
- **Pain Points:** Faculty retention, balancing research vs. clinical volume, complex referral billing
- **RISA Opportunity:** Multi-departmental charge capture, referral authorization automation
- **Money Flow:** ← Tuition, patient revenue, grants, state funding → faculty, facilities, research
- **Data Flow:** Generates → published research, training datasets; Consumes ← referral records, external imaging

### 1.3 Large Community Oncology Practices
- **Examples:** Texas Oncology, Florida Cancer Specialists, Regional Cancer Care Associates, Oncology Hematology Care (OHC)
- **Role:** Delivers 60%+ of US cancer care, volume-driven, closer to patients
- **Ownership:** Physician-owned, PE-backed, or health system–affiliated
- **Pain Points:** Margin pressure (drug reimbursement cuts, rising costs), payer denials, staffing shortages, pathway compliance burden
- **RISA Opportunity:** ⭐ **PRIMARY TARGET** — Prior auth automation, denial prevention, buy-and-bill optimization, coding accuracy for chemo regimens
- **Money Flow:** ← Patient copays, payer reimbursement, drug margin (buy-and-bill) → staff, drug purchases, overhead
- **Data Flow:** Generates → claims, treatment records, pathway adherence; Consumes ← payer policies, NCCN guidelines, drug pricing

### 1.4 Hospital System Cancer Programs
- **Examples:** HCA Healthcare, Providence, Intermountain, Northwell, CommonSpirit, Atrium
- **Role:** Integrated delivery networks, employed oncologists, inpatient + outpatient
- **Pain Points:** Oncology service line profitability, 340B optimization, employed physician productivity
- **RISA Opportunity:** Service line revenue integrity, 340B compliance, charge capture for infusion centers
- **Money Flow:** ← Payer contracts (DRG inpatient, APC outpatient), 340B savings → salaries, facilities, drugs
- **Data Flow:** Generates → large structured EHR datasets; Consumes ← benchmarking, quality metrics

### 1.5 Oncology Management / Network Organizations
- **US Oncology Network (McKesson)** — Largest; 1,400+ physicians, manages Texas Oncology, New York Oncology Hematology, etc.
  - Role: GPO, practice management, iKnowMed EHR, clinical pathways, data aggregation
- **OneOncology (TPG)** — PE-backed, 600+ providers, rapid acquisition strategy
  - Role: Practice management, shared services, pathways
- **American Oncology Network (AON)** — Physician-led, partnership model
  - Role: Back-office, analytics, value-based care support
- **Flatiron Health (Roche)** — OncoEMR + real-world data platform
  - Role: EHR, data licensing to pharma, research analytics
- **Pain Points:** Standardizing operations across diverse practices, demonstrating value-based care savings
- **RISA Opportunity:** Platform-level RCM integration (one integration → hundreds of practices), network-wide denial analytics
- **Money Flow:** ← Management fees, GPO rebates, data licensing revenue → practice support, technology
- **Data Flow:** Aggregates ← practice-level clinical + claims data; Sells → de-identified data to pharma/research

---

## 2. 💰 PAYERS & REIMBURSEMENT

### 2.1 Medicare / CMS
- **Role:** Largest single oncology payer (median cancer diagnosis age: 66)
- **Medicare Fee-for-Service (FFS)** — Traditional; pays per service
- **Medicare Advantage (MA)** — Managed care; ~52% of Medicare beneficiaries (2025), growing
  - Key MA oncology plans: UnitedHealthcare MA, Humana, Aetna, BCBS
- **Enhancing Oncology Model (EOM)** — Successor to OCM; episode-based payments, quality measures, health equity focus
  - Participating practices take on financial risk for episodes of care
- **Pain Points:** Complex coverage rules, LCD/NCD variability, slow policy updates for new therapies
- **RISA Opportunity:** ⭐ Medicare denial reduction (top payer = top denial volume), EOM reporting automation, MA prior auth automation
- **Money Flow:** ← Payroll taxes, premiums → providers (FFS payments, MA capitation) → also pays MA plans
- **Data Flow:** Generates → claims databases (SEER-Medicare), coverage policies; Consumes ← quality data from providers

### 2.2 Commercial Payers
- **UnitedHealthcare** — Largest commercial; owns Optum (analytics, PBM, care delivery)
- **Elevance Health (Anthem/BCBS)** — Large BCBS licensee
- **Aetna (CVS Health)** — Integrated with CVS pharmacy/retail
- **Cigna (The Cigna Group)** — Owns Express Scripts (PBM)
- **Blue Cross Blue Shield** — Federation of 34 independent companies
- **Mechanisms:** Prior authorization, step therapy, clinical pathway compliance requirements, site-of-care steering
- **Pain Points:** Rising oncology drug costs, appropriate utilization management, member experience
- **RISA Opportunity:** ⭐ Prior auth automation (both provider-side and potentially payer-side), claims accuracy, pathway compliance documentation
- **Money Flow:** ← Employer/individual premiums → providers (negotiated rates), pharma (rebates received)
- **Data Flow:** Generates → EOBs, prior auth decisions, network data; Consumes ← claims from providers, clinical documentation

### 2.3 Medicaid
- **Role:** State-level, covers low-income; significant for certain cancers (cervical, late-stage presentations)
- **Structure:** 50 state programs + DC, managed Medicaid dominant
- **Pain Points:** Low reimbursement rates, state variation, complex eligibility
- **RISA Opportunity:** Eligibility verification, dual-eligible (Medicare + Medicaid) coordination
- **Money Flow:** ← Federal + state funding → providers (low rates) → managed Medicaid plans
- **Data Flow:** Generates → state claims databases; Consumes ← eligibility data, provider claims

### 2.4 Specialty Pharmacy / PBMs
- **CVS Caremark** — Largest PBM
- **Express Scripts (Cigna)** — #2 PBM
- **Optum Rx (UnitedHealth)** — #3 PBM
- **Magellan Rx (Prime Therapeutics)** — Oncology specialty focus
- **Role:** Manage oral oncolytics (growing segment: ~40% of pipeline), specialty drug distribution, formulary management
- **Pain Points:** Oral parity laws, specialty drug costs, white/brown bagging policies
- **RISA Opportunity:** Oral oncolytic prior auth, benefits investigation automation, copay tracking
- **Money Flow:** ← Payer contracts, manufacturer rebates, spread pricing → pharmacies (dispensing fees)
- **Data Flow:** Generates → Rx claims, adherence data; Consumes ← prescriptions, formulary updates

### 2.5 Value-Based Care Programs
- **OCM (ended 2022) → EOM (2023+)** — CMS episode-based oncology payment model
- **Bundled Payments** — Fixed payment for episode of care
- **Clinical Pathways:**
  - Via Oncology (Elsevier) — payer-aligned pathways
  - NCCN Guidelines — gold standard
  - Elsevier Clinical Pathways
  - Value Pathways (powered by NCCN)
- **Pain Points:** Attribution complexity, data reporting burden, measuring total cost of care
- **RISA Opportunity:** EOM performance tracking, pathway adherence documentation, episode cost analytics
- **Money Flow:** ← Performance bonuses from CMS/payers ↔ risk-sharing (providers may owe money back)
- **Data Flow:** Generates → quality measures, episode costs; Consumes ← claims, clinical data, benchmarks

---

## 3. 💊 PHARMA & BIOTECH (Drug Manufacturers)

### 3.1 Large Pharma Oncology
- **Merck** — Keytruda (#1 drug globally, ~$25B), immuno-oncology leader
- **Roche/Genentech** — Tecentriq, Herceptin franchise, Foundation Medicine
- **Bristol-Myers Squibb** — Opdivo, Revlimid, Abecma (CAR-T)
- **AstraZeneca** — Tagrisso, Imfinzi, Enhertu (with Daiichi Sankyo)
- **Pfizer** — Ibrance, Seagen acquisition (ADCs), Padcev
- **Novartis** — Kisqali, Kymriah (CAR-T), Pluvicto (radioligand)
- **Eli Lilly** — Verzenio, Retevmo, Jaypirca
- **Johnson & Johnson** — Darzalex, Carvykti (CAR-T with Legend)
- **AbbVie** — Imbruvica, Venclexta, Epcoritamab
- **Sanofi** — Sarclisa, Dupixent pipeline expansion
- **Revenue:** Oncology is #1 therapeutic area (~$220B+ globally, ~$90B US)
- **Pain Points:** Market access/formulary placement, real-world evidence generation, patient adherence, HCP engagement
- **RISA Opportunity:** Provider-side coding accuracy for branded drugs (ensures correct billing → protects revenue), patient support program integration
- **Money Flow:** → Distributors (WAC pricing) → Providers (buy-and-bill markup) or PBMs/pharmacies (oral); ← Rebates to payers/PBMs; → CROs (trial costs); → Patient copay assistance
- **Data Flow:** Generates → clinical trial data, drug labels; Consumes ← RWD (Flatiron, Tempus), claims data, prescribing patterns

### 3.2 Emerging Biotech
- **Cell Therapy / CAR-T:** Kite/Gilead (Yescarta), Novartis (Kymriah), BMS (Abecma, Breyanzi), Legend/J&J (Carvykti)
- **ADCs (Antibody-Drug Conjugates):** Seagen/Pfizer (Padcev, Adcetris), Daiichi Sankyo/AZ (Enhertu), Immunomedics/Gilead (Trodelvy)
- **Bispecifics:** Amgen (Blincyto, tarlatamab), Roche (Lunsumio), AbbVie (Epcoritamab)
- **Radiopharmaceuticals:** Novartis (Pluvicto), Point Biopharma, RayzeBio/BMS
- **Pain Points:** Reimbursement for novel modalities (CAR-T: $300K-$500K per treatment), J-code delays, site-of-care requirements
- **RISA Opportunity:** Novel therapy billing (CAR-T, ADCs have complex billing), pass-through payment tracking, miscellaneous J-code management

### 3.3 Biosimilars
- **Sandoz** — Trastuzumab, bevacizumab, rituximab biosimilars
- **Amgen** — Mvasi (bev), Kanjinti (tras)
- **Teva** — Herzuma (tras)
- **Coherus** — Udenyca (pegfilgrastim)
- **Fresenius Kabi** — Multiple biosimilars
- **Role:** Disrupting reference biologics; saving 15-40% on key drugs
- **Pain Points:** Payer formulary positioning, physician switching hesitancy, interchangeability status
- **RISA Opportunity:** Biosimilar vs. reference product billing accuracy, formulary-aware coding suggestions

### 3.4 Specialty Distributors (Big 3)
- **McKesson** — #1 distributor + US Oncology Network + GPO
- **Cencora (fka AmerisourceBergen)** — #2 distributor + specialty distribution
- **Cardinal Health** — #3 distributor + nuclear pharmacy (radiopharmaceuticals)
- **Role:** Drug distribution, buy-and-bill logistics, returns, specialty handling (cold chain for biologics)
- **Pain Points:** Supply chain disruptions, drug shortage management, narrow margins
- **RISA Opportunity:** Inventory-to-billing reconciliation, drug waste billing (JW modifiers), ASP-based reimbursement optimization
- **Money Flow:** ← Manufacturers (distribution fees, prompt pay) → Providers (drug delivery); GPO rebates flow back to practices
- **Data Flow:** Generates → purchasing/distribution data, 867 sales data; Consumes ← orders, formulary data

---

## 4. 🧬 DIAGNOSTICS & PRECISION MEDICINE

### 4.1 Genomic Testing / Companion Diagnostics (CDx)
- **Foundation Medicine (Roche)** — FoundationOne CDx (tissue), FoundationOne Liquid CDx
- **Tempus** — xT, xF, xR panels; AI-driven insights platform
- **Guardant Health** — Guardant360 (liquid biopsy), Shield (CRC screening)
- **Myriad Genetics** — BRACAnalysis, myChoice CDx, Precise MRD
- **NeoGenomics** — Specialty cancer testing lab
- **Natera** — Signatera (MRD/ctDNA monitoring), tumor-informed approach
- **Invitae** — Hereditary cancer panels (acquired by LabCorp 2024)
- **Role:** NGS panels, liquid biopsy, companion diagnostics, minimal residual disease (MRD) testing
- **Pain Points:** Coverage/reimbursement inconsistency, turnaround time, integrating results into EHR workflow, LCD variation by MAC
- **RISA Opportunity:** ⭐ Genomic test prior auth, coverage determination automation (LCD/NCD matching), ABN generation
- **Money Flow:** ← Payer reimbursement (often delayed/denied), provider orders, pharma CDx partnerships → lab operations, R&D
- **Data Flow:** Generates → genomic reports, variant data, treatment recommendations; Consumes ← clinical history, specimen data

### 4.2 Pathology / Lab
- **Quest Diagnostics** — National reference lab
- **Labcorp** — National reference lab + Invitae
- **Hospital-based pathology** — Integrated, faster TAT
- **Pain Points:** Pathologist shortage, digitization, standardization of reporting
- **RISA Opportunity:** Pathology billing accuracy (technical + professional components), CPT code selection for complex specimens

### 4.3 Imaging
- **Radiology Partners, RadNet, SimonMed** — Large radiology groups
- **PET/CT Centers** — Critical for staging, response assessment
- **Role:** Staging, treatment response monitoring, surveillance
- **Pain Points:** Prior auth burden (especially PET/CT), appropriate use criteria
- **RISA Opportunity:** Imaging prior auth automation, appropriate use criteria documentation

### 4.4 AI Diagnostics
- **Paige AI** — FDA-cleared AI for pathology (prostate, breast)
- **Lunit** — AI for radiology + pathology (Lunit INSIGHT)
- **PathAI** — AI-powered pathology, biopharma partnerships
- **Role:** Augmenting pathologist/radiologist reads, quantitative biomarker scoring
- **Pain Points:** Reimbursement for AI-assisted reads, clinical adoption, regulatory pathway
- **RISA Opportunity:** Billing for AI-assisted diagnostics (emerging CPT codes), coverage advocacy data

---

## 5. 🔬 CLINICAL TRIALS & RESEARCH

### 5.1 NCI / NIH
- **NCI** — ~$7B annual budget, funds cooperative groups
- **Cooperative Groups:** SWOG, ECOG-ACRIN, Alliance, NRG Oncology, Children's Oncology Group
- **Role:** Federal research funding, setting standards, population-level studies
- **Pain Points:** Slow enrollment, funding gaps, bureaucracy
- **RISA Opportunity:** Trial billing compliance (qualifying vs. routine costs), coverage analysis for investigational treatments

### 5.2 CROs (Contract Research Organizations)
- **IQVIA** — Largest; CRO + data + analytics
- **PPD (Thermo Fisher)** — Full-service CRO
- **Parexel** — Regulatory + clinical
- **Syneos Health (acquired by Elliott)** — Integrated biopharmaceutical solutions
- **Role:** Run pharma-sponsored trials, site management, data management, regulatory submissions
- **Pain Points:** Site identification, enrollment speed, data quality
- **RISA Opportunity:** Site feasibility data (billing patterns indicate treatment volumes), trial cost benchmarking

### 5.3 Decentralized Trial Platforms
- **Medidata (Dassault)** — Rave platform, decentralized trial modules
- **Veeva Systems** — Vault CTMS, eTMF, clinical data management
- **Science 37** — Virtual/hybrid trial execution
- **Pain Points:** Regulatory acceptance, data integrity, patient technology access
- **Data Flow:** Generates → trial data, ePRO; Consumes ← EHR data, lab results

### 5.4 Trial Matching
- **Tempus** — AI-driven trial matching from genomic + clinical data
- **TrialJectory** — Patient-facing trial matching
- **Massive Bio** — AI trial matching for community oncology
- **RISA Opportunity:** Identifying trial-eligible patients from billing/clinical data patterns

### 5.5 Real-World Data / Evidence (RWD/RWE)
- **Flatiron Health (Roche)** — Gold standard oncology RWD; 280+ cancer clinics
- **Tempus** — Multimodal data (genomic + clinical + imaging)
- **ASCO CancerLinQ** — ASCO's data platform
- **Optum Labs** — Claims + EHR linked data
- **Komodo Health** — Patient journey analytics
- **Role:** Support regulatory decisions, label expansions, market access, HEOR
- **Pain Points:** Data quality, completeness, linkage across sources
- **RISA Opportunity:** Claims data enrichment for RWE (clean billing data = better RWD)

### 5.6 Philanthropic Research Accelerators
- **Parker Institute for Cancer Immunotherapy (PICI)** — Sean Parker–funded, immunotherapy focus
- **Stand Up to Cancer (SU2C)** — Dream Teams model, translational research
- **V Foundation** — 100% of donations to research
- **LLS (Leukemia & Lymphoma Society)** — Blood cancer research + patient support
- **Money Flow:** ← Donations → research grants, clinical trials

---

## 6. 💻 TECHNOLOGY & DATA

### 6.1 Oncology-Specific EHRs
- **Flatiron OncoEMR** — Purpose-built for oncology; strong in community practices
- **Varian ARIA (Siemens Healthineers)** — Radiation oncology OIS
- **Elekta MOSAIQ** — Radiation oncology OIS
- **iKnowMed (McKesson)** — US Oncology Network EHR
- **Epic Beacon** — Oncology module within Epic
- **Pain Points:** Interoperability, workflow burden, structured data capture, transition costs
- **RISA Opportunity:** ⭐ EHR integration for automated charge capture, clinical-to-billing data bridge

### 6.2 General EHRs in Oncology
- **Epic** — Dominant in large health systems; Beacon module for oncology
- **Oracle Health (Cerner)** — #2 EHR; oncology workflows
- **Role:** Core clinical documentation, orders, results
- **RISA Opportunity:** API integration (FHIR) for pulling clinical context into billing workflows

### 6.3 RCM / Billing
- **Waystar** — Claims management, prior auth, analytics (IPO 2024)
- **Availity** — Payer connectivity, eligibility, claims status
- **Change Healthcare (Optum/UHG)** — Largest claims clearinghouse (~50% of US claims)
- **R1 RCM** — End-to-end RCM outsourcing
- **Coronis Health** — RCM for specialty practices including oncology
- **Coding/Billing Firms:** TrueNorth, Oncology Analytics, ION Solutions
- **Pain Points:** ⭐ High denial rates (oncology denials 10-15%+), prior auth delays (avg 2-14 days), complex drug billing (buy-and-bill, waste, modifiers), staff burnout
- **RISA Opportunity:** ⭐⭐ **CORE MARKET** — AI-powered denial prevention, prior auth automation, coding accuracy (chemo regimens, genomic tests, radiation), underpayment detection
- **Money Flow:** ← Provider fees (% of collections or per-claim) → technology, staff
- **Data Flow:** Generates → claims data, denial patterns, payment data; Consumes ← clinical documentation, payer rules, fee schedules

### 6.4 AI Companies in Oncology
- **Clinical AI:**
  - Tempus — Genomics + AI platform, clinical decision support
  - Flatiron Health — RWD analytics, clinical trial optimization
  - Paige AI — Digital pathology
  - Lunit — Radiology + pathology AI
  - PathAI — Pathology AI for biopharma
- **RCM AI:**
  - **RISA Labs** — Oncology-focused RCM AI ⭐
  - Waystar AI — Denial prediction, prior auth
  - Olive AI (shut down 2023) — Cautionary tale; over-promised automation
  - Akasa — RCM automation
  - AKASA, Infinx — Prior auth AI
- **Patient Access AI:**
  - Notable Health — Workflow automation, patient intake
  - Qventus — Operational AI, capacity optimization
  - Cedar — Patient financial engagement
- **Pain Points:** Integration complexity, trust/explainability, proving ROI
- **RISA Opportunity:** Differentiate via oncology domain depth (vs. horizontal RCM AI)

### 6.5 Radiation Oncology Technology
- **Varian (Siemens Healthineers)** — Linear accelerators, ARIA OIS, Ethos adaptive RT
- **Elekta** — Linacs, Unity MR-Linac, MOSAIQ OIS
- **ViewRay** — MRIdian MR-guided radiation (filed bankruptcy 2023, IP acquired)
- **Accuray** — CyberKnife, TomoTherapy
- **Role:** Treatment planning, delivery, quality assurance
- **Pain Points:** Complex billing (technical + professional, planning codes), machine utilization
- **RISA Opportunity:** Radiation oncology billing accuracy (one of the most complex billing areas in medicine)

### 6.6 Data Aggregators
- **Definitive Healthcare** — Provider intelligence, claims analytics
- **IQVIA** — Prescription + medical claims + clinical trial data
- **Komodo Health** — Healthcare map, patient journey analytics
- **Symphony Health (IQVIA)** — Prescription-level data
- **Truveta** — Health system consortium data
- **Role:** Market intelligence, targeting, outcomes research
- **RISA Opportunity:** Use aggregated data for benchmarking denial rates, identifying payer-specific patterns

---

## 7. ⚖️ REGULATORS & GUIDELINES

### 7.1 FDA
- **Role:** Drug/biologic approvals, breakthrough therapy designation, accelerated approval, CDx approvals
- **Key Oncology Actions:** RTOR (Real-Time Oncology Review), Project Orbis (international collaboration)
- **Impact on RISA:** New approvals → new billing codes → coding updates needed rapidly

### 7.2 CMS
- **Role:** Coverage determinations (NCD/LCD), payment models (OPPS, PFS, IPPS), quality programs (MIPS, APMs)
- **Key Programs:** EOM, MIPS oncology measures, radiation oncology APM (RO Model)
- **Impact on RISA:** ⭐ CMS rules directly drive billing complexity; policy changes = product updates

### 7.3 NCCN (National Comprehensive Cancer Network)
- **Role:** Gold-standard treatment guidelines; compendia listing drives coverage
- **NCCN Compendia:** Used by payers to determine drug coverage (off-label use)
- **Impact on RISA:** NCCN guideline alignment = basis for medical necessity / appeal documentation

### 7.4 ASCO / ESMO
- **ASCO** — Largest US oncology society; QOPI certification, guidelines, CancerLinQ
- **ESMO** — European counterpart, increasingly influential globally
- **QOPI** — Quality Oncology Practice Initiative (accreditation for practices)
- **Impact on RISA:** Quality metrics integration, guideline-based coding validation

### 7.5 State Regulators
- **Certificate of Need (CON)** — Limits new facilities in some states
- **Scope of Practice** — NP/PA prescribing, pharmacy compounding
- **Oral Parity Laws** — Require equal cost-sharing for oral vs. IV chemo (43+ states)
- **Impact on RISA:** State-specific billing rules, parity compliance tracking

### 7.6 Accreditation Bodies
- **Commission on Cancer (CoC) / ACS** — Hospital cancer program accreditation
- **QOPI Certification (ASCO)** — Practice-level quality
- **ACR (American College of Radiology)** — Imaging center accreditation
- **FACT** — Cellular therapy accreditation (CAR-T)
- **Impact on RISA:** Accreditation requirements drive documentation standards → billing implications

---

## 8. 🎗️ PATIENTS & ADVOCACY

### 8.1 Patient Advocacy Organizations
- **American Cancer Society (ACS)** — Largest; research funding, patient support, advocacy
- **Leukemia & Lymphoma Society (LLS)** — Blood cancer focus, copay assistance
- **Susan G. Komen** — Breast cancer
- **Pancreatic Cancer Action Network (PanCAN)** — Pancreatic cancer
- **LUNGevity** — Lung cancer
- **Colorectal Cancer Alliance** — CRC
- **Prostate Cancer Foundation** — Prostate cancer research
- **Role:** Awareness, research funding, policy advocacy, patient support
- **Pain Points:** Financial toxicity of cancer care, access disparities, navigating the system
- **RISA Opportunity:** Financial toxicity reduction through cleaner billing, accurate patient responsibility estimates

### 8.2 Patient Navigation
- **Navigators** — Nurse navigators, lay navigators (CoC requirement)
- **Social Workers** — Psychosocial support, resource connection
- **Financial Counselors** — Benefits verification, assistance programs, cost estimation
- **Pain Points:** Overwhelmed, manual processes, fragmented resources
- **RISA Opportunity:** ⭐ Automated financial counseling tools, real-time benefits verification, assistance program matching

### 8.3 Patient Support Programs (PSPs)
- **Manufacturer Copay Assistance** — Most branded oncolytics have copay cards/programs
- **Foundation Support:** PAN Foundation, HealthWell Foundation, CancerCare, NeedyMeds
- **Free Drug Programs:** Manufacturer Patient Assistance Programs (PAPs) for uninsured
- **Pain Points:** Complex applications, eligibility tracking, accumulator/maximizer adjuster programs
- **RISA Opportunity:** PSP enrollment automation, copay accumulator tracking, coordination of benefits

### 8.4 Survivorship
- **Role:** Long-term follow-up, late effects management, surveillance
- **Scale:** ~18 million cancer survivors in US (growing)
- **Pain Points:** Care plan transitions, primary care coordination, long-term monitoring costs
- **RISA Opportunity:** Survivorship billing (transition of care codes, screening schedules)

---

## 9. 📈 FINANCIAL / INVESTMENT

### 9.1 Private Equity in Oncology
- **TPG Capital** — OneOncology (largest PE-backed oncology platform)
- **Webster Equity Partners** — Urology/oncology practices
- **General Atlantic** — OneOncology investor
- **GenStar Capital** — Specialty practice investments
- **Trend:** Aggressive consolidation of community oncology; 2020-2025 saw rapid PE entry
- **Thesis:** Economies of scale, ancillary revenue, value-based care upside, eventual strategic exit
- **RISA Opportunity:** PE-backed platforms are sophisticated buyers seeking tech-enabled efficiency; natural channel partners

### 9.2 Venture Capital
- **Oncology AI investments:** Tempus ($6.1B valuation at IPO), Guardant ($3B+ market cap)
- **Digital health in oncology:** Navigating Cancer, Jasper Health, Canopy
- **RCM AI:** Waystar (IPO 2024), Akasa, Infinx
- **Trend:** Shift from hype to proof of ROI; focus on revenue-generating AI
- **RISA Opportunity:** Well-positioned in "practical AI" narrative (revenue impact, measurable ROI)

### 9.3 Public Markets
- **Tempus AI (TEM)** — IPO June 2024, genomics + AI platform
- **Guardant Health (GH)** — Liquid biopsy leader, Shield for screening
- **Exact Sciences (EXAS)** — Cologuard, Oncotype DX
- **Natera (NTRA)** — Signatera MRD, Panorama
- **Veracyte (VCYT)** — Genomic diagnostics
- **Waystar (WAY)** — RCM technology, IPO 2024
- **Trend:** Market rewards revenue growth + path to profitability; oncology data assets command premium valuations

---

## 10. 🔄 RELATIONSHIP MAP — Key Flows

### Money Flows 💵
```
Patient ──copay/coinsurance──→ Provider
Payer ──reimbursement──→ Provider
CMS/Medicare ──FFS payments, EOM bonuses──→ Provider
Provider ──drug purchases (buy-and-bill)──→ Distributor ──payment──→ Pharma
Payer ──negotiated rates──→ Specialty Pharmacy ──dispensing──→ Patient (oral drugs)
Pharma ──rebates──→ Payer/PBM
Pharma ──copay assistance──→ Patient (via foundations)
Pharma ──trial funding──→ CRO ──site payments──→ Provider
PE/VC ──investment──→ Oncology practices / Tech companies
Provider ──management fees──→ Network Orgs (US Oncology, OneOncology)
NCI/NIH ──grants──→ Cancer Centers
Distributor ──GPO rebates──→ Provider
```

### Data Flows 📊
```
Provider ──claims──→ Clearinghouse ──→ Payer
Provider ──clinical data──→ EHR ──→ Data Aggregator (Flatiron, Tempus)
Diagnostics ──genomic reports──→ Provider ──→ EHR
Payer ──remittance/ERA──→ Provider (RCM system)
Payer ──prior auth decisions──→ Provider
Data Aggregator ──de-identified RWD──→ Pharma (market access, HEOR)
Data Aggregator ──benchmarks──→ Provider
NCCN ──guidelines──→ Provider + Payer (coverage basis)
FDA ──approvals/labels──→ All stakeholders
CMS ──coverage policies, fee schedules──→ Provider + Payer
Provider ──quality measures──→ CMS (MIPS, EOM)
Trial Platforms ──enrollment data──→ Pharma/CRO
```

### Prior Authorization Flow 🔄 (RISA Core Workflow)
```
1. Provider identifies treatment need (clinical)
2. Provider checks payer policy (coverage rules)
3. Provider submits prior auth request → Payer
4. Payer reviews (clinical criteria, pathway, NCCN, LCD)
5. Payer approves/denies/pends → Provider
6. If denied → Provider appeals (peer-to-peer, clinical documentation)
7. Treatment administered → Claim submitted
8. Claim adjudicated → Payment or denial
9. If denied → Appeal cycle begins again

RISA AI intervenes at steps 2, 3, 6, 7, 8, 9
```

### Buy-and-Bill Flow 💉 (Infused Drugs — RISA Opportunity)
```
1. Provider purchases drug from Distributor (at ASP or GPO price)
2. Drug administered to patient in clinic/hospital
3. Provider bills payer: Drug (J-code) + Administration (CPT 96413-96417)
4. Payer reimburses at ASP + 6% (Medicare) or contracted rate (commercial)
5. Margin = Reimbursement − Acquisition cost
6. Provider also bills for waste (JW modifier) if applicable

RISA AI optimizes: J-code accuracy, waste billing, NDC-to-HCPCS mapping, ASP monitoring
```

---

## 11. 🎯 RISA LABS — STRATEGIC OPPORTUNITY SUMMARY

### Primary Target Segments (by revenue opportunity)
1. **Large Community Oncology Practices** — Highest volume, most billing complexity, margin-sensitive
2. **Oncology Network Organizations** — Platform deals (one contract → hundreds of practices)
3. **Hospital System Cancer Programs** — Large but slower sales cycle
4. **Academic Medical Centers** — Complex billing, prestige customers

### Key RISA Value Propositions
| Capability | Stakeholder Impact |
|---|---|
| **Prior Auth Automation** | Reduces 2-14 day delays → faster treatment, less staff burden |
| **Denial Prevention** | Prevents 10-15% denial rate → immediate revenue recovery |
| **Coding Accuracy** | Correct J-codes, modifiers, regimen billing → reduces under/over-coding risk |
| **Drug Billing Optimization** | Buy-and-bill margin protection, waste billing, ASP monitoring |
| **Genomic Test Coverage** | LCD/NCD matching for molecular diagnostics → faster test approvals |
| **EOM/VBC Reporting** | Automated quality measures, episode cost tracking |
| **Appeals Intelligence** | AI-generated appeal letters with clinical evidence → higher overturn rates |

### Competitive Moat Opportunities
- **Oncology domain depth** — Horizontal RCM AI (Waystar, Akasa) lacks onc-specific logic
- **Regimen-aware billing** — Understanding multi-drug protocols, cycling, dose modifications
- **Payer policy intelligence** — Real-time oncology LCD/NCD/pathway tracking
- **Network effects** — More practices → better denial prediction models → more practices

---

*This market map is designed for conversion to a Whimsical mind map. Each numbered section = a primary branch. Subsections = child nodes. Bullet points = leaf nodes with detail.*
