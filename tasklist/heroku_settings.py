from tasklist.settings import *

import dj_database_url

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default':dj_database_url.config(default='sqlite:////' + SQLITE_DB)
}
