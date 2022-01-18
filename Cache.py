import numpy as np
import math

class Cache:
    def __init__(self, address_size, cache_data_size, block_size, cache_type, n_way = 4):
        
        self.address_size = address_size
        self.cache_data_size = cache_data_size
        self.block_size = block_size
        
        if(cache_type == 'direct map'):
            self.number_of_rows = self.cache_data_size / self.block_size
            self.number_of_offsets = math.log(block_size, 2)
            self.number_of_indexes = math.log(self.number_of_rows, 2)
            self.number_of_tags = self.address_size - (self.number_of_indexes + self.number_of_offsets)
            self.length_of_row = 1 + self.number_of_tags + (self.block_size * 8) # valid + tags + data
            self.cache_array = np.zeros((int(self.number_of_rows), int(self.length_of_row))) # creating array(cache) with zeros
            
        elif(cache_type == 'set associative'):
            self.number_of_blocks = n_way
            self.number_of_rows = self.cache_data_size / (self.block_size * self.number_of_blocks)
            self.number_of_offsets = math.log(block_size, 2)
            self.number_of_indexes = math.log(self.number_of_rows, 2)
            self.number_of_tags = self.address_size - (self.number_of_indexes + self.number_of_offsets)
            self.length_of_row = 1 + self.number_of_tags + (self.block_size * 8) # (valid + tags + data) * n-way
            
             # creating array(cache) with zeros
            self.cache_array = np.zeros((n_way, int(self.number_of_rows), int(self.length_of_row)))
        
        self.hit = 0
        self.miss = 0
        self.total = 0
        
    def show(self):
        print("tags: ",self.number_of_tags)
        print("indexes: " ,self.number_of_indexes)
        print("offsets: " ,self.number_of_offsets)
        print("rows: ",self.number_of_rows)
        
    def Direct_map(self, address):
        self.total += 1
        index = address % self.block_size # modulo for index
        current_block = self.cache_array[index] # find the block with index 
        tags = current_block[1 : int(self.number_of_tags) + 1] # slice block for it's tag
        
        binary_address = '{:032b}'.format(address) # convert number to binary
        address_tag = binary_address[ :int(self.number_of_tags)] # get the tag of address from address in binary
        block_tag =  ''.join(str(int(x)) for x in tags) # [0, 0, 0, 1] => "0001"
        
        if(int(current_block[0]) == 0):
            # validate as the block which has data
            current_block[0] = 1
            # change the tag of the block with the address block
            for i, x in enumerate(current_block[1 : int(self.number_of_tags)+ 1]):
                current_block[i + 1] = address_tag[i]
            self.miss += 1
            return print("miss occured for {}. ".format(address) + "validated and data saved \n")
        
        # check whether block's tag and address's tag are equal or not
        if(block_tag == address_tag):
            print("hit occured for {}.\n".format(address))
            self.hit += 1
            return
        else: 
            print("miss occured for {}.\n".format(address))
            self.miss += 1
            for i, x in enumerate(current_block[1 : int(self.number_of_tags)+ 1]):
                current_block[i + 1] = address_tag[i]
            return
        
    def FIFO(self, address):
        self.total +=1
        first_in = 0 # index of the first block which entered to remove it first => FIFO
        index = address % self.number_of_blocks # modulo for index
        current_row = self.cache_array[:, index] # find the blocks in the index row
        
        binary_address = '{:032b}'.format(address) # convert number to binary
        address_tag = binary_address[ :int(self.number_of_tags)] # get the tag of address from address in binary
            
        for block in current_row:
            if(int(block[0]) == 0):
                # validate as the block which has data
                block[0] = 1
                # change the tag of the block with the address block
                for i, x in enumerate(block[1 : int(self.number_of_tags)+ 1]):
                    block[i + 1] = address_tag[i]
                self.miss += 1
                return print("miss occured for {}. ".format(address) + "validated and data saved \n")
                
                
            # check whether block's tag and address's tag are equal or not
            tags_of_block = block[1 : int(self.number_of_tags) + 1] # slice block for it's tag
            string_tag =  ''.join(str(int(x)) for x in tags_of_block) # example:[0, 0, 0, 1] => "0001" for comparison
            
            if (str(address_tag) == str(string_tag)):
                print("hit occured for {}.\n".format(address))
                self.hit += 1
                return
        
        if(first_in > self.number_of_blocks):
            first_in = 0
            
        print("miss occured for {}.\n".format(address))
        self.miss += 1
        for i, x in enumerate(current_row[first_in, 1 : int(self.number_of_tags)+ 1]):
            block[i + 1] = address_tag[i]
        first_in += 1
        return
            
    
    
    
    def performance(self):
        
        miss_percent = (self.miss / self.total) * 100
        print("miss: {}% \n".format(miss_percent))
        
        hit_percent = (self.hit / self.total) * 100
        print("hit: {}%".format(hit_percent))
        


cache = Cache(32, 2048, 32, 'direct map')
cache.show()


sample_data = np.random.randint(0, 2000, size=10000) # generating 10000 random address between 0 and 2000 

for num in sample_data:
    cache.Direct_map(num)

cache.performance()


# cache_set_associative = Cache(32, 2048, 32, 'set associative', 4)
# cache_set_associative.show()

# for num in sample_data:
#     cache_set_associative.FIFO(num)

#     cache_set_associative.performance()