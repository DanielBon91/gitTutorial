#LEGB Lokal, Enclosing, Global, BuildIn

x = 'Global'

def greet():
    x = 'Enclose'
    print(x)

    def nested():
        x = 'Local'
        print(x)
    nested()

greet()
print(x)

#Enclose
#Local
#Global