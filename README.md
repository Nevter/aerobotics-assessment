# aerobotics-assessment


### Assumptions with this algorithm
1) There cant be three missing trees in a row
2) Missing tree's in internal corners cannot be found
    x x x x
      o x x   
        x x
    If there should be a tree at o but there isn't, this algorithm will not detect it. 
       
## Run:
```> docker-compose up --build server ```