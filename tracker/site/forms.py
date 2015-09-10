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
    assignees = forms.ModelMultipleChoiceField(queryset=None, required=False)

    class Meta:
        model = Ticket
        fields = ('title', 'description', 'assignees',)

    def __init__(self, project=None, *args, **kwargs):
        self.project = project
        super(TicketForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset('Edit', 'title', 'description', 'assignees'),
            ButtonHolder(
                Submit('submit', 'Change', css_class='button small'),
                css_class='align-right'
            )
        )

        self.fields['assignees'].queryset = \
            get_user_model().objects.all()#.values_list('email', flat=True)
        self.fields['assignees'].widget.attrs['class'] = 'chosen-select'

    def pre_save(self, instance):
        instance.created_by = self.user

        #When updating self.project is None so it is overriding the instance
        #  project which is actually correct. This is only needed when
        # project is updating and not when it is getting created
        if self.project:
            instance.project = self.project
