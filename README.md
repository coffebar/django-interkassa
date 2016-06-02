# Interkassa merchant for Django 1.9+

## Install

Checkout this repository or download an archive and extract it into your Django project.

### Edit your settings.py: 

Add to INSTALLED_APPS:    

    'interkassa_merchant',
    
Add your SecretKey and Checkout id

    INTERKASSA_ID = 'XXXXXXXXXXXXXXXXXXXXXXXX'
    INTERKASSA_SECRET = 'XXXXXXXXXXXXXXXX'
  
  
### Migrate

  > manage.py migrate
  
  
### Include urls 
  
    urlpatterns = [
      ...
      url(r'^merchant/', include('interkassa_merchant.urls')),
    ]
  
### Create view
    @login_required
    def balance(request):
        default_amount = 300
        if request.method == 'POST':
            amount = request.POST.get('amount')
            if amount:
                try:
                    amount = int(amount)
                except Exception:
                    amount = default_amount
            else:
                amount = default_amount
            inv = Invoice.objects.create(amount=amount, user=request.user,
                                         payment_info='Пополнение баланса')
            initial = dict(ik_co_id=settings.INTERKASSA_ID, ik_pm_no=inv.payment_no,
                           ik_am=inv.amount, ik_desc=inv.payment_info)
            form = PaymentRequestForm(initial=initial)
        else:
            form = PaymentRequestForm()
        return render(request, 'balance.html', locals())
        
### Create template
for example

    {% extends 'base.html' %}
    {% load staticfiles %}
    {% block title %}Пополнить баланс{% endblock %}
    {% block content %}
        <form role="form" method="post" action=""
              accept-charset="UTF-8" name="payment" id="merchant-form">
            <h3>Сумма пополнения</h3>
            <input type="number" min="1" max="100000"
                   name="amount" value="{{ default_amount }}">
            {{ form }}
            <br><button type="submit" class="btn pre-footer-btn">
                Пополнить</button>
            {% csrf_token %}
        </form>
    {% endblock %}
    {% block jquery_scripts %}
        if($("#id_ik_co_id").val().length>0){
            $("#merchant-form").attr('action', 'https://sci.interkassa.com/').submit();
        }
    {% endblock %}

### Config merchant on interkassa.com 
Use this config (except domain name)

![sample1](https://raw.githubusercontent.com/Hukuta/django-interkassa/master/conf1.png)

![sample2](https://raw.githubusercontent.com/Hukuta/django-interkassa/master/conf2.png)

