import socket
from collections import defaultdict

PORT_NUMBER=5000
IP_ADDR= "127.0.0.1"

#RESPONSE CODES

SUCCESSFULL_QUERY=200
SUCCESSFULL_NOQUERY=204
INVALID_QUERY=400




def pattern_algorithm(wildcard_input):
    index_dict={}
    for i in range(len(wildcard_input)):
        if(wildcard_input[i].isalpha()):
            index_dict[i] = wildcard_input[i]
    return index_dict


def open_file(path="/home/hossainmahatheer/Downloads/wordlist.txt"):
    words_list=defaultdict(list)
    with open(path,'r') as f:

        all_words=f.readlines()

        for word in all_words:
        
            word_length= len(word.strip())
             

            words_list[word_length].append(word.strip())
        
    return words_list


def query(client_wildcard,words_list):
        len_word=len(client_wildcard)
        word_set=set()

        contains_query=False
        
        index_dict= pattern_algorithm(client_wildcard)
        
        if(len_word not in words_list):
            contains_query=False

        elif(len(index_dict) == 0):
           for word in words_list[len_word]:
               
                word_set.add(word)
                contains_query=True
        else:
            for word  in words_list[len_word]:
            
                
                
                
                mismatch= False
                for index,letter in index_dict.items():
                    if word[index] == letter:
                        continue
                    else:
                        mismatch=True
                        break
                if(mismatch):
                    continue
                else:
                    word_set.add(word)
                    contains_query=True

        if(contains_query):

            response_code=SUCCESSFULL_QUERY
        else:
            response_code=SUCCESSFULL_NOQUERY

        return word_set, response_code


def main():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

  
    s.bind((IP_ADDR,PORT_NUMBER))
    
    s.listen(5)
    

    words_list=open_file()
    
   # print("Printing words with word length three through words_list[3]")
   # print(words_list[3])
    while True:
        response_code=None

        client_socket,addr= s.accept()
        print(f"Connected to {addr}")
        client_message = client_socket.recv(1024).decode().strip()
        if(len(client_message) == 0 or  not client_message or client_message.strip() == ""):
            response_code= INVALID_QUERY
            client_socket.send(f"Status code: {response_code} - Bad Request: Invalid Length".encode("utf-8"))
            continue

        print(f"The wildcard the client wants to query is {client_message} and the length of the word is {len(client_message)}")
        query_list,response_code= query(client_message,words_list)
        
        if response_code == SUCCESSFULL_NOQUERY:
            client_socket.send(f"Status Code: {response_code} -Successful request but no query found for wildcard {client_message}".encode("utf-8"))
            continue
        else:
            query_formatted= " ".join(query_list)
            print(query_formatted)
            client_socket.send(f"Status Code: {response_code} - Query found for wildcard {client_message}. The query is {query_formatted}".encode("utf-8")) 
            

     


if __name__== "__main__":
    main()

