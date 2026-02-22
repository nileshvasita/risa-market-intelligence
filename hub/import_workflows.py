#!/usr/bin/env python3
"""Parse cancer-center-workflows.md and import into market_intel.db."""

import os
import re
import sqlite3
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "market_intel.db")
MD_PATH = os.path.join(os.path.dirname(BASE_DIR), "cancer-center-workflows.md")

STAGE_NAMES = {
    1: "Referral & Access",
    2: "Intake & Registration",
    3: "Diagnosis & Staging",
    4: "Treatment Planning",
    5: "Active Treatment",
    6: "Monitoring & Response",
    7: "Survivorship & Follow-Up",
    8: "End of Life / Palliative",
    9: "Behind the Scenes",
}

# Map department keywords to common stakeholder roles
DEPT_STAKEHOLDERS = {
    "Patient Access": [
        ("Patient Access Coordinator", "Intake and scheduling", "Executor"),
        ("Insurance Verification Specialist", "Verify coverage and benefits", "Executor"),
        ("Financial Counselor", "Cost estimation and assistance", "Executor"),
        ("Front Desk Staff", "Check-in and registration", "Executor"),
    ],
    "Clinical Ops": [
        ("Oncologist (MD/DO)", "Clinical decision-making", "Approver"),
        ("Oncology Nurse (RN/OCN)", "Patient assessment and care delivery", "Executor"),
        ("Clinical Pharmacist", "Medication review and verification", "Reviewer"),
        ("APP (NP/PA)", "Clinical support and documentation", "Executor"),
    ],
    "BMT/Cell Therapy": [
        ("Transplant Physician", "Transplant decision-making", "Approver"),
        ("BMT Coordinator", "Transplant logistics and coordination", "Executor"),
        ("Transplant Pharmacist", "Drug management", "Reviewer"),
        ("Cell Therapy Lab Director", "Product quality oversight", "Approver"),
    ],
    "RCM": [
        ("Revenue Cycle Manager", "RCM operations oversight", "Approver"),
        ("Medical Coder (CPC/CCS)", "Coding and charge capture", "Executor"),
        ("Billing Specialist", "Claims and follow-up", "Executor"),
        ("Denial Management Specialist", "Appeals and denial resolution", "Executor"),
    ],
    "Research": [
        ("Principal Investigator", "Study oversight and decisions", "Approver"),
        ("Clinical Research Coordinator", "Study operations and data", "Executor"),
        ("Research Nurse", "Clinical trial patient care", "Executor"),
        ("Regulatory Specialist", "Compliance and submissions", "Executor"),
    ],
    "Quality": [
        ("Quality Director", "Quality program oversight", "Approver"),
        ("Compliance Officer", "Regulatory compliance", "Reviewer"),
        ("Quality Analyst", "Data analysis and reporting", "Executor"),
    ],
    "Admin": [
        ("Practice Administrator", "Operational oversight", "Approver"),
        ("IT Director", "Technology management", "Executor"),
        ("HR Manager", "Staffing and workforce", "Executor"),
    ],
}

