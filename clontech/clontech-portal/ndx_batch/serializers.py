from rest_framework import serializers

from .models import Batch, QuadraticCurveParameters


class QuadraticCurveParametersSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuadraticCurveParameters
        fields = ('a', 'b', 'c')


class BatchSerializer(serializers.ModelSerializer):
    parameters = QuadraticCurveParametersSerializer(source='quadratic_curve_parameters', many=False, read_only=True)
    curve_type_display = serializers.SerializerMethodField()

    class Meta:
        model = Batch
        fields = ('lot_no', 'valid_from', 'assay_type', 'unit', 'expires',
                  'is_active', 'curve_type', 'curve_type_display', 'parameters')

    def get_curve_type_display(self, obj: Batch) -> str:
        return obj.get_curve_type_display()
