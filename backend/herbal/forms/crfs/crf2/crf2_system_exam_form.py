# from django import forms
# from herbal.models.crfs.crf2.crf2_model import CRF2

# class CRF2SystemExamForm(forms.ModelForm):
#     class Meta:
#         model = CRF2
#         fields = [
#             "appearance", "appearance_comments", "appearance_signifcnt",
#             "heent", "heent_comments", "heent_signifcnt",
#             "respiratory", "respiratory_comments", "respiratory_signifcnt",
#             "cardiovascular", "cardiovascular_comments", "cardiovascular_signifcnt",
#             "abdominal", "abdominal_comments", "abdominal_signifcnt",
#             "neurological", "neurological_comments", "neurological_signifcnt",
#         ]

#         widgets = {
#             field: forms.Select(attrs={"class": "form-control"})
#             for field in [
#                 "appearance", "appearance_signifcnt",
#                 "heent", "heent_signifcnt",
#                 "respiratory", "respiratory_signifcnt",
#                 "cardiovascular", "cardiovascular_signifcnt",
#                 "abdominal", "abdominal_signifcnt",
#                 "neurological", "neurological_signifcnt",
#             ]
#         }

#         widgets.update({
#             f"{f}_comments": forms.Textarea(attrs={"class": "form-control", "rows": 2})
#             for f in [
#                 "appearance", "heent", "respiratory",
#                 "cardiovascular", "abdominal", "neurological"
#             ]
#         })