import os
import discord
from discord.ext import commands
import yt_dlp
import traceback

# 1. إعداد البوت والبادئة (يشتغل حصرياً بالنقطة ".")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

# 2. إعدادات تشغيل الصوت (yt-dlp و FFmpeg)
YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

# جلب توكن البوت الجديد من البيئة السحابية
DISCORD_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

@bot.event
async def on_ready():
    print(f'🎵 بوت الموسيقى {bot.user} جاهز وشغال على السحاب يا لورنس!')

# =========================================================
# 🎵 [أوامر الموسيقى - تشغيل وإيقاف]
# =========================================================

@bot.command(name='play')
async def play(ctx, *, url):
    if not ctx.author.voice:
        await ctx.send("اثف.. ادخل روم صوتي أول عشان ألحقك (ꏿ﹏ꏿ;)")
        return
    
    vc = ctx.voice_client
    if not vc:
        vc = await ctx.author.voice.channel.connect()

    async with ctx.typing():
        try:
            info = ytdl.extract_info(url, download=False)
            url_sound = info['url']
            vc.play(discord.FFmpegPCMAudio(url_sound, **FFMPEG_OPTIONS))
            await ctx.send(f"أبشر.. جالس أشغل الحين: **{info['title']}** 🎵")
        except Exception as e:
            traceback.print_exc()
            await ctx.send("صار خطأ وأنا أحاول أشغل الرابط ⁦(⁠ꏿ⁠﹏⁠ꏿ⁠;⁠)⁩")

@bot.command(name='stop')
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("حاضر، سكتنا عشان الهدوء 🍃")

# =========================================================
# 🔨 [أمر الطرد الصوتي السريع للأعضاء]
# =========================================================

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # إذا كتبت أنت (أوتوسان) كلمة "اطرد" ومنشنت الشخص
    if message.author.id == 893471909952516188 and "اطرد" in message.content and message.mentions:
        for target in message.mentions:
            if target.voice:
                await target.move_to(None) # يفصله من الروم الصوتي فوراً
        await message.channel.send("اثف.. بابا قال الكلب ذا ما يستاهل يجلس معنا ⁦ミ⁠●⁠﹏⁠☉⁠ミ⁩")
        return

    # تمرير الأوامر العادية (.play / .stop)
    await bot.process_commands(message)
  
