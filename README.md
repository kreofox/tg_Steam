# tg_Steam

 Здесь выполняется логика перевода суммы на аккаунт Qiwi Используйте Qiwi API для выполнения операции перевода
 Пример кода для выполнения перевода с использованием Qiwi API

         headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {QIWI_API_TOKEN}'
        }
        data = {
            'amount': {
                'currency': 'RUB',
                'value': amount
            },
            'comment': 'Перевод средств',
            'fields': {
                'account': account
            }
        }
        response = requests.post('https://api.qiwi.com/partner/bill/v1/bills/create', headers=headers, json=data)

регистрируем обработчики команд и сообщений:
```sh
updater.dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
updater.dispatcher.add_handler(telegram.ext.CommandHandler('transfer', transfer))
updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text & ~telegram.ext.Filters.command, handle_message))
updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.document, handle_message))
```

# [Документация Qiwi](https://developer.qiwi.com/ru/qiwi-wallet-personal/?python#qiwi-master-list)