import socket 

PORT_NUMBER=5000
IP_ADDR = "127.0.0.1"







def main(): 
    
    
    
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    s.connect((IP_ADDR,PORT_NUMBER))
    print(f'Connected to server with IP address {IP_ADDR} on port number {PORT_NUMBER}')
    
    
    print("You are the client and in the program you will send a wildcard that will be queried")
    print("This query will send a list of words that start with the first letter and last letter of your query with the same length")
    print("What is the wildcard you want queried from the server? ")
    wildcard_input=input()
    
    print(f"The wildcard you want queried is {wildcard_input}")

    s.send(wildcard_input.encode("utf-8"))
        

    print(s.recv(10000))
    

    s.close()
    
if __name__ == "__main__":
    main()
