from accounts.models import AddAddress, AddState, AddEmailAddress
from django.core.checks import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import Hospital, Product, ReviewRating, ProductGallery, Appointments, ProductDetailedDescriptionPanelCheck
from category.models import Category

from carts.models import CartItem
from carts.views import _cart_item
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .forms import ReviewForm, AppointmentForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from orders.models import OrderProduct
import datetime


###########

from .models import BloodCategory, Hospital
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None
    if category_slug!=None:
        categories =  get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category = categories, is_available = True)
        paginator = Paginator(products, 6)
        page=request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count =  products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page=request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
            'products':paged_products,
            'product_count':product_count,
        }
    return render(request, 'store/store.html', context)



def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart= CartItem.objects.filter(cart__cart_id = _cart_item(request), product = single_product).exists()

        try:
            product_description_panels = ProductDetailedDescriptionPanelCheck.objects.filter(product__slug = product_slug)
        except Exception as e:
            raise e
        try:
            products = Product.objects.filter(category__slug=category_slug)

        except Exception as e:
            raise e
            
    except Exception as e:
        raise e
    
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except ObjectDoesNotExist:
            orderproduct = None
    else:
        orderproduct =None

    try:
        reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)
        reviewExist =True
    except ObjectDoesNotExist:
        reviews="No review yet"
        reviewExist =False
    
    product_gallery_exists = ProductGallery.objects.filter(product_id = single_product.id).exists()

    if product_gallery_exists:
        product_gallery = ProductGallery.objects.filter(product_id = single_product.id)
    else:
        product_gallery=None

    context = {
        'single_product':single_product,
        'in_cart':in_cart,
        'orderproduct':orderproduct,
        'reviews':reviews,
        'reviewExist':reviewExist,
        'product_gallery':product_gallery,
        'product_gallery_exists':product_gallery_exists,
        'product_description_panels':product_description_panels,
        'products':products,
    

    }
    return render(request, 'store/product_detail.html', context) 


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(product_description__icontains=keyword) | Q(product_name__icontains = keyword))
            product_count = products.count()
            context={
                'products': products,
                'product_count':product_count
            }
            return render(request, 'store/store.html', context)

    return render(request, 'store/store.html')


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
    
            reviews = ReviewRating.objects.get(user__id = request.user.id, product__id = product_id)
           
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            print(form)
            messages.success(request, "Thank you! Your review has been updated. ")
            return redirect(url)
        except ObjectDoesNotExist:
           
            form = ReviewForm(request.POST)
            if form.is_valid():
               
                data =  ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                print(data)
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)


@login_required(login_url = 'login')
def appointments(request):
    current_user = request.user
 
    if request.method == "POST":
        # blood_category = request.POST['blood_category']
        hospital = request.POST['hospital']
        blood_category = BloodCategory.objects.all()
        blood_category_list=[]
        blood_dic={}
        total_amount =0
        for blood in blood_category:
            try:
                blood_category_list.append(request.POST[str(blood.category_name)])
                blood_dic[str(blood.category_name)] = blood.category_price
                total_amount += blood.category_price

                
            except:
                pass
        blood_string=",".join(blood_category_list)
        state = request.POST['state']
        form =AppointmentForm(request.POST)
        
 
        if form.is_valid():
            print("valid")
            data = Appointments()
            data.user=current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.state = AddState.objects.get(state__iexact = state)
            data.city = form.cleaned_data['city']
            data.blood_category = blood_string
            data.blood_category_detail = blood_dic
            data.hospital = Hospital.objects.get(hospital_name__iexact = hospital)
            data.total_amount = total_amount
            data.date =form.cleaned_data['date']
            data.time = form.cleaned_data['time']
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
 
            #Generate Order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d =datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            appointment_number = form.cleaned_data['city'] + current_date + str(data.id)
            data.appointment_number = appointment_number
            data.save()
 
            appointment_details = Appointments.objects.filter(user = request.user, vendorConfirmation=False)
            sub_total = 0
            
            for detail in appointment_details:
                sub_total += detail.total_amount
            
            tax = (sub_total * 2)/100
            total = sub_total + tax
            
            context = {
                'appointment_details':appointment_details,
                'sub_total':sub_total,
                'tax':tax,
                'total':total,
                'blood_dic':blood_dic
                
            }
            return render(request, 'appointment/payment.html', context)
        else:
            return redirect('site-landing')
    
 
    else:
            exists = Appointments.objects.filter(user=request.user, vendorConfirmation=False).exists
            if exists:
                appointment_details = Appointments.objects.filter(user = request.user, vendorConfirmation=False)
                sub_total = 0
                
                for detail in appointment_details:
                    sub_total+= detail.total_amount
                
                tax = (sub_total * 2)/100
                total = sub_total + tax
                
                context = {
                            'appointment_details':appointment_details,
                            'sub_total':sub_total,
                            'tax':tax,
                            'total':total,
                            
                        }
                return render(request, 'appointment/payment.html', context)
            else:
                return redirect('site-landing') 
 
 
def remove_appointment(request, appointment_number):
    try:
        if request.user.is_authenticated:
            appointments = Appointments.objects.get(user = request.user, appointment_number = appointment_number, vendorConfirmation=False)
            appointments.delete()
            return redirect('appointments')
    except:
        pass
 
                
            
        
@login_required(login_url = 'login')
def payment_appoinment(request):
    if request.user.is_authenticated:
            appointments = Appointments.objects.filter(user = request.user, vendorConfirmation=False)
            for appointment in appointments:
                appointment.vendorConfirmation = True
                appointment.save()
            
            appointments = Appointments.objects.filter(user = request.user, vendorConfirmation=True, is_billed=False)
            sub_total = 0
            tax=0
            total=0
            blood_list =[]
            
            for detail in appointments:
                import ast
                print(detail.blood_category_detail)
                blood_dic = detail.blood_category_detail
                blood = ast.literal_eval(blood_dic)
                blood_list.append(blood)
                sub_total+= detail.total_amount
                tax = (sub_total * 2)/100
                total = sub_total + tax
            user =request.user

            
            yr = int(datetime.date.today().strftime('%Y'))
            dy = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d =datetime.date(yr,mt,dy)
            current_date = d.strftime("%Y%m%d")
            mail_subject = 'Thank you for your order'
            message = render_to_string('appointment/order_recieved_email.html', {
                        'user':request.user,
                        'appointments':appointments,
                        'tax':tax,
                        'total':total,
                        'admin':False,
                        'current_date':current_date,
                        'blood_list':blood_list,
                    })
            to_email = request.user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()


            mail_subject = 'Got new appointment'
            message = render_to_string('appointment/order_recieved_email.html', {
                        'user': 'request.user',
                        'admin':True,
                        'appointments':appointments,
                        'tax':tax,
                        'total':total,
                        'current_date':current_date,
                        'blood_list':blood_list,
                       
                    })
            for appoint in appointments:
                appoint_email = appoint.state.state
                email = AddEmailAddress.objects.get(state__state = appoint_email)
                print(email)

                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()

                to_email = 'aacs807@gmail.com'
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()

            for appointment in appointments:
                appointment.is_billed = True
                appointment.save()
            # address_details = AddAddress.objects.get(user = request.user)
            print(type(appointments))
            context = {
                'appointments':appointments,
                'sub_total':sub_total,
                'tax':tax,
                'total':total,
                'user':user,
                # 'address_details':address_details,
                'current_date':current_date,
                'blood_list': blood_list,
            }
 
            return render(request, 'appointment/order_complete.html',context)
            # return redirect('site-landing')



def make_appointments(request):

    return render(request, 'store/make_appointments.html')