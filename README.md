# PMKSY Survey Django Portal

This Django project provides a data entry portal for the PMKSY socio-economic survey described in `../README.md`. It models the entities listed in `../pmksy_schema.md`, exposes them in the Django admin, and offers a dedicated Django Data Wizard endpoint for interactive imports.

## Features
- PostgreSQL-ready data model covering 17 tables (farmers, land holdings, assets, crop history, etc.).
- Django Data Wizard importer at `/datawizard/` for spreadsheet uploads and column mapping.
- Clean Django admin for manual edits, exports, and reporting filters.
- UUID primary keys for safe merging of survey spreadsheets.
- Authentication hooks (`/accounts/login/`) so the dashboard can be restricted to staff/PRA teams.

## Project layout
```
pmksy_site/
+-- manage.py
+-- pmksy_site/        # project settings & URLs
+-- survey/            # app with models, views, admin configuration
+-- templates/         # base layout, dashboard, login
+-- static/            # placeholder for site-specific assets
```

## Requirements
- Python 3.10+
- PostgreSQL 13+ (SQLite is used automatically when no Postgres env vars are set)
- `pip install -r requirements.txt`

## Local setup
1. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Review the bundled `.env` file and adjust database credentials for your setup:
   ```dotenv
   POSTGRES_DB=SocioEconomicData
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=Pass@123
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   ```
   You can alternatively export variables from the shell (PowerShell `$env:` syntax) or remove them to fall back to `db.sqlite3` for quick trials.

4. Apply migrations and create an admin account (this sets up the survey tables plus Data Wizard storage):
   ```powershell
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. Run the development server:
   ```powershell
   python manage.py runserver
   ```
6. Visit `http://127.0.0.1:8000/` for the dashboard, `http://127.0.0.1:8000/datawizard/` for the Data Wizard importer, or `http://127.0.0.1:8000/admin/` for full admin control.

## Import workflow
1. Sign in with a staff/superuser account (`IsAdminUser` permission is required to run Data Wizard).
2. Launch the wizard from the dashboard shortcut or go directly to `/datawizard/`.
3. Upload a new file source (or re-use an earlier one), pick the target dataset, and map the spreadsheet columns to model fields.
4. Confirm the previewed mappings; the wizard remembers your last mapping for future uploads with the same structure.
5. Run the import task, monitor progress, and review row-level issues under **Run Records** if anything fails.

For exports or quick edits, use the relevant Django admin changelist page and the built-in export actions.

### Dataset keys & labels
| Dashboard key | Model | Notes |
|---------------|-------|-------|
| farmers | `Farmer` | Primary profile; generate UUIDs used elsewhere. |
| land_holdings | `LandHolding` | Own/leased land parcels with irrigation metadata. |
| assets | `Asset` | Equipment inventory. |
| crop_history | `CropHistory` | Multi-season crop history with production metrics. |
| cost_of_cultivation | `CostOfCultivation` | Input cost ledger by crop. |
| weeds | `Weed` | Weed pressure and weeding costs. |
| water_management | `WaterManagement` | Season wise irrigation details. |
| pest_disease | `PestDisease` | Pest/disease management records. |
| nutrient_management | `NutrientManagement` | Fertiliser application stack. |
| income_from_crops | `IncomeFromCrops` | Yield, price and income. |
| enterprises | `Enterprise` | Allied enterprises (dairy, poultry, etc.). |
| annual_family_income | `AnnualFamilyIncome` | Non-crop income sources. |
| migration | `Migration` | Migration profile and remittances. |
| adaptation_strategies | `AdaptationStrategy` | Awareness/adoption of climate strategies. |
| financials | `Financial` | Credit, membership, training and constraints. |
| consumption_pattern | `ConsumptionPattern` | Household consumption basket. |
| market_price | `MarketPrice` | Area/production vs market price observations. |
| irrigated_rainfed | `IrrigatedRainfed` | Crop-wise irrigated vs rainfed split. |

## Production checklist
- Set `DJANGO_SECRET_KEY` and `DJANGO_DEBUG="False"` (see `pmksy_site/settings.py`).
- Configure a secure ALLOWED_HOSTS list, static/media storage, and HTTPS at the reverse proxy.
- Consider placing the dashboard behind staff login via Django's `@login_required` decorator.
- Schedule periodic exports/backups using Data Wizard exports or PostgreSQL dump scripts.

## Next steps / extensions
- Build farmer-facing forms for on-site data entry (Form Wizard / DRF API).
- Add audit trails (e.g., `django-simple-history`) for compliance.
- Integrate GIS uploads for automatic latitude/longitude validation.
- Generate validation scripts that cross-check spreadsheet headers before import.
