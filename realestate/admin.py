from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils import timezone

from realestate.models import (
    User,
    Apartment,
    ApartmentImage,
    PaymentPlan,
    Contract,
    PaymentSchedule,
    AuditLog,
)


# =========================================================
# GROUP / ROLE ADMIN
# =========================================================

try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )

    search_fields = (
        'name',
    )

    filter_horizontal = (
        'permissions',
    )

    ordering = (
        'name',
    )

    list_per_page = 25


# =========================================================
# USER / CLIENT ADMIN
# =========================================================

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'phone_number',
        'is_client',
        'is_staff',
        'is_active',
        'date_joined',
    )

    list_filter = (
        'is_client',
        'is_staff',
        'is_active',
        'is_superuser',
        'groups',
        'date_joined',
    )

    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'passport_number',
    )

    ordering = (
        '-date_joined',
    )

    readonly_fields = (
        'last_login',
        'date_joined',
    )

    list_per_page = 25

    fieldsets = UserAdmin.fieldsets + (
        (
            'HomeMarket maʼlumotlari',
            {
                'fields': (
                    'phone_number',
                    'passport_number',
                    'address',
                    'is_client',
                )
            }
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'HomeMarket maʼlumotlari',
            {
                'fields': (
                    'phone_number',
                    'passport_number',
                    'address',
                    'is_client',
                )
            }
        ),
    )


# =========================================================
# APARTMENT IMAGE INLINE
# =========================================================

class ApartmentImageInline(admin.TabularInline):
    model = ApartmentImage

    extra = 1

    fields = (
        'image',
        'is_main',
    )

    show_change_link = True


# =========================================================
# APARTMENT ACTIONS
# =========================================================

@admin.action(description='Tanlanganlarni "Bo‘sh" qilish')
def mark_apartments_available(modeladmin, request, queryset):
    queryset.update(status='available')


@admin.action(description='Tanlanganlarni "Band qilingan" qilish')
def mark_apartments_reserved(modeladmin, request, queryset):
    queryset.update(status='reserved')


@admin.action(description='Tanlanganlarni "Sotilgan" qilish')
def mark_apartments_sold(modeladmin, request, queryset):
    queryset.update(status='sold')


# =========================================================
# APARTMENT ADMIN
# =========================================================

@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'property_type',
        'room_count',
        'square_meters',
        'district',
        'floor',
        'total_floors',
        'total_price',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'property_type',
        'room_count',
        'renovation',
        'city',
        'district',
        'has_balcony',
        'has_parking',
        'has_elevator',
        'has_furniture',
        'has_air_conditioner',
    )

    search_fields = (
        'title',
        'address',
        'district',
        'city',
        'description',
    )

    ordering = (
        '-created_at',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    list_per_page = 25

    date_hierarchy = 'created_at'

    actions = (
        mark_apartments_available,
        mark_apartments_reserved,
        mark_apartments_sold,
    )

    fieldsets = (
        (
            '🏠 Asosiy maʼlumotlar',
            {
                'fields': (
                    'title',
                    'property_type',
                    'room_count',
                    'square_meters',
                    'description',
                )
            }
        ),

        (
            '📍 Joylashuv',
            {
                'fields': (
                    'city',
                    'district',
                    'address',
                )
            }
        ),

        (
            '🏢 Bino maʼlumotlari',
            {
                'fields': (
                    'floor',
                    'total_floors',
                    'building_year',
                    'renovation',
                )
            }
        ),

        (
            '💰 Narx va holat',
            {
                'fields': (
                    'total_price',
                    'status',
                )
            }
        ),

        (
            '✨ Qulayliklar',
            {
                'fields': (
                    'has_balcony',
                    'has_parking',
                    'has_elevator',
                    'has_furniture',
                    'has_air_conditioner',
                )
            }
        ),

        (
            '🧊 3D model',
            {
                'fields': (
                    'model_3d_file',
                )
            }
        ),

        (
            '⚙️ Tizim maʼlumotlari',
            {
                'fields': (
                    'created_at',
                    'updated_at',
                )
            }
        ),
    )

    inlines = (
        ApartmentImageInline,
    )


# =========================================================
# APARTMENT IMAGE ADMIN
# =========================================================

@admin.register(ApartmentImage)
class ApartmentImageAdmin(admin.ModelAdmin):
    list_display = (
        'apartment',
        'title',
        'is_main',
        'created_at',
    )

    list_filter = (
        'is_main',
        'created_at',
    )

    search_fields = (
        'title',
        'description',
        'apartment__title',
        'apartment__district',
        'apartment__address',
    )

    autocomplete_fields = (
        'apartment',
    )

    readonly_fields = (
        'created_at',
    )

    ordering = (
        '-created_at',
    )

    list_per_page = 25

    list_select_related = (
        'apartment',
    )

    fields = (
        'apartment',
        'image',
        'title',
        'description',
        'is_main',
        'created_at',
    )


# =========================================================
# PAYMENT PLAN ADMIN
# =========================================================

@admin.register(PaymentPlan)
class PaymentPlanAdmin(admin.ModelAdmin):
    list_display = (
        'duration_months',
        'min_initial_payment_percent',
        'interest_rate',
        'is_active',
    )

    list_filter = (
        'is_active',
        'duration_months',
    )

    search_fields = (
        'duration_months',
    )

    ordering = (
        'duration_months',
    )

    list_per_page = 25

    fieldsets = (
        (
            '💳 To‘lov rejasi',
            {
                'fields': (
                    'duration_months',
                    'min_initial_payment_percent',
                    'interest_rate',
                    'is_active',
                )
            }
        ),
    )


# =========================================================
# CONTRACT ACTIONS
# =========================================================

@admin.action(description='Tanlangan shartnomalarni tasdiqlash')
def approve_contracts(modeladmin, request, queryset):
    queryset.update(status='approved')


@admin.action(description='Tanlangan shartnomalarni bekor qilish')
def cancel_contracts(modeladmin, request, queryset):
    queryset.update(status='cancelled')


@admin.action(description='Tanlangan shartnomalarni kutish holatiga qaytarish')
def pending_contracts(modeladmin, request, queryset):
    queryset.update(status='pending')


# =========================================================
# CONTRACT ADMIN
# =========================================================

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        'contract_number',
        'client',
        'apartment',
        'payment_plan',
        'initial_payment',
        'monthly_payment',
        'remaining_amount',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'payment_plan',
        'created_at',
    )

    search_fields = (
        'contract_number',
        'client__username',
        'client__phone_number',
        'client__passport_number',
        'apartment__title',
        'apartment__district',
        'apartment__address',
    )

    autocomplete_fields = (
        'client',
        'apartment',
        'payment_plan',
    )

    readonly_fields = (
        'contract_number',
        'monthly_payment',
        'remaining_amount',
        'created_at',
    )

    ordering = (
        '-created_at',
    )

    list_per_page = 25

    date_hierarchy = 'created_at'

    list_select_related = (
        'client',
        'apartment',
        'payment_plan',
    )

    actions = (
        approve_contracts,
        cancel_contracts,
        pending_contracts,
    )

    fieldsets = (
        (
            '📄 Shartnoma',
            {
                'fields': (
                    'contract_number',
                    'status',
                )
            }
        ),

        (
            '👤 Mijoz',
            {
                'fields': (
                    'client',
                )
            }
        ),

        (
            '🏠 Kvartira',
            {
                'fields': (
                    'apartment',
                )
            }
        ),

        (
            '💳 To‘lov rejasi',
            {
                'fields': (
                    'payment_plan',
                )
            }
        ),

        (
            '💰 Moliyaviy maʼlumotlar',
            {
                'fields': (
                    'initial_payment',
                    'monthly_payment',
                    'remaining_amount',
                )
            }
        ),

        (
            '⚙️ Tizim maʼlumotlari',
            {
                'fields': (
                    'created_at',
                )
            }
        ),
    )


