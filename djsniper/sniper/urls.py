from django.urls import path, include
from . import views

app_name = "sniper"

urlpatterns = [
    path("", views.HomeCategoriesListView.as_view(), name="home"),
    path("projects/", views.ProjectListView.as_view(), name="projects"),
    path("create/", views.ProjectCreateView.as_view(), name="project-create"),
    path("project/<pk>/", views.ProjectDetailView.as_view(), name="project-detail"),
    path(
        "project/<pk>/update/", views.ProjectUpdateView.as_view(), name="project-update"
    ),
    path(
        "project/<pk>/delete/", views.ProjectDeleteView.as_view(), name="project-delete"
    ),
    path("project/<pk>/clear/", views.ProjectClearView.as_view(), name="project-clear"),
    path("project/<pk>/fetch-nfts/", views.FetchNFTsView.as_view(), name="fetch-nfts"),
    #path("project/<pk>/order/", views.ProjectDetailView.as_view(), name="order"),},
    path("my-projects/<str:username>/", views.UserProjectsView.as_view(), name="my-projects"),
    path("my-payments/<str:username>/", views.UserPaymentsHistoryView.as_view(), name="my-payments"),
    path("my-billings/<str:username>/", views.UserBillingsView.as_view(), name="my-billings"),
    path("add-voucher/<pk>/", views.OrderUpdateView.as_view(), name="add-voucher"),
    path("show-voucher/<pk>/", views.VoucherDetailView.as_view(), name="show-voucher"),
    path("choose/", views.ChooseRole, name="choose")

]
