from django.shortcuts import render
from django.db import connection
import pandas
from Reports.models import customer_ord_lines
from Reports.models import weather

def index(request):
    return render(request, 'Reports/index.html', 
                    dict(Content='''
                            <div class="text-center mt-5">
                                <h1>Softek Test - Jose Rivera Merla</h1>
                                <p class="lead">Reportes De Prueba</p>
                                <p>Version v1.0</p>
                            </div>
                 '''))

def DetectingChange(request):
    df                   = pandas.DataFrame([r.getData() for r in weather.objects.order_by('date')])
    df.loc[:,'rain']     = df.loc[:,'was_rainy']
    df.loc[:,'was_rainy']= df.rain.shift(1)!=df.rain

    return render(request, 'Reports/index.html', 
            dict(Content='<h1>Detecting Change</h1><br>'+df.loc[df.was_rainy.eq(True)&df.rain.eq(True)].loc[:,['date','was_rainy']].to_html()))

def SeasonsProblem(request):
    with connection.cursor() as cursor:
        query = """
        SELECT distinct 
            F.ord_id,
            F.ord_dt
        FROM reports_customer_orders F
        """
        cursor.execute(query)
        df      = pandas.DataFrame( [dict(ord_id=r[0],ord_dt=r[1]) for r in cursor.fetchall()])
        def getSeason(x):
            MyDay=(x.year*10000+x.month*100+x.day)
            if   (x.year*10000+319) >= MyDay <= (x.year*10000+619):
                rv= 'Sprint'
            elif (x.year*10000+620) >= MyDay <= (x.year*10000+921):
                rv='Summer'
            elif (x.year*10000+922) >= MyDay <= (x.year*10000+1220):
                rv='Fall'
            else:
                rv='Winter'
            return rv
        df.loc[:,'Season']=df.ord_dt.apply(getSeason)
        df.drop(['ord_dt'],axis='columns',inplace=True)
    return render(request, 'Reports/index.html', 
                    dict(Content='<h1>Order Seasons Report</h1><br>'+df.to_html()))

def CustomerOrderStatus(request):
    with connection.cursor() as cursor:
        query = """
        SELECT distinct 
            F.order_number,
            F.status
        FROM reports_customer_ord_lines F
        where F.status='CANCELLED' and 
            F.order_number not in (select order_number from reports_customer_ord_lines where status in ('PENDING','SHIPPED')) 
        union all
        SELECT distinct 
            F.order_number,
            F.status
        FROM reports_customer_ord_lines F
        where F.status='PENDING' 
        union all
        SELECT distinct 
            F.order_number,
            F.status
        FROM reports_customer_ord_lines F
        where 
            F.status='SHIPPED' and
            F.order_number not in (select order_number from reports_customer_ord_lines where status ='PENDING') 
        """
        cursor.execute(query)
        df      = pandas.DataFrame( [dict(order_number=r[0],status=r[1]) for r in cursor.fetchall()])
    return render(request, 'Reports/index.html', 
                    dict(Content='<h1>Customer Order Status Report</h1><br>'+df.to_html()))