# Templates for generating workflow steps based on department/keywords
def generate_steps(wf_name, department, description):
    """Generate 3-6 logical workflow steps based on the workflow type."""
    steps = []

    name_lower = wf_name.lower()
    desc_lower = description.lower()

    if "prior auth" in name_lower or "authorization" in name_lower:
        steps = [
            ("Identify authorization requirement", "Prior Auth Specialist", "EHR", 3, 0, 1),
            ("Gather clinical documentation from EHR", "Prior Auth Specialist", "EHR", 10, 1, 1),
            ("Complete payer-specific auth form", "Prior Auth Specialist", "Payer Portal/Fax", 8, 0, 1),
            ("Submit to payer", "Prior Auth Specialist", "Payer Portal/Fax", 5, 0, 1),
            ("Track status and follow up", "Prior Auth Specialist", "Phone/Portal", 15, 1, 1),
            ("Document outcome in EHR", "Prior Auth Specialist", "EHR", 3, 0, 1),
        ]
    elif "referral" in name_lower and "intake" in name_lower:
        steps = [
            ("Receive referral (fax/electronic)", "Referral Coordinator", "Fax Server/Portal", 2, 0, 1),
            ("Extract patient demographics and clinical info", "Referral Coordinator", "Manual/OCR", 10, 1, 1),
            ("Enter data into EHR", "Referral Coordinator", "EHR", 5, 0, 1),
            ("Triage for urgency and routing", "Triage Nurse", "EHR", 8, 1, 0),
            ("Route to appropriate provider/service", "Referral Coordinator", "EHR", 3, 0, 1),
        ]
    elif "scheduling" in name_lower or "schedule" in name_lower:
        steps = [
            ("Review scheduling request/order", "Scheduler", "EHR", 3, 0, 0),
            ("Check provider/resource availability", "Scheduler", "Scheduling System", 5, 0, 1),
            ("Match patient needs to available slots", "Scheduler", "Scheduling System", 5, 1, 1),
            ("Book appointment and send confirmation", "Scheduler", "EHR/Phone", 3, 0, 1),
            ("Send reminder and prep instructions", "Scheduler", "Patient Portal/Phone", 2, 0, 1),
        ]
    elif "billing" in name_lower or "claims" in name_lower or "charge" in name_lower:
        steps = [
            ("Capture charges from clinical activity", "Charge Capture Specialist", "EHR", 5, 0, 1),
            ("Review and validate coding", "Medical Coder", "Coding Software", 8, 1, 1),
            ("Scrub claim for errors", "Billing Specialist", "Claims Engine", 3, 0, 1),
            ("Submit claim to payer", "Billing Specialist", "Clearinghouse", 2, 0, 1),
            ("Track remittance and post payment", "Payment Poster", "Practice Mgmt System", 5, 0, 1),
        ]
    elif "denial" in name_lower or "appeal" in name_lower:
        steps = [
            ("Receive and categorize denial", "Denial Specialist", "RCM System", 5, 0, 1),
            ("Analyze root cause", "Denial Specialist", "EHR/RCM System", 10, 1, 1),
            ("Gather clinical supporting documentation", "Denial Specialist", "EHR", 15, 1, 1),
            ("Draft and submit appeal", "Denial Specialist", "Payer Portal/Fax", 20, 0, 1),
            ("Track appeal outcome", "Denial Specialist", "RCM System", 5, 0, 1),
        ]
    elif "infusion" in name_lower or "chemotherapy" in name_lower or "chemo" in name_lower:
        steps = [
            ("Verify treatment order and protocol", "Oncology Pharmacist", "EHR", 5, 0, 1),
            ("Check labs and treatment criteria", "Oncology Nurse", "EHR", 5, 1, 1),
            ("Prepare/compound medications", "Pharmacy Tech", "Pharmacy System", 15, 1, 0),
            ("Administer pre-medications", "Infusion Nurse", "EHR/Pump", 10, 0, 0),
            ("Administer treatment and monitor", "Infusion Nurse", "EHR/Pump", 30, 0, 0),
            ("Document and discharge", "Infusion Nurse", "EHR", 5, 0, 1),
        ]
    elif "radiation" in name_lower:
        steps = [
            ("Review treatment plan/prescription", "Radiation Oncologist", "Treatment Planning System", 5, 0, 0),
            ("Patient setup and positioning", "Radiation Therapist", "Linac/CBCT", 10, 0, 0),
            ("Image guidance verification", "Radiation Therapist", "IGRT System", 5, 0, 1),
            ("Deliver treatment", "Radiation Therapist", "Linac", 10, 0, 0),
            ("Document treatment delivery", "Radiation Therapist", "R&V System", 3, 0, 1),
        ]
    elif "tumor board" in name_lower:
        steps = [
            ("Identify cases for presentation", "Tumor Board Coordinator", "EHR", 5, 0, 1),
            ("Compile case materials (imaging, path, genomics)", "Tumor Board Coordinator", "EHR/PACS", 30, 1, 1),
            ("Present case to multidisciplinary team", "Presenting Physician", "Conference System", 15, 0, 0),
            ("Discuss and reach consensus", "MDT Panel", "Conference", 10, 0, 0),
            ("Document recommendations in EHR", "Tumor Board Coordinator", "EHR", 10, 0, 1),
        ]
    elif "clinical trial" in name_lower or "trial" in name_lower or "research" in name_lower:
        steps = [
            ("Review protocol requirements", "Research Coordinator", "CTMS", 10, 0, 0),
            ("Screen patient/data against criteria", "Research Coordinator", "EHR/CTMS", 15, 1, 1),
            ("Collect and enter data", "Research Coordinator", "EDC System", 20, 1, 1),
            ("Quality check and query resolution", "Research Coordinator", "EDC System", 10, 0, 1),
            ("Report/submit per protocol", "Research Coordinator", "EDC/Regulatory", 10, 0, 1),
        ]
    elif "transplant" in name_lower or "bmt" in name_lower or "stem cell" in name_lower:
        steps = [
            ("Review patient eligibility/status", "Transplant Physician", "EHR", 10, 0, 0),
            ("Coordinate logistics and scheduling", "BMT Coordinator", "EHR/Phone", 15, 1, 0),
            ("Verify labs and clinical parameters", "Transplant Nurse", "EHR/Lab", 10, 0, 1),
            ("Execute procedure/protocol step", "Clinical Team", "Clinical Systems", 20, 0, 0),
            ("Document and follow up", "BMT Coordinator", "EHR", 10, 0, 1),
        ]
    elif "car-t" in name_lower or "cell therapy" in name_lower:
        steps = [
            ("Verify eligibility and product status", "Cell Therapy Coordinator", "CTMS/EHR", 10, 0, 0),
            ("Coordinate with manufacturer/lab", "Cell Therapy Coordinator", "Phone/Portal", 15, 1, 0),
            ("Prepare patient (lymphodepletion if applicable)", "Oncologist", "EHR", 10, 0, 0),
            ("Administer therapy and monitor", "Infusion Team", "EHR/Monitoring", 30, 0, 0),
            ("Document and report outcomes", "Cell Therapy Coordinator", "EHR/Registry", 10, 0, 1),
        ]
    elif "documentation" in name_lower or "note" in name_lower or "coding" in name_lower:
        steps = [
            ("Review clinical encounter/data", "Provider/Coder", "EHR", 5, 0, 0),
            ("Draft/generate documentation", "Provider/Coder", "EHR/Coding System", 15, 1, 1),
            ("Review for accuracy and completeness", "Reviewer", "EHR", 10, 0, 1),
            ("Finalize and sign/submit", "Provider/Coder", "EHR", 3, 0, 0),
        ]
    elif "monitor" in name_lower or "surveillance" in name_lower or "tracking" in name_lower:
        steps = [
            ("Collect data/metrics", "Analyst/Coordinator", "EHR/System", 10, 0, 1),
            ("Analyze and identify trends/issues", "Analyst", "Analytics Tool", 15, 1, 1),
            ("Flag exceptions and escalate", "Analyst/Manager", "Alert System", 5, 0, 1),
            ("Report findings to stakeholders", "Manager", "Reporting Tool", 10, 0, 1),
        ]
    elif "compliance" in name_lower or "audit" in name_lower or "accreditation" in name_lower:
        steps = [
            ("Review standards/requirements", "Compliance Officer", "Policy System", 10, 0, 0),
            ("Collect documentation and evidence", "Compliance Analyst", "Multiple Systems", 20, 1, 1),
            ("Assess gaps and findings", "Compliance Officer", "Audit Tool", 15, 1, 1),
            ("Develop corrective action plan", "Compliance Officer", "Document System", 10, 0, 0),
            ("Track remediation and report", "Compliance Analyst", "Tracking System", 10, 0, 1),
        ]
    elif "patient" in name_lower and ("education" in name_lower or "consent" in name_lower or "counseling" in name_lower):
        steps = [
            ("Identify education/consent need", "Clinical Staff", "EHR", 3, 0, 1),
            ("Prepare materials for patient", "Clinical Staff", "Education System", 5, 0, 1),
            ("Deliver information to patient", "Provider/Nurse", "In-person/Portal", 15, 0, 0),
            ("Assess understanding and document", "Provider/Nurse", "EHR", 5, 0, 1),
        ]
    else:
        # Generic steps based on description keywords
        steps = [
            ("Initiate/receive request", "Staff", "EHR/Phone/System", 5, 0, 0),
            ("Review and gather required information", "Staff", "EHR/Multiple", 10, 1, 1),
            ("Process/execute main task", "Staff", "Primary System", 15, 0, 0),
            ("Verify and quality check", "Supervisor/Reviewer", "System", 5, 0, 1),
            ("Document and close", "Staff", "EHR/System", 5, 0, 1),
        ]

    return steps


