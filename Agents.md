#  Agents for Django Data Import App

This file defines the specialized agents Codex will use to build and maintain a Django application for **bulk data import**, **survey management**, **testing**, and **documentation**.

---

## 1. Database Agent
**Role:** Master of database design and optimization.  

**Responsibilities:**
- Design normalized schema for farmers, crops, weeds, land holdings, and socio-economic surveys.  
- Define relationships (One-to-Many, Many-to-Many).  
- Generate Django models + migrations.  
- Optimize for PostgreSQL (indexes, constraints, UUIDs, JSON fields).  

**Inputs:** Survey schema, Excel/CSV column mappings.  
**Outputs:** Django models, migrations, ERD diagrams.  

**Example Prompt:**
```text
Design models for Farmers (UUID PK, name, village), LandHoldings (area, irrigated, rainfed), and Crops (linked to Farmer, season, yield).
```

---

## 2. Survey Agent
**Role:** Specialist in complex socio-economic survey data.  

**Responsibilities:**
- Build import workflows for multi-section surveys (18+ sections).  
- Handle hierarchical data (farmer → plots → crops → inputs → costs).  
- Create file upload + column-to-field mapping.  
- Apply validation rules (e.g., rainfall > 0, no duplicate IDs, valid crop seasons).  
- Generate summary reports (per farmer, per crop, per district).  

**Inputs:** Uploaded files, survey metadata.  
**Outputs:** Validated DB records, import reports, dashboards.  

**Example Prompt:**
```text
Implement a workflow where users can upload Excel sheets with 10,000+ survey records, map columns to database fields, validate data, and save.
```

---

## 3. Testing Agent
**Role:** Guardian of reliability and stability.  

**Responsibilities:**
- Write pytest/Django test cases for imports, validation, and relationships.  
- Use synthetic survey files for testing.  
- Stress test large uploads (50k+ rows).  
- Integrate CI/CD workflows (GitHub Actions).  
- Provide test coverage reports.  

**Inputs:** Functions, models, import workflows.  
**Outputs:** Automated tests (`tests/`), CI status badge.  

**Example Prompt:**
```text
Write tests to simulate uploading a farmer survey Excel file with missing village names and ensure validation rejects them.
```

---

## 4. Docs Agent
**Role:** Documentation and knowledge management specialist.  

**Responsibilities:**
- Maintain **README.md** with setup, usage, and examples.  
- Generate API docs for models, serializers, and views.  
- Document import workflows (Excel → Validation → DB).  
- Keep **CHANGELOG.md** updated for schema/import logic changes.  
- Add developer notes (migrations, tests, deployment).  
- Generate schema diagrams and ERD automatically.  

**Inputs:** Database schema, workflows, tests.  
**Outputs:** Markdown docs, docstrings, diagrams.  

**Example Prompt:**
```text
Update README.md with instructions for running the Django app locally, importing an Excel file into the Farmers table, and viewing the import summary.
```

---

#  Collaboration Workflow
1. **Database Agent** → builds schema & models.  
2. **Survey Agent** → develops import + validation workflows.  
3. **Testing Agent** → ensures correctness + scalability.  
4. **Docs Agent** → documents for developers + users.  

---
