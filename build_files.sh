# build_files.sh
echo "Running build script..."
pip install -r requirements.txt
python3.9 manage.py collectstatic --noinput