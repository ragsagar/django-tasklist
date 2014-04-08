from tasklist.settings import *

import dj_database_url

DATABASES = {
    'default':dj_database_url.config()
    #{
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #}
}
