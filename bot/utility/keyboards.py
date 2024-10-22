from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database.enums import UserStage


# START COMMAND KEYBOARDS
s1_keyboard = [
        [
            InlineKeyboardButton("📌 نحوه استفاده", callback_data="usage"),
            InlineKeyboardButton("📑 قوانین استفاده", callback_data="terms")
        ],
        [
            InlineKeyboardButton("📝 ارسال نظرات و پیشنهادات", callback_data='message'),
        ]
]

s2_keyboard = [
    [InlineKeyboardButton("🌐 ورود به سامانه", callback_data="login")]
] + s1_keyboard

s3_keyboard = [
    [
        InlineKeyboardButton("🍽 سلف", callback_data="self"),
        InlineKeyboardButton("💎 اشتراک", callback_data="subscription")
    ],
    [ 
        InlineKeyboardButton("⚙️ تنظیمات", callback_data="setting"),
        InlineKeyboardButton("🙎‍♂️ پروفایل", callback_data="profile")
    ]
] + s1_keyboard

def get_main_keyboard(stage: int) -> InlineKeyboardMarkup:
    
    # 0:first time | 1:new | 2:terms accepted | 3:logged in | 4:premium
    print(f"STAGE: {stage}")
    if stage == UserStage.NEW.value:
        keyboard = s1_keyboard
    elif stage == UserStage.TERMS.value:
        keyboard = s2_keyboard
    elif stage <= UserStage.PAID.value:
        keyboard = s3_keyboard
    else:
        raise Exception("Stage is not in range of 0 to 4")
    return InlineKeyboardMarkup(keyboard)

# =========================

def get_back_keyboard(query: str, markup: bool = True) -> InlineKeyboardMarkup:
    if markup:
        return InlineKeyboardMarkup([[InlineKeyboardButton("↩️ برگشت", callback_data=query)]])
    return [[InlineKeyboardButton("↩️ برگشت", callback_data=query)]]

terms_keyboard = InlineKeyboardMarkup([
    [   
        InlineKeyboardButton("✅ میپذیرم", callback_data="terms_accepted"),
        InlineKeyboardButton("❌ نمیپذیرم", callback_data="start")
    ]
])

self_keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("✏️ رزرو دستی", callback_data="self_manual"),
        InlineKeyboardButton("🤖 رزرو خودکار", callback_data="self_automatic")
    ],
    [
        InlineKeyboardButton("🗓 برنامه غذایی", callback_data="self_program"),
        InlineKeyboardButton("🍾 لیست اولویت", callback_data="self_priority"),
    ],
    [InlineKeyboardButton("↩️ برگشت", callback_data="start")]
])
