from . import validate
from telebot import *
from users.user_storage import *
from logging_features.previledge_logger import *

def add(bot: TeleBot, message):
    admins = UserStorage('admins.txt').append_user('ncinsli')
    
    target = message.text.replace(' ', '')[len('/add_admin'):].replace('@', '')

    if target == '':
        bot.reply_to(message, 'Если Вы хотите добавить администратора, Вы должны указать его имя пользователя или Telegram ID')
        return
    
    if (validate.check(message, admins) and not admins.contains(target)):
        admins.append_user(target)
        log_admin_adding(message.from_user.username, target)
        bot.reply_to(message, f'✅ @{target} теперь администратор')

    elif not admins.contains(target):
        bot.reply_to(message, '❌ У Вас нет прав администратора')
        log_rejected_admin_adding(message.from_user.username, target, 'ACCESS_DENIED')
        
    else:
        bot.reply_to(message, f'❌ @{target} уже администратор')
        log_rejected_admin_adding(message.from_user.username, target, 'NO_SUCH_ADMIN')

def remove(bot: TeleBot, message):
    admins = UserStorage('admins.txt').append_user('ncinsli')
    
    target = message.text.replace(' ', '')[len('/rm_admin'):].replace('@', '')

    if target == '':
        bot.reply_to(message, 'Если Вы хотите удалить администратора, Вы должны указать его имя пользователя или Telegram ID')
        return
    
    if (validate.check(message, admins) and admins.contains(target)):
        admins.remove_user(target)
        log_admin_removing(message.from_user.username, target)
        bot.reply_to(message, f'✅ @{target} теперь не администратор')

    elif admins.contains(target):
        bot.reply_to(message, '❌ У Вас нет прав администратора')
        log_rejected_admin_removing(message.from_user.username, target, 'ACCESS_DENIED')

    else:
        bot.reply_to(message, f'❌ @{target} не был администратором')
        log_rejected_admin_removing(message.from_user.username, target, 'NO_SUCH_ADMIN')
