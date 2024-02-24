import random
from collections import deque
from getting_data import *

class Encryption(Data_Prep):
     

    def __init__(self,file:str):
        super().__init__(file)
        self.break_to_16() 
        self.cross_over_points = None
        self.mutations = None
        self.permutation_factor = None
        self.private_random_num = None
        self.params = None 

    def generate_params(self):
        cross_temp = []
        mutation_temp = [] 
        while len(cross_temp)!= 4:
             
            n = random.randint(0,15)
            if n not in cross_temp:

                cross_temp.append(n)
        cross_temp.sort()
        while len(mutation_temp)!= 3:
            r = random.randint(0,15)
            if r not in mutation_temp:
                mutation_temp.append(r)
        


        self.cross_over_points = cross_temp
        self.mutations = mutation_temp 
        self.permutation_factor = random.randint(1,8)
        self.private_random_num = random.randint(0,15)
    
    def gen_algo(self,ind,cross_over_points,mutations):
        
        #print(self.cross_over_points) 
        
        
        for i in range(cross_over_points[0]+1,cross_over_points[1]+1):
                     #print(i) 
                     c = self.parts_16[ind][i] 
                     self.parts_16[ind][i] = self.parts_16[ind+1][i]
                     self.parts_16[ind+1][i] = c
        for j in range(cross_over_points[2]+1,cross_over_points[3]+1):
                     c1 = self.parts_16[ind][j]
                     self.parts_16[ind][j] = self.parts_16[ind+1][j]
                     self.parts_16[ind+1][j] = c1
        for mu in mutations:
                     self.parts_16[ind][mu] = 128 - self.parts_16[ind][mu]
                     self.parts_16[ind+1][mu] = 128 - self.parts_16[ind+1][mu]



    def public_key_gen(self):
        self.generate_params()
        f_op = open("public_key.txt",'w')
        f_op.write(str(self.cross_over_points))
        f_op.write("\n")
        f_op.write(str(self.mutations))
        f_op.write("\n") 
        f_op.write(str(self.permutation_factor))
        f_op.write("\n") 
        f_op.write(str(self.private_random_num))
        f_op.close()
    

    def private_key_gen(self):
        self.params = self.cross_over_points + self.mutations + self.permutation_factor + self.private_random_num 

    #     pass 
    #    params = self.cross_over_points + self.mutations + [self.permutation_factor] + [self.private_random_num]
    #    params = sum(params,[])

   
        
    


    def encryption(self):
        per = self.permutation_factor
        params = self.cross_over_points + self.mutations
        for ind in range(0,len(self.parts_16),2):
            if ind ==0:
                self.gen_algo(ind,self.cross_over_points,self.mutations)
            else:
                params = deque(params)
                params.rotate(-1*per)
                params = list(params)
                cross_temp = []
                mutation_temp = []
                c = 0

                for i in params:
                    if c<4:
                        cross_temp.append(i)
                    elif c>3 and c<7:
                        mutation_temp.append(i)
                
                self.gen_algo(ind,cross_temp,mutation_temp)
            f = open("encrypt.txt",'wb')
            bytea = sum(self.parts_16,[])
            bytess = bytes(bytea)
            f.write(bytess)
            f.close()
    

    



                

         
        
if __name__ == "__main__":
        obj = Encryption(file ="./getting_data.py")
        #obj.generate_params()
        obj.public_key_gen()
        obj.encryption()
        #obj.encryption()
        #obj.cross_over()
        

