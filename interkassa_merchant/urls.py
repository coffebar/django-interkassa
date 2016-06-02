from django.conf.urls import url

from interkassa_merchant.views import result, success, fail, wait

urlpatterns = [
    url(r'^result/$', result, name='interkassa_result'),
    url(r'^success/$', success, name='interkassa_success'),
    url(r'^fail/$', fail, name='interkassa_fail'),
    url(r'^wait/$', wait, name='interkassa_wait'),
]
