from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect

from openpyxl import load_workbook, Workbook

from basket import models


@admin.register(models.Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.Motorcycle)
class AdminMotorcycle(admin.ModelAdmin):
    list_display = ['name', 'category']
    prepopulated_fields = {'slug': ['name']}
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.excel_file:
            try:
                wb: Workbook = load_workbook(obj.excel_file)
                ws = wb[wb.sheetnames[0]]

                mainparts = []
                parts = []
                counter_mainparts = 0
                previous_value = 0

                # Получаем данные с Excel файла и создаем объект экземпляра MainPart
                for row in ws.iter_rows(min_row=1, min_col=2, max_col=6):
                    value_mainpart = str(row[0].value)
                    for i in range(1, 100):
                        if value_mainpart is not None and value_mainpart.startswith(str(i) + '.'):
                            obj_mainaprt = models.MainPart(
                                name=value_mainpart,
                                motorcycle=obj,
                            )
                            mainparts.append(obj_mainaprt)

                # Создаем объекты MainPart
                models.MainPart.objects.bulk_create(mainparts)

                # Получаем данные с Excel файла и создаем объект экземпляра Part
                for row in ws.iter_rows(min_row=1, min_col=2, max_col=6):
                    name_value = str(row[3].value)
                    value_code = str(row[1].value)
                    if value_code is not None and value_code.startswith('R'):
                        number_value = int(row[0].value)
                        if number_value > previous_value:
                            previous_value = number_value

                            # Создаем экземпляр модели Part
                            part = models.Part(
                                main_part=mainparts[counter_mainparts],
                                number=number_value,
                                code=value_code,
                                name=name_value
                            )

                            parts.append(part)
                        elif number_value == 1:
                            counter_mainparts += 1
                            previous_value = number_value

                            part = models.Part(
                                main_part=mainparts[counter_mainparts],
                                number=number_value,
                                code=value_code,
                                name=name_value
                            )

                            parts.append(part)

                # Создаем модели Part
                models.Part.objects.bulk_create(parts)
            except Exception as ex:
                obj.delete()
                messages.error(request, "Не удалось получить данные с excel файла")


@admin.register(models.MainPart)
class AdminMainPart(admin.ModelAdmin):
    list_display = ['name', 'motorcycle']


@admin.register(models.Part)
class AdminPart(admin.ModelAdmin):
    list_display = ['name', 'main_part', 'price', 'number']


class OrderedPartInline(admin.TabularInline):
    model = models.OrderedPart
    extra = 0
    readonly_fields = ('part', 'quantity')


@admin.register(models.CheckoutCart)
class CheckoutCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'created_at')
    inlines = (OrderedPartInline,)


admin.site.register(models.OrderedPart)
