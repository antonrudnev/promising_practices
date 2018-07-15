SOLR_COLLECTION = "http://54.173.176.161:8983/solr/promising_practices3"
DASHBOARD_URL = "http://54.173.176.161:8983/solr/banana/promising_practices_tst/index.html"
SYSTEM_DATABASE = "system.sqlite"
ITEMS_PER_PAGE = 15
PAGER_RANGE = 2

ALL_FIELDS = ["id", "title", "intervention_name", "summary", "link", "citation", "program_success", "city", "geography",
              "region", "source_type", "race", "intervention_goal", "implementers", "scale", "country",
              "program_components", "population", "status"]
MULTIVALUED_FIELDS = ["geography", "region", "race", "intervention_goal", "implementers", "scale", "country",
                      "program_components", "population"]


COUNTRIES = ["Domestic", "International"]

IMPLEMENTERS = ["Health Care Providers", "Mental Health Care Providers", "Pharmacists", "State Officials",
                "Community Officials", "Federal Officials", "County Officials", "Police", "Courts", "Schools",
                "Correctional Institutions", "Faith Communities", "First Responders", "Child Welfare",
                "Juvenile Justice", "Recovery Community", "Public Health Officials", "Anti-Drug Coalition",
                "Non-Governmental Community Organization"]

INTERVENTION_GOALS = ["Prevention", "Harm Reduction", "Treatment", "Recovery"]

INTERVENTION_NAMES = ["Prescription Drug Monitoring Programs", "Family Functional Therapy",
                      "Multi-Dimensional Family Therapy", "Cognitive Behavioral Therapy", "Hub and Spoke Model",
                      "Co-Prescription of Naloxone", "Integration of PDMP and EHR",
                      "Community Distribution of Naloxone", "Layperson Training in Administration of Naloxone",
                      "Drug Disposal Programs", "Prescription of Naloxone in ER", "Safe Storage Programs",
                      "Use of Naloxone by First Responders",
                      "Providing Naloxone Upon Release from Correctional Facilities",
                      "Safe Consumption Sites", "Syringe Services", "Lock-In Programs",
                      "Recovery Programs and Support Groups", "Drug Courts", "Treatment in Correctional Institutions",
                      "Employment for People in Recovery", "Youth Education Program", "Helpline",
                      "Contingency Management", "Naloxone Distribution at Pharmacies",
                      "Support or Educational Programs in Correctional Facilities", "Tele-Health", "Social Media",
                      "Public Awareness Campaign", "Family Education Programs",
                      "Pharmacotherapy Related Programs & Policies", "Fentanyl Testing Kits",
                      "Offering Pharmacotherapy to High Risk Individuals at the ER", "Other"]

POPULATIONS = ["General", "Adults", "Youth", "Pregnant Women", "Women of Childbearing Age", "Neonates", "Not Specified"]

PROGRAM_COMPONENTS = ["Cognitive Behavioral Therapy", "Naloxone", "Training", "Policy", "Medication Assisted Treatment",
                      "Pharmacotherapy", "Behavioral", "Mental Health", "Communication",
                      "Prescription Drug Monitoring Program", "Epidemiological Surveillance", "Remote or Tele-Medicine",
                      "Recovery Program", "Incentives", "Transportation", "Housing", "Prescription Drug Disposal",
                      "Lock-In", "Syringe Services", "Prescription Drug Storage", "Supervised Consumption Sites",
                      "Outreach", "Family Involvement", "Wrap-Around Services", "Peer-Support", "Hub and Spoke"]

PROGRAM_SUCCESSES = ["Significant Improvement", "No Significant Change", "Significant Decline", "Findings Mixed",
                     "No Evaluation", "Clearinghouse Endorsement"]

RACES = ["Black or African American", "White", "Asian or Pacific Islander", "American Indian or Alaska Native",
         "Hispanic or Latino"]

REGIONS = ["Urban", "Rural", "Suburban", "Not Specified", "General"]

SCALES = ["Community", "County", "State", "Federal"]

SOURCE_TYPES = ["Community Example", "Published Literature", "Report", "Clearinghouse", "Systematic Review",
                "Recommendations from Government", "Recommendations from Non-Governmental Group", "Other"]

STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY",
          "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH",
          "OK", "OR", "PA", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]


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
