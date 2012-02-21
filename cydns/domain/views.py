# Create your views here.

from django.template import RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list_detail import object_list
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from session_csrf import anonymous_csrf
from django.forms.formsets import formset_factory
from django.contrib import messages
from django.views.generic import DetailView, ListView, CreateView, UpdateView


from cyder.cydns.domain.models import Domain, DomainForm, DomainUpdateForm, DomainHasChildDomains
from cyder.cydns.domain.models import DomainExistsError, MasterDomainNotFoundError
from cyder.cydns.address_record.models import AddressRecord
from cyder.cydns.soa.models import SOA
from cyder.cydns.mx.models import MX
from cyder.cydns.common.utils import tablefy

import pdb
from operator import itemgetter

class DomainView(object):
    queryset            = Domain.objects.all()

class DomainListView(DomainView, ListView):
    template_name       = "domain_list.html"
    context_object_name = "domains"


class DomainDetailView(DomainView, DetailView):
    context_object_name = "domain"
    template_name       = "domain_detail.html"

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        domain = kwargs.get('object', False)
        if not domain:
            return context
        address_objects = AddressRecord.objects.filter( domain = domain )
        adr_headers, adr_matrix, adr_urls = tablefy( address_objects )

        mx_objects = MX.objects.filter( domain = domain )
        mx_headers, mx_matrix, mx_urls = tablefy( mx_objects )

        # Join the two dicts
        context = dict( {
                    # A and AAAA
                    "address_headers": adr_headers,
                    "address_matrix": adr_matrix,
                    "address_urls": adr_urls,
                    # MX
                    "mx_headers": mx_headers,
                    "mx_matrix": mx_matrix,
                    "mx_urls": mx_urls
                        }.items() + context.items() )
        return context

@csrf_exempt
def domain_create(request):
    if request.method == 'POST':
        domain_form = DomainForm(request.POST)
        # Try to create the domain. Catch all exceptions.
        try:
            # If there were errors collect them and render the page again, displaying the errors.
            if domain_form.errors:
                errors = ""
                for k,v in domain_form.errors.items():
                    for reason in v:
                        errors += k+": "+reason+"\n"
                messages.error( request, errors )
                return render( request, "domain_create.html", { "domain_form": domain_form } )
            domain_form.is_valid()
            domain = domain_form.save(commit=False)
            if domain_form.cleaned_data['inherit_soa'] and domain.master_domain:
                domain.soa = domain.master_domain.soa
            domain.save()
        except Exception, e:
            messages.error( request, e.__str__() )
            return render( request, "domain_create.html", { "domain_form": domain_form } )

        # Success. Redirect.
        messages.success(request, '%s was successfully created.' % (domain.name))
        return redirect( domain )
    else:
        domain_form = DomainForm()
        return render( request, "domain_create.html", { 'domain_form': domain_form } )


@csrf_exempt
def domain_update(request, pk):
    # Construct tables of the child objects.
    domain = get_object_or_404( Domain, pk = pk )
    if request.method == 'POST':
        try:
            domain_form = DomainUpdateForm(request.POST)
            if domain_form.data.get('delete', False):
                domain.delete()
                messages.success(request, '%s was successfully deleted.' % (domain.name))
                return redirect('cyder.cydns.domain.views.domain_list')
            new_soa_pk = domain_form.data.get('soa', None)
            if new_soa_pk:
                new_soa = SOA.objects.get( pk = new_soa_pk )
                domain.soa = new_soa

            if domain.soa and not new_soa_pk:
                domain.soa = None

            if domain_form.data.get('inherit_soa', False) and domain.master_domain:
                domain.soa = domain.master_domain.soa

            domain.save() # Major exception handling logic goes here.
        except Exception, e:
            domain_form = DomainUpdateForm(instance=domain)
            messages.error( request, e.__str__() )
            return render( request, "domain_update.html", { "domain_form": domain_form } )

        messages.success(request, '%s was successfully updated.' % (domain.name))

        return redirect( domain )
    else:
        domain_form = DomainUpdateForm(instance=domain)
        return render( request, "domain_update.html", { 'domain_form': domain_form } )
