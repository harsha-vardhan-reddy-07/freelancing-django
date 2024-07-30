from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),

    path('load-freelancer/', views.loadFreelancer),
    path('freelancer/<str:id>', views.freelancer),

    path('load-allProjects/', views.loadAllProjects),
    path('allProjects/<str:id>', views.allProjects),

    path('load-myProjects/', views.loadMyProjects),
    path('myProjects/<str:id>', views.myProjects),

    path('load-myApplications/', views.loadMyApplications),
    path('myApplications/<str:id>', views.myApplications),

    path('load-project/<str:proId>/', views.loadProject),
    path('project/<str:proId>/<str:userId>', views.project),

    path("submit-bid/<str:proId>/<str:userId>", views.submitBid),
    path("submit-project/<str:id>", views.submitProject),


    path('load-client/', views.loadClient),
    path('client/<str:id>', views.client),

    path('load-projectApplications/', views.loadProjectApplications),
    path('projectApplications/<str:id>', views.projectApplications),

    path('approve-application/<str:id>', views.approveApplication),
    path('reject-application/<str:id>', views.rejectApplication),


    path('approve-submission/<str:id>', views.approveSubmission),
    path('reject-submission/<str:id>', views.rejectSubmission),

    path('load-newProject/', views.loadNewProject),
    path('newProject/<str:id>', views.newProject),

    path('load-clientProject/<str:proId>/', views.loadClientProject),
    path('clientProject/<str:proId>/<str:clientId>', views.clientProject),

 
    path('admin/', views.admin),
    path('adminProjects/', views.adminProjects),
    path('adminApplications/', views.adminApplications),
    path('allUsers/', views.allUsers),

]
