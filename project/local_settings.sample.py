DEBUG = False
SECRET_KEY = '123'

ALLOWED_HOSTS = []

ANSIBLE_USER = ''
ANSIBLE_WORK_DIR = ''
ANSIBLE_PLAYBOOKS_PATH = ANSIBLE_WORK_DIR + ''

ALERT_USERS = {
    'name1': {
        'phone': '79111111111',
        'days': (1, 2, 3, 4, 5, 6, 7),  # sunday = 1
        'hour': 00,
        'minute': 00,
    },
    'name2': {
        'phone': '79111111111',
        'days': (1, 2, 3, 4, 5, 6, 7), # sunday = 1
        'hour': 00,
        'minute': 00,
    }
}

ALERT_DELAY = 5  # minute

ALERT_HANDLERS = [
    'core.datatools.alert_handlers.notify_handler.NotifyHandler',
]

TELEGRAM_TOKEN = ''
TELEGRAM_CHAT_ID = ''

# For the notifications module to work (https://notify.soft-way.biz)
# NOTIFY_HANDLER_TOKEN = ''  # To access ansible-manager to notify
NOTIFY_SERVICE_TOKEN = ''  # To access notify to ansible-manager
NOTIFY_SERVICE_URL = ''
