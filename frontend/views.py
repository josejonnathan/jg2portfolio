from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from curriculum.models import Profile

class CurriculumDetailView(DetailView):
    model = Profile
    template_name = 'curriculum_detail.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()

        # Agregar la información relacionada
        context['skills'] = profile.skills.all()
        context['languages'] = profile.languages.all()
        context['interests'] = profile.interests.all()
        context['projects'] = profile.projects.all()
        context['education'] = profile.education.all()
        context['experience'] = profile.experience.all()


        return context