# =========================================================
# PAYMENT SCHEDULE ACTIONS
# =========================================================

@admin.action(description='Tanlangan to‘lovlarni "To‘langan" qilish')
def mark_payments_paid(modeladmin, request, queryset):
    queryset.update(
        status='paid',
        paid_at=timezone.now(),
    )


@admin.action(description='Tanlangan to‘lovlarni "Kutilmoqda" qilish')
def mark_payments_pending(modeladmin, request, queryset):
    queryset.update(
        status='pending',
        paid_at=None,
    )


@admin.action(description='Tanlangan to‘lovlarni "Muddati o‘tgan" qilish')
def mark_payments_overdue(modeladmin, request, queryset):
    queryset.update(
        status='overdue',
    )


# =========================================================
# PAYMENT SCHEDULE ADMIN
# =========================================================

@admin.register(PaymentSchedule)
class PaymentScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'contract',
        'month_number',
        'amount',
        'due_date',
        'status',
        'paid_at',
    )

    list_filter = (
        'status',
        'due_date',
        'paid_at',
    )

    search_fields = (
        'contract__contract_number',
        'contract__client__username',
        'contract__client__phone_number',
    )

    autocomplete_fields = (
        'contract',
    )

    readonly_fields = (
        'paid_at',
    )

    ordering = (
        'due_date',
        'month_number',
    )

    list_per_page = 25

    date_hierarchy = 'due_date'

    list_select_related = (
        'contract',
        'contract__client',
    )

    actions = (
        mark_payments_paid,
        mark_payments_pending,
        mark_payments_overdue,
    )

    fieldsets = (
        (
            '📅 To‘lov maʼlumotlari',
            {
                'fields': (
                    'contract',
                    'month_number',
                    'amount',
                    'due_date',
                )
            }
        ),

        (
            '💰 To‘lov holati',
            {
                'fields': (
                    'status',
                    'paid_at',
                )
            }
        ),
    )


# =========================================================
# AUDIT LOG ADMIN
# =========================================================

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'action',
        'model_name',
        'object_id',
        'ip_address',
        'created_at',
    )

    list_filter = (
        'action',
        'model_name',
        'created_at',
    )

    search_fields = (
        'user__username',
        'model_name',
        'object_id',
        'description',
        'ip_address',
    )

    readonly_fields = (
        'user',
        'action',
        'model_name',
        'object_id',
        'description',
        'ip_address',
        'created_at',
    )

    ordering = (
        '-created_at',
    )

    list_per_page = 50

    date_hierarchy = 'created_at'

    list_select_related = (
        'user',
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False