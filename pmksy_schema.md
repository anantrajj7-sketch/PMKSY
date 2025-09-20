# 📑 PMKSY Database Schema – Data Dictionary
This document lists the schema for the PMKSY socio-economic survey form, converted into normalized relational tables.

## Farmers (Basic Profile)
| Column Name | Table Name | Data Type | Relation |
|-------------|------------|-----------|----------|
| farmer_id | farmers | UUID (PK) | – |
| name | farmers | TEXT | – |
| address | farmers | TEXT | – |
| village | farmers | TEXT | – |
| taluka_block | farmers | TEXT | – |
| district | farmers | TEXT | – |
| contact_no | farmers | TEXT | – |
| education | farmers | TEXT | – |
| caste_religion | farmers | TEXT | – |
| farming_experience_years | farmers | INT | – |
| latitude | farmers | DOUBLE PRECISION | – |
| longitude | farmers | DOUBLE PRECISION | – |
| altitude | farmers | DOUBLE PRECISION | – |
| family_males | farmers | INT | – |
| family_females | farmers | INT | – |
| family_children | farmers | INT | – |
| family_adult | farmers | INT | – |

---

## Land Holdings
| Column Name | Table Name | Data Type | Relation |
|-------------|------------|-----------|----------|
| land_id | land_holdings | UUID (PK) | – |
| farmer_id | land_holdings | UUID (FK) | → farmers.farmer_id |
| category | land_holdings | TEXT | – |
| total_area_ha | land_holdings | NUMERIC | – |
| irrigated_area_ha | land_holdings | NUMERIC | – |
| irrigation_source | land_holdings | TEXT | – |
| irrigation_no | land_holdings | TEXT | – |
| irrigation_latitude | land_holdings | DOUBLE PRECISION | – |
| irrigation_longitude | land_holdings | DOUBLE PRECISION | – |
| soil_details | land_holdings | TEXT | – |

---

## Assets
| Column Name | Table Name | Data Type | Relation |
|-------------|------------|-----------|----------|
| asset_id | assets | UUID (PK) | – |
| farmer_id | assets | UUID (FK) | → farmers.farmer_id |
| item_name | assets | TEXT | – |
| quantity | assets | INT | – |
| years_owned | assets | INT | – |
| current_value | assets | NUMERIC | – |

---

## Crop History
| Column Name | Table Name | Data Type | Relation |
|-------------|------------|-----------|----------|
| crop_hist_id | crop_history | UUID (PK) | – |
| farmer_id | crop_history | UUID (FK) | → farmers.farmer_id |
| crop_name | crop_history | TEXT | – |
| variety | crop_history | TEXT | – |
| season | crop_history | TEXT | – |
| area_ha | crop_history | NUMERIC | – |
| production_kg | crop_history | NUMERIC | – |
| sold_market_kg | crop_history | NUMERIC | – |
| retained_seed_kg | crop_history | NUMERIC | – |
| home_consumption_kg | crop_history | NUMERIC | – |

---

## Cost of Cultivation
| Column Name | Table Name | Data Type | Relation |
|-------------|------------|-----------|----------|
| cost_id | cost_of_cultivation | UUID (PK) | – |
| farmer_id | cost_of_cultivation | UUID (FK) | → farmers.farmer_id |
| crop_name | cost_of_cultivation | TEXT | – |
| particular | cost_of_cultivation | TEXT | – |
| quantity | cost_of_cultivation | NUMERIC | – |
| cost_rs | cost_of_cultivation | NUMERIC | – |

---

## Weeds
| Column Name | Table Name | Data Type | Relation |
|-------------|------------|-----------|----------|
| weed_id | weeds | UUID (PK) | – |
| farmer_id | weeds | UUID (FK) | → farmers.farmer_id |
| season | weeds | TEXT | – |
| weed_type | weeds | TEXT | – |
| weeding_time | weeds | TEXT | – |
| herbicide | weeds | TEXT | – |
| chemical_cost | weeds | NUMERIC | – |
| labour_days | weeds | NUMERIC | – |
| labour_charge | weeds | NUMERIC | – |

---

## Water Management
| Column Name | Table Name | Data Type | Relation |
|-------------|------------|-----------|----------|
| wm_id | water_management | UUID (PK) | – |
| farmer_id | water_management | UUID (FK) | → farmers.farmer_id |
| season | water_management | TEXT | – |
| irrigation_source | water_management | TEXT | – |
| irrigation_count | water_management | INT | – |
| depth | water_management | NUMERIC | – |
| energy_cost | water_management | NUMERIC | – |
| labour_charge | water_management | NUMERIC | – |

---

## Pest & Disease
| Column Name | Table Name | Data Type | Relation |
|-------------|------------|-----------|----------|
| pest_id | pest_disease | UUID (PK) | – |
| farmer_id | pest_disease | UUID (FK) | → farmers.farmer_id |
| season | pest_disease | TEXT | – |
| pest_disease | pest_disease | TEXT | – |
| chemical_used | pest_disease | TEXT | – |
| chemical_qty | pest_disease | NUMERIC | – |
| chemical_cost | pest_disease | NUMERIC | – |
| labour_days | pest_disease | NUMERIC | – |
| labour_charge | pest_disease | NUMERIC | – |

---

