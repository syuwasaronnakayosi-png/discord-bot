import os
import discord
from discord.ext import commands
from discord import app_commands
from urllib.parse import quote_plus

# ============================
# 🔧 Bot 設定
# ============================
TOKEN = os.getenv("SHUWA_OBO_SYSTEM_BOT_TOKUN")
intents = discord.Intents.default()
intents.members = True  # ロール取得に必要

# command_prefix を追加
bot = commands.Bot(command_prefix="!", intents=intents)

# ============================
# 🔧 Googleフォーム設定
# ============================
FORM_BASE = os.getenv("FORM_BASE")

# Googleフォームの項目ID（entry.xxxxx）
ENTRY_NAME = "entry.1650814136"   # お名前
ENTRY_CLASS = "entry.1210829640"  # クラス

# ============================
# 📌 クラス（ロール）自動判定 
# ※複数ロール設定無いよね？（確認）
# ============================
def detect_class(member: discord.Member):
    role_names = [role.name for role in member.roles]

    if "初級" in role_names:
        return "初級"
    elif "中級" in role_names:
        return "中級"
    elif "上級" in role_names:
        return "上級"
    else:
        return ""


# ============================
# 📌 Bot 起動時
# ============================
@bot.event
async def on_ready():
    print(f"ログインしました: {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"スラッシュコマンド同期完了: {len(synced)}")
    except Exception as e:
        print(e)


# ============================
# 📌 /応募する コマンド
# ============================
@bot.tree.command(name="応募する", description="手話教室の応募フォームを開きます！")
async def apply(interaction: discord.Interaction):

    # Discord名（表示名）
    discord_name = interaction.user.display_name

    # クラス（ロールから自動判定）
    user_class = detect_class(interaction.user)

    # Googleフォームの事前入力URL生成
    url = (
        f"{FORM_BASE}?usp=pp_url"
        f"&{ENTRY_NAME}={quote_plus(discord_name)}"
        f"&{ENTRY_CLASS}={quote_plus(user_class)}"
    )

    await interaction.response.send_message(
        f"**{interaction.user.mention} さんの手話教室応募フォームはこちらです！**\n{url}",
        ephemeral=True
    )


# ============================
# 🚀 Bot 起動
# ============================
bot.run(TOKEN)
