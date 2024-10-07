from telegram import Update,KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
import subprocess,os
from time import sleep
import logging,json
from datetime import *
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import arabic_reshaper
from bidi.algorithm import get_display
import random
admin=6542761604
token="8064869953:AAGWK4neEDsd3IfRR4bBBqoWNMMpm4Ol_sQ"
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
ID,DATE,LIB,SAVE,APP_ID,API_HASH,SESSION,TOKEN,EX,EX2,DELETE= range(11)
def send_command_to_screen(screen_name, command):
        full_command = f'screen -S {screen_name} -X stuff \'{command}\\n\''
        os.system(full_command)
def check_screen_session(session_name):
    try:
        result = subprocess.run(['screen', '-ls'], capture_output=True, text=True, check=True)
        if session_name in result.stdout:
            return False
        else:
            return True

    except:
        return True
def prepare_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)  # Reshape text
    bidi_text = get_display(reshaped_text)  # Handle bidirectional text
    return bidi_text
x=open("list_date.txt","r").read().split("\n")
for a in x:
    if a!="":
     b=a.split(":::")
     if check_screen_session(b[0]):
       if datetime.strptime(datetime.now().strftime('%Y-%m-%d'), "%Y-%m-%d") <= datetime.strptime(b[3], "%Y-%m-%d"):
           os.system(f"screen -dmS {str(b[0])}")
           if b[1]=="joker":
            commands = [
            f'cd {os.getcwd()}/{b[0]}/yamahdi',
            'python3 -m JoKeRUB'
            ]
            for command in commands:
             try:
               sleep(2)
               send_command_to_screen(f"{str(b[0])}",command)
             except:
              pass
           elif b[1]=="zdthon":
            commands = [
            f'cd {os.getcwd()}/{b[0]}/ZThon',
            'python3 -m zira'
            ]
            for command in commands:
             try:
               sleep(3)
               send_command_to_screen(f"{str(b[0])}",command)
             except:
              pass
