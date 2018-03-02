def group_by_owners(dictionary):
    #loop through dictionary

    result_dict = {}
    for value in dictionary.values(): #['Randy', 'Stan', 'Randy']
        result_arr = []
        for key in dictionary.keys(): #['Input.txt', 'Code.py', 'Output.txt']
            #if the value of one key is the same as another, put the keys in a list 
            if dictionary[key] == value:
                if value not in result_arr:
                    result_arr.append(key)#['Input.txt']
                    result_dict[value] = result_arr #{'Randy': ['Input.txt']}

    return result_dict

#res = group_by_owners( {'Input.txt': 'Randy', 'Code.py': 'Stan', 'Output.txt': 'Randy'})

#print(res)

def is_palindrome(word):
        #normalize string
        word = word.lower()
        #split into array
        word_arr = list(word)
        
        #reverse array
        reversed_array = list(reversed(word_arr))
        
        #compare array elements
        l = len(word_arr)
        for i in range(l-1):
            if word_arr[i] != reversed_array[i]:
                return False
            
            return True

res = is_palindrome('Deleveled')
print(res)
