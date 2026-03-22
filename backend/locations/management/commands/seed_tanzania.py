from django.core.management.base import BaseCommand
from locations.models import Region, District, Ward


class Command(BaseCommand):
    help = "Seed Tanzania Regions, Districts, Wards"

    def handle(self, *args, **kwargs):

        data = {
            "Dar es Salaam": {
                "Ilala": ["Upanga", "Kariakoo", "Buguruni"],
                "Kinondoni": ["Kawe", "Mikocheni", "Sinza"],
                "Temeke": ["Mbagala", "Kurasini", "Chang'ombe"]
            },
            "Arusha": {
                "Arusha Urban": ["Sombetini", "Sekei"],
                "Arusha Rural": ["Usa River", "Nkoaranga"]
            }
        }

        for region_name, districts in data.items():
            region, _ = Region.objects.get_or_create(name=region_name)

            for district_name, wards in districts.items():
                district, _ = District.objects.get_or_create(
                    name=district_name,
                    region=region
                )

                for ward_name in wards:
                    Ward.objects.get_or_create(
                        name=ward_name,
                        district=district
                    )

        self.stdout.write(self.style.SUCCESS("Data seeded successfully"))