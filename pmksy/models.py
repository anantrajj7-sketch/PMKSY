import uuid

from data_wizard.models import Run
from django.db import models


def generate_registration_id() -> str:
    """Generate a stable registration identifier for farmers."""

    return uuid.uuid4().hex


class TimeStampedModel(models.Model):
    """Abstract base model that tracks creation and update timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ImportRunMetadata(TimeStampedModel):
    """Per-run configuration collected during the upload step."""

    run = models.OneToOneField(
        Run,
        on_delete=models.CASCADE,
        related_name="pmksy_metadata",
    )
    sheet_name = models.CharField(max_length=255, blank=True)
    header_row_index = models.PositiveIntegerField(default=0)
    data_start_row_index = models.PositiveIntegerField(default=1)
    column_mappings = models.JSONField(default=dict, blank=True)
    loader_options = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "pmksy_import_run_metadata"
        verbose_name = "import run metadata"
        verbose_name_plural = "import run metadata"

    def __str__(self) -> str:  # pragma: no cover - human readable helper
        base = f"Run {self.run_id}" if self.run_id else "Unbound run"
        if self.sheet_name:
            return f"{base} – sheet '{self.sheet_name}'"
        return base


class Farmer(TimeStampedModel):
    farmer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    registration_id = models.CharField(
        max_length=64,
        unique=True,
        null=True,
        blank=True,
        default=generate_registration_id,
    )
    survey_serial_number = models.CharField(max_length=32, blank=True)
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    village = models.CharField(max_length=255, blank=True)
    taluka_block = models.CharField(max_length=255, blank=True)
    district = models.CharField(max_length=255, blank=True)
    contact_no = models.CharField(max_length=32, blank=True)
    education = models.CharField(max_length=255, blank=True)
    caste_religion = models.CharField(max_length=255, blank=True)
    farming_experience_years = models.IntegerField(null=True, blank=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    altitude = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )
    family_males = models.IntegerField(null=True, blank=True)
    family_females = models.IntegerField(null=True, blank=True)
    family_children = models.IntegerField(null=True, blank=True)
    family_adult = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "farmers"

    def __str__(self) -> str:
        return self.name or str(self.farmer_id)


class LandHolding(TimeStampedModel):
    land_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer = models.ForeignKey(
        Farmer, related_name="land_holdings", on_delete=models.CASCADE
    )
    category = models.CharField(max_length=255, blank=True)
    total_area_ha = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    irrigated_area_ha = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    cultivated_area_ha = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    waste_land_area_ha = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    irrigation_source = models.CharField(max_length=255, blank=True)
    irrigation_no = models.CharField(max_length=255, blank=True)
    irrigation_latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    irrigation_longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    soil_type = models.CharField(max_length=255, blank=True)
    soil_details = models.TextField(blank=True)

    class Meta:
        db_table = "land_holdings"

    def __str__(self) -> str:
        return self.category or f"Land Holding {self.land_id}"


class Asset(TimeStampedModel):
    asset_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer = models.ForeignKey(
        Farmer, related_name="assets", on_delete=models.CASCADE
    )
    item_name = models.CharField(max_length=255)
    quantity = models.IntegerField(null=True, blank=True)
    years_owned = models.IntegerField(null=True, blank=True)
    current_value = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )

    class Meta:
        db_table = "assets"

    def __str__(self) -> str:
        return self.item_name


class CropHistory(TimeStampedModel):
    crop_hist_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer = models.ForeignKey(
        Farmer, related_name="crop_history", on_delete=models.CASCADE
    )
    crop_name = models.CharField(max_length=255)
    variety = models.CharField(max_length=255, blank=True)
    season = models.CharField(max_length=255, blank=True)
    area_ha = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    production_kg = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    sold_market_kg = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    retained_seed_kg = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    home_consumption_kg = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )

    class Meta:
        db_table = "crop_history"

    def __str__(self) -> str:
        return f"{self.crop_name} ({self.season})"


class CostOfCultivation(TimeStampedModel):
    cost_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer = models.ForeignKey(
        Farmer, related_name="cultivation_costs", on_delete=models.CASCADE
    )
    crop_name = models.CharField(max_length=255)
    particular = models.CharField(max_length=255)
    quantity = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    cost_rs = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = "cost_of_cultivation"

    def __str__(self) -> str:
        return f"{self.crop_name} - {self.particular}"


class Weed(TimeStampedModel):
    weed_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer = models.ForeignKey(
        Farmer, related_name="weeds", on_delete=models.CASCADE
    )
    season = models.CharField(max_length=255, blank=True)
    weed_type = models.CharField(max_length=255, blank=True)
    weeding_time = models.CharField(max_length=255, blank=True)
    herbicide = models.CharField(max_length=255, blank=True)
    chemical_cost = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    labour_days = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    labour_charge = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )

    class Meta:
        db_table = "weeds"

    def __str__(self) -> str:
        return self.weed_type or str(self.weed_id)


class WaterManagement(TimeStampedModel):
    wm_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer = models.ForeignKey(
        Farmer, related_name="water_management", on_delete=models.CASCADE
    )
    season = models.CharField(max_length=255, blank=True)
    irrigation_source = models.CharField(max_length=255, blank=True)
    irrigation_count = models.IntegerField(null=True, blank=True)
    depth = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    energy_cost = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    labour_charge = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    water_availability = models.CharField(max_length=255, blank=True)
    farm_pond_available = models.BooleanField(null=True, blank=True)

    class Meta:
        db_table = "water_management"

    def __str__(self) -> str:
        return f"{self.irrigation_source} ({self.season})"


class PestDisease(TimeStampedModel):
    pest_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer = models.ForeignKey(
        Farmer, related_name="pest_diseases", on_delete=models.CASCADE
    )
    season = models.CharField(max_length=255, blank=True)
    pest_disease = models.CharField(max_length=255)
    chemical_used = models.CharField(max_length=255, blank=True)
    chemical_qty = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    chemical_cost = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    labour_days = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    labour_charge = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )

    class Meta:
        db_table = "pest_disease"

    def __str__(self) -> str:
        return self.pest_disease


class NutrientManagement(TimeStampedModel):
    nutrient_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer = models.ForeignKey(
        Farmer, related_name="nutrient_management", on_delete=models.CASCADE
    )
    season = models.CharField(max_length=255, blank=True)
    crop_name = models.CharField(max_length=255, blank=True)
    fym_compost_kg_ha = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    urea_kg_ha = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    dap_kg_ha = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    mop_kg_ha = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    other_fertilizer_kg_ha = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )

    class Meta:
        db_table = "nutrient_management"

    def __str__(self) -> str:
        return f"{self.crop_name} ({self.season})"


class IncomeCrop(TimeStampedModel):
    income_crop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer = models.ForeignKey(
        Farmer, related_name="income_crops", on_delete=models.CASCADE
    )
    season = models.CharField(max_length=255, blank=True)
    crop_name = models.CharField(max_length=255)
    production_qntl = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    yield_qntl_ha = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    price_rs_qntl = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    gross_income_rs = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    byproduct_income_rs = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )

    class Meta:
        db_table = "income_crops"

    def __str__(self) -> str:
        return f"{self.crop_name} ({self.season})"


class Enterprise(TimeStampedModel):
    enterprise_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer = models.ForeignKey(
        Farmer, related_name="enterprises", on_delete=models.CASCADE
    )
    enterprise_type = models.CharField(max_length=255)
    number = models.IntegerField(null=True, blank=True)
    production = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    home_consumption = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    sold_market = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    market_price = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )

    class Meta:
        db_table = "enterprises"

    def __str__(self) -> str:
        return self.enterprise_type


class AnnualFamilyIncome(TimeStampedModel):
    afi_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer = models.ForeignKey(
        Farmer, related_name="annual_family_income", on_delete=models.CASCADE
    )
    source = models.CharField(max_length=255)
    income_rs = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    employment_days = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "annual_family_income"

    def __str__(self) -> str:
        return f"{self.source}: {self.income_rs}"


class Migration(TimeStampedModel):
    migration_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer = models.ForeignKey(
        Farmer, related_name="migration_records", on_delete=models.CASCADE
    )
    members_migrated = models.IntegerField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=32, blank=True)
    age_gender = models.CharField(max_length=255, blank=True)
    reason = models.CharField(max_length=255, blank=True)
    migration_type = models.CharField(max_length=255, blank=True)
    remittance = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    income_contribution_details = models.TextField(blank=True)

    class Meta:
        db_table = "migration"

    def __str__(self) -> str:
        return self.reason or str(self.migration_id)


class AdaptationStrategy(TimeStampedModel):
    strategy_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer = models.ForeignKey(
        Farmer, related_name="adaptation_strategies", on_delete=models.CASCADE
    )
    strategy = models.CharField(max_length=255)
    aware = models.BooleanField(null=True, blank=True)
    adopted = models.BooleanField(null=True, blank=True)
    strategy_order = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = "adaptation_strategies"

    def __str__(self) -> str:
        return self.strategy


class Financial(TimeStampedModel):
    fin_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer = models.ForeignKey(
        Farmer, related_name="financials", on_delete=models.CASCADE
    )
    loan = models.BooleanField(null=True, blank=True)
    loan_purpose = models.CharField(max_length=255, blank=True)
    credit_returned = models.BooleanField(null=True, blank=True)
    kcc = models.BooleanField(null=True, blank=True)
    kcc_used = models.BooleanField(null=True, blank=True)
    memberships = models.JSONField(null=True, blank=True)
    membership_fpo = models.BooleanField(null=True, blank=True)
    membership_cooperative = models.BooleanField(null=True, blank=True)
    membership_marketing = models.BooleanField(null=True, blank=True)
    membership_shg = models.BooleanField(null=True, blank=True)
    membership_useful = models.BooleanField(null=True, blank=True)
    benefits = models.TextField(blank=True)
    soil_testing = models.BooleanField(null=True, blank=True)
    training = models.TextField(blank=True)
    info_sources = models.TextField(blank=True)
    constraints = models.TextField(blank=True)
    soil_erosion_problem = models.BooleanField(null=True, blank=True)
    transportation_facilities = models.BooleanField(null=True, blank=True)
    road_connectivity = models.BooleanField(null=True, blank=True)
    cold_storage_facilities = models.BooleanField(null=True, blank=True)
    market_availability = models.BooleanField(null=True, blank=True)
    distance_to_market_km = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    direct_marketing_mode = models.IntegerField(null=True, blank=True)
    sell_to_government_msp = models.BooleanField(null=True, blank=True)
    cooperative_marketing_society = models.BooleanField(null=True, blank=True)
    wild_animal_problem = models.BooleanField(null=True, blank=True)
    additional_constraints = models.TextField(blank=True)

    class Meta:
        db_table = "financials"

    def __str__(self) -> str:
        return f"Financials for {self.farmer}"


class ConsumptionPattern(TimeStampedModel):
    cp_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer = models.ForeignKey(
        Farmer, related_name="consumption_patterns", on_delete=models.CASCADE
    )
    commodity = models.CharField(max_length=255)
    unit = models.CharField(max_length=64, blank=True)
    purchased_from_market_qty = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    through_pds_qty = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    other_source_qty = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    food_expenditure_rs_month = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )

    class Meta:
        db_table = "consumption_pattern"

    def __str__(self) -> str:
        return self.commodity


class MarketPrice(TimeStampedModel):
    price_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer = models.ForeignKey(
        Farmer, related_name="market_prices", on_delete=models.CASCADE
    )
    crop = models.CharField(max_length=255)
    season = models.CharField(max_length=255, blank=True)
    area_ha = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    production_tons = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    price_rs_qntl = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )

    class Meta:
        db_table = "market_price"

    def __str__(self) -> str:
        return f"{self.crop} ({self.season})"


class IrrigatedRainfed(TimeStampedModel):
    ir_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer = models.ForeignKey(
        Farmer, related_name="irrigated_rainfed", on_delete=models.CASCADE
    )
    crop = models.CharField(max_length=255)
    sowing_date = models.DateField(null=True, blank=True)
    harvesting_date = models.DateField(null=True, blank=True)
    rainfed_area = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    irrigated_area = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    fertilizer_rate = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )

    class Meta:
        db_table = "irrigated_rainfed"

    def __str__(self) -> str:
        return self.crop


class ImportRecordLabel(models.Model):
    """Store persistent labels for data wizard records backed by UUID keys."""

    record = models.OneToOneField(
        "data_wizard.Record",
        on_delete=models.CASCADE,
        related_name="pmksy_label",
    )
    label = models.TextField()

    class Meta:
        verbose_name = "import record label"
        verbose_name_plural = "import record labels"

    def __str__(self) -> str:
        return self.label