def start(update: Update, context: CallbackContext) -> int:
 if update.message.chat_id==admin:
    keyboard = [
        [KeyboardButton("/new")],
        [KeyboardButton("/delete")],
        [KeyboardButton("/add_date")]
           ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    update.message.reply_text("""مرحبا بك في بوت تنصيب سورسات زدثون والجوكر
تستطيع من خلالي تنصيب سورسات زدثون و جوكر بسهولة وسلاسة والتحكم بالحسابات

ان كنت تريد ان نبدأ ارسل ايدي المشتري
                              
او استخدم احدى الازرار👇👇""",reply_markup=reply_markup)
    return ID


def handle_message(js,update: Update, context: CallbackContext) -> None:
 if update.message.chat.id==1938276557:
  if js["lib"]=="joker":
    os.system(f"screen -dmS {str(js['id'])}")
    commands = [
        f'cd {os.getcwd()}',
        f'mkdir {js["id"]}',
        f"sudo chmod -R 755 {os.getcwd()}/{str(js['id'])}",
        f"cp {os.getcwd()}/data.sh {js['id']}",
        f'cd {js["id"]}',
        "chmod +x data.sh",
        f"sudo bash data.sh {js['id']}",
        'git clone https://github.com/almul8ab/yamahdi',
        f"sudo chmod -R 755 {os.getcwd()}/{str(js['id'])}",
        'cd yamahdi',
        'rm -rf exampleconfig.py',
        'python3 -m JoKeRUB'
    ]

    for command in commands:
        try:
            sleep(5)
            send_command_to_screen(f"{str(js['id'])}",command)
            if command=="rm -rf exampleconfig.py":
                open(f"{os.getcwd()}/{str(js['id'])}/yamahdi/config.py","w").write(f'''from sample_config import Config
class Development(Config):
    # get this values from the my.telegram.org
    APP_ID = {js["app_id"]}
    API_HASH = "{js["api_hash"]}"
    # the name to display in your alive message
    ALIVE_NAME = "alikwiq"
    DB_URI = "postgresql://postgres:your_password@localhost:5432/{str(js['id'])}"
    STRING_SESSION = "{js["SESSION"]}"
    TG_BOT_TOKEN = "{js["token"]}"
    COMMAND_HAND_LER = "."
    SUDO_USERS = []
    SUDO_COMMAND_HAND_LER = "."''')
        except subprocess.CalledProcessError as e:
            logger.error(f"Command: {command}\nError: {e}")
    now = datetime.now()
    future_date = now + timedelta(days=int(js["date"]))
    open(f"{os.getcwd()}/{str(js['id'])}/date.txt","w").write(f"{now.strftime('%Y-%m-%d')}\n{future_date.strftime('%Y-%m-%d')}\n{js['date']} day")
    sleep(60)
    c = canvas.Canvas(f"{os.getcwd()}/{str(js['id'])}/date.pdf", pagesize=A4)
    width, height = A4
    pdfmetrics.registerFont(TTFont('Amiri', 'text.ttf'))
    c.setFont("Amiri", 30)
    prepared_buyer_name = prepare_arabic_text(f"ايدي المشتري:-{str(js['id'])}")
    c.drawRightString(width - 2 * cm, height - 5 * cm, prepared_buyer_name)
    c.setStrokeColor(colors.black)
    c.setLineWidth(2)
    c.line(2 * cm, height - 6 * cm, width - 2 * cm, height - 6 * cm)
    c.setFont("Amiri", 14)
    prepared_buyer_name = prepare_arabic_text(f"تاريخ بدء الاشتراك:-{now.strftime('%Y-%m-%d')}")
    c.drawRightString(width - 2 * cm, height - 8 * cm, prepared_buyer_name)
    prepared_buyer_name = prepare_arabic_text(f"تاريخ انتهاء الاشتراك:-{future_date.strftime('%Y-%m-%d')}")
    c.drawRightString(width - 2 * cm, height - 10 * cm, prepared_buyer_name)
    prepared_buyer_name = prepare_arabic_text(f"مدة الاشتراك:-{js['date']} day")
    c.drawRightString(width - 2 * cm, height - 12 * cm, prepared_buyer_name)
    prepared_buyer_name = prepare_arabic_text(f"نوع الاشتراك:-{js['lib']}")
    c.drawRightString(width - 2 * cm, height - 14 * cm, prepared_buyer_name)
    c.setFont("Amiri", 0.01)
    prepared_buyer_name = prepare_arabic_text(f"@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq")
    c.drawRightString(width - 2 * cm, height - 20 * cm, prepared_buyer_name)
    c.showPage()
    c.save()
    update.message.reply_document(document=open(f"{os.getcwd()}/{str(js['id'])}/date.pdf", 'rb'))
    open("list_date.txt","a").write(f"{js['id']}:::{js['lib']}:::{now.strftime('%Y-%m-%d')}:::{future_date.strftime('%Y-%m-%d')}\n")
    return 0
  if js["lib"]=="zdthon":
    os.system(f"screen -dmS {str(js['id'])}")
    commands = [
        f'cd {os.getcwd()}',
        f'mkdir {js["id"]}',
        f"sudo chmod -R 755 {os.getcwd()}/{str(js['id'])}",
        f"cp {os.getcwd()}/data.sh {js['id']}",
        f'cd {js["id"]}',
        "chmod +x data.sh",
        f"sudo bash data.sh {js['id']}",
        'git clone https://github.com/Zilzalll/ZThon',
        f"sudo chmod -R 755 {os.getcwd()}/{str(js['id'])}",
        'cd ZThon',
        'rm -rf exampleconfig.py',
        'python3 -m zira'
    ]

    for command in commands:
        try:
            sleep(5)
            send_command_to_screen(f"{str(js['id'])}",command)
            if command=="rm -rf exampleconfig.py":
                open(f"{os.getcwd()}/{str(js['id'])}/ZThon/config.py","w").write(f'''from sample_config import Config


class Development(Config):
    APP_ID = {js["app_id"]}
    API_HASH = "{js["api_hash"]}"
    ALIVE_NAME = "alikwiq"
    DB_URI = "postgresql://postgres:your_password@localhost:5432/{str(js['id'])}"
    STRING_SESSION = "{js["SESSION"]}"
    TG_BOT_TOKEN = "{js["token"]}"
    PRIVATE_GROUP_BOT_API_ID = {js["save"]}
    COMMAND_HAND_LER = "."
    SUDO_COMMAND_HAND_LER = "."
    TZ = "Asia/Baghdad"''')
        except subprocess.CalledProcessError as e:
            logger.error(f"Command: {command}\nError: {e}")
    now = datetime.now()
    future_date = now + timedelta(days=int(js["date"]))
    open(f"{os.getcwd()}/{str(js['id'])}/date.txt","w").write(f"{now.strftime('%Y-%m-%d')}\n{future_date.strftime('%Y-%m-%d')}\n{js['date']} day")
    sleep(60)
    c = canvas.Canvas(f"{os.getcwd()}/{str(js['id'])}/date.pdf", pagesize=A4)
    width, height = A4
    pdfmetrics.registerFont(TTFont('Amiri', 'text.ttf'))
    c.setFont("Amiri", 30)
    prepared_buyer_name = prepare_arabic_text(f"ايدي المشتري:-{str(js['id'])}")
    c.drawRightString(width - 2 * cm, height - 5 * cm, prepared_buyer_name)
    c.setStrokeColor(colors.black)
    c.setLineWidth(2)
    c.line(2 * cm, height - 6 * cm, width - 2 * cm, height - 6 * cm)
    c.setFont("Amiri", 14)
    prepared_buyer_name = prepare_arabic_text(f"تاريخ بدء الاشتراك:-{now.strftime('%Y-%m-%d')}")
    c.drawRightString(width - 2 * cm, height - 8 * cm, prepared_buyer_name)
    prepared_buyer_name = prepare_arabic_text(f"تاريخ انتهاء الاشتراك:-{future_date.strftime('%Y-%m-%d')}")
    c.drawRightString(width - 2 * cm, height - 10 * cm, prepared_buyer_name)
    prepared_buyer_name = prepare_arabic_text(f"مدة الاشتراك:-{js['date']} day")
    c.drawRightString(width - 2 * cm, height - 12 * cm, prepared_buyer_name)
    prepared_buyer_name = prepare_arabic_text(f"نوع الاشتراك:-{js['lib']}")
    c.drawRightString(width - 2 * cm, height - 14 * cm, prepared_buyer_name)
    c.setFont("Amiri", 0.01)
    prepared_buyer_name = prepare_arabic_text(f"@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq@alikwiq")
    c.drawRightString(width - 2 * cm, height - 20 * cm, prepared_buyer_name)
    c.showPage()
    c.save()
    update.message.reply_document(document=open(f"{os.getcwd()}/{str(js['id'])}/date.pdf", 'rb'))
    open("list_date.txt","a").write(f"{js['id']}:::{js['lib']}:::{now.strftime('%Y-%m-%d')}:::{future_date.strftime('%Y-%m-%d')}\n")
    return 0
def id_user(update: Update, context: CallbackContext) -> int:
 if update.message.chat_id==admin:
   user_data = context.user_data
   for num in range(99999):
    num=num+1
    if str(update.message.text+f"-v{num}") not in open("list_date.txt","r").read():
     user_data['id'] = str(update.message.text+f"-v{num}")
     keyboard = [
        [KeyboardButton("/cancel")]
           ]
     reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
     update.message.reply_text(f"""تم الحفظ بنجاح

الان قم بارسال عدد الايام الخاصه بلاشتراك
مثلا ان اردت اسبوع تقوم بارسال رقم 7 فقط""",reply_markup=reply_markup)
     return DATE
     
def date_user(update: Update, context: CallbackContext):
 if update.message.chat_id==admin:
    user_data = context.user_data
    user_data['date'] = update.message.text
    keyboard = [
        [KeyboardButton("zdthon")],
        [KeyboardButton("joker")],
        [KeyboardButton("/cancel")]
           ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(f"""الان قم بارسال نوع الاشتراك المطلوب قم بتحديد زدثون او الجوكر 
يمكنك الاختيار من الازرار في الاسفل👇""",reply_markup=reply_markup)
    return LIB

def lib_user(update: Update, context: CallbackContext):
 if update.message.chat_id==admin:
    user_data = context.user_data
    user_data['lib'] = update.message.text
    keyboard = [
        [KeyboardButton("/cancel")]
           ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(f"""ارسل ايدي قناة الخزن
في حال كان التنصيب الجوكر يمكنك ارسال اي شيء لكن في حال كان التنصيب زدثون عليك ارسال ايدي قناة الخزن حقيقي""",reply_markup=reply_markup)
    return SAVE

def save_user(update: Update, context: CallbackContext):
 if update.message.chat_id==admin:
    user_data = context.user_data
    user_data['save'] = update.message.text
    keyboard = [
        [KeyboardButton("/cancel")]
           ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(f"API_ID قم بإرسال",reply_markup=reply_markup)
    return APP_ID

def app_id_user(update: Update, context: CallbackContext):
 if update.message.chat_id==admin:
    user_data = context.user_data
    user_data['app_id'] = update.message.text
    keyboard = [
        [KeyboardButton("/cancel")]
           ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(f"API_HASH قـم بإرسال",reply_markup=reply_markup)
    return API_HASH

def api_hash_user(update: Update, context: CallbackContext):
 if update.message.chat_id==admin:
    user_data = context.user_data
    user_data['api_hash'] = update.message.text
    keyboard = [
        [KeyboardButton("/cancel")]
           ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(f"""قم بارسال الجلسه(كود الترمكس)""",reply_markup=reply_markup)
    return SESSION

def session_user(update: Update, context: CallbackContext):
 if update.message.chat_id==admin:
    user_data = context.user_data
    user_data['session'] = update.message.text
    keyboard = [
        [KeyboardButton("/cancel")]
           ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(f"قم بارسال توكن البوت",reply_markup=reply_markup)
    return TOKEN

def token_user(update: Update, context: CallbackContext):
 if update.message.chat_id==admin:
  try:
    user_data = context.user_data
    user_data['token'] = update.message.text
    update.message.reply_text("""جار بدء التنصيب
ملاحظه!!:- لا ترسل اي شيء حتى اخبرك بانتهاء التنصيب""")
    info={}
    if user_data['lib']=="zdthon":
     info={"date":int(user_data['date']),
"id":f"{user_data['id']}",
"app_id":int(user_data['app_id']),
"api_hash":f"{user_data['api_hash']}",
"SESSION":f"{user_data['session']}",
"token":f"{user_data['token']}",
"lib":f"{user_data['lib']}",
"save":int(user_data['save'])}
    else:
      info={"date":int(user_data['date']),
"id":f"{user_data['id']}",
"app_id":int(user_data['app_id']),
"api_hash":f"{user_data['api_hash']}",
"SESSION":f"{user_data['session']}",
"token":f"{user_data['token']}",
"lib":f"{user_data['lib']}"}
    handle_message(info,update,context)
    keyboard = [
        [KeyboardButton("/new")],
        [KeyboardButton("/delete")],
        [KeyboardButton("/add_date")]
           ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("""تم التنصيب بنجاح✅✅""",reply_markup=reply_markup)
    return ConversationHandler.END
  except Exception as e:
    update.message.reply_text(f"error:-{e}")
    return ConversationHandler.END

def ex_user(update: Update, context: CallbackContext):
 if update.message.chat_id==admin:
    user_data = context.user_data
    user_data['ex_date'] = update.message.text
    update.message.reply_text(f"""حسنا!
ارسل الان عدد الايام اللتي تريد اضافتها الى الحساب""")
    return EX2

def delete_user(update: Update, context: CallbackContext):
 if update.message.chat_id==admin:
    x=open("list_date.txt","r").read().split("\n")
    for a in x:
     if a=="":
       pass
     else:
        b=a.split(":::")
        if b[0]==update.message.text:
         os.system(f"screen -X -S {b[0]} quit")
         os.system(f'sudo su - postgres -c "dropdb {b[0]}"')
         os.system(f"rm -rf {b[0]}")
         text=open("list_date.txt","r").read().replace(f"{a}\n","")
         open("list_date.txt","w").write(text)
         update.message.reply_text(f"""تم حذف التنصيب بنجاح✅
المستخدم:-{b[0]}
تاريخ بدء الاشتراك:-{b[2]}
تاريخ الانتهاء:-{b[3]}
نوع الاشتراك:-{b[1]}""")
         return ConversationHandler.END
    update.message.reply_text("لم يتم العثور على المستخدم تاكد من الاختيار واعد المحاولة")
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
 if update.message.chat_id==admin:
    keyboard = [
        [KeyboardButton("/new")],
        [KeyboardButton("/delete")],
        [KeyboardButton("/add_date")]
           ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text('تم الغاء العمليه بنجاح✅✅',reply_markup=reply_markup)
    return ConversationHandler.END
def new(update: Update, context: CallbackContext):
 if update.message.chat_id==admin:
    keyboard = [[KeyboardButton("/cancel")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("""ارسل ايدي المشتري""",reply_markup=reply_markup)
    return ID
def delete(update: Update, context: CallbackContext):
 if update.message.chat_id==admin:
    keyboard = [[KeyboardButton("/cancel")]]
    for a in open("list_date.txt","r").read().split("\n"):
       b=a.split(":::")
       keyboard.append([KeyboardButton(str(b[0]))])
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("""اختر احد المستخدمين من القائمة في الاسفل لحذف التنصيب👇""",reply_markup=reply_markup)
    return DELETE
def add(update: Update, context: CallbackContext):
   if update.message.chat_id==admin:
     keyboard = [[KeyboardButton("/cancel")]]
     for a in open("list_date.txt","r").read().split("\n"):
       b=a.split(":::")
       keyboard.append([KeyboardButton(str(b[0]))])
     reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
     update.message.reply_text("""اختر الحساب الذي تريد تمديد اشتراكه""",reply_markup=reply_markup)
     return EX
def ex2_user(update: Update, context: CallbackContext):
   if update.message.chat_id==admin:
     days=int(update.message.text)
     user_data = context.user_data
     x=open("list_date.txt","r").read().split("\n")
     for a in x:
      if a=="":
       pass
      else:
        b=a.split(":::")
        if b[0]==user_data['ex_date']:
         militime=datetime.strptime(b[3], "%Y-%m-%d")
         militime+=timedelta(days=days)
         know=militime.strftime('%Y-%m-%d')
         edit=a.replace(b[3],know)
         text=open("list_date.txt","r").read().replace(a,edit)
         open("list_date.txt","w").write(text)
         update.message.reply_text(f"""تم تمديد الاشتراك بنجاح
المستخدم:-{b[0]}
تاريخ بدء الاشتراك:-{b[2]}
تاريخ الانتهاء:-{know}
نوع الاشتراك:-{b[1]}""")
         return ConversationHandler.END
     return ConversationHandler.END
def main() -> None:
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("new", new),CommandHandler("delete", delete),CommandHandler("add_date", add)],
        states={
            ID: [MessageHandler(Filters.text & ~Filters.command, id_user)],
            DATE: [MessageHandler(Filters.text & ~Filters.command, date_user)],
            LIB: [MessageHandler(Filters.text & ~Filters.command, lib_user)],
            SAVE: [MessageHandler(Filters.text & ~Filters.command, save_user)],
            APP_ID: [MessageHandler(Filters.text & ~Filters.command, app_id_user)],
            API_HASH: [MessageHandler(Filters.text & ~Filters.command, api_hash_user)],
            SESSION: [MessageHandler(Filters.text & ~Filters.command, session_user)],
            TOKEN: [MessageHandler(Filters.text & ~Filters.command, token_user)],
            EX: [MessageHandler(Filters.text & ~Filters.command, ex_user)],
            EX2: [MessageHandler(Filters.text & ~Filters.command, ex2_user)],
            DELETE: [MessageHandler(Filters.text & ~Filters.command, delete_user)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()
