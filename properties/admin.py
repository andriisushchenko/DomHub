from django.contrib import admin
from .models import Category, Agent, Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'agency', 'phone', 'email')


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'deal_type', 'category', 'owner', 'is_active')
    list_filter = ('deal_type', 'is_active', 'category')
    search_fields = ('title', 'address')
    inlines = [PropertyImageInline]


