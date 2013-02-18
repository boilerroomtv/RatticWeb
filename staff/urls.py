from django.conf.urls import patterns, include, url
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User, Group
from views import NewUser, UpdateUser

urlpatterns = patterns('staff.views',
    # Views in views.py
    url(r'^$', 'home'),
    url(r'^userdetail/(?P<uid>\d+)/$','userdetail'),
    url(r'^groupdetail/(?P<gid>\d+)/$','groupdetail'),
) + patterns('',
    # Class based views
    url(r'^userdelete/(?P<pk>\d+)/$', staff_member_required(DeleteView.as_view(model=User, template_name='staff_userdel.html',  success_url='/staff/'))),
    url(r'^groupdelete/(?P<pk>\d+)/$', staff_member_required(DeleteView.as_view(model=Group, template_name='staff_groupdel.html',  success_url='/staff/'))),
    url(r'^groupadd/$', staff_member_required(CreateView.as_view(model=Group, template_name='staff_groupedit.html',  success_url='/staff/'))),
    url(r'^groupedit/(?P<pk>\d+)/$', staff_member_required(UpdateView.as_view(model=Group, template_name='staff_groupedit.html',  success_url='/staff/'))),
) + patterns('',
    # Custom class based views
    url(r'^useradd/$', NewUser.as_view()),
    url(r'^useredit/(?P<pk>\d+)/$', UpdateUser.as_view()),
)