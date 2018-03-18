    
## Del 2
         
    
    Med sortering behövs N * log2(N) och utan N * index från max (index=1 är max)
      
N | vilket index som det blir mer efektift med sortering
--- | ---
 10 | 4 

N=10 | 1:a längsta | 2:a längsta | 3:e längsta | 4:e längsta | 5:e längsta 
 --- | ---| ---| ---| ---| ---
Osorterad  | 0.00386 | 0.00795 | 0.01083 | 0.01499 | 0.01846
sorterad| 0.0159| 0.0158| 0.0165| 0.0176| 0.0162

