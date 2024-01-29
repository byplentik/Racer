import logging
import re

from django.contrib import admin, messages
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.views.main import ChangeList
from openpyxl import load_workbook, Workbook

from basket import models
from basket.forms import MotorcycleAdminForm


@admin.register(models.Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.Motorcycle)
class AdminMotorcycle(admin.ModelAdmin):
    list_display = ['name', 'category']
    prepopulated_fields = {'slug': ['name']}

    def get_form(self, request, obj=None, change=False, **kwargs):
        kwargs['form'] = MotorcycleAdminForm
        return super().get_form(request, obj, **kwargs)
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        mainparts = []

        if obj.excel_file:
            try:
                wb: Workbook = load_workbook(obj.excel_file)
                ws = wb[wb.sheetnames[0]]

                counter_mainparts = -1
                previous_value = 0

                # Получаем данные с Excel файла и создаем объект экземпляра MainPart
                for row in ws.iter_rows(min_row=1, min_col=2, max_col=6):
                    value_mainpart_or_number = str(row[0].value)
                    try:
                        value_number = int(value_mainpart_or_number)
                        code_value = str(row[1].value)
                        name_value = str(row[3].value)

                        if value_number > previous_value and code_value.startswith('R'):
                            models.Part.objects.create(
                                main_part=mainparts[counter_mainparts],
                                number=value_number,
                                code=code_value,
                                name=name_value,
                            )

                            previous_value = value_number
                    except:
                        mainpart_value = str(value_mainpart_or_number)
                        if mainpart_value != 'None' and any(mainpart_value.startswith(str(i) + '.') for i in range(1, 101)):
                            # Извлечение номера с помощью regex
                            match = re.match(r'^(\d+)\.', mainpart_value)

                            if match:
                                number_mainpart = int(match.group(1))
                                mainpart_obj, created = models.MainPart.objects.get_or_create(
                                    motorcycle=obj,
                                    name=mainpart_value,
                                    ordering=number_mainpart,
                                )
                                counter_mainparts += 1
                                previous_value = 0
                                mainparts.append(mainpart_obj)
            except Exception as ex:
                obj.delete()
                messages.error(request, "Не удалось получить данные с excel файла")

            if mainparts:
                imgs_for_mainparts_list = request.FILES.getlist('imgs_for_mainparts')
                for i in range(0, len(mainparts)):
                    mainparts[i].image = imgs_for_mainparts_list[i]
                    mainparts[i].save()


@admin.register(models.MainPart)
class AdminMainPart(admin.ModelAdmin):
    list_display = ['name', 'motorcycle', 'ordering']


@admin.register(models.Part)
class AdminPart(admin.ModelAdmin):
    list_display = ['name', 'code', 'main_part', 'price', 'number']


class OrderedPartInline(admin.TabularInline):
    model = models.OrderedPart


@admin.register(models.CheckoutCart)
class CheckoutCartAdmin(admin.ModelAdmin):
    list_display = ('id_as_order_number', 'client', 'total_price', 'created_at', 'order_status')
    list_display_links = ['id_as_order_number', 'client']
    list_filter = ['order_status', 'created_at']
    search_fields = ['id']
    date_hierarchy = 'created_at'
    inlines = (OrderedPartInline,)
    change_form_template = 'admin/basket/CheckoutCart/change_form_custom.html'

    # def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    #     response = super().changeform_view(request, object_id, form_url, extra_context)
    #     return response


@admin.register(models.ExcelFileCatalog)
class AdminExcelFileCatalog(admin.ModelAdmin):
        def save_model(self, request, obj, form, change):
            super().save_model(request, obj, form, change)
            parts = []

            if obj.excel_file:
                try:
                    wb: Workbook = load_workbook(obj.excel_file)
                    ws = wb[wb.sheetnames[0]]

                    for row in ws.iter_rows(min_row=1, min_col=1, max_col=3):
                        if row[0].value is not None and str(row[0].value).startswith('R'):
                            code_value = str(row[0].value)
                            price_value = str(row[2].value)
                            try:
                                part = models.Part.objects.filter(
                                    code=code_value
                                ).update(price=price_value)
                            except models.Part.DoesNotExist as ex:
                                logging.error(f'An error occurred while updating the price: {ex}')
                except FileNotFoundError as ex:
                    logging.error(f'Произошла ошибка при загрузке файла Excel: {ex}')


# @admin.register(models.ProxyCheckoutCartModel)
# class AdminProxyCheckoutCartModel(admin.ModelAdmin):
#     list_display = ('id', 'user', 'total_price', 'created_at')
