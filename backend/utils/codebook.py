from django.db import models

EXCLUDED_FIELDS = {
    "id",
    "created_at",
    "updated_at",
    "created_by",
    "updated_by",
    "deleted_at",
    "deleted_by",
    "is_active",
    "is_deleted",
    "delete_reason",
    "inclusion_criteria_met",
    "exclusion_criteria_met",
    "cancer_types",
    "after_visit",
    "crf",
    "crf2",
    "ae_staff",
    "clinician_name",
    "cpersid",
    "region",
    "district",
    "ward",
    "subject",
    "screening",
    "enrollment",
    "visit",
}


def get_model_codebook(model):
    codebook = []

    for field in model._meta.get_fields():

        # ✅ only real fields
        if not isinstance(field, models.Field):
            continue

        # ✅ exclude unwanted
        if field.name in EXCLUDED_FIELDS:
            continue

        field_name = field.name
        field_type = field.get_internal_type()
        label = getattr(field, "verbose_name", field_name)
        required = not getattr(field, "blank", True)

        base_row = {
            "field_name": field_name,
            "label": str(label),
            "type": field_type,
            "required": required,
        }

        # =========================
        # ✅ FOREIGN KEYS → MULTIPLE ROWS
        # =========================
        if isinstance(field, models.ForeignKey):

            related_model = field.related_model

            try:
                queryset = related_model.objects.all()

                for obj in queryset:
                    display = (
                        getattr(obj, "label", None)
                        or getattr(obj, "name", None)
                        or getattr(obj, "code", None)
                        or str(obj)
                    )

                    codebook.append({
                        **base_row,
                        "choice_code": obj.pk,
                        "choice_label": display,
                    })

            except Exception as e:
                codebook.append({
                    **base_row,
                    "choice_code": "",
                    "choice_label": f"Error: {str(e)}",
                })

        # =========================
        # ✅ DJANGO CHOICES → MULTIPLE ROWS
        # =========================
        elif field.choices:

            for c in field.choices:
                codebook.append({
                    **base_row,
                    "choice_code": c[0],
                    "choice_label": c[1],
                })

        # =========================
        # ✅ NORMAL FIELD → SINGLE ROW
        # =========================
        else:
            codebook.append({
                **base_row,
                "choice_code": "",
                "choice_label": "",
            })

    return codebook