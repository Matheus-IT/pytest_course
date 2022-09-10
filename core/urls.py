from django.contrib import admin
from django.urls import path, include
from companies.urls import companies_router
from companies import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(companies_router.urls)),
    path('send-email/', views.send_company_email),
    path('fibonacci/<n>', views.fibonacci, name='fibonacci'),
]

# Silk url config
urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]

# Serving static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