def get_stakeholders(wf_name, department):
    """Return context-specific stakeholders based on workflow name + department."""
    name = wf_name.lower()

    # --- Workflow-specific mappings (checked first) ---
    if "prior auth" in name or "authorization" in name:
        return [
            ("Prior Auth Specialist", "Compile clinical docs and submit PA requests", "Executor"),
            ("Medical Director (Payer)", "Review and approve/deny auth requests", "Approver"),
            ("Oncologist", "Provide clinical justification and peer-to-peer", "Reviewer"),
            ("Patient Access Director", "Oversee PA operations and escalations", "Informed"),
            ("Payer Representative", "Process auth requests per plan criteria", "External"),
        ]
    if "referral" in name and ("intake" in name or "triage" in name):
        return [
            ("Referral Coordinator", "Receive, parse, and route referrals", "Executor"),
            ("Triage Nurse (RN)", "Clinical assessment and urgency classification", "Executor"),
            ("Patient Access Director", "Oversee referral operations", "Approver"),
            ("Referring Physician", "Originate referral and provide clinical data", "External"),
        ]
    if "scheduling" in name or "schedule" in name:
        return [
            ("Scheduling Coordinator", "Book appointments and manage calendars", "Executor"),
            ("Practice Manager", "Oversee scheduling templates and policies", "Reviewer"),
            ("Provider (MD/APP)", "Set schedule preferences and availability", "Informed"),
        ]
    if ("insurance" in name or "eligibility" in name or "benefits" in name) and "bmt" not in name and "transplant" not in name:
        return [
            ("Insurance Verification Specialist", "Verify coverage and benefits details", "Executor"),
            ("Financial Counselor", "Communicate costs and options to patient", "Executor"),
            ("Patient Access Director", "Oversee verification operations", "Approver"),
            ("Payer Representative", "Provide eligibility and benefit data", "External"),
        ]
    if "financial counsel" in name or "copay" in name or "payment plan" in name or "assistance" in name:
        return [
            ("Financial Counselor", "Assess patient financial needs and options", "Executor"),
            ("Patient Access Director", "Approve financial assistance decisions", "Approver"),
            ("CFO/Finance Director", "Set financial assistance policies", "Informed"),
            ("Patient", "Provide financial information and make decisions", "External"),
        ]
    if "denial" in name or "appeal" in name:
        return [
            ("Denial Management Specialist", "Analyze denials and prepare appeals", "Executor"),
            ("Revenue Cycle Director", "Oversee denial management operations", "Approver"),
            ("Oncologist", "Provide clinical support for appeals", "Reviewer"),
            ("Medical Coder (CPC/CCS)", "Review coding accuracy on denied claims", "Reviewer"),
            ("Payer Medical Director", "Review appeals and make coverage decisions", "External"),
        ]
    if "billing" in name or "claims" in name or "charge" in name:
        return [
            ("Billing Specialist", "Submit and manage claims", "Executor"),
            ("Medical Coder (CPC/CCS)", "Assign diagnosis and procedure codes", "Executor"),
            ("Revenue Cycle Director", "Oversee billing operations", "Approver"),
            ("CFO", "Financial oversight and reporting", "Informed"),
        ]
    if "coding" in name:
        return [
            ("Medical Coder (CPC/CCS)", "Assign ICD-10/CPT codes from documentation", "Executor"),
            ("CDI Specialist", "Query providers for documentation specificity", "Executor"),
            ("Coding Manager", "Oversee coding accuracy and compliance", "Approver"),
            ("Compliance Officer", "Audit coding for regulatory compliance", "Reviewer"),
        ]
    if "drug" in name and ("billing" in name or "reimbursement" in name or "waste" in name):
        return [
            ("Pharmacy Billing Specialist", "Manage drug charge capture and coding", "Executor"),
            ("Oncology Pharmacist", "Verify drug administration and waste", "Reviewer"),
            ("Revenue Cycle Director", "Oversee drug revenue integrity", "Approver"),
            ("CFO", "Monitor drug margin and reimbursement", "Informed"),
        ]
    if "infusion" in name and ("admin" in name or "suite" in name or "chair" in name):
        return [
            ("Infusion Nurse (OCN/ONS)", "Administer treatment and monitor patient", "Executor"),
            ("Charge Nurse", "Manage chair assignments and nursing staff", "Executor"),
            ("Oncology Pharmacist", "Verify orders and prepare medications", "Reviewer"),
            ("Clinical Ops Director", "Oversee infusion operations", "Approver"),
        ]
    if "chemotherapy" in name or "chemo" in name:
        return [
            ("Oncologist", "Order and oversee chemotherapy regimen", "Approver"),
            ("Oncology Pharmacist", "Verify doses, interactions, and compound", "Reviewer"),
            ("Infusion Nurse (OCN)", "Administer treatment", "Executor"),
            ("Clinical Ops Director", "Oversee treatment operations", "Informed"),
        ]
    if "radiation" in name:
        return [
            ("Radiation Oncologist", "Prescribe and oversee radiation therapy", "Approver"),
            ("Medical Physicist", "Plan dosimetry and QA", "Reviewer"),
            ("Radiation Therapist (RTT)", "Deliver daily treatments", "Executor"),
            ("Dosimetrist", "Develop treatment plans", "Executor"),
        ]
    if "tumor board" in name:
        return [
            ("Tumor Board Coordinator", "Prepare cases and manage logistics", "Executor"),
            ("Medical Oncologist", "Present and discuss treatment options", "Reviewer"),
            ("Surgical Oncologist", "Provide surgical perspective", "Reviewer"),
            ("Radiation Oncologist", "Provide radiation perspective", "Reviewer"),
            ("Pathologist", "Review and present pathology findings", "Reviewer"),
        ]
    if "surgery" in name or "surgical" in name:
        return [
            ("Surgical Oncologist", "Perform surgical procedure", "Approver"),
            ("Anesthesiologist", "Manage anesthesia and periop care", "Executor"),
            ("OR Nurse", "Assist in surgery and specimen handling", "Executor"),
            ("Surgical Coordinator", "Schedule and coordinate pre/post-op", "Executor"),
        ]
    if "pathology" in name or "specimen" in name:
        return [
            ("Pathologist", "Interpret specimens and issue reports", "Approver"),
            ("Histotechnologist", "Process and prepare tissue specimens", "Executor"),
            ("Lab Director", "Oversee laboratory operations", "Reviewer"),
        ]
    if "genomic" in name or "molecular" in name or "genetic" in name:
        return [
            ("Genetic Counselor", "Counsel patients and interpret results", "Executor"),
            ("Oncologist", "Order testing and integrate into treatment plan", "Approver"),
            ("Molecular Pathologist", "Oversee testing and reporting", "Reviewer"),
            ("Lab Coordinator", "Manage specimen logistics and tracking", "Executor"),
        ]
    if "transplant" in name or "bmt" in name or "stem cell" in name:
        return [
            ("Transplant Physician", "Clinical decision-making for transplant", "Approver"),
            ("BMT Coordinator", "Coordinate logistics and patient management", "Executor"),
            ("Transplant Pharmacist", "Manage conditioning and immunosuppression", "Reviewer"),
            ("Social Worker", "Psychosocial assessment and support", "Executor"),
            ("BMT Program Director", "Program oversight and quality", "Informed"),
        ]
    if "car-t" in name or "cell therapy" in name:
        return [
            ("Cell Therapy Physician", "Oversee CAR-T treatment decisions", "Approver"),
            ("Cell Therapy Coordinator", "Manage manufacturing logistics", "Executor"),
            ("Cell Therapy Pharmacist", "Drug management and REMS compliance", "Reviewer"),
            ("Cell Processing Lab Director", "Product quality and release", "Approver"),
        ]
    if "donor" in name:
        return [
            ("Transplant Physician", "Donor selection decisions", "Approver"),
            ("Donor Coordinator", "Manage donor search and logistics", "Executor"),
            ("HLA Lab Director", "Oversee typing and matching", "Reviewer"),
            ("NMDP/Registry Coordinator", "External donor registry liaison", "External"),
        ]
    if "gvhd" in name or "engraftment" in name:
        return [
            ("Transplant Physician", "Manage GVHD prevention and treatment", "Approver"),
            ("Transplant Nurse", "Monitor symptoms and administer treatment", "Executor"),
            ("Transplant Pharmacist", "Manage immunosuppression levels", "Reviewer"),
        ]
    if "clinical trial" in name or "trial" in name:
        return [
            ("Principal Investigator", "Scientific and regulatory oversight", "Approver"),
            ("Clinical Research Coordinator", "Day-to-day study operations", "Executor"),
            ("Research Nurse", "Clinical care of trial patients", "Executor"),
            ("IRB/Ethics Board", "Ethical review and approval", "Approver"),
            ("Sponsor/CRO", "Study funding and monitoring", "External"),
        ]
    if "irb" in name or "regulatory" in name:
        return [
            ("Regulatory Specialist", "Prepare and submit regulatory documents", "Executor"),
            ("Principal Investigator", "Regulatory signatory", "Approver"),
            ("IRB Chair", "Review and approve protocols", "Approver"),
            ("Research Compliance Officer", "Ensure regulatory compliance", "Reviewer"),
        ]
    if "grant" in name:
        return [
            ("Principal Investigator", "Write and manage grant", "Executor"),
            ("Grants Administrator", "Budget and compliance management", "Executor"),
            ("Department Chair", "Institutional endorsement", "Approver"),
            ("NIH/Funding Agency", "Review and fund grants", "External"),
        ]
    if "data" in name and ("collection" in name or "entry" in name or "report" in name):
        return [
            ("Clinical Research Coordinator", "Collect and enter study data", "Executor"),
            ("Data Manager", "Ensure data quality and compliance", "Reviewer"),
            ("Biostatistician", "Analyze study data", "Executor"),
            ("Principal Investigator", "Oversee data integrity", "Approver"),
        ]
    if "palliative" in name or "hospice" in name or "end of life" in name:
        return [
            ("Palliative Care Physician", "Lead goals-of-care discussions", "Approver"),
            ("Palliative Care Nurse", "Symptom management and coordination", "Executor"),
            ("Social Worker", "Psychosocial support and hospice coordination", "Executor"),
            ("Oncologist", "Collaborate on care transition", "Reviewer"),
            ("Chaplain", "Spiritual care and support", "Executor"),
        ]
    if "survivorship" in name:
        return [
            ("Oncologist", "Develop survivorship care plan", "Approver"),
            ("Survivorship Nurse/APP", "Deliver survivorship care", "Executor"),
            ("Primary Care Physician", "Continue monitoring in community", "External"),
            ("Social Worker", "Connect to support resources", "Executor"),
        ]
    if "triage" in name or "nurse" in name and "phone" in name:
        return [
            ("Triage Nurse (RN/OCN)", "Assess symptoms and determine urgency", "Executor"),
            ("On-Call Oncologist", "Provide medical guidance for escalations", "Approver"),
            ("Clinical Ops Director", "Oversee triage operations", "Informed"),
        ]
    if "documentation" in name or "note" in name or "scribe" in name:
        return [
            ("Oncologist/APP", "Author clinical documentation", "Executor"),
            ("Medical Scribe", "Assist with real-time documentation", "Executor"),
            ("CDI Specialist", "Review documentation quality", "Reviewer"),
            ("HIM Director", "Oversee health information management", "Informed"),
        ]
    if "quality" in name or "qopi" in name or "accreditation" in name:
        return [
            ("Quality Director", "Oversee quality programs", "Approver"),
            ("Quality Analyst", "Collect and analyze quality data", "Executor"),
            ("Medical Director", "Clinical quality leadership", "Reviewer"),
            ("Compliance Officer", "Ensure regulatory compliance", "Reviewer"),
        ]
    if "compliance" in name or "audit" in name or "hipaa" in name:
        return [
            ("Compliance Officer", "Lead compliance programs", "Approver"),
            ("Compliance Analyst", "Monitor and investigate", "Executor"),
            ("Legal Counsel", "Legal guidance on compliance matters", "Reviewer"),
            ("CEO/Practice Administrator", "Organizational accountability", "Informed"),
        ]
    if "credentialing" in name or "enrollment" in name or "licensing" in name:
        return [
            ("Credentialing Coordinator", "Process applications and verifications", "Executor"),
            ("Medical Staff Director", "Oversee credentialing program", "Approver"),
            ("Provider", "Submit required documentation", "Informed"),
        ]
    if "lab" in name and ("draw" in name or "processing" in name or "result" in name):
        return [
            ("Phlebotomist", "Draw blood specimens", "Executor"),
            ("Lab Technologist", "Process and run lab tests", "Executor"),
            ("Lab Director", "Oversee laboratory operations", "Approver"),
            ("Oncologist", "Review and act on results", "Reviewer"),
        ]
    if "imaging" in name:
        return [
            ("Radiologist", "Interpret imaging studies", "Approver"),
            ("Imaging Technologist", "Perform imaging procedures", "Executor"),
            ("Oncologist", "Order and review imaging", "Reviewer"),
            ("Imaging Coordinator", "Schedule and manage imaging workflow", "Executor"),
        ]
    if "pharmacy" in name or "drug" in name or "medication" in name:
        return [
            ("Oncology Pharmacist", "Clinical pharmacy oversight", "Reviewer"),
            ("Pharmacy Technician", "Prepare and compound medications", "Executor"),
            ("Pharmacy Director", "Manage pharmacy operations", "Approver"),
            ("Oncologist", "Prescribe and adjust medications", "Approver"),
        ]
    if "social work" in name or "distress" in name or "psycho" in name:
        return [
            ("Oncology Social Worker", "Psychosocial assessment and support", "Executor"),
            ("Psycho-Oncologist", "Specialized psychological care", "Executor"),
            ("Clinical Ops Director", "Oversee supportive care services", "Approver"),
        ]
    if "nutrition" in name or "dietitian" in name:
        return [
            ("Oncology Dietitian", "Nutritional assessment and counseling", "Executor"),
            ("Oncologist", "Refer and collaborate on nutrition", "Reviewer"),
            ("Clinical Ops Director", "Oversee nutrition services", "Informed"),
        ]
    if "patient portal" in name or "telehealth" in name or "remote" in name:
        return [
            ("IT Support Specialist", "Technical setup and troubleshooting", "Executor"),
            ("Clinical Staff", "Guide patients through technology", "Executor"),
            ("IT Director", "Oversee digital health platforms", "Approver"),
        ]
    if "payer contract" in name or "fee schedule" in name or "contract" in name:
        return [
            ("Payer Contracting Manager", "Negotiate and manage contracts", "Executor"),
            ("CFO", "Approve contract terms and financial models", "Approver"),
            ("Revenue Cycle Director", "Assess operational impact", "Reviewer"),
            ("Payer Representative", "Negotiate on behalf of health plan", "External"),
        ]
    if "340b" in name:
        return [
            ("340B Program Manager", "Manage 340B operations and compliance", "Executor"),
            ("Pharmacy Director", "Oversee drug purchasing under 340B", "Approver"),
            ("Compliance Officer", "Ensure HRSA audit readiness", "Reviewer"),
            ("CFO", "Monitor 340B revenue impact", "Informed"),
        ]
    if "value" in name and ("based" in name or "eom" in name or "ocm" in name):
        return [
            ("Value-Based Care Manager", "Track episodes and quality measures", "Executor"),
            ("Medical Director", "Clinical quality and cost leadership", "Approver"),
            ("Data Analyst", "Analyze episode costs and outcomes", "Executor"),
            ("Practice Administrator", "Operational transformation", "Reviewer"),
        ]
    if "staffing" in name or "recruit" in name or "onboard" in name or "workforce" in name:
        return [
            ("HR Manager", "Manage recruitment and onboarding", "Executor"),
            ("Department Manager", "Define role requirements and interview", "Reviewer"),
            ("Practice Administrator", "Approve hiring decisions", "Approver"),
        ]
    if "it" in name or "ehr" in name or "cyber" in name or "system" in name:
        return [
            ("IT Director", "Oversee technology infrastructure", "Approver"),
            ("IT Analyst/Engineer", "Implement and maintain systems", "Executor"),
            ("CISO/Security Officer", "Manage cybersecurity", "Reviewer"),
            ("Clinical Informatics", "Bridge clinical needs with IT", "Reviewer"),
        ]
    if "marketing" in name or "outreach" in name or "referral develop" in name:
        return [
            ("Marketing Director", "Oversee marketing and outreach strategy", "Approver"),
            ("Physician Liaison", "Develop referral relationships", "Executor"),
            ("Practice Administrator", "Approve marketing investments", "Informed"),
        ]

    # --- Fall back to department-level mappings ---
    for key, roles in DEPT_STAKEHOLDERS.items():
        if key.lower() in department.lower():
            return roles
    dept_lower = department.lower()
    if "access" in dept_lower or "front" in dept_lower:
        return DEPT_STAKEHOLDERS["Patient Access"]
    if "clinical" in dept_lower or "ops" in dept_lower:
        return DEPT_STAKEHOLDERS["Clinical Ops"]
    if "bmt" in dept_lower or "cell" in dept_lower or "transplant" in dept_lower:
        return DEPT_STAKEHOLDERS["BMT/Cell Therapy"]
    if "rcm" in dept_lower or "revenue" in dept_lower or "billing" in dept_lower:
        return DEPT_STAKEHOLDERS["RCM"]
    if "research" in dept_lower or "trial" in dept_lower:
        return DEPT_STAKEHOLDERS["Research"]
    if "quality" in dept_lower or "compliance" in dept_lower:
        return DEPT_STAKEHOLDERS["Quality"]
    return DEPT_STAKEHOLDERS["Admin"]