## Nutrient Management
| Column Name | Table Name | Data Type | Relation |
|-------------|------------|-----------|----------|
| nutrient_id | nutrient_management | UUID (PK) | – |
| farmer_id | nutrient_management | UUID (FK) | → farmers.farmer_id |
| season | nutrient_management | TEXT | – |
| crop_name | nutrient_management | TEXT | – |
| fym_kg | nutrient_management | NUMERIC | – |
| nitrogen_kg | nutrient_management | NUMERIC | – |
| phosphate_kg | nutrient_management | NUMERIC | – |
| gromer_kg | nutrient_management | NUMERIC | – |
| other_fertilizer | nutrient_management | TEXT | – |

---

## Income from Crops
| Column Name | Table Name | Data Type | Relation |
|-------------|------------|-----------|----------|
| income_crop_id | income_crops | UUID (PK) | – |
| farmer_id | income_crops | UUID (FK) | → farmers.farmer_id |
| season | income_crops | TEXT | – |
| crop_name | income_crops | TEXT | – |
| production_qntl | income_crops | NUMERIC | – |
| yield_qntl_ha | income_crops | NUMERIC | – |
| price_rs_qntl | income_crops | NUMERIC | – |
| gross_income_rs | income_crops | NUMERIC | – |
| byproduct_income_rs | income_crops | NUMERIC | – |

---

## Enterprises
| Column Name | Table Name | Data Type | Relation |
|-------------|------------|-----------|----------|
| enterprise_id | enterprises | UUID (PK) | – |
| farmer_id | enterprises | UUID (FK) | → farmers.farmer_id |
| enterprise_type | enterprises | TEXT | – |
| number | enterprises | INT | – |
| production | enterprises | NUMERIC | – |
| home_consumption | enterprises | NUMERIC | – |
| sold_market | enterprises | NUMERIC | – |
| market_price | enterprises | NUMERIC | – |

---

## Annual Family Income
| Column Name | Table Name | Data Type | Relation |
|-------------|------------|-----------|----------|
| afi_id | annual_family_income | UUID (PK) | – |
| farmer_id | annual_family_income | UUID (FK) | → farmers.farmer_id |
| source | annual_family_income | TEXT | – |
| income_rs | annual_family_income | NUMERIC | – |
| employment_days | annual_family_income | INT | – |

---

## Migration
| Column Name | Table Name | Data Type | Relation |
|-------------|------------|-----------|----------|
| migration_id | migration | UUID (PK) | – |
| farmer_id | migration | UUID (FK) | → farmers.farmer_id |
| age_gender | migration | TEXT | – |
| reason | migration | TEXT | – |
| migration_type | migration | TEXT | – |
| remittance | migration | NUMERIC | – |

---

## Adaptation Strategies
| Column Name | Table Name | Data Type | Relation |
|-------------|------------|-----------|----------|
| strategy_id | adaptation_strategies | UUID (PK) | – |
| farmer_id | adaptation_strategies | UUID (FK) | → farmers.farmer_id |
| strategy | adaptation_strategies | TEXT | – |
| aware | adaptation_strategies | BOOLEAN | – |
| adopted | adaptation_strategies | BOOLEAN | – |

---

## Financials
| Column Name | Table Name | Data Type | Relation |
|-------------|------------|-----------|----------|
| fin_id | financials | UUID (PK) | – |
| farmer_id | financials | UUID (FK) | → farmers.farmer_id |
| loan | financials | BOOLEAN | – |
| loan_purpose | financials | TEXT | – |
| credit_returned | financials | BOOLEAN | – |
| kcc | financials | BOOLEAN | – |
| kcc_used | financials | BOOLEAN | – |
| memberships | financials | TEXT/JSON | – |
| benefits | financials | TEXT | – |
| soil_testing | financials | BOOLEAN | – |
| training | financials | TEXT | – |
| info_sources | financials | TEXT | – |
| constraints | financials | TEXT | – |

---

## Consumption Pattern
| Column Name | Table Name | Data Type | Relation |
|-------------|------------|-----------|----------|
| cp_id | consumption_pattern | UUID (PK) | – |
| farmer_id | consumption_pattern | UUID (FK) | → farmers.farmer_id |
| crop | consumption_pattern | TEXT | – |
| crop_product | consumption_pattern | TEXT | – |
| consumption_kg_month | consumption_pattern | NUMERIC | – |
| purchased | consumption_pattern | BOOLEAN | – |
| pds | consumption_pattern | BOOLEAN | – |

---

## Market Price
| Column Name | Table Name | Data Type | Relation |
|-------------|------------|-----------|----------|
| price_id | market_price | UUID (PK) | – |
| farmer_id | market_price | UUID (FK) | → farmers.farmer_id |
| crop | market_price | TEXT | – |
| season | market_price | TEXT | – |
| area_ha | market_price | NUMERIC | – |
| production_tons | market_price | NUMERIC | – |
| price_rs_qntl | market_price | NUMERIC | – |

---

## Irrigated & Rainfed
| Column Name | Table Name | Data Type | Relation |
|-------------|------------|-----------|----------|
| ir_id | irrigated_rainfed | UUID (PK) | – |
| farmer_id | irrigated_rainfed | UUID (FK) | → farmers.farmer_id |
| crop | irrigated_rainfed | TEXT | – |
| sowing_date | irrigated_rainfed | DATE | – |
| harvesting_date | irrigated_rainfed | DATE | – |
| rainfed_area | irrigated_rainfed | NUMERIC | – |
| irrigated_area | irrigated_rainfed | NUMERIC | – |
| fertilizer_rate | irrigated_rainfed | NUMERIC | – |
