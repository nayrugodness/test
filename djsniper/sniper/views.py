import json
import sys
from operator import attrgetter

from celery.result import AsyncResult
from django.http import Http404, HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.detail import SingleObjectMixin, View
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from djsniper.sniper.forms import ConfirmForm, ProjectForm
from djsniper.sniper.models import NFTAttribute, NFTProject, Category
from djsniper.sniper.tasks import fetch_nfts_task
from rest_framework import viewsets
from djsniper.sniper.api import serializers
from djsniper.users.forms import OrderCreationForm, OrderUpdateForm
from djsniper.users.models import Order, User
from django.views.generic.edit import ModelFormMixin
from djsniper.users.api.serializers import OrderSerializer
from itertools import groupby

sys.setrecursionlimit(10000)


class HomeCategoriesListView(generic.ListView):
    template_name = "base.html"

    def get_queryset(self):
        return Category.objects.all()


def ChooseRole(request):
    return render(request, "account/choose_role.html")


class ProjectViewset(viewsets.ModelViewSet):
    queryset = NFTProject.objects.all()
    serializer_class = serializers.NFTProjectSerializer

    def get_queryset(self):
        project = NFTProject.objects.all()

        name = self.request.GET.get('name')

        if name:

            project = project.filter(name__contains=name)

        else:

            return project


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        category = Category.objects.all()

        name = self.request.GET.get('name')

        if name:

            category = category.filter(name__contains=name)

        else:

            return category

class OrdersViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        category = Category.objects.all()

        #name = self.request.GET.get('name')
        #if name:
        #    category = category.filter(name__contains=name)
        #else:
        #    return category

class ProjectListView(generic.ListView):
    template_name = "sniper/project_list.html"

    def get_queryset(self):
        return NFTProject.objects.all()


class UserProjectsView(generic.ListView):
    template_name = "users/my_projects.html"

    #def get_queryset(self):
    #    objects = Order.objects.all()

    #    grouped_objects = groupby(objects.values('nft'))
    #    print(grouped_objects, lambda x: x['id'])
    #    return {'grouped_objects': grouped_objects}
    #     return Order.objects.filter(approved=True)
    model = Order

    def __init__(self):
        self.orders = Order.objects.all()

    def group_by_project(self):
        grouped_orders = {}
        for order in self.orders:
            if order.nft not in grouped_orders:
                grouped_orders[order.nft] = []
            grouped_orders[order.nft].append(order)
        return print(grouped_orders)

    def filter_by_approval(self, approved=True):
        filtered_orders = []
        for order in self.orders:
            if order.approved == approved:
                filtered_orders.append(order)
                grouped_objects = filtered_orders
        return print(grouped_objects)


class UserBillingsView(generic.ListView):
    template_name = "users/billings.html"

    def get_queryset(self):
        return Order.objects.all()


class UserPaymentsHistoryView(generic.ListView):
    template_name = "users/payments_history.html"

    def get_queryset(self):
        return Order.objects.all()


# class ProjectDetailView(generic.DetailView):
#    template_name = "sniper/project_detail.html"

#    def get_queryset(self):
#        return NFTProject.objects.all()

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        nft_project = self.get_object()
#        order = self.request.GET.get("order", None)
#        nfts = nft_project.nfts.all()
#        if order == "rank":
#            nfts = nfts.order_by("rank")
#        context.update({"nfts": nfts[0:12]})
#        return context

# class ProjectDetailView(FormMixin, generic.DetailView):

#    model = Order
#    context_object_name = 'object'
#    template_name = 'sniper/order_create.html'
#    form_class = OrderCreationForm

#    def get_success_url(self):
#        return reverse('project-detail', kwargs={'pk': self.object.pk})
#        #return reverse('sniper:home')

#    def get_object(self):
#        try:
#            my_object = NFTProject.objects.get(id=self.kwargs.get('pk'))
#            return my_object
#        except self.model.DoesNotExist:
#            raise Http404("No MyModel matches the given query.")

#    def get_context_data(self, *args, **kwargs):
#        context = super(ProjectDetailView, self).get_context_data(*args, **kwargs)
#        nft_project = self.get_object()
# form
#        context['form'] = self.get_form()
#        context['project'] = nft_project
#        return context

#    def post(self, request, *args, **kwargs):
#        self.object = self.get_object()
#        form = self.get_form()
#        if form.is_valid():
#            return self.form_valid(form)
#        else:
#            return self.form_invalid(form)

#    def form_valid(self, form):
# put logic here
#        return super(ProjectDetailView, self).form_valid(form)

#    def form_invalid(self, form):
# put logic here
#        return super(ProjectDetailView, self).form_invalid(form)


