SECRET_KEY=$(hexdump -vn16 -e'4/4 "%08X" 1 "\n"' /dev/urandom) gunicorn -w 4 --log-level debug app:app
