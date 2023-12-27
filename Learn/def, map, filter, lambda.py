def square(x):
    return x * x
l = [1,2,3,4,5]
print(list(map(square, l)))

def adult(age):
    return age>=18
ages = [14,18,21,16,30]
print(list(filter(adult, ages)))

adult_lambda = lambda age: age>=18
print(list(filter(adult_lambda, ages)))
print(list(map(square, l)))

multi = lambda x,y: x*y
print(multi(5,6))