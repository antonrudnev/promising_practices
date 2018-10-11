SOLR_COLLECTION = "http://10.0.49.27:8983/solr/promising_practices"
DASHBOARD_URL = "http://34.231.243.2:8983/solr/banana/opioid-dashboard/opioid-vagrant/src-host/index.html"
SYSTEM_DATABASE = "system.sqlite"
ITEMS_PER_PAGE = 15
PAGER_RANGE = 2

ALL_FIELDS = ["id", "title", "intervention_name", "summary", "public_summary", "link", "citation", "program_success",
              "city", "geography", "region", "source_type", "race", "intervention_goal", "implementers", "scale",
              "country", "program_components", "population", "status"]

MULTIVALUED_FIELDS = ["geography", "region", "race", "intervention_goal", "implementers", "scale", "country",
                      "program_components", "population"]

WORKFLOW = [{"current": "DRAFT", "next": "SUBMITTED", "action": "SUBMIT"},
            {"current": "SUBMITTED", "next": "REJECTED", "action": "REJECT"},
            {"current": "SUBMITTED", "next": "APPROVED", "action": "APPROVE"},
            {"current": "REJECTED", "next": "SUBMITTED", "action": "SUBMIT"},
            {"current": "APPROVED", "next": "REVOKED", "action": "REVOKE"},
            {"current": "REVOKED", "next": "REJECTED", "action": "REJECT"},
            {"current": "REVOKED", "next": "APPROVED", "action": "APPROVE"}]

ACTION_STYLE = {"SUBMIT": "btn-outline-primary",
                "REJECT": "btn-outline-secondary",
                "APPROVE": "btn-outline-success",
                "REVOKE": "btn-outline-warning"}

STATUS_BADGE_STYLE = {"DRAFT": "secondary",
                      "SUBMITTED": "primary",
                      "REJECTED": "secondary",
                      "APPROVED": "success",
                      "REVOKED": "warning"}

STATUS_INDEX_STYLE = {"DRAFT": "btn-outline-secondary",
                      "SUBMITTED": "btn-primary",
                      "REJECTED": "btn-secondary",
                      "APPROVED": "btn-outline-success",
                      "REVOKED": "btn-warning"}

COUNTER_QUERIES = {
    "legal_reforms_and_policies": 'status:"APPROVED" AND (intervention_name:"Drug Courts" OR intervention_name:"Pharmacotherapy Related Programs & Policies" OR intervention_name:"Employment for People in Recovery")',
    "medication_assisted_treatment": 'status:"APPROVED" AND (intervention_name:"Offering Pharmacotherapy to High Risk Individuals at the ER" OR program_components:"Medication Assisted Treatment" OR program_components:"Pharmacotherapy")',
    "overdose_prevention_and_response": 'status:"APPROVED" AND (intervention_name:"Co-prescription of naloxone" OR intervention_name:"Community Distribution of Naloxone" OR intervention_name:"Layperson Training in Administration of Naloxone" OR intervention_name:"Safe Consumption Sites" OR intervention_name:"Drug Disposal Programs" OR intervention_name:"Prescription of Naloxone in ER" OR intervention_name:"Use of Naloxone by First Responders" OR intervention_name:"Providing Naloxone Upon Release from Correctional Facilities" OR intervention_name:"Naloxone Distribution at Pharmacies")',
    "prevention_and_education": 'status:"APPROVED" AND (intervention_name:"Family Education Programs" OR intervention_name:"Youth Education Program" OR intervention_name:"Public Awareness Campaign" OR intervention_name:"Social Media" OR intervention_name:"Communication Campaign")',
    "psychosocial_therapy": 'status:"APPROVED" AND (intervention_name:"Contingency management" OR intervention_name:"Multi-dimensional family therapy" OR intervention_name:"Family functional therapy" OR intervention_name:"Cognitive Behavioral Therapy" OR intervention_name:"Recovery Programs and Support Groups" OR intervention_name:"Support or Educational Programs in Correctional Facilities")',
    "safe_prescribing": 'status:"APPROVED" AND (intervention_name:"Prescription Drug Monitoring Programs" OR intervention_name:"Integration of PDMP and EHR" OR intervention_name:"Lock-in programs" OR intervention_name:"Safe storage programs")',
    "treatment_delivery_models": 'status:"APPROVED" AND (intervention_name:"Telehealth" OR intervention_name:"Helpline" OR intervention_name:"Hub and Spoke Model")'}
