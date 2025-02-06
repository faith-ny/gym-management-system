from django.shortcuts import render,redirect
from .import models
from django.template.loader import get_template
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Count
from .import forms
import stripe
from datetime import timedelta


# Create your views here.
#home page
def home(request):
    banners=models.Banners.objects.all()
    services=models.Service.objects.all()[:3]
    gimgs=models.GalleryImage.objects.all().order_by('-id')[:9]
    return render(request, 'home.html',{'banners':banners, 'services': services,'gimgs':gimgs})

#pagedetail
def page_detail(request,id):
    page=models.Page.objects.get(id=id)
    return render(request, 'page.html',{'page':page})

#FAQ
def faq_list(request):
    faq=models.Faq.objects.all()
    return render(request, 'faq.html',{'faqs':faq})


#Contact page
def contact_page(request):
    return render(request, 'contact_us.html')

#enquiry
def enquiry(request):
    msg=''
    if request.method =='POST':
        form=forms.EnquiryForm(request.POST)
        if form.is_valid ():
            form.save()
            msg='Data has been saved'
    form= forms.EnquiryForm
    return render(request, 'enquiry.html',{'form':form,'msg': msg})

#show galleries
def gallery(request):
    gallery=models.Gallery.objects.all().order_by('-id')
    return render(request, 'gallery.html',{'gallerys':gallery})


#show gallery photos
def gallery_detail(request,id):
    gallery=models.Gallery.objects.get(id=id)
    gallery_imgs=models.GalleryImage.objects.filter(gallery=gallery).order_by('-id')
    return render(request, 'gallery_imgs.html',{'gallery_imgs':gallery_imgs, 'gallery': gallery})

#subplans
def pricing(request):
    pricing=models.SubPlan.objects.annotate(total_members=Count('subscription')). all().order_by('price')
    dfeatures=models.SubPlanFeatures.objects.all()
    dfeatures=models.SubPlanFeatures.objects.all()
    return render(request, 'pricing.html',{'plans': pricing,'dfeatures':dfeatures})

#sign up
def signup(request):
    msg=None
    if request.method == 'POST':
        form= forms.SignUp(request.POST)
        if form.is_valid():
            form.save()
            msg='Thanks for signing up!'
    form=forms.SignUp
    return render(request, 'registration/signup.html',{'form':form, 'msg': msg})


#checkout
def checkout(request,plan_id):
    planDetail=models.SubPlan.objects.get(pk=plan_id)
    return render(request, 'checkout.html',{'plan': planDetail,})

stripe.api_key='sk_test_51Q1OIxBxoCFZ6pmKjUPf2PU2iqPhh66CCBm12sxBTztwlxP20p6iTO8tf8fgG5kYOVFkocMcMhtvece5i0hHbXac00sXHGZIMF'

def checkout_session(request,plan_id):
    plan=models.SubPlan.objects.get(pk=plan_id)
    session=stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
          'price_data': {
            'currency': 'usd',
            'product_data': {
             'name': plan.title,
            },
            'unit_amount': plan.price*100,
          },
           'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/pay_success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='http://127.0.0.1:8000/pay_cancel',
        client_reference_id=plan_id
    )
    return redirect(session.url, code=303)

# success
from django.core.mail import EmailMessage

def pay_success(request):
    session = stripe.checkout.Session.retrieve(request.GET['session_id'])
    plan_id=session.client_reference_id
    plan=models.SubPlan.objects.get(pk=plan_id)
    user=request.user
    models.Subscription.objects.create(
        plan=plan,
        user=user,
        price=plan.price
    )
    subject='Order Email'
    html_content=get_template('orderemail.html').render({'title':plan.title})
    from_email='fnyambura.g@gmail.com'
    
    msg = EmailMessage(subject, html_content, from_email, ['immaculate@gmail.com'])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
    
    return render(request,'success.html')

#cancel
def pay_cancel(request):
    return render(request,'cancel.html')

 #user dashboard section start 
def user_dashboard(request):
    current_plan=models.Subscription.objects.get(user=request.user)
    my_trainer=models.AssignSubscriber.objects.get(user=request.user)
    enddate=current_plan.reg_date+timedelta(days=current_plan.plan.validity_days)
    
    #notifications
    data=models.Notify.objects.all().order_by('-id')
    notifStatus=False
    jsonData=[]
    totalUnread=0
    for d in data:
        try:
            notifStatusData=models.NotifUserStatus.objects.filter(user=request.user,notif=d)
            if notifStatusData:
                notifStatus=True
        except models.NotifUserStatus.DoesNotExist:
            notifStatus=False
        if not notifStatus:
            totalUnread= totalUnread+1                       
    
    return render(request,'user/dashboard.html',{
        'current_plan':current_plan,
        'my_trainer':my_trainer,
        'total_unread':totalUnread,
        'enddate':enddate
        
    })

