# App Server & APIs:

Create APIs to perform CRUD operations on the Blog using the class/object model that you built earlier (in #1). 

## Rubric:

### App Server Installation 

Instance ID: `i-0d8d5b324b2dc42af`

Static IP: `54.152.6.67`

Server DNS: `ec2-54-152-6-67.compute-1.amazonaws.com`

#### Installation: 
- Successfully installs the app server. 

A python virtual environment was used for this app named `blog_venv` 
gunicorn was used for this flask app. 
`pip install gunicorn` 

![venv setup](/images/venv_list.png)

#### Configuration 
- Properly configures the server to run the application. 

The app was setup to persistently run using `systemd`. A copy of the configuration file placed in `/etc/systemd/system/app.service` is in this repo.
To start the service, the following commands were used on ec2:
```
sudo systemctl daemon-reload
sudo systemctl start app
sudo systemctl enable app
```

To check that the app is running: `sudo systemctl status app`
![app status](/images/systemd_service_status.png)

### CRUD APIs 
- Create API: API to create blog entries works correctly. 
- Read API: API to read blog entries (single and all) works correctly. 
- Update API: API to update blog entries works correctly. 
- Delete API: API to delete blog entries works correctly. 

API code & functionality is in `app.py`

Postman API Documentation:
https://documenter.getpostman.com/view/37591410/2sA3s3HqxY

### Front End UX/UI Setup

**My Blog** : [http://54.152.6.67/](http://54.152.6.67/)

Flask was used to serve the HTML/Javascript page to access the blog. 

First the project files were reorganized under the following directory structure in the home directory of the EC2 instance
```
myblogapp/
│
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── scripts.js
│
├── templates/
│   └── index.html
│
├── app.py
└── req.txt
```

`index.html` is linked to the endpoint `/` in `app.py`:
```python
@app.route('/')
def index():
    return render_template('index.html')
```

To set up the service, `gunicorn` and `systemd` was used.

The `gunicorn` command sets up the site on port 8080:
`/home/ec2-user/myblogapp/blog_venv/bin/gunicorn -b 0.0.0.0:8080 app:app`

The `systemd` config file was modified to point to the new directory structure:
```bash
[Unit]
Description=Gunicorn instance to serve app
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/myblogapp
Environment="PATH=/home/ec2-user/myblogapp/blog_venv/bin"
ExecStart=/home/ec2-user/myblogapp/blog_venv/bin/gunicorn -b 0.0.0.0:8080 app:app

[Install]
WantedBy=multi-user.target
```

To enable access to the site on port 80, a reverse proxy was set up using `nginx`:

To install `nginx`: `sudo yum install nginx -y `
To enable the service: 
```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```
The nginx conf file was updated (`/etc/nginx/nginx.conf`):
```bash
server {
    listen 80;
    server_name 54.152.6.67;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Screenshots

##### Read Blog
![Read Blog](/images/read_blog_frontpage.png)

##### New Blog
![Create Blog](/images/new_blog_ui.png)

##### Update Blog
![Update Blog](/images/update_blog.png)




