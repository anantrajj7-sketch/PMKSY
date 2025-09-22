"""Serializers for PMKSY models."""

from rest_framework import serializers

from . import models


class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Farmer
        fields = "__all__"


class LandHoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LandHolding
        fields = "__all__"


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Asset
        fields = "__all__"


class CropHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CropHistory
        fields = "__all__"


class CostOfCultivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CostOfCultivation
        fields = "__all__"


class WeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Weed
        fields = "__all__"


class WaterManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WaterManagement
        fields = "__all__"


class PestDiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PestDisease
        fields = "__all__"


class NutrientManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NutrientManagement
        fields = "__all__"


class IncomeCropSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IncomeCrop
        fields = "__all__"


class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Enterprise
        fields = "__all__"


class AnnualFamilyIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnnualFamilyIncome
        fields = "__all__"


class MigrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Migration
        fields = "__all__"


class AdaptationStrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AdaptationStrategy
        fields = "__all__"


class FinancialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Financial
        fields = "__all__"


class ConsumptionPatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ConsumptionPattern
        fields = "__all__"


class MarketPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MarketPrice
        fields = "__all__"


class IrrigatedRainfedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IrrigatedRainfed
        fields = "__all__"
