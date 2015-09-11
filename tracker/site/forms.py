from django import forms
from django.contrib.auth import get_user_model

from crispy_forms_foundation.forms import FoundationModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Fieldset

from .models import Project, Ticket


class BaseTrackerForm(FoundationModelForm):
    def __init__(self, user=None, title=None, *args, **kwargs):
        self.title = title
        self.user = user
        self.switches = True

        super(BaseTrackerForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label

    def save(self, *args, **kwargs):
        commit = kwargs.pop('commit', True)
        instance = super(BaseTrackerForm, self).save(
            commit=False, *args, **kwargs)

        self.pre_save(instance)

        if commit:
            instance.save()

        return instance

    def pre_save(self, instance):
        pass


class ProjectForm(BaseTrackerForm):
    class Meta:
        model = Project
        fields = ('title',)

    def pre_save(self, instance):
        instance.created_by = self.user


class TicketForm(BaseTrackerForm):
    assignees = forms.MultipleChoiceField(required=False)

    class Meta:
        model = Ticket
        fields = ('title', 'description', 'assignees', 'status')

    def __init__(self, project=None, *args, **kwargs):
        self.project = project
        super(TicketForm, self).__init__(*args, **kwargs)

        self.fields['assignees'].choices = [(a.pk, a.email) for a in
                                            get_user_model().objects.all()]
        self.fields['assignees'].widget.attrs['class'] = 'chosen-select'

        if kwargs['title'] == 'Create ticket':
            del self.fields['status']

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(kwargs['title'], 'title', 'description',
                     'assignees', 'status'),
            ButtonHolder(
                Submit('submit', kwargs['title'], css_class='button small'),
                css_class='align-right'
            )
        )

    def pre_save(self, instance):
        instance.created_by = self.user

        if self.project:
            instance.project = self.project
