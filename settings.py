SOLR = "http://54.173.176.161:8983/solr/promising_practices2"
DIRECTORY_DATABASE = "directory.sqlite"
ITEMS_PER_PAGE = 15
PAGER_RANGE = 2

STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY",
          "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH",
          "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

INTERVENTION_GOALS = ["Harm Reduction", "Prevention", "Recovery", "Treatment"]

IMPLEMENTERS = ["Community", "County", "Faith Communities", "Health Care", "National", "Police", "Prisons/Jails",
                "Schools", "State"]

PROGRAM_COMPONENTS = ["Behavioral", "Communication", "Lock In", "MAT", "Mental Health", "Monitoring", "Naloxone",
                      "Opioid Disposal", "Opioid Storage", "PDMP", "Policy", "Recovery Program", "Remote",
                      "Supervised Consumption Sites", "Syringe Services", "Training"]

POPULATIONS = ["Adults", "General", "Neonates", "Pregnant Women", "Youth"]

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

STATUS_STYLE_INDEX = {"DRAFT": "btn-outline-secondary",
                      "SUBMITTED": "btn-primary",
                      "REJECTED": "btn-secondary",
                      "APPROVED": "btn-outline-success",
                      "REVOKED": "btn-warning"}