def estimate_complexity(pain_points, description):
    """Estimate workflow complexity from text."""
    text = (pain_points + " " + description).lower()
    high_indicators = ["complex", "life-threatening", "critical", "extensive", "manual",
                       "multiple", "hundreds", "thousands", "time-consuming"]
    score = sum(1 for w in high_indicators if w in text)
    if score >= 3:
        return "High"
    elif score >= 1:
        return "Medium"
    return "Low"


def estimate_bottleneck(pain_points, description, department):
    """Estimate bottleneck severity 1-5."""
    text = (pain_points + " " + description).lower()
    score = 0
    # High-severity indicators
    for w in ["#1 pain point", "life-threatening", "critical bottleneck", "massive", "#1 driver",
              "#1 rcm", "billions", "crisis"]:
        if w in text: score += 3
    # Medium-severity indicators
    for w in ["delay", "bottleneck", "time-consuming", "high volume", "backlog", "burnout",
              "manual", "thousands", "hundreds", "hours", "wasted", "loss", "lost", "denied",
              "denials", "shortage", "complex", "inconsistent", "error", "burden", "frustrated",
              "compliance", "risk", "slow", "wait", "gap", "miss", "incomplete", "difficult",
              "track", "multiple", "confus", "variab", "overbook", "barriers", "under-",
              "opaqu", "costly", "expensive", "patient", "volume", "frequent", "limited",
              "labor", "intensive", "fragmented", "siloed", "duplicat", "redund", "fail"]:
        if w in text: score += 1
    # Department weight (patient-facing higher)
    dept = department.lower()
    if "access" in dept: score += 1
    if "rcm" in dept or "revenue" in dept: score += 1
    if "clinical" in dept: score += 1
    # Normalize to 1-5 (aim for bell curve centered around 3)
    if score >= 8: return 5
    if score >= 6: return 4
    if score >= 4: return 3
    if score >= 2: return 2
    return 1


