from django.conf.urls import url,include
from . import views
from . import webViews

from rest_framework import routers


router = routers.DefaultRouter()
# router.register(r'users',views.UserViewSet)
# router.register(r'articals',views.ArticalViewSet)
# router.register(r'taglist',views.ArticalTagViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),

    url(r'^articals$', views.Artical_list_api),#文章列表
    url(r'^articalTags$', views.Artical_Tag_List_api),#文集列表

    url(r'^register$', views.UserRegisterAPIView.as_view()),
    url(r'^login$', views.UserLoginAPIView.as_view()),
    
    url(r'^web_login/$', webViews.login,name='login'),
    url(r'^web_register/$', webViews.register,name='register'),
    url(r'^index/$', webViews.index,name='index'),
    url(r'^mine/$', webViews.myHome,name='mine'),
    url(r'^author/(?P<username>\w+)$', webViews.author,name='author'),

    url(r'^web_taglist/$', webViews.tagList,name='web_taglist'),
    url(r'^tag_detail/(?P<tag_id>[0-9]+)$', webViews.tag_detail,name='tag_detail'),

    url(r'^edit_artical/(?P<artical_id>[0-9]+)$', webViews.edit_page,name='edit_artical'),
    url(r'^pup_artical/$', webViews.pup_page,name='pup_artical'),
    url(r'^artical_detail/(?P<artical_id>[0-9]+)$', webViews.artical_detail,name='artical_detail'),
    
    url(r'^artical_draft_save/$', views.artical_draft_save,name='artical_draft_save'),


    url(r'^user_taglist/$', webViews.get_userTag,name='get_userTag'),
    url(r'^get_articalBy_tag/(?P<tag_id>[0-9]+)$', webViews.get_articalBy_tag,name='get_articalBy_tag'),

    url(r'^meiHome/$', webViews.meiHome,name='meiHome'),
    url(r'^meiNeibor/$', webViews.meiNeibor,name='meiNeibor'),

]


