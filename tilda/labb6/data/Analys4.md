## Del 1
        
        N | Linjärsökningen O(N) | Quicksort O(N*log(N)) | Binarysökningen O(N*log(N)) | Dictsökningen O(1)
        --- | --- |  --- | --- | ---
 10 | 0.00094 | 0.02154 | 0.0022 | 0.00023
 15 | 0.00126 | 0.03317 | 0.00226 | 0.00022    

## Del 2
         
    
Med sortering behövs N * log2(N) och utan N * index från max (index=1 är max)
      
N | vilket index som det blir mer efektift med sortering
--- | ---
 10 | 4 

N=10 | 1:a längsta | 2:a längsta | 3:e längsta | 4:e längsta | 5:e längsta | 6:e längsta | 7:e längsta | 8:e längsta | 9:e längsta | 10:e längsta 
 --- | ---| ---| ---| ---| ---| ---| ---| ---| ---| ---
Osorterad  | 0.00642 | 0.01177 | 0.02972 | 0.07026 | 0.05521 | 0.09112 | 0.05881 | 0.04329 | 0.04639 | 0.05083
sorterad| 0.02148| 0.02371| 0.02178| 0.02702| 0.02448| 0.02412| 0.02457| 0.02365| 0.02511| 0.02506

