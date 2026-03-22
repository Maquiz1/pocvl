from django import forms
from herbal.models.queries.query_model import DataQuery


class QueryCreateForm(forms.ModelForm):

    class Meta:

        model = DataQuery

        fields = [
            "field_name",
            "query_text",
        ]


class QueryResponseForm(forms.ModelForm):

    class Meta:

        model = DataQuery

        fields = [
            "response",
        ]