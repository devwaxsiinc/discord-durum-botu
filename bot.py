import discord
from discord.ext import commands
import os

# --- AYARLAR ---
# Koyeb'de Environment Variables kısmına "BOT_TOKEN" isminde ekle.
TOKEN = os.getenv('BOT_TOKEN') or 'BURAYA_TOKENINI_YAZABILIRSIN'

HEDEF_DURUM = ".gg/E6BPFM6GRY" 
ROL_ID = 1438232938629300324    
LOG_KANAL_ID = 1456242599089406025 
# ---------------

# Tüm izinleri (Intents) açıyoruz
intents = discord.Intents.default()
intents.presences = True      # Durumları takip etmek için
intents.members = True        # Rol vermek ve üyeleri tanımak için
intents.message_content = True 

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    # --- İSTEDİĞİN GÖRSELDEKİ DURUM AYARI ---
    # Botun kendisi de Rahatsız Etmeyin modunda ve taçlı görünür
    custom_status = discord.CustomActivity(name="👑 .gg/E6BPFM6GRY")
    await bot.change_presence(status=discord.Status.dnd, activity=custom_status)
    
    print(f'📢 Bot {bot.user} olarak başarıyla bağlandı!')
    print(f'🔍 Takip edilen kelime: {HEDEF_DURUM}')
    print(f'🚀 Botun durumu ayarlandı: 👑 .gg/E6BPFM6GRY')

@bot.event
async def on_presence_update(before, after):
    guild = after.guild
    if guild is None:
        return

    role = guild.get_role(ROL_ID)
    log_channel = bot.get_channel(LOG_KANAL_ID)

    if not role:
        return

    has_status = False
    for activity in after.activities:
        if isinstance(activity, discord.CustomActivity):
            status_text = ""
            if activity.name:
                status_text += activity.name
            if activity.state:
                status_text += activity.state
            
            if HEDEF_DURUM in status_text:
                has_status = True
                break

    try:
        if has_status:
            if role not in after.roles:
                await after.add_roles(role)
                print(f"✅ {after} durumuna ekledi, rol verildi.")
        else:
            if role in after.roles:
                await after.remove_roles(role)
                print(f"❌ {after} durumdan sildi, rol alındı.")
                if log_channel:
                    await log_channel.send(f"{after.mention} durum fix")
    except discord.Forbidden:
        print(f"⚠️ HATA: Botun rolü yetersiz!")
    except Exception as e:
        print(f"⚠️ Bir hata oluştu: {e}")

if __name__ == "__main__":
    bot.run(TOKEN)
