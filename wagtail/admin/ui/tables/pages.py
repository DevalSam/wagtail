from django.utils.safestring import mark_safe
from django.utils.translation import gettext

from wagtail.admin.ui.tables import BaseColumn, BulkActionsCheckboxColumn, Column, Table


class PageTitleColumn(BaseColumn):
    cell_template_name = "wagtailadmin/pages/listing/_page_title_cell.html"

    def __init__(self, *args, show_locale_labels=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.show_locale_labels = show_locale_labels

    def get_cell_context_data(self, instance, parent_context):
        context = super().get_cell_context_data(instance, parent_context)
        context["page_perms"] = instance.permissions_for_user(
            parent_context["request"].user
        )
        context["show_locale_labels"] = self.show_locale_labels
        return context


class ParentPageColumn(Column):
    cell_template_name = "wagtailadmin/pages/listing/_parent_page_cell.html"

    def get_value(self, instance):
        return instance.get_parent()


class PageStatusColumn(BaseColumn):
    cell_template_name = "wagtailadmin/pages/listing/_page_status_cell.html"


class BulkActionsColumn(BulkActionsCheckboxColumn):
    def get_header_context_data(self, parent_context):
        context = super().get_header_context_data(parent_context)
        parent_page = parent_context.get("parent_page")
        if parent_page:
            context["parent"] = parent_page.id
        return context

    def get_cell_context_data(self, instance, parent_context):
        context = super().get_cell_context_data(instance, parent_context)
        context.update(
            {
                "obj_type": "page",
                "aria_labelledby_prefix": "page_",
                "aria_labelledby": str(instance.pk),
                "aria_labelledby_suffix": "_title",
                "checkbox_aria_label": gettext("Select page"),
            }
        )
        return context


class NavigateToChildrenColumn(BaseColumn):
    cell_template_name = "wagtailadmin/pages/listing/_navigation_explore.html"

    def get_cell_context_data(self, instance, parent_context):
        context = super().get_cell_context_data(instance, parent_context)
        context["page"] = instance
        context["page_perms"] = instance.permissions_for_user(
            parent_context["request"].user
        )
        return context

    def render_header_html(self, parent_context):
        return mark_safe("<th></th>")


class PageTable(Table):
    def get_row_classname(self, instance):
        if not instance.live:
            return "unpublished"
        else:
            return ""
