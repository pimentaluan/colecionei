# build_files.sh
echo "Running build script..."
pip install -r requirements.txt
python3.3.12.1 manage.py collectstatic --noinput
