from django.contrib import admin

from .models import (
    AdaptationStrategy,
    AnnualFamilyIncome,
    Asset,
    ConsumptionPattern,
    CostOfCultivation,
    CropHistory,
    Enterprise,
    Farmer,
    Financial,
    IncomeCrop,
    IrrigatedRainfed,
    LandHolding,
    MarketPrice,
    Migration,
    NutrientManagement,
    PestDisease,
    WaterManagement,
    Weed,
)

admin.site.register(
    [
        AdaptationStrategy,
        AnnualFamilyIncome,
        Asset,
        ConsumptionPattern,
        CostOfCultivation,
        CropHistory,
        Enterprise,
        Farmer,
        Financial,
        IncomeCrop,
        IrrigatedRainfed,
        LandHolding,
        MarketPrice,
        Migration,
        NutrientManagement,
        PestDisease,
        WaterManagement,
        Weed,
    ]
)
