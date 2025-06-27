from rest_framework import serializers
from .models import Asset, Manager, AssetManager, TripDetails,  DieselEntry, Breakdown, Mechanic, DieselStock, Operator,MonthlyRent
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from django.db.models import Sum

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'asset_id', 'registration_no', 'name', 'make', 'type', 'owner', 'category',
                'purchase_value', 'purchase_date', 'chasis_no', 'emi_amount', 'emi_provider',
                'emi_payment_date', 'emi_start_date', 'emi_end_date', 'insurance_amount',
                'insurance_provider', 'insurance_validity','puc_amount', 'puc_start_date', 'puc_end_date',
                'ot_road_tax','fitness_amount', 'fitness_start_date', 'fitness_end_date','road_tax_amount', 'road_tax_start_date',
                'road_tax_end_date','permit_amount', 'permit_start_date', 'permit_end_date', 'rate_per_month',
                'rate_per_hr', 'rate_per_shift', 'rate_per_night', 'charges', 'last_updated']

    def update(self, instance, validated_data):
        instance.emi_amount = validated_data.get('emi_amount', instance.emi_amount)
        instance.emi_provider = validated_data.get('emi_provider', instance.emi_provider)
        instance.emi_payment_date = validated_data.get('emi_payment_date', instance.emi_payment_date)
        instance.emi_start_date = validated_data.get('emi_start_date', instance.emi_start_date)
        instance.emi_end_date = validated_data.get('emi_end_date', instance.emi_end_date)
        
        instance.insurance_amount = validated_data.get('insurance_amount', instance.insurance_amount)
        instance.insurance_provider = validated_data.get('insurance_provider', instance.insurance_provider)
        instance.insurance_validity = validated_data.get('insurance_validity', instance.insurance_validity)

        instance.puc_amount = validated_data.get('puc_amount', instance.puc_amount)
        instance.fitness_amount = validated_data.get('fitness_amount', instance.fitness_amount)
        instance.road_tax_amount = validated_data.get('road_tax_amount', instance.road_tax_amount)
        instance.permit_amount = validated_data.get('permit_amount', instance.permit_amount)

        instance.puc_start_date = validated_data.get('puc_start_date', instance.puc_start_date)
        instance.puc_end_date = validated_data.get('puc_end_date', instance.puc_end_date)

        instance.ot_road_tax = validated_data.get('ot_road_tax', instance.ot_road_tax)
        instance.road_tax_start_date = validated_data.get('road_tax_start_date', instance.road_tax_start_date)
        instance.road_tax_end_date = validated_data.get('road_tax_end_date', instance.road_tax_end_date)

        instance.fitness_start_date = validated_data.get('fitness_start_date', instance.fitness_start_date)
        instance.fitness_end_date = validated_data.get('fitness_end_date', instance.fitness_end_date)

        instance.permit_start_date = validated_data.get('permit_start_date', instance.permit_start_date)
        instance.permit_end_date = validated_data.get('permit_end_date', instance.permit_end_date)

        instance.rate_per_month = validated_data.get('rate_per_month', instance.rate_per_month)
        instance.rate_per_hr = validated_data.get('rate_per_hr', instance.rate_per_hr)
        instance.rate_per_shift = validated_data.get('rate_per_shift', instance.rate_per_shift)
        instance.rate_per_night = validated_data.get('rate_per_night', instance.rate_per_night)

        instance.charges = validated_data.get('charges', instance.charges)

        instance.save()
        return instance

    
class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ['id','name','phone','salary','grade','sub_grade']

class MechanicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mechanic
        fields = ['id','name','phone','salary','grade','sub_grade']

class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = ['id','name','role','type','salary','grade','sub_grade','phone']
    
class AssetManagerSerializer(serializers.ModelSerializer):
    asset_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )

    class Meta:
        model = AssetManager
        fields = ['manager', 'asset_ids', 'site']

    def create(self, validated_data):
        asset_ids = validated_data.pop('asset_ids')
        manager = validated_data['manager']
        site = validated_data['site']

        asset_managers = []
        for asset_id in asset_ids:
            try:
                asset = Asset.objects.get(id=asset_id)
                asset_manager = AssetManager(asset=asset, manager=manager, site=site)
                asset_managers.append(asset_manager)
            except Asset.DoesNotExist:
                raise ValidationError(f"Asset with ID {asset_id} does not exist.")

        AssetManager.objects.bulk_create(asset_managers)
        return validated_data


class SimpleAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id','name','registration_no','type','rate_per_month',
                'rate_per_hr', 'rate_per_shift', 'rate_per_night', 'charges']

