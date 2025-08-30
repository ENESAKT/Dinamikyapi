from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from veri_yonetimi.models import Sütun, AnaVeri, VeriDeger

class Command(BaseCommand):
    help = 'Add test data to the database'

    def handle(self, *args, **options):
        self.stdout.write('🧪 Adding test data...')
        
        # Get admin user
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            self.stdout.write(self.style.ERROR('❌ No admin user found!'))
            return
        
        # Get active columns
        aktif_sutunlar = Sütun.objects.filter(aktif=True).order_by('sıra')
        if not aktif_sutunlar.exists():
            self.stdout.write(self.style.ERROR('❌ No active columns found!'))
            return
        
        self.stdout.write(f'Using columns: {[s.ad for s in aktif_sutunlar]}')
        
        # Sample data
        test_cities = ['Ankara', 'İstanbul', 'İzmir', 'Bursa', 'Antalya']
        
        for i, city in enumerate(test_cities, 1):
            try:
                # Create AnaVeri instance
                ana_veri = AnaVeri.objects.create(
                    il_adi=city,
                    kurulacak_cihaz_sayisi=100 + (i * 10),
                    kurulan_cihaz_sayisi=50 + (i * 5),
                    arizali_cihaz_sayisi=5 + i
                )
                
                # Create VeriDeger instances for dynamic columns
                for sutun in aktif_sutunlar:
                    if sutun.tip not in ['kurulacak', 'kurulan', 'arizali', 'tamamlanma']:
                        VeriDeger.objects.create(
                            ana_veri=ana_veri,
                            sutun=sutun,
                            deger=f'Test_{sutun.ad}_{i}'
                        )
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Created test data for {city} (ID: {ana_veri.id})')
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error creating data for {city}: {e}')
                )
        
        total_records = AnaVeri.objects.count()
        self.stdout.write(f'\\n📊 Total AnaVeri records: {total_records}')