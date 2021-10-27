#!/usr/bin/env bash

echo "RELEASE SCRIPT:"
echo $HEROKU_APP_NAME
# echo "release " $HEROKU_SLUG_COMMIT
python manage.py migrate --no-input
  