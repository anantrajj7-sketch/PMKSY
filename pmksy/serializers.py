"""Serializers for PMKSY models."""

from data_wizard.serializers import RecordSerializer as BaseRecordSerializer
from rest_framework import serializers

from . import models
from .models import ImportRecordLabel


class FarmerByNameField(serializers.RelatedField):
    """Serializer field that resolves farmers by their name."""

    default_error_messages = {
        "required": "Please provide a farmer name.",
        "blank": "Please provide a farmer name.",
        "does_not_exist": "Farmer with name '{value}' does not exist.",
        "invalid": "Invalid farmer name provided.",
        "multiple": "Multiple farmers found with name '{value}'.",
    }

    def __init__(self, **kwargs):
        kwargs.setdefault("queryset", models.Farmer.objects.all())
        super().__init__(**kwargs)

    def to_internal_value(self, value):
        if value is None:
            self.fail("required")

        if isinstance(value, str):
            value = value.strip()

        if value == "":
            self.fail("blank")

        if isinstance(value, models.Farmer):
            return value

        if not isinstance(value, str):
            self.fail("invalid")

        try:
            return self.get_queryset().get(name=value)
        except models.Farmer.DoesNotExist:  # pragma: no cover - simple reraised error
            self.fail("does_not_exist", value=value)
        except models.Farmer.MultipleObjectsReturned:  # pragma: no cover - simple reraised error
            self.fail("multiple", value=value)

    def to_representation(self, value):
        if isinstance(value, models.Farmer):
            return value.name
        return str(value)


class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Farmer
        fields = "__all__"


class LandHoldingSerializer(serializers.ModelSerializer):
    farmer = FarmerByNameField()

    class Meta:
        model = models.LandHolding
        fields = "__all__"


class AssetSerializer(serializers.ModelSerializer):
    farmer = FarmerByNameField()

    class Meta:
        model = models.Asset
        fields = "__all__"


class CropHistorySerializer(serializers.ModelSerializer):
    farmer = FarmerByNameField()

    class Meta:
        model = models.CropHistory
        fields = "__all__"


class CostOfCultivationSerializer(serializers.ModelSerializer):
    farmer = FarmerByNameField()

    class Meta:
        model = models.CostOfCultivation
        fields = "__all__"


class WeedSerializer(serializers.ModelSerializer):
    farmer = FarmerByNameField()

    class Meta:
        model = models.Weed
        fields = "__all__"


class WaterManagementSerializer(serializers.ModelSerializer):
    farmer = FarmerByNameField()

    class Meta:
        model = models.WaterManagement
        fields = "__all__"


class PestDiseaseSerializer(serializers.ModelSerializer):
    farmer = FarmerByNameField()

    class Meta:
        model = models.PestDisease
        fields = "__all__"


class NutrientManagementSerializer(serializers.ModelSerializer):
    farmer = FarmerByNameField()

    class Meta:
        model = models.NutrientManagement
        fields = "__all__"


class IncomeCropSerializer(serializers.ModelSerializer):
    farmer = FarmerByNameField()

    class Meta:
        model = models.IncomeCrop
        fields = "__all__"


class EnterpriseSerializer(serializers.ModelSerializer):
    farmer = FarmerByNameField()

    class Meta:
        model = models.Enterprise
        fields = "__all__"


class AnnualFamilyIncomeSerializer(serializers.ModelSerializer):
    farmer = FarmerByNameField()

    class Meta:
        model = models.AnnualFamilyIncome
        fields = "__all__"


class MigrationSerializer(serializers.ModelSerializer):
    farmer = FarmerByNameField()

    class Meta:
        model = models.Migration
        fields = "__all__"


class AdaptationStrategySerializer(serializers.ModelSerializer):
    farmer = FarmerByNameField()

    class Meta:
        model = models.AdaptationStrategy
        fields = "__all__"


class FinancialSerializer(serializers.ModelSerializer):
    farmer = FarmerByNameField()

    class Meta:
        model = models.Financial
        fields = "__all__"


class ConsumptionPatternSerializer(serializers.ModelSerializer):
    farmer = FarmerByNameField()

    class Meta:
        model = models.ConsumptionPattern
        fields = "__all__"


class MarketPriceSerializer(serializers.ModelSerializer):
    farmer = FarmerByNameField()

    class Meta:
        model = models.MarketPrice
        fields = "__all__"


class IrrigatedRainfedSerializer(serializers.ModelSerializer):
    farmer = FarmerByNameField()

    class Meta:
        model = models.IrrigatedRainfed
        fields = "__all__"


class ImportRecordSerializer(BaseRecordSerializer):
    """Expose stored labels when a generic relation is unavailable."""

    def get_object_label(self, instance):
        if not instance.content_object:
            try:
                return instance.pmksy_label.label
            except ImportRecordLabel.DoesNotExist:
                pass
        return super().get_object_label(instance)
