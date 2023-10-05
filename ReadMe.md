This is Recruitment Api

To run the application
after cloning the repo, open the terminal in the same dirctory 

bash: sudo docker-compose build (wait until the command finish its process)
bash: sudo docker-compose up (after finishing open new tab in the terminal) 
bash: docker ps (you will see 2 containers running get the api name it will be like that recruitment_site_api_doc_1)
bash: docker exec -it <image_name>  /bin/bash (repalce the <image_name> with the api name recruitment_site_api_doc_1)
bash: python3 manage.py createsuperuser (enter your email and password for the admin panel)

now open your browser and type:
http://127.0.0.1:8000/ to see all urls
http://127.0.0.1:8000/admin to open the database (enter your email and password that you created befor)

If you have any advice, please don't hesitate to tell me.

Enjoy until I rewrite the readme with all things.