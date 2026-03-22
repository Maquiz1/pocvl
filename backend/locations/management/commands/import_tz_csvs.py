import os
import csv

from django.core.management.base import BaseCommand
from locations.models import Region, District, Ward, Street


# def clean(name):
#     return name.strip().title()

def clean(name):
    if not name:
        return None
    return name.strip().title()

class Command(BaseCommand):
    help = "Import full Tanzania dataset (with codes)"

    def handle(self, *args, **kwargs):

        base_path = "data/regions"

        region_map = {}
        district_map = {}

        for file_name in os.listdir(base_path):

            if not file_name.endswith(".csv"):
                continue

            file_path = os.path.join(base_path, file_name)

            self.stdout.write(f"Processing {file_name}...")

            with open(file_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                # ✅ Normalize headers
                reader.fieldnames = [f.strip().lower() for f in reader.fieldnames]

                for row in reader:

                    # ✅ Extract values safely
                    region_name = clean(row.get("region"))
                    district_name = clean(row.get("district"))
                    ward_name = clean(row.get("ward"))

                    # ✅ Handle optional codes (may not exist)
                    region_code = row.get("regioncode") or row.get("postcode")
                    district_code = row.get("districtcode")
                    ward_code = row.get("wardcode")

                    # -------------------
                    # REGION
                    # -------------------
                    if region_name not in region_map:
                        region, _ = Region.objects.get_or_create(
                            name=region_name,
                            defaults={"code": region_code}
                        )
                        region_map[region_name] = region

                    # -------------------
                    # DISTRICT
                    # -------------------
                    district_key = (region_name, district_name)

                    if district_key not in district_map:
                        district, _ = District.objects.get_or_create(
                            name=district_name,
                            region=region_map[region_name],
                            defaults={"code": district_code}
                        )
                        district_map[district_key] = district

                    # -------------------
                    # WARD
                    # -------------------
                    ward_obj, _ = Ward.objects.get_or_create(
                        name=ward_name,
                        district=district_map[district_key],
                        defaults={"code": ward_code}
                    )

                    # 👉 ADD THIS (street import)
                    street_name = clean(row.get("street"))

                    if street_name:
                        Street.objects.get_or_create(
                            name=street_name,
                            ward=ward_obj
    )

        self.stdout.write(self.style.SUCCESS("✅ Full Tanzania dataset imported!"))