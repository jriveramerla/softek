from django.shortcuts import render
from django.db import connection
import pandas
from Reports.models import customer_ord_lines

def index(request):
    return render(request, 'Reports/index.html', 
                    dict(Content='''
                            <div class="text-center mt-5">
                                <h1>Softek Test - Jose Rivera Merla</h1>
                                <p class="lead">Reportes De Prueba</p>
                                <p>Version v1.0</p>
                            </div>
                 '''))

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
