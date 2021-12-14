# yumflow

A website for creating different models for training data with different methods and compare them. This website is being used by Dr.Mahdi Jafari Siavoshani's Lab.

## how to setup project
```
mkdir project
cd project
git clone git@github.com:sh3rLock3d/yumflow.git
cd yumflow
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
npm install
npm run dev
--------------- in another terminal
cd project/yumflow
source venv/bin/activate
cd yumflow
python manage.py migrate
python manage.py runserver
```
