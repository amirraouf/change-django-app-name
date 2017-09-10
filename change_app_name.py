from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

from django.db import connection
from django.db.models import Q


ContentType.objects.filter(app_label='<old_app_name>').update(app_label='<app_name>')  # change content type to prevent django migrations from re-migrate
permissions = Permission.objects.filter(Q(content_type__app_label='url_integrations') |
                                        Q(content_type__app_label='pcm'))
admin_grp = Group.objects.get(name='<grp_name>')  # add new permissions if changed or deleted
for p in permissions:
    admin_grp.permissions.add(p)
with connection.cursor() as c:
    c.execute("update django_migrations set app='<app_name>' where app='<old_app_name>';")  # update django migrations table to set new app name
    c.execute("select relname from pg_stat_user_tables where relname like '<old_app_name>%';")  # select all tables of database to rename it
    data = c.fetchall()
    for d in data:
        name = d[0]
        name = name.split("url_integration_")[1]
        c.execute("ALTER table %s RENAME to <app_name>_%s;" % (d[0], name))
