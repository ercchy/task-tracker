from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, \
    DeleteView

from djangae.contrib.consistency import improve_queryset_consistency

from .forms import ProjectForm, TicketForm
from .models import Project, Ticket


class ProjectContextMixin(object):
    project = None
    ticket = None
    tickets = None

    def get_project(self):
        if not self.project:
            self.project = get_object_or_404(Project, pk=self.kwargs[
                'project_id'])

        return self.project

    def get_ticket(self):
        if not self.ticket:
            self.ticket = get_object_or_404(Ticket, pk=self.kwargs[
                'ticket_id'])

        return self.ticket

    def get_context_data(self, **kwargs):
        context = super(ProjectContextMixin, self).get_context_data(**kwargs)
        context['current_project'] = self.get_project()
        return context


class ProjectListView(ListView):
    template_name = "site/project_list.html"

    def get_queryset(self):
        return improve_queryset_consistency(Project.objects.all())

project_list_view = ProjectListView.as_view()


class CreateProjectView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "site/project_form.html"

    def get_success_url(self):
        return reverse("project-list")

    def get_form_kwargs(self):
        kwargs = super(CreateProjectView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['title'] = 'Create project'
        return kwargs

create_project_view = login_required(CreateProjectView.as_view())


class UpdateProjectView(ProjectContextMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    pk_url_kwarg = 'project_id'
    template_name = "site/project_form.html"

    def get_success_url(self):
        return reverse("project-list")

    def get_form_kwargs(self):
        kwargs = super(UpdateProjectView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['title'] = "Edit {0}".format(self.object.title)
        return kwargs

update_project_view = login_required(UpdateProjectView.as_view())


class ProjectView(ProjectContextMixin, TemplateView):
    template_name = "site/project_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        user_id = str(self.request.user.pk)
        project = self.get_project()
        tickets = project.tickets.all()
        tickets = improve_queryset_consistency(tickets)
        tickets = sorted(tickets,
                         key=lambda i: user_id in i.assignees_ids,
                         reverse=True)

        context.update({
            "project": project,
            "tickets": tickets
        })
        return context

project_view = ProjectView.as_view()


class MyTicketsView(TemplateView):
    template_name = "site/my_tickets.html"

    def get_context_data(self):
        if self.request.user.is_authenticated():
            tickets = (
                Ticket.objects
                .filter(assignees=str(self.request.user.pk), status="OPEN")
                .order_by('-modified')
            )
            print self.request.user.pk
        else:
            tickets = []

        return {
            'tickets': tickets
        }

my_tickets_view = MyTicketsView.as_view()


class CreateTicketView(ProjectContextMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = "site/ticket_form.html"

    def get_success_url(self):
        return reverse("project-detail", kwargs={"project_id": self.kwargs['project_id']})

    def get_form_kwargs(self):
        kwargs = super(CreateTicketView, self).get_form_kwargs()
        kwargs['project'] = self.get_project()
        kwargs['user'] = self.request.user
        kwargs['title'] = 'Create ticket'
        return kwargs

create_ticket_view = login_required(CreateTicketView.as_view())


class UpdateTicketView(ProjectContextMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    pk_url_kwarg = 'ticket_id'
    template_name = "site/ticket_form.html"

    def get_success_url(self):
        return reverse("project-detail",
                       kwargs={"project_id": self.kwargs['project_id']})

    def get_form_kwargs(self):
        kwargs = super(UpdateTicketView, self).get_form_kwargs()
        kwargs['project'] = self.project
        kwargs['user'] = self.request.user
        kwargs['title'] = "Edit {0}".format(self.object.title)
        return kwargs

update_ticket_view = login_required(UpdateTicketView.as_view())


class TicketView(ProjectContextMixin, TemplateView):
    template_name = "site/ticket_detail.html"

    def get_context_data(self, **kwargs):
        context = super(TicketView, self).get_context_data(**kwargs)

        ticket = self.get_ticket()
        context.update({
            "ticket": ticket,
        })
        return context

ticket_view = TicketView.as_view()

class DeleteTicketView(ProjectContextMixin, DeleteView):
    model = Ticket
    pk_url_kwarg = 'ticket_id'

    def get_success_url(self):
        return reverse("project-detail",
                       kwargs={"project_id": self.kwargs['project_id']})

delete_ticket_view = DeleteTicketView.as_view()
