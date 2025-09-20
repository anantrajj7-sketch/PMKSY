"""Data wizard importer registrations for PMKSY."""

from data_wizard import registry

from . import serializers


REGISTRATIONS = (
    ("Farmers", serializers.FarmerSerializer),
    ("Land Holdings", serializers.LandHoldingSerializer),
    ("Assets", serializers.AssetSerializer),
    ("Crop History", serializers.CropHistorySerializer),
    ("Cost of Cultivation", serializers.CostOfCultivationSerializer),
    ("Weeds", serializers.WeedSerializer),
    ("Water Management", serializers.WaterManagementSerializer),
    ("Pest & Disease", serializers.PestDiseaseSerializer),
    ("Nutrient Management", serializers.NutrientManagementSerializer),
    ("Income from Crops", serializers.IncomeCropSerializer),
    ("Enterprises", serializers.EnterpriseSerializer),
    ("Annual Family Income", serializers.AnnualFamilyIncomeSerializer),
    ("Migration", serializers.MigrationSerializer),
    ("Adaptation Strategies", serializers.AdaptationStrategySerializer),
    ("Financials", serializers.FinancialSerializer),
    ("Consumption Pattern", serializers.ConsumptionPatternSerializer),
    ("Market Price", serializers.MarketPriceSerializer),
    ("Irrigated & Rainfed", serializers.IrrigatedRainfedSerializer),
)


for name, serializer in REGISTRATIONS:
    registry.register(name, serializer)
