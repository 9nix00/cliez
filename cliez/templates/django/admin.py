# -*- coding: utf-8 -*-

from . import models
from django.contrib import admin


# from django.shortcuts import get_object_or_404
# from django.core.urlresolvers import reverse_lazy, reverse
# from django.contrib.admin import SimpleListFilter
# from django.http import HttpResponseForbidden


# class StatusFilter(SimpleListFilter):
#     title = 'title'
#     parameter_name = 'url_param_name'
#
#     def lookups(self, request, model_admin):
#         return [('yes', 'YES'), ('no', 'no')]
#
#     def queryset(self, request, queryset):
#         value = self.value()
#         qs = queryset
#
#         if value == 'yes':
#             qs = queryset
#         elif value == 'no':
#             qs = queryset
#
#         return qs


# class DetailInline(admin.TabularInline):
#     model = ''
#     extra = 0
#     readonly_fields = []
#
#     def __str__(self):
#         return str(self.id)
#
#
#     pass


# @admin.register(models.Model)
# class TicketAdmin(admin.ModelAdmin):
#     list_display = ('id',)
#     list_filter = [StatusFilter, ]
#
#     search_fields = []
#     readonly_fields = []
#
#     fieldsets = (
#         (None, {'fields': ('',)
#                 }),
#         ('section1', {
#             'fields': ('',),
#         }),
#         ('section2', {
#             'fields': ('',),
#         }),
#     )
#
#     inlines = [DetailInline]
#
#     def __str__(self):
#         return str(self.id)
#
#     pass
