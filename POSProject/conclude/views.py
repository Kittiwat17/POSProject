from django.http import HttpResponse
from django.shortcuts import render
from django.template.context_processors import request
from django.template.defaulttags import register

from sale.models import Order

# Create your views here.

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_count(lists):
    return lists.count()

def conclude(request):
    run_number = 0
    old_year = ''
    old_month = ''
    old_week = ''
    old_day = ''

    submit_btn = request.GET.get('submit_btn', '')
    income_order = Order.objects.all().order_by('date_time')

    report_scope = []
    year_list = []
    year_income = {}

    month_list = {}
    month_income = {}

    month_income = []
    month_income.append([])

    week_income = []
    week_income.append([])

    day_income = []
    day_income.append([])

    if submit_btn == 'yearly':
        report_scope = ['YEAR', 'INCOME']

        year_income = []
        year_income.append([])

        old_year = ''
        for y in income_order:
            yy = str(y.date_time.year)
            if yy == old_year:
                year_income[run_number][1] = year_income[run_number][1] + y.total_price
            else:
                run_number = run_number + 1
                year_income.append([])
                year_income[run_number].append(yy)
                year_income[run_number].append(y.total_price)
            old_year = yy

    elif submit_btn == 'monthly':
        report_scope = ['YEAR', 'MONTH', 'INCOME']
  
        month_income = []
        month_income.append([])

        old_year = ''
        old_month = ''
        for y in income_order:
            yy = str(y.date_time.year)
            mm = str(y.date_time.month)
            if yy == old_year:
                if mm == old_month:
                    month_income[run_number][2] = month_income[run_number][2] + y.total_price
                else:
                    run_number = run_number + 1
                    month_income.append([])
                    month_income[run_number].append(yy)
                    month_income[run_number].append(mm)
                    month_income[run_number].append(y.total_price)
            else:
                run_number = run_number + 1
                month_income.append([])
                month_income[run_number].append(yy)
                month_income[run_number].append(mm)
                month_income[run_number].append(y.total_price)

            old_year = yy
            old_month = mm

    elif submit_btn == 'weekly':
        report_scope = ['YEAR', 'MONTH', 'WEEK', 'INCOME']
        week_income = []
        week_income.append([])

        for order in income_order:
            yy = str(order.date_time.year)
            mm = str(order.date_time.month)
            ww = str(order.date_time.isocalendar()[1] + 1)
            if ww == '54':
                ww = '1'

            if yy == old_year:
                if ww == old_week:
                    week_income[run_number][3] = week_income[run_number][3] + order.total_price
                else:
                    run_number = run_number + 1
                    week_income.append([])
                    week_income[run_number].append(yy)
                    week_income[run_number].append(mm)
                    week_income[run_number].append(ww)
                    week_income[run_number].append(order.total_price)
            else:
                run_number = run_number + 1
                week_income.append([])
                week_income[run_number].append(yy)
                week_income[run_number].append(mm)
                week_income[run_number].append(ww)
                week_income[run_number].append(order.total_price)
            old_year = yy
            old_week = ww

    elif submit_btn == 'daily':
        report_scope = ['YEAR', 'MONTH', 'WEEK', 'DAY', 'INCOME']
        day_income = []
        day_income.append([])

        for order in income_order:
            yy = str(order.date_time.year)
            mm = str(order.date_time.month)
            dd = str(order.date_time.day)
            ww = str(order.date_time.isocalendar()[1] + 1)
            if ww == '54':
                ww = '1'
            if yy == old_year and mm == old_month and dd == old_day:
                day_income[run_number][4] = day_income[run_number][4] + order.total_price
            else:
                run_number = run_number + 1
                day_income.append([])
                day_income[run_number].append(yy)
                day_income[run_number].append(mm)
                day_income[run_number].append(ww)
                day_income[run_number].append(dd)
                day_income[run_number].append(order.total_price)
            old_year = yy
            old_month = mm
            old_day = dd

    return render(request, template_name='conclude/conclude_page.html', context={
        'year_income': year_income,
        'report_scope': report_scope,
        'month_income': month_income,
        'week_income': week_income,
        'day_income': day_income,
        'submit_btn': submit_btn
    })