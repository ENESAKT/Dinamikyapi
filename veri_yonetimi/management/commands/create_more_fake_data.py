from django.core.management.base import BaseCommand
from veri_yonetimi.models import Sütun, AnaVeri, VeriDeger
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Daha fazla fake veri ekle'

    def handle(self, *args, **options):
        self.stdout.write('📊 Daha fazla fake veri ekleniyor...')
        
        # Faker'ı Türkçe olarak ayarla
        fake = Faker(['tr_TR'])
        
        # Mevcut sütunları al
        existing_columns = list(Sütun.objects.all())
        
        # Yeni sütunlar oluştur
        new_columns_data = [
            {'ad': 'Telefon', 'tip': 'dinamik', 'sıra': 6},
            {'ad': 'Adres', 'tip': 'dinamik', 'sıra': 7},
            {'ad': 'E-posta', 'tip': 'dinamik', 'sıra': 8},
            {'ad': 'Durum', 'tip': 'dinamik', 'sıra': 9},
            {'ad': 'Notlar', 'tip': 'dinamik', 'sıra': 10},
            {'ad': 'Son Güncelleme', 'tip': 'dinamik', 'sıra': 11},
            {'ad': 'Sorumlu Kişi', 'tip': 'dinamik', 'sıra': 12},
            {'ad': 'Bütçe', 'tip': 'dinamik', 'sıra': 13},
            {'ad': 'Öncelik', 'tip': 'dinamik', 'sıra': 14},
            {'ad': 'Tamamlanma Tarihi', 'tip': 'dinamik', 'sıra': 15},
        ]
        
        created_columns = []
        for col_data in new_columns_data:
            column, created = Sütun.objects.get_or_create(
                ad=col_data['ad'],
                defaults={
                    'tip': col_data['tip'],
                    'sıra': col_data['sıra'],
                    'aktif': True
                }
            )
            if created:
                created_columns.append(column)
                self.stdout.write(f'  ✅ {column.ad} sütunu oluşturuldu')
        
        # Mevcut verilere yeni değerler ekle
        ana_veriler = AnaVeri.objects.all()
        status_options = ['Aktif', 'Pasif', 'Beklemede', 'Tamamlandı', 'İptal']
        priority_options = ['Düşük', 'Orta', 'Yüksek', 'Acil']
        
        updated_count = 0
        for ana_veri in ana_veriler:
            for column in created_columns:
                # Sütun tipine göre fake veri oluştur
                if column.ad == 'Telefon':
                    value = fake.phone_number()
                elif column.ad == 'Adres':
                    value = fake.address()
                elif column.ad == 'E-posta':
                    value = fake.email()
                elif column.ad == 'Durum':
                    value = random.choice(status_options)
                elif column.ad == 'Notlar':
                    value = fake.text(max_nb_chars=100)
                elif column.ad == 'Son Güncelleme':
                    value = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M')
                elif column.ad == 'Sorumlu Kişi':
                    value = fake.name()
                elif column.ad == 'Bütçe':
                    value = f"{random.randint(10000, 500000)} TL"
                elif column.ad == 'Öncelik':
                    value = random.choice(priority_options)
                elif column.ad == 'Tamamlanma Tarihi':
                    value = fake.future_date().strftime('%Y-%m-%d')
                else:
                    value = fake.text(max_nb_chars=50)
                
                # Veri değeri oluştur
                veri_deger, created = VeriDeger.objects.get_or_create(
                    ana_veri=ana_veri,
                    sutun=column,
                    defaults={'deger': value}
                )
                
                if created:
                    updated_count += 1
        
        self.stdout.write('')
        self.stdout.write('✅ Daha fazla fake veri başarıyla eklendi!')
        self.stdout.write(f'📊 Toplam {len(created_columns)} yeni sütun oluşturuldu')
        self.stdout.write(f'📊 Toplam {updated_count} yeni veri değeri eklendi')
        self.stdout.write('')
        self.stdout.write('📋 Yeni Sütunlar:')
        for column in created_columns:
            self.stdout.write(f'   - {column.ad} (Sıra: {column.sıra})')
