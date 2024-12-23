# WireGuard Manager

## Описание

Этот проект представляет собой менеджер VPN, который использует WireGuard для создания и управления VPN-клиентами. Проект включает в себя Flask API для взаимодействия с WireGuard и управления конфигурациями клиентов.

## Переменные окружения

Проект использует файл .env для хранения переменных окружения. Пример содержимого файла .env:
```bash
API_KEY = "key" # Ключ для авторизации на сервере

WG_INTERFACE = "wg0"
WG_CONF = "/etc/wireguard/wg0.conf"
CLIENTS_DIR = "/etc/wireguard/clients" 

LISTEN_PORT = "51820" # Порт для прослушивания WireGuard
```

## Структура проекта

```
VPNmanager/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── config.py
│   ├── routes.py
│   ├── utils.py
│   └── wg.py
├── .env
├── .gitignore
├── readme.md
├── requirements.txt
├── run.py
└── start.sh
```

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/altrest105/VPNmanager
cd VPNmanager
```

2. Сделайте файл start.sh исполняемым:
```bash
chmod +x start.sh
```

3. Запустите проект, выполнив команду:
```bash
./start.sh
```

Сервер будет доступен по адресу `0.0.0.0:5000`

## Использование

### Создание клиента

Для создания нового VPN-клиента отправьте POST-запрос на /create_client с телом запроса, содержащим subscription_id:
```json
{
  "subscription_id": "your_subscription_id"
}
```

### Удаление клиента

Для удаления существующего VPN-клиента отправьте POST-запрос на /delete_client с телом запроса, содержащим subscription_id:
```json
{
  "subscription_id": "your_subscription_id"
}
```

### Получение клиента

Для получения существующего VPN-клиента отправьте POST-запрос на /get_client с телом запроса, содержащим subscription_id:
```json
{
  "subscription_id": "your_subscription_id"
}
```