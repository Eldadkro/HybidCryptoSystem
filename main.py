# %%

from Knapsack.Knapsak import Knapsack
from ellipticcurve.ecdsa import ElipticDSA
from player import player


def main():

    print("system initing - creating keys for each party and publishing public keys")
    a_ecdsa = ElipticDSA()
    a_knap = Knapsack()
    b_ecdsa = ElipticDSA()
    b_knap = Knapsack()

    players = [
        player(
            "alice",
            a_knap,
            Knapsack(pub_key=b_knap.public_key),
            a_ecdsa,
            ElipticDSA(publicKey=b_ecdsa.public)
        ),
        player(
            "bob",
            b_knap,
            Knapsack(pub_key=a_knap.public_key),
            b_ecdsa,
            ElipticDSA(publicKey=a_ecdsa.public)
        )
    ]

    while True:
        print("choose user by entering it's number, enter exit to exit:")
        while(True):
            for i, p in enumerate(players):
                print("{0}. {1}".format(i, p.__repr__()))
            index = input()
            try:
                if(index == "exit" or int(index) >= 0 and int(index) < len(players)):
                    break
            except:
                print("incorrect input try again...")
        if(index == "exit"):
            return
        try:
            sender = players[int(index)]
            receiver = players[(int(index) + 1) % 2]
        except:
            print("invalid user chosen")

        print("enter msg to send to the other user:")
        msg = input()
        
        if(not sender.des):
            verification = receiver.keyexchange(sender.keyexchange())
            print("key exchange happend and the signature is: ",verification)
        y = sender.send(msg, receiver.name)
        print("the encrypted message:")
        print(y)
        print("\n")
        recived_msg = receiver.recive(y)
        x = recived_msg[0]
        sign = recived_msg[1]
        print("signature verification: ", sign)
        print("mail content:")
        print("#"*40)
        print("-"*40)
        for title,contant in x.items():
            print(title," : ")
            index=0
            while(index < len(contant)):
                print(contant[index:index+40])
                index += 40
            print("-"*40)
        print("#"*40)
        


if __name__ == "__main__":
    main()

# %%
