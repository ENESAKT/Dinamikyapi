from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from faker import Faker
import random

class Command(BaseCommand):
    help = '20 adet fake kullanıcı oluştur'

    def handle(self, *args, **options):
        self.stdout.write('👥 Fake kullanıcılar oluşturuluyor...')
        
        # Faker'ı Türkçe olarak ayarla
        fake = Faker(['tr_TR'])
        
        # Kullanıcı gruplarını al
        try:
            il_sorumlusu_group = Group.objects.get(name='İl Sorumlusu')
        except Group.DoesNotExist:
            il_sorumlusu_group = Group.objects.create(name='İl Sorumlusu')
        
        # Normal kullanıcı grubu
        normal_user_group, created = Group.objects.get_or_create(name='Normal Kullanıcı')
        
        # Kullanıcı rolleri
        roles = ['İl Sorumlusu', 'Normal Kullanıcı', 'Veri Girişçisi', 'Rapor Sorumlusu']
        
        created_users = []
        
        for i in range(20):
            # Fake veriler oluştur
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"{first_name.lower()}{last_name.lower()}{random.randint(100, 999)}"
            email = fake.email()
            password = f"pass{random.randint(1000, 9999)}"
            
            # Kullanıcı zaten var mı kontrol et
            if User.objects.filter(username=username).exists():
                username = f"{username}{random.randint(1000, 9999)}"
            
            # Rastgele rol seç
            role = random.choice(roles)
            
            # Kullanıcı oluştur
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_staff=role in ['İl Sorumlusu', 'Rapor Sorumlusu'],
                is_superuser=False
            )
            
            # Gruba ekle
            if role == 'İl Sorumlusu':
                user.groups.add(il_sorumlusu_group)
            else:
                user.groups.add(normal_user_group)
            
            created_users.append({
                'username': username,
                'password': password,
                'role': role,
                'email': email
            })
            
            self.stdout.write(f'  ✅ {username} kullanıcısı oluşturuldu (Şifre: {password}, Rol: {role})')
        
        self.stdout.write('')
        self.stdout.write('✅ Fake kullanıcılar başarıyla oluşturuldu!')
        self.stdout.write(f'📊 Toplam {len(created_users)} yeni kullanıcı eklendi.')
        self.stdout.write('')
        self.stdout.write('🔑 Oluşturulan Kullanıcılar:')
        for user_info in created_users:
            self.stdout.write(f'   - {user_info["username"]} (Şifre: {user_info["password"]}, Rol: {user_info["role"]})')
        self.stdout.write('')
        self.stdout.write('👑 Admin Kullanıcı:')
        self.stdout.write('   - Kullanıcı adı: admin')
        self.stdout.write('   - Şifre: admin123')
        self.stdout.write('   - Yetki: Süper Kullanıcı')
