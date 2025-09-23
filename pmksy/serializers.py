"""Serializers for PMKSY models."""

from django.db.models import Q
from data_wizard.serializers import RecordSerializer as BaseRecordSerializer
from rest_framework import serializers

from . import models
from .models import ImportRecordLabel


class FarmerByNameField(serializers.RelatedField):
    """Serializer field that resolves farmers by their registration identifier."""

    default_error_messages = {
        "required": "Please provide a farmer registration ID.",
        "blank": "Please provide a farmer registration ID.",
        "invalid": "Invalid farmer registration ID provided.",
        "does_not_exist": "Farmer with registration ID '{value}' does not exist.",
        "multiple": "Multiple farmers found with identifier '{value}'.",
        "name_missing": "Farmer with name '{value}' does not exist.",
    }

    def __init__(self, **kwargs):
        kwargs.setdefault("queryset", models.Farmer.objects.all())
        kwargs.setdefault("label", "Farmer Registration ID")
        kwargs.setdefault(
            "help_text",
            "Provide the farmer registration ID generated from the farmer dataset. "
            "Farmers missing an identifier will continue to match by name.",
        )
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

        queryset = self.get_queryset()

        try:
            return queryset.get(registration_id=value)
        except models.Farmer.MultipleObjectsReturned:  # pragma: no cover - defensive
            self.fail("multiple", value=value)
        except models.Farmer.DoesNotExist:
            pass

        fallback_queryset = queryset.filter(name=value).filter(
            Q(registration_id__isnull=True) | Q(registration_id="")
        )

        count = fallback_queryset.count()
        if count == 1:
            return fallback_queryset.get()
        if count > 1:  # pragma: no cover - defensive safeguard
            self.fail("multiple", value=value)

        self.fail("name_missing", value=value)

    def to_representation(self, value):
        if isinstance(value, models.Farmer):
            if value.registration_id:
                return value.registration_id
            if value.name:
                return value.name
            return str(value.farmer_id)
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
