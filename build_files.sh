# build_files.sh
echo "Running build script..."
python3 -m pip install -r requirements.txt
python3 manage.py collectstatic --noinput
