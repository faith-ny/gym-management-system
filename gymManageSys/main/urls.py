from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from .import views


urlpatterns = [
    path('', views.home, name='home'),
    path('pagedetail/<int:id>', views.page_detail, name='pagedetail'),
    path('faq',views.faq_list,name='faq'),
    path('enquiry',views.enquiry,name='enquiry'),
    path('contact_page',views.contact_page,name='contact_page'),
    path('gallery',views.gallery,name='gallery'),
    path('gallerydetail/<int:id>',views.gallery_detail,name='gallery_detail'),
    path('pricing',views.pricing,name='pricing'),
    path('accounts/signup',views.signup,name='signup'),
    path('checkout/<int:plan_id>',views.checkout,name='checkout'),
    path('checkout_session/<int:plan_id>',views.checkout_session,name='checkout_session'),
    path('pay_success',views.pay_success,name='pay_success'),
    path('pay_cancel',views.pay_cancel,name='pay_cancel'),
    
    #user dashboard section start 
    path('user-dashboard',views.user_dashboard,name='user_dashboard'),
    path('update-profile',views.update_profile,name='update_profile'),
    
    
    #trainer login
    path('trainerlogin',views.trainerlogin,name='trainerlogin'),   
    path('trainerlogout',views.trainerlogout,name='trainerlogout'),
    path('trainer_dashboard',views.trainer_dashboard,name='trainer_dashboard'),
    path('trainer_profile',views.trainer_profile,name='trainer_profile'),
    path('trainer_subscribers',views.trainer_subscribers,name='trainer_subscribers'),
    path('trainer_payments',views.trainer_payments,name='trainer_payments'),
    path('trainer_changepassword',views.trainer_changepassword,name='trainer_changepassword'),
    #path('trainer_subscribers',views.trainer_subscribers,name='trainer_subscribers'),
    path('trainer_notifs',views.trainer_notifs,name='trainer_notifs'),   
    #notification   
    path('notifs',views.notifs,name='notifs'),   
    path('get_notifs',views.get_notifs,name='get_notifs'),   
    path('mark_as_read_notif',views.mark_as_read_notif,name='mark_as_read_notif'),   
    #messages
    path('messages',views.trainer_msgs,name='messages'),  
    path('report_for_user',views.report_for_user,name='report_for_user'),  
] 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