#edit form
def update_profile(request):
    msg=None
    if request.method=='POST':
        form=forms.ProfileForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            msg='Data has been saved'
    form=forms.ProfileForm(instance=request.user)
    return render(request,'user/update-profile.html',{'form':form,'msg':msg})


#trainer login
def trainerlogin(request):
    msg=''
    if request.method =='POST':
        username=request.POST['username']
        pwd=request.POST['pwd']
        trainer=models.Trainer.objects.filter(username=username,pwd=pwd).count()
        if trainer > 0:
            trainer=models.Trainer.objects.filter(username=username,pwd=pwd).first()
            request.session['trainerLogin']=True
            request.session['trainerid']=trainer.id
            return redirect('/trainer_dashboard')
        else:
            msg='Invalid!'   
    form=forms.TrainerLoginForm
    return render(request, 'trainer/trainer.html',{'form':form,'msg': msg})

#trainer logout
def trainerlogout(request):
    del request.session['trainerLogin']
    return redirect('/trainerlogin')

#trainer dashboard
def trainer_dashboard(request):
    return render(request,'trainer/dashboard.html')

#trainer profile
def trainer_profile(request):
    t_id=request.session['trainerid']
    trainer=models.Trainer.objects.get(id=t_id)
    msg=None
    if request.method == 'POST':
        form=forms.TrainerProfileForm(request.POST,request.FILES,instance=trainer)
        if form.is_valid():
            form.save()
            msg='Profile has been updated'
    form=forms.TrainerProfileForm(instance=trainer)
    return render(request,'trainer/profile.html',{'form':form,'msg':msg })

#notifs
def notifs(request):
    data=models.Notify.objects.all().order_by('-id')
    return render(request,'notifs.html',{'data':data})
    
    
# get all notifs
def get_notifs(request):
    data=models.Notify.objects.all().order_by('-id')
    notifStatus=False
    jsonData=[]
    for d in data:
        try:
            notifStatusData=models.NotifUserStatus.objects.filter(user=request.user,notif=d)
            if notifStatusData:
                notifStatus=True
        except models.NotifUserStatus.DoesNotExist:
            notifStatus=False
        if not notifStatus:
            totalUnread= totalUnread+1                       
        jsonData.append({
            'pk':d.id,
            'notify_detail':d.notify_detail,
            'notifStatus':notifStatus
        })
    
    
   # jsonData=serializers.serialize('json',data)
    return JsonResponse({'data':jsonData,'totalUnread':totalUnread})


# maek read by user
def mark_as_read_notif(request):
    notif=request.GET['notif']
    notif=models.Notify.objects.get(pk=notif)
    user=request.user
    models.NotifUserStatus.objects.create(notif=notif,user=user,status=True)
    return JsonResponse({'bool':True})



#trainer subscribers
def trainer_subscribers(request):
    trainer=models.Trainer.objects.get(pk=request.session['trainerid'])
    trainer_subs=models.AssignSubscriber.objects.filter(trainer=trainer).order_by('-id')
    
    return render(request,'trainer/trainer_subscribers.html',{'trainer_subs':trainer_subs})


#trainer payments
def trainer_payments(request):
    trainer=models.Trainer.objects.get(pk=request.session['trainerid'])
    trainer_pays=models.TrainerSalary.objects.filter(trainer=trainer).order_by('-id')
    
    return render(request,'trainer/trainer_payments.html',{'trainer_pays':trainer_pays})

#trainer change password
def trainer_changepassword(request):
    msg:None
    if request.method=='POST':
        new_password=request.POST['new_password']
        updateRes= models.Trainer.objects.filter(pk=request.session['trainerid']).update(pwd=new_password)
        if updateRes:
            del request.session['trainerLogin']
            return redirect('/trainerlogin')
        else:
            msg='Oops! Something is wrong'
            
    form=forms.TrainerChangePassword
    return render(request,'trainer/trainer_changepassword.html',{'form':form})



#trainer notifications
def trainer_notifs(request):
    data=models.TrainerNotification.objects.all().order_by('-id')
    return render(request,'trainer/notifs.html',{'notifs':data})


#trainer notifications
def trainer_msgs(request):
    data=models.TrainerMsg.objects.all().order_by('-id')
    return render(request,'trainer/msgs.html',{'msgs':data})

#report for user
def report_for_user(request):
    trainer=models.Trainer.objects.get(id=request.session['trainerid'])
    print(trainer)
    msg=''
    if request.method =='POST':
        form=forms.ReportForUserForm  (request.POST)
        if form.is_valid ():
            new_form=form.save(commit=False)
            new_form.report_from_trainer=trainer
            new_form.save()
            msg='Data has been saved'
        else:
            print(form)    
    form=forms.ReportForUserForm        
    return render(request,'report_for_user.html',{'form':form,'msg':msg})