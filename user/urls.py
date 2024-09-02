from django.urls import path
from django.contrib.auth import views as auth_views
from user import views as user_views

urlpatterns = [
    path('login/', user_views.login_view, name='login'),
    path('register/', user_views.register_view, name='register'),
    path('logout/', user_views.logout_view, name='logout'),
    path('activate/<uidb64>/<token>/', user_views.activate_view, name='activate'),
    path('registration_complete/', user_views.registration_complete_view, name='registration_complete'),
    path('activation_complete/', user_views.activation_complete_view, name='activation_complete'),

    # Rutas para el restablecimiento de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    
    # Rutas para el perfil de usuario
    path('details/', user_views.UserDetailView.as_view(), name='user_detail'),  
    path('profile/update/', user_views.ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/template/', user_views.ProfileTemplateUpdateView.as_view(), name='profile_template'),
    
    # Rutas para Skills
    path('skills/create/', user_views.SkillCreateView.as_view(), name='skill_create'),
    path('skills/update/<int:pk>/', user_views.SkillUpdateView.as_view(), name='skill_update'),
    path('skills/delete/<int:pk>/', user_views.SkillDeleteView.as_view(), name='skill_delete'),

    # Rutas para Languages
    path('languages/', user_views.LanguageListView.as_view(), name='language_list'),
    path('languages/create/', user_views.LanguageCreateView.as_view(), name='language_create'),
    path('languages/update/<int:pk>/', user_views.LanguageUpdateView.as_view(), name='language_update'),
    path('languages/delete/<int:pk>/', user_views.LanguageDeleteView.as_view(), name='language_delete'),

    # Rutas para Interests
    path('interests/', user_views.InterestListView.as_view(), name='interest_list'),
    path('interests/create/', user_views.InterestCreateView.as_view(), name='interest_create'),
    path('interests/update/<int:pk>/', user_views.InterestUpdateView.as_view(), name='interest_update'),
    path('interests/delete/<int:pk>/', user_views.InterestDeleteView.as_view(), name='interest_delete'),

    # Rutas para Education
    path('education/', user_views.EducationListView.as_view(), name='education_list'),
    path('education/create/', user_views.EducationCreateView.as_view(), name='education_create'),
    path('education/update/<int:pk>/', user_views.EducationUpdateView.as_view(), name='education_update'),
    path('education/delete/<int:pk>/', user_views.EducationDeleteView.as_view(), name='education_delete'),

    # Rutas para Experience
    path('experience/', user_views.ExperienceListView.as_view(), name='experience_list'),
    path('experience/create/', user_views.ExperienceCreateView.as_view(), name='experience_create'),
    path('experience/update/<int:pk>/', user_views.ExperienceUpdateView.as_view(), name='experience_update'),
    path('experience/delete/<int:pk>/', user_views.ExperienceDeleteView.as_view(), name='experience_delete'),

    # Rutas para Projects
    path('projects/', user_views.ProjectListView.as_view(), name='project_list'),
    path('projects/create/', user_views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/update/<int:pk>/', user_views.ProjectUpdateView.as_view(), name='project_update'),
    path('projects/delete/<int:pk>/', user_views.ProjectDeleteView.as_view(), name='project_delete'),

]

