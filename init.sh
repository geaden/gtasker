export SECRET_KEY=$( cat secret.txt )
export DJANGO_SETTINGS_MODULE=gtasker.settings.local
export PYTHONPATH=$PYTHONPATH:./gasker/gtasker/
export ADMIN_USER=$( cat admin.txt )
source google.sh
