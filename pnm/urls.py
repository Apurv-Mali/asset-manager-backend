from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('assets', views.AssetViewSet, basename='asset')
router.register('unassigned-assets', views.UnassignedAssetsListView, basename='unassigned-asset')
router.register('assign-assets', views.AssetManagerViewSet, basename='asset-manager')
router.register('managers', views.ManagerViewSet, basename='manager')
router.register('mechanics', views.MechanicViewSet, basename='mechanic')
router.register('operators', views.OperatorViewSet, basename='operator')
router.register('monthly-rent', views.MonthlyRentViewSet, basename='monthly-rent')
router.register('revoke-assets', views.RevokeAssetsViewSet, basename='revoke-asset-data')
router.register('trip-details', views.TripDetailViewSet, basename='trip-details')
router.register('receivable-trips', views.ReceivableTripViewSet, basename='receivable-trip')
router.register('diesel-entry', views.DieselEntryViewSet, basename='diesel-entry-details')
router.register('breakdown', views.BreakdownViewSet, basename='breakdowns')
router.register('breakdown-report', views.BreakdownReportViewSet, basename='breakdown-report')
router.register('diesel-report', views.DieselReportViewSet, basename='diesel-report')
router.register('diesel-stock', views.DieselStockViewSet, basename='diesel-stock')

urlpatterns = [
    path('', include(router.urls)),
    path('logged-in-manager/', views.LoggedInManagerView.as_view(), name='logged-in-manager'),
    path('logged-in-mechanic/', views.LoggedInMechanicView.as_view(), name='logged-in-mechanic'),
    path('tipper-report/', views.TipperMonthlyReportView.as_view(), name='tipper-report'),
    path('tipper-report-excel/', views.TipperMonthlyReportExportView.as_view(), name='tipper-report-excel'),
    path('excavator-report/', views.ExcavatorMonthlyReportView.as_view(), name='excavator-report'),
    path('excavator-report-excel/', views.ExcavatorMonthlyReportExportView.as_view(), name='excavator-report-excel'),
    path('other-report/', views.OtherAssetsMonthlyReportView.as_view(), name='other-report'),
    path('other-report-excel/', views.OtherAssetsMonthlyReportExportView.as_view(), name='other-report-excel'),
    path('complete-report/', views.CompleteAssetMonthlyReportView.as_view(), name='complete-report'),
    path('complete-report-excel/', views.CompleteAssetMonthlyReportExcelView.as_view(), name='complete-report-excel'),
    path('trip-report/', views.TripDetailsReportView.as_view(), name='trip-report'),
    path("trip-report-excel/", views.TripDetailsReportExcelView.as_view(), name="trip-report-excel"),
        
]