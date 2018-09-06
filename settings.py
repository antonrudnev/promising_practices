SOLR_COLLECTION = "http://10.0.15.138:8983/solr/promising_practices"
DASHBOARD_URL = "http://54.242.41.222:8983/solr/banana/promising_practices/index.html"
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
