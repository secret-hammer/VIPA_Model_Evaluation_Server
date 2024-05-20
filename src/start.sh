python manage.py makemigrations
python manage.py migrate

if [ "$1" = "dev" ]; then
    python manage.py runserver 0.0.0.0:8099
else
    gunicorn ME.wsgi:application --bind 0.0.0.0:8090
fi

