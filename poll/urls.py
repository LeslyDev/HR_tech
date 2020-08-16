from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from poll.views import *

urlpatterns = [
    path('list_of_blocks/', blocks_view, name='list_of_blocks_url'),
    path('block/<int:block_id>/', block_detail, name='block_detail_url'),
    path('test_result/<block_id>/', finish_test, name='finish_test_url'),
    path('interview_result/<block_id>/', finish_interview,
         name='finish_interview_url'),
    path('completed_list/', completed_block_list, name='completed_list_url'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('index/', index, name='index'),
    path('rating/', rating, name='rating_url'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
