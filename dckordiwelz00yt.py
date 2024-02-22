import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Kordinatları tutmak için boş bir sözlük
hesaplar = {}


# Dosyadan kordinatları okuma
def verileri_oku(dosya_adı):
  with open(dosya_adı, 'r') as dosya:
    hesap_adi = None
    for satir in dosya:
      satir = satir.strip().split()
      if len(satir) == 1:
        hesap_adi = satir[0]
        hesaplar[hesap_adi] = {}
      elif len(satir) == 3:
        dunya, x, z = satir
        hesaplar[hesap_adi][dunya] = {"x": int(x), "z": int(z)}


# En yakın hesabı bulma
def en_yakin_hesap(dunya, x, z):
  en_kucuk_mesafe = float('inf')
  en_yakin_hesap = None
  for hesap, dunya_koordinatlari in hesaplar.items():
    koordinatlar = dunya_koordinatlari.get(dunya)
    if koordinatlar:
      mesafe = abs(koordinatlar['x'] - x) + abs(koordinatlar['z'] - z)
      if mesafe < en_kucuk_mesafe:
        en_kucuk_mesafe = mesafe
        en_yakin_hesap = hesap
  return en_yakin_hesap, en_kucuk_mesafe


# Bot hazır olduğunda yapılandırma
@bot.event
async def on_ready():
  print(f'{bot.user.name} olarak giriş yapıldı!')


# !kordinat komutu
@bot.command()
async def kordinat(ctx):
  await ctx.send("# X kordinatını girin:")
  x_koordinati = await bot.wait_for(
      'message', check=lambda message: message.author == ctx.author)
  x_koordinati = int(x_koordinati.content)

  await ctx.send("# Z kordinatını girin:")
  z_koordinati = await bot.wait_for(
      'message', check=lambda message: message.author == ctx.author)
  z_koordinati = int(z_koordinati.content)

  await ctx.send("# Dünya ismini girin:")
  dunya = await bot.wait_for(
      'message', check=lambda message: message.author == ctx.author)
  dunya = dunya.content.lower()

  hesap, mesafe = en_yakin_hesap(dunya, x_koordinati, z_koordinati)
  mesaj = (
      f"**{dunya.capitalize()}** dünyasında **X: {x_koordinati}** **Z: {z_koordinati}** en yakın hesap **{hesap}** hesabı, "
      f"__X kordinatı yakınlığı__ {abs(x_koordinati - hesaplar[hesap][dunya]['x'])} __Z kordinatı yakınlığı__ {abs(z_koordinati - hesaplar[hesap][dunya]['z'])} ve toplam olarak **{int(mesafe)}** blok uzaklıkta."
  )
  await ctx.send(mesaj)


# Belirli bir kanaldan gelen mesajları kontrol etme
@bot.event
async def on_message(message):
  if message.channel.id == 1208676101803745310:  # Sadece belirli bir kanalın ID'si
    await bot.process_commands(message)


# Botu çalıştırma
dosya_adi = "kordinatlar.txt"
verileri_oku(dosya_adi)
bot.run(
    'MTIwMjg5MDE1MjY4MzUxMTg4OA.GanXp8.S1U61cD6i_uDnqL0gr0asPStZszeTxZ0lVLfII'
)  # Buraya botunuzun tokenini eklemelisiniz
