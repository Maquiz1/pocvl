from django import forms
from herbal.models import Subject
from locations.models import Region, District, Ward
import re


def normalize_tz_phone(phone):
    """Normalize Tanzanian phone number to 255XXXXXXXXX format"""
    if not phone:
        return phone

    # Remove spaces, dashes, etc.
    phone = re.sub(r"\D", "", phone)

    # Normalize
    if phone.startswith("0"):
        phone = "255" + phone[1:]
    elif phone.startswith("255"):
        pass
    elif phone.startswith("+" ):
        phone = phone[1:]
    
    return phone


def is_valid_tz_phone(phone):
    """Validate normalized TZ number"""
    return re.fullmatch(r"255\d{9}", phone)

class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject

        exclude = ["subject_id", "site"]  # auto + calculated

        labels={
            "reg_date":"Registration Date",
            "dob":"Date of Birth",
            "sex":"Sex",
            "hid":"Hospital ID",
            "idn":"ID Number",
            "other_id":"Other Identification",
        }
        widgets = {
            "reg_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "dob": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "age": forms.NumberInput(attrs={"class": "form-control"}),

            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "middle_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),

            "sex": forms.Select(attrs={"class": "form-control"}),
            "identification_type": forms.Select(attrs={"class": "form-control"}),
            "other_id": forms.TextInput(attrs={"class": "form-control"}),
            "marital_status": forms.Select(attrs={"class": "form-control"}),
            "education_level": forms.Select(attrs={"class": "form-control"}),
            "occupation": forms.Select(attrs={"class": "form-control"}),
            "other_occupation": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Specify occupation"
            }),
            "hid": forms.TextInput(attrs={"class": "form-control"}),
            "idn": forms.TextInput(attrs={"class": "form-control"}),

            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "other_phone": forms.TextInput(attrs={"class": "form-control"}),

            "street": forms.TextInput(attrs={"class": "form-control"}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),

            # Select2 fields
            "region": forms.Select(attrs={"class": "form-control", "id": "region"}),
            "district": forms.Select(attrs={"class": "form-control", "id": "district"}),
            "ward": forms.Select(attrs={"class": "form-control", "id": "ward"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ✅ Define required fields
        required_fields = [
            "reg_date", "sex", "first_name",  "last_name","marital_status",
            "phone_number", "region", "district","ward","occupation","education_level"
        ]
        
        # optional_fields = ["dob","middle_name", "other_phone","ward", "remarks"]

        for field in required_fields:
            self.fields[field].required = True
            
        # for field in optional_fields:
        #     self.fields[field].required = False
    
        # AJAX-controlled fields
        self.fields["region"].queryset = Region.objects.none()
        self.fields["district"].queryset = District.objects.none()
        self.fields["ward"].queryset = Ward.objects.none()

        # FIX for POST (validation)
        if self.data:
            region_id = self.data.get("region")
            district_id = self.data.get("district")

            if region_id:
                self.fields["region"].queryset = Region.objects.filter(id=region_id)
                self.fields["district"].queryset = District.objects.filter(region_id=region_id)

            if district_id:
                self.fields["ward"].queryset = Ward.objects.filter(district_id=district_id)

        # FIX for edit mode
        elif self.instance.pk:
            if self.instance.region:
                self.fields["region"].queryset = Region.objects.filter(id=self.instance.region_id)
                self.fields["district"].queryset = District.objects.filter(region=self.instance.region)

            if self.instance.district:
                self.fields["ward"].queryset = Ward.objects.filter(district=self.instance.district)
                
    def clean(self):
        cleaned_data = super().clean()

        # AGE VALIDATIONS 
        dob = cleaned_data.get("dob")
        reg_date = cleaned_data.get("reg_date")
        age = cleaned_data.get("age")

        occupation = cleaned_data.get("occupation")
        other = cleaned_data.get("other_occupation")

        identification_type = cleaned_data.get("identification_type")
        other_id = cleaned_data.get("other_id")

        # ✅ Require at least one
        if not dob and not age:
            self.add_error("dob", "Provide either Date of Birth or Age.")
            self.add_error("age", "Provide either Date of Birth or Age.")
        
        # ✅ Calculate age using REG DATE
        if dob and reg_date:
            calculated_age = reg_date.year - dob.year - (
                (reg_date.month, reg_date.day) < (dob.month, dob.day)
            )

            # Validate age range
            if calculated_age < 18:
                self.add_error("dob", "Subject must be at least 18 years old at registration.")

            if calculated_age > 120:
                self.add_error("dob", "Age cannot exceed 120 years at registration.")

            # Optional: enforce consistency with entered age
            if age is not None and abs(age - calculated_age) > 1:
                self.add_error("age", f"Age should be approximately {calculated_age} based on DOB and registration date.")
                

        # OCCOPATION
        if occupation and occupation.id == 3 and not other:
            self.add_error("other_occupation", "Please specify occupation")

        # IDENTIFICATIONS
        if identification_type and identification_type.id == 3 and not other_id:
            self.add_error("other_id", "Please specify other identification")

        return cleaned_data
    
    def clean_age(self):
        age = self.cleaned_data.get("age")

        if age is not None:
            if age < 18:
                raise forms.ValidationError("Subject must be at least 18 years old.")
            if age > 120:
                raise forms.ValidationError("Age cannot be greater than 120.")

        return age
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")

        if phone:
            phone = normalize_tz_phone(phone)

            if not is_valid_tz_phone(phone):
                raise forms.ValidationError(
                    "Enter a valid phone number (e.g. 0712345678, +255712345678)."
                )

            # ✅ uniqueness check
            qs = Subject.objects.filter(phone_number=phone)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError("This phone number is already registered.")

        return phone

    def clean_other_phone(self):
        phone = self.cleaned_data.get("other_phone")

        if phone:
            phone = normalize_tz_phone(phone)

            if not is_valid_tz_phone(phone):
                raise forms.ValidationError(
                    "Enter a valid phone number (e.g. 0712345678, +255712345678)."
                )
                
            # ✅ uniqueness check
            qs = Subject.objects.filter(other_phone=phone)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError("This other phone number is already registered.")

        return phone