from django.conf.urls import url, include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='API')

urlpatterns = [
    url(r'^api/docs/$', schema_view),
    url(r'^api/', include('webapps.API.urls')),
]
