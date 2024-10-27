# build_files.sh
echo "Running build script..."
pip3 install -r requirements.txt
python manage.py collectstatic --noinput