class AssetManagerAssetSerializer(serializers.ModelSerializer):
    asset = serializers.SerializerMethodField()

    class Meta:
        model = AssetManager
        fields = ['id', 'asset']

    def get_asset(self, obj):
        return {
            "asset_id":obj.asset.id,
            "name": obj.asset.name,
            "registration_no": obj.asset.registration_no,
            "type":obj.asset.type
        }

class ManagerWithAssetsSerializer(serializers.ModelSerializer):
    assets = serializers.SerializerMethodField()

    class Meta:
        model = Manager
        fields = ['id', 'name', 'assets']

    def get_assets(self, obj):
        asset_managers = AssetManager.objects.filter(manager=obj)
        return AssetManagerAssetSerializer(asset_managers, many=True).data

class TripDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripDetails
        fields = ['id','asset','date','from_location','to_location','material','rate','distance','net_weight','deal_type','hours','manager','receiver','shift','start_time','end_time','operator']

class ViewTripDetailsSerializer(serializers.ModelSerializer):
    asset = SimpleAssetSerializer()
    class Meta:
        model = TripDetails
        fields = ['id','asset','date','from_location','to_location','material','rate','distance','net_weight','deal_type','hours','manager','receiver','shift','start_time','end_time','operator']

class DieselEntrySerializer(serializers.ModelSerializer):
    date =  serializers.DateTimeField(read_only = True)
    class Meta:
        model = DieselEntry
        fields = ['id','asset','date','quantity','previous_reading','rate','reading','site','manager']

class BreakdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breakdown
        fields = ['id','asset','date','site','issue','action_taken','estimated_delivery_date','delivered_at_date','status','cost','manpower_cost','material_used','manager','mechanic']


class BreakdownReportSerializer(serializers.ModelSerializer):
    asset = SimpleAssetSerializer()
    manager = ManagerSerializer()
    mechanic = MechanicSerializer()
    amount =serializers.SerializerMethodField()
    class Meta:
        model = Breakdown
        fields = ['id','asset','date','site','issue','action_taken','estimated_delivery_date','delivered_at_date','status','cost','manpower_cost','amount','material_used','manager','mechanic']

    def get_amount(self, obj):
        return round(obj.cost + obj.manpower_cost,2)

class DieselReportSerializer(serializers.ModelSerializer):
    asset = SimpleAssetSerializer()
    manager = ManagerSerializer()
    amount = serializers.SerializerMethodField()
    class Meta:
        model = DieselEntry
        fields  = ['id','asset','date','site','previous_reading','reading','rate','quantity','amount','manager']

    def get_amount(self, obj):
        return round(obj.rate * obj.quantity,2)
    
class DieselStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = DieselStock
        fields = ['id', 'challan_no', 'date', 'quantity', 'rate', 'amount', 'party_name', 'stock']
        read_only_fields = ['id', 'date', 'amount', 'stock']

class MonthlyRentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyRent
        fields = ['id','asset','manager','rate_per_month','rate_per_hr','rate_per_shift','rate_per_night','charges']

class TipperMonthlyReportSerializer(serializers.Serializer):
    asset_name = serializers.CharField()
    manager = serializers.CharField()
    material = serializers.CharField()
    material_quantity = serializers.DecimalField(max_digits=10, decimal_places=2)
    rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    diesel_consumed = serializers.DecimalField(max_digits=10, decimal_places=2)
    diesel_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    distance = serializers.DecimalField(max_digits=10, decimal_places=2)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    final_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    status = serializers.CharField()

class ExcavatorMonthlyReportSerializer(serializers.Serializer):
    asset_name = serializers.CharField()
    manager = serializers.CharField()
    working_hours = serializers.DecimalField(max_digits=10, decimal_places=2)
    monthly_charge = serializers.DecimalField(max_digits=10, decimal_places=2)
    shift_charge = serializers.DecimalField(max_digits=10, decimal_places=2)
    no_of_shifts = serializers.DecimalField(max_digits=10, decimal_places=2)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    diesel_quantity = serializers.DecimalField(max_digits=10, decimal_places=2)
    diesel_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    final_amount = serializers.DecimalField(max_digits=12, decimal_places=2)

class OtherMonthlyReportSerializer(serializers.Serializer):
    asset_name = serializers.CharField()
    manager = serializers.CharField()
    monthly_charge = serializers.DecimalField(max_digits=10, decimal_places=2)
    shift_charge = serializers.DecimalField(max_digits=10, decimal_places=2)
    no_of_shifts = serializers.DecimalField(max_digits=10, decimal_places=2)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    diesel_quantity = serializers.DecimalField(max_digits=10, decimal_places=2)
    diesel_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    final_amount = serializers.DecimalField(max_digits=12, decimal_places=2)