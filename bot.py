import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# 🔧 إعدادات البوت
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8200504499:AAFxKfMV6ioudGs1FQJ_ndhvhP8lOMBCFi8')
OWNER_ID = 7614032958

# ⚙️ إعدادات التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class WerewolfBot:
    def __init__(self):
        self.active_games = {}
        logger.info("🎮 بوت الذئب initiated")

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """🎯 أمر /start الرئيسي"""
        user = update.effective_user
        
        welcome_text = f"""
🌟 أهلاً بك {user.first_name} في بوت الذئب! 🌟

🤖 أنا بوت مخصص لإدارة لعبة الذئب في القنوات

👑 المالك: @lYXX5

🎮 **طريقة اللعب السهلة:**
1. بدء لعبة جديدة
2. اختيار القناة
3. مشاركة الرابط
4. اللعب مع الأصدقاء

👇 اختر من الأزرار:
        """
        
        keyboard = [
            [InlineKeyboardButton("🎮 بدء لعبة جديدة", callback_data="start_game")],
            [InlineKeyboardButton("📖 كيف ألعب؟", callback_data="how_to_play")],
            [InlineKeyboardButton("📊 الإحصائيات", callback_data="stats")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
        logger.info(f"👤 User {user.id} started the bot")

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """🔄 معالجة الضغط على الأزرار"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        user = query.from_user
        
        logger.info(f"🔘 User {user.id} pressed: {data}")
        
        if data == "start_game":
            await self.start_game_flow(query)
        elif data == "how_to_play":
            await self.show_instructions(query)
        elif data == "stats":
            await self.show_stats(query)
        elif data == "back_main":
            await self.back_to_main(query)
        elif data == "game_channel":
            await self.create_channel_game(query)
        elif data == "game_group":
            await self.create_group_game(query)

    async def start_game_flow(self, query):
        """🚀 بدء تدفق اللعبة"""
        text = """
🎯 **بدء لعبة جديدة**

اختر نوع اللعبة:

📺 **لعبة في قناة** - الأفضل للقنوات العامة
👥 **لعبة في مجموعة** - للمجموعات الخاصة

        """
        
        keyboard = [
            [InlineKeyboardButton("📺 لعبة في قناة", callback_data="game_channel")],
            [InlineKeyboardButton("👥 لعبة في مجموعة", callback_data="game_group")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="back_main")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)

    async def create_channel_game(self, query):
        """📺 إنشاء لعبة في قناة"""
        text = """
📺 **لعبة في قناة**

🎮 جاري إعداد اللعبة للقنوات...

⚠️ **المتطلبات:**
• البوت مضاف في القناة
• لديك صلاحية إدارة الرسائل

🔜 الميزات القادمة:
• إنشاء اللعبة تلقائياً في القناة
• إدارة اللاعبين
• بدء اللعبة عند اكتمال العدد

        """
        
        keyboard = [
            [InlineKeyboardButton("🔄 تحديث", callback_data="game_channel")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="start_game")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)

    async def create_group_game(self, query):
        """👥 إنشاء لعبة في مجموعة"""
        text = """
👥 **لعبة في مجموعة**

🎮 جاري إعداد اللعبة للمجموعات...

⚠️ **المتطلبات:**
• البوت مضاف في المجموعة
• لديك صلاحية إدارة الرسائل

🔜 الميزات القادمة:
• إنشاء اللعبة تلقائياً في المجموعة
• إدارة اللاعبين
• بدء اللعبة عند اكتمال العدد

        """
        
        keyboard = [
            [InlineKeyboardButton("🔄 تحديث", callback_data="game_group")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="start_game")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)

    async def show_instructions(self, query):
        """📖 عرض تعليمات اللعبة"""
        text = """
🎮 **شرح لعبة الذئب (Werewolf)**

🐺 **فكرة اللعبة:**
قرية فيها ذئاب متخفية وقرويون يحاولون اكتشافهم!

👥 **الأدوار الأساسية:**
• 🐺 **الذئب** - يقتل لاعباً كل ليلة
• 👨‍🌾 **القروي** - يحاول اكتشاف الذئاب
• 🔮 **العراف** - يكشف هوية لاعب كل ليلة  
• 🩺 **الطبيب** - ينقذ لاعباً من الموت

🔄 **كيفية اللعب:**
1. 🌙 **الليل** - الذئاب والعراف والطبيب ينفذون أدوارهم
2. ☀️ **النهار** - الجميع يناقش ويصوت على مشتبه به
3. 🔁 **التكرار** - حتى يفوز فريق

🎯 **شروط الفوز:**
• 🐺 فوز الذئاب: عندما يصبح عددهم مساوي للقرويين
• 👨‍🌾 فوز القرويين: عندما يتم القضاء على جميع الذئاب

        """
        
        keyboard = [
            [InlineKeyboardButton("🎮 جرب لعبة", callback_data="start_game")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="back_main")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)

    async def show_stats(self, query):
        """📊 عرض الإحصائيات"""
        user_id = query.from_user.id
        
        if user_id == OWNER_ID:
            text = f"""
👑 **لوحة تحكم المالك**

📊 **إحصائيات البوت:**
• الألعاب النشطة: {len(self.active_games)}
• آيدي المالك: {OWNER_ID}
• حالة البوت: ✅ نشط

🎮 **الإصدار:** 1.0
🌐 **الاستضافة:** Render.com

🔧 **الميزات القادمة:**
• إدارة القنوات
• نظام اللعبة الكامل
• الإحصائيات المتقدمة
            """
        else:
            text = """
📊 **إحصائيات البوت**

🎮 البوت يعمل بشكل طبيعي
✅ جاهز لبدء الألعاب

👑 للإحصائيات المتقدمة، تواصل مع المالك
            """
        
        keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)

    async def back_to_main(self, query):
        """🔙 العودة للقائمة الرئيسية"""
        await self.start(query, None)

def main():
    """🚀 التشغيل الرئيسي للبوت"""
    logger.info("🎮 Starting Werewolf Bot...")
    
    try:
        # إنشاء تطبيق البوت
        application = Application.builder().token(BOT_TOKEN).build()
        
        # إنشاء instance من البوت
        bot = WerewolfBot()
        
        # إضافة ال handlers
        application.add_handler(CommandHandler("start", bot.start))
        application.add_handler(CallbackQueryHandler(bot.handle_callback))
        
        logger.info("✅ Bot is running and ready!")
        print("🎮 Bot started successfully!")
        print("🤖 Go to Telegram and try /start")
        
        # بدء البوت
        application.run_polling()
        
    except Exception as e:
        logger.error(f"❌ Error starting bot: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
