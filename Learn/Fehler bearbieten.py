def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as ex:
        print(f'Fehler: {ex}')

print(divide(6,0))
