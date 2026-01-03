import discord
from discord.ext import commands
import json
import os

# Config dosyasını oku
with open('config.json', 'r') as f:
    config = json.load(f)

class StatusBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="/",
            intents=discord.Intents.default()
        )

    async def on_ready(self):
        # GÖRSELDEKİ DURUMU AYARLA
        # discord.Status.dnd -> Rahatsız Etmeyin (Kırmızı)
        # CustomActivity -> Özel yazı ve emoji
        custom_activity = discord.CustomActivity(name="👑.gg/E6BPFM6GRY")
        
        await self.change_presence(
            status=discord.Status.dnd, 
            activity=custom_activity
        )
        
        print(f"✅ Durum Ayarlandı: {self.user.name}")
        print(f"🚀 Mevcut Durum: 👑 .gg/E6BPFM6GRY")

bot = StatusBot()

# Tokeni hem config'den hem de Koyeb'den alabilir
TOKEN = config.get("token") or os.getenv("TOKEN")

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ HATA: Token bulunamadı!")