from . import views
from django.conf.urls import url


#contains url for site
urlpatterns  = [
    url(r'^$', views.IndexView, name='index'),
    url(r'^live/$',views.LiveView,name="live"),
    url(r'^time/$',views.TimeView,name='time'),
    url(r'^graph/$',views.GraphView,name='graph'),
    url(r'^timeline/$',views.TimelineView,name='timeline'),
    # url(r'^register/$', views.Affiliate_new, name="register_affiliate"),
    # url(r'^admin_index/$', views.Admin,name='admin_index'),
    # url(r'^admin_index/generate/$',views.generate_bitlinks, name = 'generate_bitlink'),
    # url(r'admin_index/search/$',views.search_affiliate, name = "search_affiliate"),
    # url(r'admin_index/approve_request/$',views.approve_request, name = "approve_request"),
    # url(r'affilate_login/$',views.affiliate_login,name = "affiliate_login"),
    # url(r'affiliate_login/logout/$',views.affiliate_logout,name = 'affiliate_logout'),
    # url(r'admin_index/generate_excel/$',views.create_excel,name = 'create_excel'),
    # url(r'affiliate_login/generate_bitlink/$',views.generate_bitlink_aff,name="generate_bitlink_aff")
]