def estimate_time(department, description):
    """Estimate average time in minutes."""
    desc = description.lower()
    # Look for explicit time mentions
    m = re.search(r'(\d+)-?(\d+)?\s*min', desc)
    if m:
        return int(m.group(2) or m.group(1))
    m = re.search(r'(\d+)-?(\d+)?\s*hour', desc)
    if m:
        return int(m.group(2) or m.group(1)) * 60

    dept = department.lower()
    if "access" in dept:
        return random.choice([10, 15, 20, 25, 30])
    if "clinical" in dept:
        return random.choice([15, 20, 30, 45, 60])
    if "bmt" in dept or "cell" in dept:
        return random.choice([30, 45, 60, 90, 120])
    if "rcm" in dept or "revenue" in dept:
        return random.choice([10, 15, 20, 30])
    if "research" in dept:
        return random.choice([20, 30, 45, 60])
    return random.choice([15, 20, 30])


def parse_workflows(md_path):
    """Parse the markdown file and return list of workflow dicts."""
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Pattern: WF### | Name | Category | Stage | Description | Centers | Pain Points | AI Opportunity
    pattern = re.compile(
        r'^(WF\d{3})\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(\d)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*\*\*(.+?)\*\*\s*[-—]\s*(.+?)$',
        re.MULTILINE
    )

    workflows = []
    for m in pattern.finditer(content):
        wf_id = m.group(1)
        name = m.group(2).strip()
        department = m.group(3).strip()
        stage = int(m.group(4))
        description = m.group(5).strip()
        centers = m.group(6).strip()
        pain_points = m.group(7).strip()
        risa_product = m.group(8).strip()
        risa_detail = m.group(9).strip()

        workflows.append({
            "workflow_id": wf_id,
            "name": name,
            "department": department,
            "patient_journey_stage": stage,
            "stage_name": STAGE_NAMES.get(stage, "Unknown"),
            "description": description,
            "centers_applicable": centers,
            "pain_points": pain_points,
            "risa_opportunity": "{} - {}".format(risa_product, risa_detail),
            "complexity": estimate_complexity(pain_points, description),
            "avg_time_minutes": estimate_time(department, description),
            "bottleneck_severity": estimate_bottleneck(pain_points, description, department),
        })

    return workflows


