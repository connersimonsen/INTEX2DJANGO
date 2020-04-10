from rest_framework import serializers

from api.models import Campaign, Category

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = [ 'url', 'campaign_id', 'auto_fb_post_mode', 'category_id', 'currencycode',
         'current_amount', 'goal', 'donators', 'days_active', 'title', 'description', 'has_beneficiary',
         'turn_off_donations' , 'user_id', 'user_first_name', 'visible_in_search', 'deactivated', 'campaign_image_url', 
         'launch_date', 'campaign_hearts', 'social_share_total', 'social_share_last_update', 'location_city', 'location_country', 
         'is_charity', 'charity_valid', 'charity_name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [ 'id', 'title' ]