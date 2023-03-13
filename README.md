## Source Project
https://github.com/ahmedbesbes/cartoonify

## Descriptions
Create APIs to generate cartoonify image and save in the server.  
Provide 4 styles: Hosoda, Hayao, Shinkai, Paprika.

## Quick Start
```
$ pip3 install -r requirements.txt
$ uvicorn main:app --host 0.0.0.0 --port 8000
```
Open link: http://localhost:8000/docs

## Endpoints
1. POST /predict  
{  
  "style": "Hosoda",  
  "file_path": "./input_images/01.png"  
}  
2. POST /predictAllStyle  
{  
"style": "",  
"file_path": "./input_images/"  
}  

## Result
![image](./output_images/combined_01.png)
![image](./output_images/combined_02.png)
![image](./output_images/combined_03.png)
![image](./output_images/combined_04.png)
![image](./output_images/combined_05.png)
![image](./output_images/combined_06.png)
![image](./output_images/combined_07.png)
![image](./output_images/combined_08.png)
![image](./output_images/combined_09.png)
![image](./output_images/combined_10.png)
