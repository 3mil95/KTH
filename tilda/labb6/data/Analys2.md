
## Del 2
         
    
Med sortering behövs N * log2(N) och utan N * index från max (index=1 är max)
      
N | vilket index som det blir mer efektift med sortering
--- | ---
 10 | 4 
 20 | 5 
 30 | 5 

N=10 | 1:a längsta | 2:a längsta | 3:e längsta | 4:e längsta | 5:e längsta | 6:e längsta | 7:e längsta | 8:e längsta | 9:e längsta | 10:e längsta 
 --- | ---| ---| ---| ---| ---| ---| ---| ---| ---| ---
Osorterad  | 0.00394 | 0.00785 | 0.01074 | 0.01667 | 0.01864 | 0.0222 | 0.02535 | 0.02917 | 0.03275 | 0.03697
sorterad| 0.016| 0.0156| 0.0161| 0.0157| 0.0152| 0.0158| 0.0162| 0.016| 0.0159| 0.0159

N=20 | 1:a längsta | 2:a längsta | 3:e längsta | 4:e längsta | 5:e längsta | 6:e längsta | 7:e längsta | 8:e längsta | 9:e längsta | 10:e längsta 
 --- | ---| ---| ---| ---| ---| ---| ---| ---| ---| ---
Osorterad  | 0.00763 | 0.01552 | 0.02169 | 0.02709 | 0.03495 | 0.04181 | 0.0474 | 0.05646 | 0.06093 | 0.06972
sorterad| 0.0368| 0.0363| 0.036| 0.0405| 0.036| 0.0366| 0.0356| 0.036| 0.0354| 0.036

N=30 | 1:a längsta | 2:a längsta | 3:e längsta | 4:e längsta | 5:e längsta | 6:e längsta | 7:e längsta | 8:e längsta | 9:e längsta | 10:e längsta 
 --- | ---| ---| ---| ---| ---| ---| ---| ---| ---| ---
Osorterad  | 0.01032 | 0.02004 | 0.02941 | 0.03974 | 0.04988 | 0.05963 | 0.07008 | 0.07967 | 0.08858 | 0.09907
sorterad| 0.0524| 0.0532| 0.0527| 0.0535| 0.0531| 0.0526| 0.0534| 0.052| 0.0538| 0.0527

