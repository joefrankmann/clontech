flake8

if [[ $# -eq 0 ]] ; then
   ./manage.py test
else
   ./manage.py test $1
fi