def import_workflows():
    """Main import function."""
    random.seed(42)  # Reproducible estimates

    workflows = parse_workflows(MD_PATH)
    print("Parsed {} workflows from markdown".format(len(workflows)))

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Clear existing data
    c.execute("DELETE FROM workflow_stakeholders")
    c.execute("DELETE FROM workflow_steps")
    c.execute("DELETE FROM workflows")

    imported = 0
    for wf in workflows:
        c.execute("""
            INSERT OR REPLACE INTO workflows
            (workflow_id, name, department, patient_journey_stage, stage_name,
             description, centers_applicable, pain_points, risa_opportunity,
             complexity, avg_time_minutes, bottleneck_severity)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, [
            wf["workflow_id"], wf["name"], wf["department"],
            wf["patient_journey_stage"], wf["stage_name"],
            wf["description"], wf["centers_applicable"],
            wf["pain_points"], wf["risa_opportunity"],
            wf["complexity"], wf["avg_time_minutes"],
            wf["bottleneck_severity"],
        ])
        db_id = c.lastrowid

        # Generate and insert steps
        steps = generate_steps(wf["name"], wf["department"], wf["description"])
        for i, (desc, actor, system, time_min, is_bottle, is_auto) in enumerate(steps, 1):
            c.execute("""
                INSERT INTO workflow_steps
                (workflow_id, step_number, description, actor, system_used,
                 avg_time_minutes, is_bottleneck, is_automatable)
                VALUES (?,?,?,?,?,?,?,?)
            """, [db_id, i, desc, actor, system, time_min, is_bottle, is_auto])

        # Generate and insert stakeholders
        stakeholders = get_stakeholders(wf["name"], wf["department"])
        for role_name, responsibility, authority in stakeholders:
            c.execute("""
                INSERT INTO workflow_stakeholders
                (workflow_id, role_name, responsibility, decision_authority)
                VALUES (?,?,?,?)
            """, [db_id, role_name, responsibility, authority])

        imported += 1

    conn.commit()

    # Print summary
    c.execute("SELECT COUNT(*) FROM workflows")
    wf_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM workflow_steps")
    step_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM workflow_stakeholders")
    stake_count = c.fetchone()[0]

    print("Import complete:")
    print("  Workflows: {}".format(wf_count))
    print("  Steps: {}".format(step_count))
    print("  Stakeholders: {}".format(stake_count))

    # Department breakdown
    c.execute("SELECT department, COUNT(*) FROM workflows GROUP BY department ORDER BY COUNT(*) DESC")
    print("\nBy Department:")
    for row in c.fetchall():
        print("  {}: {}".format(row[0], row[1]))

    conn.close()


if __name__ == "__main__":
    import_workflows()
