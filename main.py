import telegram
import requests


QIWI_API_TOKEN=''

def hanlder_message(update, context):
    message = update.message

    if message.text:
        account = message.text.split('\n')
        account = [account.strip() for account in account if account.strip()]

        if account:
            context.user.data['account'] = account
            message.reply_text(f'Принято {len(account)} аккаунтов. Теперь введите сумму для перевода.')
        else:
            message.reply_text('Список аккаунтов пуст.')
    elif message.document:
        file = message.document.get.file()
        account = []

        with file.download_as_bytearray() as byte_array:
            content = byte_array.decode('utf-8')
            account = content.split('\n')
            account = [account.strip() for account in account if account.strip()]
        

        if account:
            context.user_data['accounts'] = account
            message.reply_text(f'Принято {len(account)} аккаунтов. Теперь введите сумму для перевода')
        else:
            message.reply_text('пустой')
    else:
        message.reply_text('Неверный формат')
    
def distribute_funda(accounts, amount):
    for account in accounts:


        headers = {
            'Content-Type' : 'application/json',
            'Authorization': f'Bearer {QIWI_API_TOKEN}'
                }

        data = {
            'amoint':{
                'currency': 'RUB',
                'value' : amount
            },
            'comment': 'Перевод средств',
            'fields':{
                'account': account
                }
            }
        response = requests.post('https://api.qiwi.com/partner/bill/v1/bills/create', headers=headers, json=data)

        if response.status_code == 200:
            print(f'Перевод {amount} рубли на аккаунт Qiwi: {account}')
        else:
            print(f'Ошибка при переводе {amount} рубли на аккаутн Qiwi: {account}')
def start(update, account):
    context.user_data.clear()
    update.message.reply_text("Привет! Пришлите список аккаунтов Qiwi в виде текстового сообщения или файла.")
def transfer(update, context):
    message = update.message
    if 'account' in context.user_data:
        accounts = context.user_data['account']
        amount = message.text.strip()

        try:
            amount = float(amount)
            if amount <= 0:
                message.reply_text('Некорректная сумма для перевода.')
                return  
            distribute_funds(accounts, amount)
            message.reply_text(f"Выполнен перевод {amount} тенге на каждый аккаунт Qiwi.")
        except ValueError:
            message.reply_tet('Не найден список аккаунтов Qiwi')

bot_token = ''
bot = telegram.Bot(token=bot_token)
updater = telegram.ext.Updater(bot=bot,use_context=True)

updater.dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
updater.dispatcher.add_handler(telegram.ext.CommandHandler('transfer', transfer))
updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text & ~telegram.ext.Filters.command, handle_message))
updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.document, handle_message))

updater.start_polling()
updater.idle()