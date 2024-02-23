class Stack:

    def __init__(self):
        # Для хранения элементов в списке используем приватный атрибут. 
        # На его приватность указывают два подчёркивания в имени.
        self.__items = []

    def push(self, item):
        """Добавить элемент в стек."""
        self.__items.append(item)

    def pop(self):
        """Взять элемент из стека."""
        return self.__items.pop()

    def peek(self):
        """Посмотреть последний элемент без изъятия."""
        return self.__items[-1]

    def size(self):
        """Вернуть размер стека."""
        return len(self.__items) 