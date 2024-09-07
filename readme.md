# SDDE330 Blog App

### App Server/EC2 Information 

Instance ID: `i-0d8d5b324b2dc42af`

Static IP: `54.152.6.67`

Server DNS: `ec2-54-152-6-67.compute-1.amazonaws.com`

URL: [http://54.152.6.67](http://54.152.6.67)

#### Setup Overview: 
Database for blog data: sqlite3
App Server/Backend: Flask, gunicorn
Front End/UI: HTML/CSS served with Flask

#### Configuration 
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

API code & functionality is in `app.py` and `database.py`

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
├── app.py (API & App code)
├── database.py (Database operations)
├── bloglog.py (Singleton API Logger)
├── bloglog.py (Log File)
├── myblog.db (Blog sqlite3 Database)
└── req.txt (python venv requirements packages)
└── blog_venv (python venv for app)

```
#### Screenshots

##### Read Blog
![Read Blog](/images/read_blog_frontpage.png)

##### New Blog
![Create Blog](/images/new_blog_ui.png)

##### Update Blog
![Update Blog](/images/update_blog.png)




