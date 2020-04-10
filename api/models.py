from django.db import models
from api.fields import JSONField
    
class Campaign(models.Model):
    url = models.TextField()
    campaign_id = models.IntegerField()
    auto_fb_post_mode = models.TextField()
    category_id = models.TextField()
    currencycode = models.TextField()
    current_amount = models.IntegerField()
    goal = models.IntegerField()
    donators = models.IntegerField()
    days_active = models.IntegerField()
    title = models.TextField()
    description = models.TextField()
    has_beneficiary = models.TextField()
    turn_off_donations = models.IntegerField()
    user_id = models.IntegerField()
    user_first_name = models.TextField()
    visible_in_search = models.TextField()
    deactivated = models.TextField()
    campaign_image_url = models.TextField()
    launch_date = models.TextField()
    campaign_hearts = models.IntegerField()
    social_share_total = models.IntegerField()
    social_share_last_update = models.TextField()
    location_city = models.TextField()
    location_country = models.TextField()
    is_charity = models.TextField()
    charity_valid = models.TextField()
    charity_name = models.TextField(null=True)

class Category(models.Model):
    title = models.TextField()