# class ProjectDetailView(generic.DetailView):
#    template_name = "sniper/project_detail.html"

#    def get_queryset(self):
#        return NFTProject.objects.all()

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        nft_project = self.get_object()
#        order = self.request.GET.get("order", None)
#        nfts = nft_project.nfts.all()
#        if order == "rank":
#            nfts = nfts.order_by("rank")
#        context.update({"nfts": nfts[0:12]})
#        return context

class ProjectDetailView(ModelFormMixin, generic.DetailView):
    model = NFTProject
    template_name = 'sniper/project_detail.html'
    form_class = OrderCreationForm

    # no get_context_data override

    def post(self, request, *args, **kwargs):
        # first construct the form to avoid using it as instance
        form = self.get_form()
        user = request.user
        nft_project = self.get_object()

        if form.is_valid():
            # instance = form.save()
            NFTProject.objects.filter(pk=nft_project.id).update(
                supply=int(int(nft_project.supply) - int(form.cleaned_data["bonuses"])))
            user.project.add(nft_project.id)
            # form.cleaned_data["purchase"] = nft_project.price * form.cleaned_data["bonuses"]
            # form = nft_project.price * form.cleaned_data["bonuses"]
            # instance = form.save()
            # updateProjectSupply(project, instance.bonuses)
            print(form)
            instance = form.save()
            Order.objects.filter(pk=instance.id).update(
                purchase=int(int(nft_project.price) * int(form.cleaned_data["bonuses"])))
            return redirect("sniper:home")
        else:
            print(form)
            return super(ProjectDetailView, self.get_object()).form_invalid(form)

            # return form

    def get_success_url(self):
        return redirect("sniper:home")


class OrderCreateView(generic.CreateView):
    template_name = "sniper/order_create.html"
    form_class = OrderCreationForm
    model = NFTProject

    def form_valid(self, form):
        # instance = form.save()
        # nft_project = self.get_object()
        # NFTProject.objects.filter(pk=nft_project.id).update(supply=('supply') - instance.bonuses)
        # instance = form.save()
        # updateProjectSupply(project, instance.bonuses)
        return redirect("sniper:home")

    def get_queryset(self):
        return Order.objects.all()


class ProjectCreateView(generic.CreateView):
    template_name = "sniper/project_create.html"
    form_class = ProjectForm

    def form_valid(self, form):
        instance = form.save()
        return redirect("sniper:project-detail", pk=instance.id)

    def get_queryset(self):
        return NFTProject.objects.all()


class ProjectUpdateView(generic.UpdateView):
    template_name = "sniper/project_update.html"
    form_class = ProjectForm

    def get_queryset(self):
        return NFTProject.objects.all()

    def get_success_url(self):
        return reverse("sniper:project-detail", kwargs={"pk": self.get_object().id})


class OrderUpdateView(generic.UpdateView):
    template_name = "users/add_voucher.html"
    form_class = OrderUpdateForm

    def get_queryset(self):
        return Order.objects.all()

    def get_success_url(self):
        return reverse("sniper:home")  # , kwargs={"username": self.get_object().id})


class VoucherDetailView(generic.DetailView):
    template_name = "users/show_voucher.html"

    def get_queryset(self):
        return Order.objects.all()


class ProjectDeleteView(generic.DeleteView):
    template_name = "sniper/project_delete.html"

    def get_queryset(self):
        return NFTProject.objects.all()

    def get_success_url(self):
        return reverse("sniper:project-list")


class ProjectClearView(SingleObjectMixin, generic.FormView):
    template_name = "sniper/project_clear.html"
    form_class = ConfirmForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_queryset(self):
        return NFTProject.objects.all()

    def form_valid(self, form):
        nft_project = self.get_object()
        nft_project.nfts.all().delete()
        NFTAttribute.objects.filter(project=nft_project).delete()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("sniper:project-detail", kwargs={"pk": self.kwargs["pk"]})


def nft_list(request):
    project = NFTProject.objects.get(name="BAYC")
    nfts = project.nfts.all().order_by("-rarity_score")[0:12]
    return render(request, "nfts.html", {"nfts": nfts})


class FetchNFTsView(generic.FormView):
    template_name = "sniper/fetch_nfts.html"
    form_class = ConfirmForm

    def form_valid(self, form):
        result = fetch_nfts_task.apply_async((self.kwargs["pk"],), countdown=1)
        return render(self.request, self.template_name, {"task_id": result.task_id})


def get_progress(request, task_id):
    result = AsyncResult(task_id)
    response_data = {
        "state": result.state,
        "details": result.info,
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")
