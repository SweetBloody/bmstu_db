from task_1 import task_1
from task_2 import task_2
from task_3 import task_3

def menu():
  print("------------------MENU------------------")
  print("1. LINQ to Object")
  print("2. LINQ to XML/JSON")
  print("3. LINQ to SQL")
  print("0. Выход")
  print("----------------------------------------")


def input_choice(a, b):
  choice = -1
  while choice < a or choice > b:
    try:
      choice = int(input("> "))
      if choice < a or choice > b:
        print("Введите число от {} до {}".format(a, b))
    except Exception:
        print("Введите число от {} до {}".format(a, b))
  return choice

if __name__ == "__main__":
    while True:
        menu()
        choice = input_choice(0, 3)
        if choice == 1:
            task_1()
        elif choice == 2:
            task_2()
        elif choice == 3:
            task_3()
        else:
            break