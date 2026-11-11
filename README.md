# Promising Practices — Research Workflow & Literature Analytics Platform

> **Project Status & Disclaimer:** This repository contains the open-source **Proof of Concept (PoC)** version of the platform, published for portfolio and demonstration purposes. Following the successful validation of this prototype, the solution evolved into a full-scale proprietary production system at the **American Institutes for Research (AIR)**, which remains closed-source due to intellectual property and confidentiality agreements.

A lightweight, multi-user content management, search, and visual text analytics platform designed to streamline systematic literature reviews on **opioid overdose prevention and treatment**, while providing a public-facing evidence discovery portal and automated lead-tracking pipeline for external clients and stakeholders.

## 📋 Overview

**Promising Practices** automates the collection, peer review, and indexing of scientific publications and public health interventions across key domains such as *Medication-Assisted Treatment*, *Overdose Prevention & Response*, *Safe Prescribing*, and *Psychosocial Therapy*.

* **Internal Research & Peer-Review Workflow (`eswat`):** Supports collaborative literature curation with Role-Based Access Control (RBAC), a multi-stage editorial state machine, inline user comments with `@mentions`, and bulk CSV import/export.
* **Search & Visual Text Analytics (`corrd`):** Powered by **Apache Solr**, enabling full-text search, faceted filtering across standardized public health taxonomies, and an interactive **visual analytics dashboard** (`/dashboard/index.html`) featuring tag clouds.
* **External Discovery & Lead Generation:** Exposes approved (`status:"APPROVED"`) research summaries to external policymakers, researchers, and prospective clients. When an external visitor requests a platform demo or presentation, the system logs the inquiry (`demo_request`) and triggers an **instant Telegram Bot alert** so administrators can track engagement and follow up promptly.

## 🛠 Tech Stack

* **Backend / CMS (`eswat`):** Python 3.9, Flask 3.0, Gunicorn, Pandas, `pysolr`
* **Search Engine & Analytics (`corrd`):** Apache Solr 7.7 (Alpine) with custom pre-configured core (`promising-practices`) and visual analytics dashboard
* **Databases:** 
  * **SQLite (`system.sqlite`):** Users, RBAC roles/permissions, controlled vocabularies (`master_data`), threaded comments/mentions, and external demo requests
  * **Apache Solr:** Primary document store, full-text search index, and faceted analytics engine
* **Lead Notifications:** Telegram Bot API (`python-telegram-bot`) for real-time external demo/presentation request alerts
* **Web Server & Reverse Proxy:** Nginx 1.17
* **Infrastructure:** Docker & Docker Compose

## 🏗 Project Structure

```text
promising_practices/
├── eswat/                  # Flask CMS, RBAC auth, editorial workflow & admin tools
│   ├── Dockerfile          # Python 3.9-slim + Gunicorn setup (port 5000)
│   └── src/                # Application source code, SQLite DB & CSV upload storage
├── opioid-research/        # Apache Solr search & visual analytics service
│   ├── Dockerfile          # Solr 7.7-alpine image setup (port 8983)
│   ├── solrcore.tar.gz     # Pre-configured 'promising-practices' Solr core & schema
│   └── dashboard.tar.gz    # Interactive tag cloud & visual text analytics UI
├── nginx/                  # Nginx reverse proxy configuration
│   └── nginx.conf          # Routing rules for Flask app and Solr dashboard
└── docker-compose.yml      # Multi-container orchestration & persistent volumes
```

## 🔐 Role-Based Access Control (RBAC)

The platform implements fine-grained permission management (24 distinct permissions) mapped to four primary user roles:

| Role | Responsibilities & Permissions |
| :--- | :--- |
| **`data_entry`** | Creates, edits, and deletes `DRAFT` and `REJECTED` records; submits entries for review (`ACTION_CREATE`, `ACTION_SUBMIT`). |
| **`data_validation`** | Reviews `SUBMITTED` records; edits, approves, rejects, or revokes published entries (`ACTION_APPROVE`, `ACTION_REJECT`, `ACTION_REVOKE`). |
| **`supervisor`** | Read-only oversight across all editorial statuses (`VIEW_DRAFT` through `VIEW_REVOKED`). |
| **`administrator`** | Full system administration: user/role management (`ADMIN_SECURITY`), bulk CSV data import/export (`ADMIN_CONTENT`), taxonomy management (`ADMIN_MASTERDATA`), and external demo request triage (`ADMIN_DEMOREQUESTS`). |

## 🔄 Editorial Workflow & Taxonomy

Publications progress through a controlled moderation pipeline before appearing on the external portal:

```text
DRAFT ──(SUBMIT)──▶ SUBMITTED ──(APPROVE)──▶ APPROVED ──(REVOKE)──▶ REVOKED
                        │                        ▲                     │
                    (REJECT)                 (APPROVE)             (REJECT)
                        ▼                        │                     ▼
                    REJECTED ───(SUBMIT)─────────┴─────────────────▶ REJECTED
```

To ensure research consistency, records are tagged against centrally managed controlled vocabularies (`master_data`) covering **50+ standardized intervention types**, **program components**, **intervention goals** (*Prevention, Harm Reduction, Treatment, Recovery*), **target populations**, **implementers**, **geographic scales**, and **evaluation outcomes**.

## 🚀 Getting Started

### Prerequisites

* [Docker](https://docker.com)
* [Docker Compose](https://docker.com)

### Installation & Deployment

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd promising_practices
   ```

2. **Configure environment & security settings:**
   * Review `eswat/src/settings.py` to configure `SECRET_KEY`, `SOLR_COLLECTION`, and `CORRD_MANAGER_BOT`.
   * *(Security Note: Rotate default secret keys, set a strong password for the default `admin` account in `system.sqlite`, and update the Telegram bot token before deploying to production.)*

3. **Build and launch the containers:**
   ```bash
   docker-compose up -d --build
   ```

4. **Access the platform:**
   * **Public Portal & Research CMS:** `http://localhost/` (routed via Nginx on port `80`)
   * **Visual Analytics Dashboard:** `http://localhost/dashboard/index.html`

## 🔧 Administration & Maintenance

* **Bulk Data Import / Export (`/admin/download/`, `/admin/upload/`):** Administrators can export the entire Solr corpus to CSV or batch-upload structured CSV datasets directly into the search index.
* **Master Data Management (`/admin/master/`):** Dynamic management of dropdown taxonomies and display ordering without code changes.
* **External Lead Tracking:** Incoming demo and presentation inquiries are stored in `demo_request` and immediately pushed to administrators via the configured Telegram bot (`CORRD_MANAGER_BOT`).
* **Logs & Lifecycle:**
  ```bash
  docker-compose logs -f eswat corrd   # Stream application and Solr logs
  docker-compose down                  # Stop services (data persists in volumes)
  ```

  ## 📄 License & Intellectual Property

The code in this repository represents an early **Proof of Concept (PoC)** prototype. The subsequent enterprise production version is proprietary software owned by the **American Institutes for Research (AIR)** and cannot be publicly distributed.

