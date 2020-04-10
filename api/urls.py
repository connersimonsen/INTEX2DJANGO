from api import views
from django.urls import path

urlpatterns = [
    path('campaign/', views.CampaignList.as_view()),
    path('campaignDetail/<int:pk>/', views.CampaignDetail.as_view()),    
    path('category_id/', views.CategoryList.as_view()),
    path('category_id/<int:pk>/', views.CategoryDetail.as_view()),
    path('search/', views.SearchCampaign.as_view()),
    path('predict/', views.Predict.as_view())
]