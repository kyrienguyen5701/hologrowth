import subprocess

if __name__ == '__main__':
    # run cron
    p1 = subprocess.Popen('cron && tail -f /var/log/cron_crawl.log', shell=True)
    
    # run wsgi
    p2 = subprocess.Popen('gunicorn --bind :8000 --workers 1 --threads 8 --timeout 300 app:app', shell=True)
    
    # wait for both programs to finish
    p1.wait()