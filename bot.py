import discord
from discord.ext import commands
import os

# --- AYARLAR ---
# Koyeb kullanıyorsan TOKEN kısmını 'os.getenv' ile bırak, paneldin ayarla.
# Eğer bilgisayarda deneyeceksen tırnak içine tokenini yazabilirsin.
TOKEN = os.getenv('BOT_TOKEN') or 'BURAYA_TOKENINI_YAZABILIRSIN'

HEDEF_DURUM = ".gg/E6BPFM6GRY" 
ROL_ID = 1438232938629300324    
LOG_KANAL_ID = 1456242599089406025 
# ---------------

# Tüm izinleri (Intents) açıyoruz
intents = discord.Intents.default()
intents.presences = True      # Durumları takip etmek için
intents.members = True        # Rol vermek ve üyeleri tanımak için
intents.message_content = True # Başlangıçtaki uyarı hatasını almamak için

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f'📢 Bot {bot.user} olarak başarıyla bağlandı!')
    print(f'🔍 Takip edilen kelime: {HEDEF_DURUM}')

@bot.event
async def on_presence_update(before, after):
    # Botun bir sunucu içinde olup olmadığını kontrol edelim
    guild = after.guild
    if guild is None:
        return

    role = guild.get_role(ROL_ID)
    log_channel = bot.get_channel(LOG_KANAL_ID)

    # Rol veya kanal bulunamazsa hata vermemesi için kontrol
    if not role:
        return

    # Kullanıcının yeni durumunda hedef metin var mı?
    has_status = False
    for activity in after.activities:
        if isinstance(activity, discord.CustomActivity):
            # activity.name bazen None dönebilir, o yüzden kontrol ediyoruz
            status_text = ""
            if activity.name:
                status_text += activity.name
            if activity.state:
                status_text += activity.state
            
            if HEDEF_DURUM in status_text:
                has_status = True
                break

    # Rol İşlemleri
    try:
        if has_status:
            # Durumunda yazı var ve rolü yoksa rolü ver
            if role not in after.roles:
                await after.add_roles(role)
                print(f"✅ {after} durumuna ekledi, rol verildi.")
        else:
            # Durumunda yazı YOK ama rolü VARSA rolü al ve mesaj at
            if role in after.roles:
                await after.remove_roles(role)
                print(f"❌ {after} durumdan sildi, rol alındı.")
                if log_channel:
                    await log_channel.send(f"{after.mention} durum fix")
    except discord.Forbidden:
        print(f"⚠️ HATA: {after.name} kullanıcısına rol verme yetkim yok! Botun rolü yukarıda olmalı.")
    except Exception as e:
        print(f"⚠️ Bir hata oluştu: {e}")

bot.run(TOKEN)