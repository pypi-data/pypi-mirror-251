def _help():
    print('''
Алфавит:
ж - zh
х - kh
ц - ts
ч - ch
ш - sh
щ - shch
ю - yu
я - ya

Заметки:
1) Если функции совпадают в 5 буквах, пишется 6-ая (7-ая или 8-ая) (для помощи используйте Tab)
2) Слова в () и в {} учитываются
3) Цифры, переменные, примеры по типу 'hello world', 'l' и 'o' → 'he wrd' не учитываются.
4) Фразы "Метод должен изменять исходный список" и " Функция должна возвращать отсортированный список." не учитываются
5) Примеры учитываются (смотрим на русские слова)

Проблема с Бинарным деревом:
1) В методе __str__ исправтьте строчку на '\н'.join(self._display(self.root)[0]) !!!н поменяйте на n!!!
2) Найдите переменную second_line (в двух местах) и добавьтее к '\' второй такой же слэж 

Задачи по группам:
1) Лямбда-функции: fchyaks, bstsk, lpschsi, isusd, nipsu, pyaksz, chsrchd, pavzs, lpssszva, lpschsz, evpks, lichsz, nipchd, chpyaks, rvbts, ndnin, tstsks, chspvch, tnzks, kchyaks, achyaks, akvpn, lpschts, lpschz, pivia, lichsz, lpssszvch     
2) Сортировки: kkemi, skvbg, chpobd, skdup, kkevv, skvzi, applv
3) Классы (с дочерними): Автомобиль - khzsap, Фильм - rivgz, Продукт - sitszs, Животное - oipzs, Студент - dtibs
4) Классы: Банк - fuvko, Круг - tstsirr, Студент - vvisv, Recipe - dtiyai, Animal - zhtsups, Student - suknf, Книга - igpkd, BankAccount - sokvv, Movie - fzhups, Прямоугольник - pppds
5) Двусвязный список: nneei, nsitn, sdvev, sdvem, sieui, sivii, sdvek
6) Стэк: sedkya, sepdya, chchyank
7) Бинарное дерево поиска: pdbvn, pdbvz
8) Очередь: ddnot, ddnot, upobd
9) Хеш-таблица: tyaovkh, tyaovkhdoa
10) Быстрая сорт: sbapsd
11) Пузырьком сорт: psaps
12) Вставками сорт: vsapsa, vsapsu
13) Выбором сорт: vsapss

Интересные методы:
1) a.lower() - преобразует строку в нижний регистр
2) a.isdigit() - проверка на цифру
3) a.isupper() - проверка на большие буквы
4) isinstance(obj, class) принадлежит ли объект определенному типу или нет

Вывод функций подряд:
a = ['fchyaks', 'bstsk', 'lpschsi', 'isusd', 'nipsu', 'pyaksz', 'chsrchd', 'pavzs', 'lpssszva', 'lpschsz', 'evpks']
for i in (getattr(exam, b) for b in a):
    print('\n')
    i()''')

#Допка
def HashTable():
    print('''
class HashTable:
    def __init__(self):
        self.size = 10
        self.table = [[] for _ in range(self.size)]

    def _hash_func(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        hash_key = self._hash_func(key)
        for idx, kv in enumerate(self.table[hash_key]):
            k, v = kv
            if key == k:
                self.table[hash_key][idx] = (key, value)
                break
        else:
            self.table[hash_key].append((key, value))

    def search(self, key):
        hash_key = self._hash_func(key)
        for k, v in self.table[hash_key]:
            if key == k:
                return v
        raise KeyError(key)

    def delete(self, key):
        hash_key = self._hash_func(key)
        for idx, kv in enumerate(self.table[hash_key]):
            k, v = kv
            if key == k:
                del self.table[hash_key][idx]
                return
        raise KeyError(key)

    def display(self):
        print("{:<15} {}".format("Key", "Value"))
        print("---------------")
        for bucket in self.table:
            for k, v in bucket:
                print("{:<15} {}".format(k, v))


Метод `display` выводит все ключи и значения на экран, отформатированные в виде таблицы с двумя столбцами. Он проходит по каждой корзинке хэш-таблицы и для каждой пары ключ-значение выводит строку в формате `"{:<15} {}"`, где `'{:<15}'` означает, что первый столбец должен занимать 15 символов и быть выровнен по левому краю, а `{}` - это второй столбец со значением.''')
    
#1
def fchyaks():
    print('''#Используя лямбда-функцию, найдите все числа в заданном списке, которые являются числами Фибоначчи.

is_fibo = (lambda a: lambda v,fib=0,n=1: a(a,v,fib,n))(lambda f,value,fib,n: f(f,value,fib+n,fib) if fib < value else fib==value)

# Заданный список чисел
numbers = list(range(100))

# Использование лямбда-функции для фильтрации чисел Фибоначчи из списка
fibonacci_numbers = list(filter(is_fibo, numbers))

# Вывод результатов
print(fibonacci_numbers)''')
    
def kkemi():
    print('''#Напишите программу для сортировки заданного списка кортежей по разности между максимальным и минимальным элементами каждого кортежа.

# Заданный список кортежей
tuples = [(3, 8, 2), (1, 5, 10), (4, 7, 6), (2, 9, 1)]

# Функция для получения разности между максимальным и минимальным элементами кортежа
get_diff = lambda tuple: max(tuple) - min(tuple)

# Сортировка списка кортежей по разности между максимальным и минимальным элементами
sorted_tuples = sorted(tuples, key=get_diff)

# Вывод отсортированного списка кортежей
print(sorted_tuples)''')
    
def bstsk():
    print('''#Используя лямбда-функцию, найдите все строки в заданном списке строк, которые содержат только согласные буквы.

# Заданный список строк
strings = ['hll', 'wrld', 'bye', 'peace', 'aisd', 'sht']

# Функция для проверки строки на наличие только согласных букв
is_consonant = lambda s: all(letter.lower() not in 'aeiou' for letter in s)

# Фильтрация списка строк с помощью лямбда-функции
consonant_strings = list(filter(is_consonant, strings))

# Вывод результатов
print(consonant_strings)''')
    
def sieui():
    print('''#Реализовать функцию, которая находит максимальный элемент в двусвязном списке и удаляет его из списка. 

#реализация двусвязного списка
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
            new_node.prev = current

    def delete_node(self, data):
        if self.head is None:
            return
        elif self.head.data == data:
            if self.head.next is not None:
                self.head = self.head.next
                self.head.prev = None
            else:
                self.head = None
        else:
            current = self.head
            while current.next is not None and current.next.data != data:
                current = current.next
            if current.next is None:
                return
            else:
                current.next = current.next.next
                if current.next is not None:
                    current.next.prev = current

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self):
        if self.head == None:
            return f"Двусвязный список пустой"
        current = self.head
        dllist_str = ""
        while current:
            dllist_str += " ⇄ " + str(current.data)
            current = current.next
        return dllist_str.lstrip(" ⇄ ") 
    
#программа

def find_and_remove_max(dllist):
    if dllist.head is None:
        return None

    current = dllist.head
    max_node = current

    # Находим узел с максимальным значением
    while current.next:
        current = current.next
        if current.data > max_node.data:
            max_node = current

    # Удаляем узел с максимальным значением
    if max_node.prev:
        max_node.prev.next = max_node.next
    else:
        dllist.head = max_node.next

    if max_node.next:
        max_node.next.prev = max_node.prev

    return max_node.data

#проверка
dllist = DoublyLinkedList()
dllist.add_node(5)
dllist.add_node(10)
dllist.add_node(8)
dllist.add_node(3)

print("Изначальный список:", dllist)
max_value = find_and_remove_max(dllist)
print("Максимальное значение:", max_value)
print("Список после удаления максимального элемента:", dllist)''')

#2    
def lpschsi():
    print('''#Отфильтровать список целых чисел на простые и составные числа с помощью лямбда-функции.

# Заданный список целых чисел
numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10]

# Лямбда-функция для проверки числа на простоту
is_prime = lambda num: all(num % i != 0 for i in range(2, int(num**0.5) + 1)) and num > 1

# Фильтрация списка на простые числа
prime_numbers = list(filter(is_prime, numbers))

# Фильтрация списка на составные числа
composite_numbers = list(filter(lambda num: not is_prime(num), numbers))

prime_numbers, composite_numbers''')
    
def isusd():
    print('''#Для удаления определённых символов из заданной строки используйте лямбда-функцию. Пример: дана строка 'hello world', удалить символы 'l' и 'o' → 'he wrd'.

string = 'hello world'
characters_to_remove = ['l', 'o']

# Функция для удаления символов из строки
remove_characters = lambda s: ''.join([char for char in s if char not in characters_to_remove])

# Применение лямбда-функции к строке
result = remove_characters(string)

# Вывод результата
print(result)''')
    
def nipsu():
    print('''#Используя лямбда-функцию, проверить, является ли указанный список палиндромом или нет

is_pal = lambda x: (x == (x[::-1]))

lst1 = [1,2,1]
lst2 = [1,2,3]
lst3 = ['a','b','a']
lst4 = ['a','b','c']

is_pal(lst1), is_pal(lst2), is_pal(lst3), is_pal(lst4)''')

def nsitn():
    print('''#Реализовать функцию, которая проверяет, является ли двусвязный список палиндромом (элементы списка читаются одинаково как слева направо, так и справа налево)

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
            new_node.prev = current

    def delete_node(self, data):
        if self.head is None:
            return
        elif self.head.data == data:
            if self.head.next is not None:
                self.head = self.head.next
                self.head.prev = None
            else:
                self.head = None
        else:
            current = self.head
            while current.next is not None and current.next.data != data:
                current = current.next
            if current.next is None:
                return
            else:
                current.next = current.next.next
                if current.next is not None:
                    current.next.prev = current

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self):
        if self.head == None:
            return f"Двусвязный список пустой"
        current = self.head
        dllist_str = ""
        while current:
            dllist_str += " ⇄ " + str(current.data)
            current = current.next
        return dllist_str.lstrip(" ⇄ ")   
    
#программа

def is_palindrome(dllist):
    if dllist.head is None:
        return True

    # Получаем длину списка
    length = len(dllist)

    # Объявляем два указателя, один идет с начала списка, другой - с конца
    front = dllist.head
    back = dllist.head

    # Перемещаем указатель back к последнему элементу списка
    while back.next:
        back = back.next

    # Проверяем значения элементов, двигая указатели front и back
    while front != back and front.prev != back:
        if front.data != back.data:
            return False
        front = front.next
        back = back.prev

    return True

dllist = DoublyLinkedList()
dllist.add_node(1)
dllist.add_node(2)
dllist.add_node(3)
dllist.add_node(2)
dllist.add_node(1)

print(dllist)
print(is_palindrome(dllist))  # Вывод: True

dllist.add_node(4)
print('\n', dllist)
print(is_palindrome(dllist))  # Вывод: False''')

#3    
def fuvko():
    print('''#Создайте класс «Банк» с атрибутами название, адрес и список клиентов.
Каждый клиент представлен классом «Клиент» с атрибутами имя,
фамилия, номер счета и баланс. Напишите методы для добавления
клиента в банк, удаления клиента из банка и вывода информации
о банке в виде «Банк '{название}', адрес - {адрес}, клиенты - {список
клиентов}». Используйте магический метод __str__ для вывода
информации о клиенте в удобном формате.

class Bank:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.clients = []
    
    def add_client(self, client):
        self.clients.append(client)
    
    def remove_client(self, client):
        if client in self.clients:
            self.clients.remove(client)
        else:
            print('Клиента нет в базе')
    
    def __str__(self):
        client_info = '\n'.join(str(client) for client in self.clients)
        return f"Банк '{self.name}', адрес - {self.address}, клиенты:\n{client_info}"  

class Client:
    def __init__(self, name, surname, account, balance):
        self.name = name
        self.surname = surname
        self.account = account
        self.balance = balance 
    def __str__(self):
        return f"Клиент: {self.name} {self.surname}, Номер счета: {self.account}, Баланс: {self.balance}"
    
bank = Bank("MFBank", "123 Ryasansky Avenue")

client1 = Client("Russell", "Westbrook", "8954792453", 10000)
client2 = Client("Busta", "Rhimes", "4472933908", 99999)

bank.add_client(client1)
bank.add_client(client2)

print(bank)''')
    
def sedkya():
    print('''# Дан стек. Необходимо проверить, содержит ли он хотя бы один элемент,
# который является квадратом другого элемента стека.

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def push(self, item):
        new_node = Node(item)
        new_node.next = self.head
        self.head = new_node

    def pop(self):
        if self.is_empty():
            return None
        else:
            popped_item = self.head.data
            self.head = self.head.next
            return popped_item

    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.head.data

    def __str__(self):
        current = self.head
        stack_str = ""
        while current:
            stack_str += str(current.data) + " → "
            current = current.next
        return stack_str.rstrip(" → ")

#программа

def square(stack):
    if stack.is_empty():
        return False

    # Создаем множество для хранения уникальных элементов стека
    unique_elements = set()

    # Проходим по всем элементам стека
    current = stack.head
    while current:
        # Проверяем, является ли текущий элемент квадратом другого элемента
        if current.data ** 2 in unique_elements:
            return True

        # Добавляем текущий элемент в множество уникальных элементов
        unique_elements.add(current.data)

        current = current.next

    return False

lst1 = [1,2,3,5,9,25]
lst2 = [1,3,5,7,11,13,17]

stack1 = Stack()
stack2 = Stack()

for item in lst1:
    stack1.push(item)

for item in lst2:
    stack2.push(item)

print(f'Стек 1: {stack1}, {square(stack1)}')
print(f'Стек 2: {stack2}, {square(stack2)}')''')

#4    
def khzsap():
    print('''# Создайте класс АВТОМОБИЛЬ с методами, позволяющими вывести на
# экран информацию об автомобиле, а также определить, подходит ли
# данный автомобиль для заданных условий. Создайте дочерние классы
# ЛЕГКОВОЙ (марка, модель, год выпуска, объем двигателя, тип
# топлива), ГРУЗОВОЙ (марка, модель, год выпуска, грузоподъемность),
# ПАССАЖИРСКИЙ (марка, модель, год выпуска, количество мест) со
# своими методами вывода информации на экран и определения
# соответствия заданным условиям. Создайте список автомобилей,
# выведите полную информацию из базы на экран, а также организуйте
# поиск автомобилей с заданными характеристиками.

class Car:
    def __init__(self, brand, model, year, engine_capacity):
        self.brand = brand
        self.model = model
        self.year = year
        self.engine_capacity = engine_capacity

    def display_info(self):
        print(f"Марка: {self.brand}")
        print(f"Модель: {self.model}")
        print(f"Год выпуска: {self.year}")
        print(f"Объем двигателя: {self.engine_capacity} л")

    def is_matching(self, conditions):
        for key, value in conditions.items():
            if getattr(self, key) != value:
                return False
        return True


class PassengerCar(Car):
    def __init__(self, brand, model, year, engine_capacity, fuel_type, seats):
        super().__init__(brand, model, year, engine_capacity)
        self.fuel_type = fuel_type
        self.seats = seats

    def display_info(self):
        super().display_info()
        print(f"Тип топлива: {self.fuel_type}")
        print(f"Количество мест: {self.seats}")

    def is_matching(self, conditions):
        if not super().is_matching(conditions):
            return False
        if 'fuel_type' in conditions and self.fuel_type != conditions['fuel_type']:
            return False
        if 'seats' in conditions and self.seats < conditions['seats']:
            return False
        return True


class FreightCar(Car):
    def __init__(self, brand, model, year, engine_capacity, load_capacity):
        super().__init__(brand, model, year, engine_capacity)
        self.load_capacity = load_capacity

    def display_info(self):
        super().display_info()
        print(f"Грузоподъемность: {self.load_capacity} т")

    def is_matching(self, conditions):
        if not super().is_matching(conditions):
            return False
        if 'load_capacity' in conditions and self.load_capacity < conditions['load_capacity']:
            return False
        return True


class PassengerVan(Car):
    def __init__(self, brand, model, year, engine_capacity, seats):
        super().__init__(brand, model, year, engine_capacity)
        self.seats = seats

    def display_info(self):
        super().display_info()
        print(f"Количество мест: {self.seats}")

    def is_matching(self, conditions):
        if not super().is_matching(conditions):
            return False
        if 'seats' in conditions and self.seats < conditions['seats']:
            return False
        return True
    
cars = [
    PassengerCar("Toyota", "Camry", 2020, 2.5, "бензин", 5),
    FreightCar("Volvo", "FH16", 2018, 13.0, 30),
    PassengerVan("Mercedes-Benz", "Sprinter", 2019, 2.2, 9)
]

# Вывод полной информации о всех автомобилях
for car in cars:
    car.display_info()
    print()

# Поиск автомобилей по заданным характеристикам
search_conditions = {
    'brand': "Toyota",
    'engine_capacity': 2.5
}

matching_cars = [car for car in cars if car.is_matching(search_conditions)]

if matching_cars:
    print("Результаты поиска:")
    for car in matching_cars:
        car.display_info()
else:
    print("Нет автомобилей, удовлетворяющих заданным характеристикам.")
''')


def sdvev():
    print('''# Реализовать функцию, которая находит произведение квадратов всех
# элементов в двусвязном списке.

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
            new_node.prev = current

    def delete_node(self, data):
        if self.head is None:
            return
        elif self.head.data == data:
            if self.head.next is not None:
                self.head = self.head.next
                self.head.prev = None
            else:
                self.head = None
        else:
            current = self.head
            while current.next is not None and current.next.data != data:
                current = current.next
            if current.next is None:
                return
            else:
                current.next = current.next.next
                if current.next is not None:
                    current.next.prev = current

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
    
    def calculate_square_product(self):
        if self.head is None:
            return 1  # Если список пустой, возвращаем 1

        product = 1
        current = self.head
        while current:
            product *= current.data ** 2
            current = current.next

        return product
    
    def __str__(self):
        if self.head == None:
            return f"Двусвязный список пустой"
        current = self.head
        dllist_str = ""
        while current:
            dllist_str += " ⇄ " + str(current.data)
            current = current.next
        return dllist_str.lstrip(" ⇄ ")  
    
dllist = DoublyLinkedList()
dllist.add_node(2)
dllist.add_node(3)
dllist.add_node(4)
dllist.add_node(5)

square_product = dllist.calculate_square_product()
print(dllist)
print("Произведение квадратов элементов в списке:", square_product)''')

#5    
def rivgz():
    print('''# Создайте класс ФИЛЬМ с методами, позволяющими вывести на экран
# информацию о фильме, а также определить, подходит ли данный фильм
# для заданных условий. Создайте дочерние классы КОМЕДИЯ
# (название, год выпуска, режиссер, актеры), ДРАМА (название, год
# выпуска, режиссер, актеры), ФАНТАСТИКА (название, год выпуска,
# режиссер, актеры) со своими методами вывода информации на экран и
# определения соответствия заданным условиям. Создайте список
# фильмов, выведите полную информацию из базы на экран, а также
# организуйте поиск фильмов с заданным годом выпуска или режиссером.

class Film:
    def __init__(self, title, year, director, actors):
        self.title = title
        self.year = year
        self.director = director
        self.actors = actors

    def display_info(self):
        print("Фильм:", self.title)
        print("Год выпуска:", self.year)
        print("Режиссер:", self.director)
        print("Актеры:", ', '.join(self.actors))

    def matches_condition(self, year=None, director=None):
        if year and self.year != year:
            return False
        if director and self.director != director:
            return False
        return True


class Comedy(Film):
    def display_info(self):
        print("Комедия:")
        super().display_info()


class Drama(Film):
    def display_info(self):
        print("Драма:")
        super().display_info()


class Fantasy(Film):
    def display_info(self):
        print("Фантастика:")
        super().display_info()


# Создание списка фильмов
films = [
    Comedy("Комедия 1", 2000, "Режиссер 1", ["Актер 1", "Актер 2"]),
    Drama("Драма 1", 2005, "Режиссер 2", ["Актер 3", "Актер 4"]),
    Fantasy("Фантастика 1", 2010, "Режиссер 3", ["Актер 5", "Актер 6"]),
    Comedy("Комедия 2", 2000, "Режиссер 1", ["Актер 7", "Актер 8"]),
]

# Вывод полной информации о фильмах
for film in films:
    film.display_info()
    print()

# Поиск фильмов по заданным условиям
print("Фильмы, выпущенные в 2000 году:")
for film in films:
    if film.matches_condition(year=2000):
        film.display_info()
        print()

print("Фильмы режиссера 'Режиссер 1':")
for film in films:
    if film.matches_condition(director="Режиссер 1"):
        film.display_info()
        print()
''')
    
def pdbvn():
    print('''#Найти высоту бинарного дерева поиска

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None        

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        new_node = Node(data)
        if self.root is None:
            self.root = new_node
        else:
            current = self.root
            while True:
                if data < current.data:
                    if current.left is None:
                        current.left = new_node
                        break
                    else:
                        current = current.left
                else:
                    if current.right is None:
                        current.right = new_node
                        break
                    else:
                        current = current.right

    def search(self, data):
        current = self.root
        while current is not None:
            if data == current.data:
                return True
            elif data < current.data:
                current = current.left
            else:
                current = current.right
        return False

    def delete(self, data):
        if self.root is not None:
            self.root = self._delete(data, self.root)

    def _delete(self, data, node):
        if node is None:
            return node

        if data < node.data:
            node.left = self._delete(data, node.left)
        elif data > node.data:
            node.right = self._delete(data, node.right)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            temp = self._find_min_node(node.right)
            node.data = temp.data
            node.right = self._delete(temp.data, node.right)

        return node

    def _find_min_node(self, node):
        while node.left is not None:
            node = node.left
        return node

    def __str__(self):
        return '\n'.join(self._display(self.root)[0])

    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return 0
        else:
            left_height = self._height(node.left)
            right_height = self._height(node.right)
            return max(left_height, right_height) + 1


    def _display(self, node):
        if node.right is None and node.left is None:
            line = str(node.data)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        if node.right is None:
            lines, n, p, x = self._display(node.left)
            s = str(node.data)
            u = len(s)
            first_line = (x + 1)*' ' + (n - x - 1)*'_' + s
            second_line = x*' ' + '/' + (n - x - 1 + u)*' '
            shifted_lines = [line + u*' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        if node.left is None:
            lines, n, p, x = self._display(node.right)
            s = str(node.data)
            u = len(s)
            first_line = s + x*'_' + (n - x)*' '
            second_line = (u + x)*' ' + '\\' + (n - x - 1)*' '
            shifted_lines = [u*' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        left, n, p, x = self._display(node.left)
        right, m, q, y = self._display(node.right)
        s = str(node.data)
        u = len(s)
        first_line = (x + 1)*' ' + (n - x - 1)*'_' + s + y*'_' + (m - y)*' '
        second_line = x*' ' + '/' + (n - x - 1 + u + y)*' ' + '\\' + (m - y - 1)*' '
        if p < q:
            left += [n*' ']*(q - p)
        elif q < p:
            right += [m*' ']*(p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u*' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2
    
from random import shuffle

# создание объекта класса BinaryTree
tree = BinaryTree()

# создание списка элементов
items = list(range(1,11))
shuffle(items)

# добавление элементов в бинарное дерево
for item in items:
    tree.insert(item)

# вывод бинарного дерева на экран
print(items)
print(tree)
tree.height()''')

#6   
def pyaksz():
    print('''#Используя лямбда-функцию, найдите все числа в заданном списке,
которые являются палиндромами.
my_list = [121, 55, 4664, 10, 12321, 88, 67876]
palindromes = filter(lambda x: str(x) == str(x)[::-1], my_list)
print(list(palindromes))''')
    
def skvbg():
    print('''#Напишите программу для сортировки заданного списка строк по
количеству гласных букв в каждой строке
my_list = ['apple', 'peach', 'banana', 'watermelon', 'aboooooooooooba', 'lol', 'kk']

def count_vowels(word):
  vowels = 'aeiouAEIOU'
  k = 0
  for letter in word:
    if letter in vowels:
      k += 1
  return k


sorted_list = sorted(my_list, key = count_vowels)
print(sorted_list)''')
    
def chsrchd():
    print('''#Используя лямбда-функцию, найдите все числа в заданном списке,
которые являются совершенными числами (сумма делителей числа
равна самому числу).
my_list = [6, 12, 28, 9, 496, 99, 8128, 24]
perfect_nums = filter(lambda x: sum([i for i in range(1, x) if x % i == 0]) == x, my_list)
print(list(perfect_nums))''')

def pdbvz():
    print('''#Найти наибольший элемент, меньший заданного значения, в бинарном дереве поиска.
class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None        

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        new_node = Node(data)
        if self.root is None:
            self.root = new_node
        else:
            current = self.root
            while True:
                if data < current.data:
                    if current.left is None:
                        current.left = new_node
                        break
                    else:
                        current = current.left
                else:
                    if current.right is None:
                        current.right = new_node
                        break
                    else:
                        current = current.right

    def search(self, data):
        current = self.root
        while current is not None:
            if data == current.data:
                return True
            elif data < current.data:
                current = current.left
            else:
                current = current.right
        return False

    def delete(self, data):
        if self.root is not None:
            self.root = self._delete(data, self.root)

    def _delete(self, data, node):
        if node is None:
            return node

        if data < node.data:
            node.left = self._delete(data, node.left)
        elif data > node.data:
            node.right = self._delete(data, node.right)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            temp = self._find_min_node(node.right)
            node.data = temp.data
            node.right = self._delete(temp.data, node.right)

        return node

    def _find_min_node(self, node):
        while node.left is not None:
            node = node.left
        return node

    def __str__(self):
        return '\n'.join(self._display(self.root)[0])

    def _display(self, node):
        if node.right is None and node.left is None:
            line = str(node.data)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        if node.right is None:
            lines, n, p, x = self._display(node.left)
            s = str(node.data)
            u = len(s)
            first_line = (x + 1)*' ' + (n - x - 1)*'_' + s
            second_line = x*' ' + '/' + (n - x - 1 + u)*' '
            shifted_lines = [line + u*' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        if node.left is None:
            lines, n, p, x = self._display(node.right)
            s = str(node.data)
            u = len(s)
            first_line = s + x*'_' + (n - x)*' '
            second_line = (u + x)*' ' + '\\' + (n - x - 1)*' '
            shifted_lines = [u*' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        left, n, p, x = self._display(node.left)
        right, m, q, y = self._display(node.right)
        s = str(node.data)
        u = len(s)
        first_line = (x + 1)*' ' + (n - x - 1)*'_' + s + y*'_' + (m - y)*' '
        second_line = x*' ' + '/' + (n - x - 1 + u + y)*' ' + '\\' + (m - y - 1)*' '
        if p < q:
            left += [n*' ']*(q - p)
        elif q < p:
            right += [m*' ']*(p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u*' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2



def find_max(node, x):
  values = []
  if node == None:
    return []
  elif node.data < x:
    values.append(node.data)
  values += find_max(node.left, x)
  values += find_max(node.right, x)
  return values


from random import shuffle
t = list(range(1, 11))
shuffle(t)
tree = BinaryTree()
for i in t:
  tree.insert(i)

print(tree)


a = max(find_max(tree.root, 9))
a''')
    
#7
def tstsirr():
    print('''#Создайте класс «Круг» с атрибутами радиус и цвет. Напишите методы
для вычисления площади и длины окружности круга. Используйте
магический метод __str__ для вывода информации о круге в виде «Круг
радиуса {радиус} и цвета {цвет}»
from math import pi

class Circle():

  def __init__(self, radius, color = 'transparent'):
    self.radius = radius
    self.color = color

  def area(self):
    return pi * self.radius ** 2

  def length(self):
    return 2 * pi * self.radius

  def __str__(self):
    return f'Круг радиуса {self.radius} и цвета {self.color}'
    
c = Circle(3, 'red')
print(c)''')
    
    
def sdvem():
    print('''#Реализовать функцию, которая находит минимальный элемент в двусвязном списке

class Node():

  def __init__(self, data = None):
    self.data = data
    self.next = None
    self.prev = None

class DoublyLinkedList():

  def __init__(self):
    self.head = None

  def add_node(self, data):
    new_node = Node(data)

    if self.head is None:
      self.head = new_node
    else:
      cur = self.head
      while cur.next:
        cur = cur.next
      cur.next = new_node
      new_node.prev = cur
  
  def find_min(self):
    if self.head == None:
      return 'the list is empty'

    cur = self.head
    min = float('inf')
    while cur.next:
      if cur.data < min:
        min = cur.data
      cur = cur.next
    if cur.data < min:
      min = cur.data


    return min

  
  def __str__(self):
    if self.head == None:
      return 'the list is empty'
    else:
      st = ''
      cur = self.head
      while cur:
       st += str(cur.data) + ' <-> '
       cur = cur.next
      return st.strip(' <-> ')

nums = [10, 9, 8, 4, 3, 9, 4, 0]
n =  DoublyLinkedList()
for i in nums:
  n.add_node(i)

print(n)
print(n.find_min())''')
    
#8    
def vvisv():
    print('''#Создайте класс «Студент» с атрибутами имя, возраст и список оценок.
Напишите методы для вычисления среднего балла и определения
успеваемости студента (средний балл выше 4). Используйте магический
метод __repr__ для вывода информации о студенте в виде «Студент
{имя}, возраст {возраст}»
class Student():
  def __init__(self, name, age, marks = None):
    self.name = name
    self.age = age
    self.marks = marks if marks is not None else []
  
  def average_score(self):
    if self.marks is not None:
      return sum(self.marks)/len(self.marks)
    else:
      return 'no marks'

  def performance(self):
    if self.average_score() > 4.0:
      return 'good student'
    else:
      return 'bad student'

  def __repr__(self):
    return f'Студент {self.name}, возраст {self.age}'
''')


def ddnot():
    print('''#Создать класс очереди, который будет хранить только элементы,
большие заданного значения. Значение задается при инициализации
объекта класса очереди. При добавлении элемента, если он меньше или
равен заданному значению, то он не должен добавляться.
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue():
    def __init__(self, limit = 0):
        self.head = None
        self.tail = None
        self.limit = limit

    def is_empty(self):
        return not bool(self.head)

    def enqueue(self, data):
        if data > self.limit:
            new_node = Node(data)
            if not self.head:
                self.head = new_node
                self.tail = new_node
            else:
                self.tail.next = new_node
                self.tail = new_node

    def dequeue(self):
        data = self.head.data
        self.head = self.head.next
        if not self.head:
            self.tail = None
        return data

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self):
        current = self.head
        queue_str = ""
        while current:
            queue_str += " → " + str(current.data)
            current = current.next
        return queue_str.lstrip(" → ")  


q1 = Queue(5)
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
for i in range(len(nums)):
  q1.enqueue(i)
print(q1)''')
    
#9    
def pavzs():
    print('''#Используя лямбда-функцию, отсортировать список строковых значений в алфавитном порядке.
fruits = ['apple', 'Orage', 'peach', 'kiwi', 'Banana', 'grapes', 'Lemon']
sorted(fruits, key=lambda x: x[0].lower())''')
    
    
def lpssszva():
    print('''#Найдите все анаграммы в заданном списке строк с помощью лямбда-функции
words = ['нос','апельсин', 'собака', 'тапок', 'топка',  'автор', 'шакал',  'отвар', 'товар', 'алкаш', 'шкала', 'кот', 'капот', 'покат', 'ток', 'сон', 'кошка']
anagrams_dict = {}
for w in words:
  key = ''.join(sorted(w))
  anagrams_dict[key] = []
  for ww in words:
    if key == ''.join(sorted(ww)):
      anagrams_dict[key].append(ww)

result = list(filter(lambda x: len(x) > 1, anagrams_dict.values()))''')
    
    
def lpschsz():
    print('''#Найти индекс и значение максимального и минимального значений в заданном списке чисел с помощью лямбда-функции.
nums = [876, 9, 3, 4, 5, 6, 876, 453, 98, 543, 48] 
max_index, max_value = max(enumerate(nums), key=lambda x: x[1])
min_index, min_value = min(enumerate(nums), key=lambda x: x[1])

print("Максимальное значение:", max_value)
print("Индекс максимального значения:", max_index)
print("Минимальное значение:", min_value)
print("Индекс минимального значения:", min_index)''')
    
    
def sepdya():
    print('''#Дан стек. Необходимо удалить из него все элементы, которые не являются делителями последнего элемента стека.
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def push(self, item):
        new_node = Node(item)
        new_node.next = self.head
        self.head = new_node

    def pop(self):
        if self.is_empty():
            return None
        else:
            popped_item = self.head.data
            self.head = self.head.next
            return popped_item

    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.head.data
    

    def __str__(self):
        current = self.head
        stack_str = ""
        while current:
            stack_str += str(current.data) + " → "
            current = current.next
        return stack_str.rstrip(" → ")


def remove_non_divisors(stack):
    last_element = stack.pop()
    
    print(last_element)
    new_stack = Stack()
    new_stack.push(last_element)
    cur = stack.head
    while cur:
        if  last_element % cur.data == 0:
            new_stack.push(cur.data)
        cur = cur.next
    
    return new_stack



stack = Stack()

# добавление элементов в стек
from random import randint

for i in range(10):
    stack.push(randint(1, 10))

# вывод стека на экран
print(f'Стек: {stack}')

stack = remove_non_divisors(stack)
print(f'Стек: {stack}')''')

#10
def evpks():
    print('''#Используя лямбда-функцию, отсортировать список кортежей по второму элементу.
my_list = [(3, 4), (1, 2), (5, 7), (2, 8)]
sorted_list = sorted(my_list, key=lambda x: x[1])
print(sorted_list)''')
    
def lichsz():
    print('''#Найти все числа, которые делятся на три или пять, из заданного списка чисел, используя лямбда-функцию.
my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
three_five = list(filter(lambda x: x % 3 == 0 or x % 5 == 0, my_list))
three_five''')
    
    
def chpobd():
    print('''#Напишите программу для сортировки заданного смешанного списка
#целых чисел и строк с помощью лямбда-функции. Строки должны быть
#отсортированы перед числами
lst=[1,2,"bb",3,0,"aa","%%"]
print(sorted(list(filter(lambda x: type(x) is str,lst))) + sorted(list(filter(lambda x: type(x) is not str,lst))))
''')
    
    
def nneei():
    print('''#Написать функцию, которая принимает на вход двусвязный список
#и значение элемента, который нужно найти. Функция должна вернуть
#индекс первого вхождения элемента в список или -1, если элемент не
#найден.

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
            new_node.prev = current

    def delete_node(self, data):
        if self.head is None:
            return
        elif self.head.data == data:
            if self.head.next is not None:
                self.head = self.head.next
                self.head.prev = None
            else:
                self.head = None
        else:
            current = self.head
            while current.next is not None and current.next.data != data:
                current = current.next
            if current.next is None:
                return
            else:
                current.next = current.next.next
                if current.next is not None:
                    current.next.prev = current

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self):
        if self.head == None:
            return f"Двусвязный список пустой"
        current = self.head
        dllist_str = ""
        while current:
            dllist_str += " ⇄ " + str(current.data)
            current = current.next
        return dllist_str.lstrip(" ⇄ ") 

def find_ind(dllist, x):
    current_node = dllist.head
    c = 0
    while current_node:
        if current_node.data == x:
          return c

        c += 1   
        current_node = current_node.next
    return -1
        
dll = DoublyLinkedList()
from random import randint

# добавление элементов в двухсвязный список
for i in range(randint(5,10)):
    dll.add_node(randint(1,20))

# вывод двусвязного списка на экран
print(f'Двусвязный список (len = {len(dll)}): {dll}')
print(find_ind(dll, 1))''')

#11
def nipchd():
    print('''# С помощью лямбда-функции проверьте, является ли данное число простым или нет
is_prime = lambda num: all(num % i != 0 for i in range(2, int(num ** 0.5) + 1)) and num > 1
print(is_prime(7))   # Output: True
print(is_prime(20))  # Output: False''')
    
    
def dodzp():
    print('''#Напишите программу для поиска чисел в заданном диапазоне, которые являются суммой двух квадратов. Пример: задан диапазон от 1 # до 50 → [1, 2, 4, 5, 8, 9, 10, 13, 16, 17, 18, 20, 25, 26, 29, 32, 34, 36, 37, 40,
#41, 45, 49, 50]
def sumSquare(n):
 
    s = dict()
    for i in range(1, n):
 
        if i * i > n:
            break
 
        # store square value in hashmap
        s[i * i] = 1
 
        if (n - i * i) in s.keys():
            print((n - i * i)**(1 / 2),
                       "^2 +", i, "^2")
            return True
         
    return False

lst = [1, 2, 4, 5, 8, 9, 10, 13, 16, 17, 18, 20, 25, 26, 29, 32, 34, 36, 37, 40, 41, 45, 49, 50]
ss = list(filter(lambda x: (sumSquare(x)), lst))
ss''')
    
    
def psdvp():
    print('''#Удалите все элементы из заданного списка, не присутствующие в другом списке. Пример: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [2, 4, 6, 8] → [2, 4, 6, 8]
lst1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
lst2 = [2, 4, 6, 8, 13, 25]
lst1 = [i for i in lst1 if i in lst2]

print(lst1)''')
    
    
def tyaovkh():
    print('''#Создать класс хеш-таблицы для хранения объектов класса «Сотрудник».
#Хеш-функция должна основываться на поле «должность» сотрудника.
#Если два сотрудника имеют одну и ту же должность, они должны
#храниться в одной ячейке таблицы

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, Employee):
        index = self.hash_function(Employee.position)
        self.table[index].append(Employee.name)

    def find(self, position):
        index = self.hash_function(position)
        return self.table[index]
        
class Employee:
    def __init__(self, position, name):
        self.position = position
        self.name = name

    def __str__(self):
        return f"Должность: {self.position}, имя: {self.name}"
        
Employees = HashTable(6)
employees_list = [Employee('Programmer', 'Boris Godunov'), Employee('Programmer', 'Ilya'),
              Employee('Manager', 'Anna')]
for b in employees_list:
    Employees.insert(b)
    print(b)

print(Employees.find('Programmer'))
''')

#12    
def dtiyai():
    print('''#Опишите класс Recipe, заданный названием, списком ингредиентов
#и шагами приготовления. Включите в описание класса методы: вывода
#информации о рецепте на экран, проверки, есть ли все ингредиенты для
#приготовления блюда, и свойство, позволяющее установить тип кухни
#(например, итальянская, японская и т. д.).
class Recipe:
    def __init__(self, name, ingredients, steps):
        self.name = name
        self.ingredients = ingredients
        self.steps = steps
        self._cuisine_type = None

    def display_recipe(self):
        print(f"{self.name}\nIngredients: {self.ingredients}\nSteps:")
        for i, step in enumerate(self.steps, start=1):
            print(f"{i}. {step}")
        if self.cuisine_type:
            print(f"Тип кухни: {self.cuisine_type}\n")

    def check_ingredients(self, available_ingredients):
        for ingredient in self.ingredients:
            if ingredient not in available_ingredients:
                return False
        return True

    @property
    def cuisine_type(self):
        return self._cuisine_type

    @cuisine_type.setter
    def cuisine_type(self, cuisine):
        self._cuisine_type = cuisine

recipe = Recipe("Pasta with tomato sauce", ["pasta", "tomatoes", "garlic"], ["Cook pasta", "Make tomato sauce", "Combine pasta and sauce"])

recipe.display_recipe()

if recipe.check_ingredients(["pasta", "tomatoes", "garlic"]):
    print("I have all the ingredients")
else:
    print("I need to buy some ingredients")

recipe.cuisine_type = "Italian"
print(recipe.cuisine_type)''')

    
def sbapsd():
    print('''#Написать метод класса «Заказ», который сортирует список заказов по
#дате с помощью алгоритма быстрой сортировки. Метод должен
#изменять исходный список.


class Order:
    def __init__(self, id, date, amount):
        self.id = id
        self.date = date
        self.amount = amount
        
class OrderList:
    def __init__(self, orders):
        self.orders = orders
        
    def sort_by_date(self):
        self._quicksort(0, len(self.orders) - 1)
        
    def _quicksort(self, start, end):
        if start >= end:
            return
        
        pivot_idx = self._partition(start, end)
        self._quicksort(start, pivot_idx - 1)
        self._quicksort(pivot_idx + 1, end)
        
    def _partition(self, start, end):
        pivot = self.orders[end].date
        i = start - 1
        
        for j in range(start, end):
            if self.orders[j].date <= pivot:
                i += 1
                self.orders[i], self.orders[j] = self.orders[j], self.orders[i]
                
        self.orders[i + 1], self.orders[end] = self.orders[end], self.orders[i + 1]
        return i + 1



orders = [
    Order(1, "2021-01-01", 100),
    Order(2, "2021-02-01", 200),
    Order(3, "2021-01-15", 150),
    Order(4, "2021-03-01", 75),
]

order_list = OrderList(orders)
order_list.sort_by_date()

for order in order_list.orders:
    print(order.date)''')
    
#13
def chpyaks():
    print('''# а) Используя лямбда-функцию, найдите все числа в заданном списке, которые являются простыми числами.
import numpy as np
lst = np.random.randint(1, 100, 30)
A = list(filter(lambda a: np.sum([i for i in range (2, a) if a % i == 0]) == 0, lst))
print(A)''')
    
def skdup():
    print('''# б) Напишите программу для сортировки заданного списка строк по убыванию длины каждой строки.
st = ['twewgre', 'ewgregerh', 'rehr', 'rgrehreh', 'wqgre', 'qwergjb', 'et']
def sorting(lst):
    return sorted(lst, key=lambda a: len(a), reverse=True)
sorting(st)''')
    
def rvbts():
    print('''# в) Используя лямбда-функцию, найдите все строки в заданном списке строк, которые содержат только буквы верхнего регистра
st = ['RHGR', 'EGHTYHegF', 'rehGr', 'GETG', 'wqgre', 'qwergjb', 'eGt']
C = list(filter(lambda a: a.isupper(), st))
print(C)''')
    
def tyaovkhdoa():
    print('''#Реализовать класс хеш-таблицы для хранения объектов класса «Книга». 
#Хеш-функция должна основываться на поле «автор книги». Если две
#книги имеют одного и того же автора, они должны храниться в одной
#ячейке таблицы

# реализация хеш-таблицы методом цепочек
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        slot = self.hash_function(key)
        for pair in self.table[slot]:
            if pair[0] == key:
                pair.append(value)
                return
        self.table[slot].append([key, value])

    def find(self, key):
        slot = self.hash_function(key)
        for pair in self.table[slot]:
            if pair[0] == key:
                return pair[1]
        return None
    
class Book:
    def __init__(self, author, name):
        self.author = author
        self.name = name

    def __str__(self):
        return f"Автор: {self.author}, название: {self.name}"
    
books = HashTable(6)
books_list = [Book('Pushkin', 'Boris Godunov'), Book('Dostoevskiy', 'Prestuplenie i nakazanie'),
              Book('Pushkin', 'Evgeniy Onegin')]
for b in books_list:
    books.insert(b.author,b.name)
    print(b)
    
books.table''')

#14    
def ndnin():
    print('''#а) Используя лямбда-функцию, найдите все числа в заданном списке, которые делятся на 3 и не делятся на 5.
import numpy as np
lst = np.random.randint(1, 100, 30)
A = list(filter(lambda a: (a % 3 == 0)*(a % 5 != 0), lst))
print(A)''')
    
def kkevv():
    print('''#б) Напишите программу для сортировки заданного списка кортежей по возрастанию второго элемента каждого кортежа.
def sort_tuples(tup):
    return sorted(tup, key=lambda a: a[1])

# Пример использования
st = [(7, 3), (4, 5), (2, 7), (4, 2), (1, 1)]
sort_tuples(st)''')
    
def tstsks():
    print('''#в) Используя лямбда-функцию, найдите все строки в заданном списке строк, которые содержат только цифры
st = ['67875', 'EGHT4YHegF', 'rehGr', 'GETG', '5478', 'qwer3gjb', 'e4Gt']
C = list(filter(lambda a: a.isdigit(), st))
print(C)''')
    
def ddnot():
    print('''#Создать класс очереди, который будет хранить только уникальные
#элементы. При добавлении элемента, если он уже есть в очереди, то он
#не должен добавляться

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return not bool(self.head)

    def enqueue(self, data):
        new_node = Node(data)
        current = self.head
        k = 0
        while current:
            if current.data == new_node.data:
                k = 1
                break
            current = current.next
        if k == 0:
            if not self.head:
                self.head = new_node
                self.tail = new_node
            else:
                self.tail.next = new_node
                self.tail = new_node

    def dequeue(self):
        data = self.head.data
        self.head = self.head.next
        if not self.head:
            self.tail = None
        return data

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self):
        current = self.head
        queue_str = ""
        while current:
            queue_str += " → " + str(current.data)
            current = current.next
        return queue_str.lstrip(" → ")  
    
import random
q = Queue()
for i in range(10):
    c = random.randint(-10,10)
    q.enqueue(c)
print(q)''')

#15    
def sitszs():
    print('''# Создайте класс ПРОДУКТ с методами, позволяющими вывести на экран
# информацию о продукте, а также определить, подходит ли данный
# продукт для заданных условий. Создайте дочерние классы МЯСО
# (название, цена, производитель, срок годности), ОВОЩИ (название,
# цена, производитель, сезонность), ФРУКТЫ (название, цена,
# производитель, сезонность) со своими методами вывода информации на
# экран и определения соответствия заданным условиям. Создайте список
# продуктов, выведите полную информацию из базы на экран, а также
# организуйте поиск продуктов с заданной ценой или сезонностью. 


class Product():
    def __init__(self, name, price, manufacturer):
        self.name = name
        self.price = price
        self.manufacturer = manufacturer
    def info(self):
        return self.__dict__
    def find_conditions(self):
        return True
    
class Meat(Product):
    def __init__(self, name, price, manufacturer, exp_date):
        super().__init__(name, price, manufacturer)
        self.exp_date = exp_date
    def find_conditions(self, a):
        return self.price <= a
    
class Vegetables(Product):
    def __init__(self, name, price, manufacturer, season):
        super().__init__(name, price, manufacturer)
        self.season = season
    def find_conditions(self, a):
        return self.season == a
    
class Fruits(Product):
    def __init__(self, name, price, manufacturer, season):
        super().__init__(name, price, manufacturer)
        self.season = season
    def find_conditions(self, a):
        return self.season == a
        
pr1 = Product('Сметана', 75, 'Простоквашино')
pr2 = Product('Молоко', 70, 'Молочный знак')
m1 = Meat('Говядина', 200, 'Волков', 15)
m2 = Meat('Свинина', 150, 'Волков', 10)
m3 = Meat('Курятина', 130, 'Мираторг', 20)

v1 = Vegetables('Помидор', 50, 'Овощной мастер', 'лето')
v2 = Vegetables('Капуста', 60, 'Супер-овощи', 'лето')
v3 = Vegetables('Морковь', 40, 'Мега-овощи', 'осень')

f1 = Fruits('Яблоко', 70, 'Apple', 'весна')
f2 = Fruits('Груша', 60, 'Фруктики', 'лето')
f3 = Fruits('Банан', 80, 'Фруктос', 'лето')

lst = [pr1,pr2,m1,m2,m3,v1,v2,v3,f1,f2,f3]
for p in lst:
    print(p.info())

print('_________')  
for p in lst:
    if p.price < 80:
        print(p.info())
print('_________')     
for p in lst:
    try:
        if p.find_conditions('лето'):
            print(p.info())
    except:
        pass''')
    
def chchyank():
    print('''#Дан стек. Необходимо удалить из него все элементы, которые не являются четными числами
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def push(self, item):
        new_node = Node(item)
        new_node.next = self.head
        self.head = new_node

    def pop(self):
        if self.is_empty():
            return None
        else:
            popped_item = self.head.data
            self.head = self.head.next
            return popped_item

    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.head.data

    def __str__(self):
        current = self.head
        stack_str = ""
        while current:
            stack_str += str(current.data) + " → "
            current = current.next
        return stack_str.rstrip(" → ")
    
import random
stack = Stack()
for i in range(10):
    stack.push(random.randint(-10,10))
print(stack)

def del_chet(stack):
    val = stack.head
    basket = []
    while val:
        if val.data % 2 == 0:
            pp = stack.pop()
            while pp != val.data:
                basket.append(pp)
                pp = stack.pop()
        val = val.next
    for i in reversed(basket):
        stack.push(i)
    return stack
print(del_chet(stack))''')

#16    
def oipzs():
    print('''# Создайте класс ЖИВОТНОЕ с методами, позволяющими вывести на
# экран информацию о животном, а также определить, подходит ли
# данное животное для заданных условий. Создайте дочерние классы
# КОШКА (кличка, порода, возраст, окрас), СОБАКА (кличка, порода,
# возраст, размер), ПТИЦА (вид, возраст, окрас) со своими методами
# вывода информации на экран и определения соответствия заданным
# условиям. Создайте список животных, выведите полную информацию
# из базы на экран, а также организуйте поиск животных с заданной
# породой или окрасом

class Animal():
    def __init__(self, species, age):
        self.species = species
        self.age = age
    def info(self):
        return self.__dict__
    def find_conditions(self):
        return True
    
class Cat(Animal):
    def __init__(self, name, species, age, color):
        super().__init__(species, age)
        self.name = name
        self.color = color
    def find_conditions(self, a):
        return self.color == a
    
class Dog(Animal):
    def __init__(self, name, species, age, size):
        super().__init__(species, age)
        self.name = name
        self.size = size
    def find_conditions(self, a):
        return self.species == a
    
class Bird(Animal):
    def __init__(self, species, age, color):
        super().__init__(species, age)
        self.color = color
    def find_conditions(self, a):
        return self.color == a
        
c1 = Cat('Муся', 'Обычная', 10, 'Серый')
c2 = Cat('Пуся', 'Британская', 5, 'Рыжий')

d1 = Dog('Хан', 'Овчарка', 7, 15)
d2 = Dog('Моджо', 'Чихуахуа', 2, 3)

b1 = Bird('Пингвин', 4, 'Черно-белый')
b2 = Bird('Голубь', 1, 'Серый')

lst = [c1,c2,d1,d2,b1,b2]

for a in lst:
    print(a.info())

print('_______')
for a in lst:
    try:
        if a.species == 'Овчарка':
            print(a.info())
    except:
        pass
    
print('_______')
for a in lst:
    try:
        if a.find_conditions('Серый'):
            print(a.info())
    except:
        pass''')
    
def sivii():
    print('''# Написать функцию, которая принимает на вход двусвязный список и индекс элемента, который нужно удалить. Функция должна удалить
# элемент с указанным индексом и вернуть измененный список

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
            new_node.prev = current

    def delete_node(self, data):
        if self.head is None:
            return
        elif self.head.data == data:
            if self.head.next is not None:
                self.head = self.head.next
                self.head.prev = None
            else:
                self.head = None
        else:
            current = self.head
            while current.next is not None and current.next.data != data:
                current = current.next
            if current.next is None:
                return
            else:
                current.next = current.next.next
                if current.next is not None:
                    current.next.prev = current

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self):
        if self.head == None:
            return f"Двусвязный список пустой"
        current = self.head
        dllist_str = ""
        while current:
            dllist_str += " ⇄ " + str(current.data)
            current = current.next
        return dllist_str.lstrip(" ⇄ ")
        
lst1 = DoublyLinkedList()

for i in range(10):
    lst1.add_node(random.randint(0,9))

print(lst1)

def delete_element(lst, i):
    l = len(lst)
    cur = lst.head
    lst_new = DoublyLinkedList()
    for _ in range(i):
        lst_new.add_node(cur.data)
        cur = cur.next
    for _ in range(i+1, l):
        cur = cur.next
        lst_new.add_node(cur.data)
    return lst_new
print(delete_element(lst1, 8))''')

#17    
def dtibs():
    print('''# Создайте класс СТУДЕНТ с методами, позволяющими вывести на экран
# информацию о студенте, а также определить, соответствует ли данный
# студент заданным критериям. Создайте дочерние классы БАКАЛАВР
# (фамилия, имя, отчество, группа, курс, средний балл), МАГИСТР
# (фамилия, имя, отчество, группа, курс, средний балл, тема диссертации)
# со своими методами вывода информации на экран и определения
# соответствия заданным критериям. Создайте список студентов,
# выведите полную информацию из базы на экран, а также организуйте
# поиск студентов с заданным средним баллом или темой диссертации. 

class Student():
    def __init__(self, surname, name, patronymic, group, course, average_grade):
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.group = group
        self.course = course
        self.average_grade = average_grade
    def info(self):
        return self.__dict__
    def find_conditions(self):
        return True
    
class Bachelor(Student):
    def __init__(self, surname, name, patronymic, group, course, average_grade):
        super().__init__(surname, name, patronymic, group, course, average_grade)
    def find_conditions(self, a):
        return self.average_grade == a
    
class Master(Student):
    def __init__(self, surname, name, patronymic, group, course, average_grade, topic):
        super().__init__(surname, name, patronymic, group, course, average_grade)
        self.topic = topic
    def find_conditions(self, a):
        return self.topic == a
        
b1 = Bachelor('Иванов','Иван','Иванович',1,1,5)
b2 = Bachelor('Петров','Петр','Петрович',2,3,4)

m1 = Master('Николаев','Иван','Николаевич',3,6,5,'Математика')
m2 = Master('Андреева','Алина','Андреевна',3,6,4,'Физика')

lst = [b1,b2,m1,m2]

for s in lst:
    print(s.info())
    
print('_______')
for s in lst:
    if s.average_grade == 5:
        print(s.info())

print('_______')
for s in lst:
    try:
        if s.find_conditions('Математика'):
            print(s.info())
    except:
        pass''')
    
def psapsvpk():
    print('''# Написать метод класса «Клиент», который сортирует список клиентов по возрасту с помощью алгоритма сортировки пузырьком. Метод должен изменять исходный список
class Client():
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self):
        return f"Имя: {self.name}, Возраст: {self.age}"
    @staticmethod
    def sorting(clients):
        n = len(clients)
        for i in range(n):
            for j in range(n - i - 1):
                if clients[j].age > clients[j + 1].age:
                    clients[j], clients[j + 1] = clients[j + 1], clients[j]
                    
clients = [Client("Ivan", 25),Client("Elena", 18),Client("Alex", 37),Client("Petr", 64)]
Client.sorting(clients)
for i in clients:
    print(i)''')

#18    
def chspvch():
    print('''# а) Используя лямбда-функцию, найдите все числа в заданном списке,
# которые являются числами Кармайкла (для любого числа a, взаимно
# простого с числом n, a^(n-1) mod n = 1).

import numpy as np
import math
lst = [561, 346, 256, 4246, 56, 2821, 578, 1105]
print(lst)
A = list(filter(lambda n: np.sum([1 for a in range(2,n) if (math.gcd(a,n) == 1) and (a**(n-1)%n != 1)]) == 0, lst))
print(A)''')
    
def skvzi():
    print('''# б) Напишите программу для сортировки заданного списка строк по
# количеству символов-разделителей (пробелов или запятых) в каждой
# строке.

def sorting(strings):
    return sorted(strings, key=lambda a: a.count(" ") + a.count(","))

strings = ['RGEG, E   TEH,', 'WETRETER ', 'WTEY , EW', 'WETWT', 'EQERWT,,, ']
sorting(strings)''')
    
def tnzks():
    print('''# в) Используя лямбда-функцию, найдите все строки в заданном списке
# строк, которые заканчиваются на точку.
strings = ['RGEG, E   TEH,', 'WETRETER ','twter.', 'wrert.ehrth', 'wetwrytre.', 'WTEY , EW', 'WETWT', 'EQERWT,,, ']
C = list(filter(lambda s: s[-1] == '.', strings))
print(C)''')
    
def upobd():
    print('''# Создать класс очереди, который будет хранить только элементы типа int
# и отсортированные по убыванию. При добавлении элемента, если он не
# является целым числом, то он не должен добавляться. При получении
# элементов из очереди они должны быть отсортированы по убыванию. 

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, data):
        new_node = Node(data)
        if isinstance(new_node.data , int):
            if not self.head:
                self.head = new_node
                self.tail = new_node
            else:
                self.tail.next = new_node
                self.tail = new_node

    def dequeue(self):
        data = self.head.data
        self.head = self.head.next
        if not self.head:
            self.tail = None
        return data
    
    def get_queue(self):
        q = []
        cur = self.head
        while cur:
            q.append(cur.data)
            cur = cur.next
        return sorted(q, reverse = True)

    def __str__(self):
        current = self.head
        queue_str = ""
        while current:
            queue_str += " → " + str(current.data)
            current = current.next
        return queue_str.lstrip(" → ") 
    
import random
q = Queue()
for i in range(10):
    c = random.randint(-10,10)
    q.enqueue(c)
print(q)

q.enqueue(0.6)
print(q)

q.enqueue(6)
print(q)

print(q.get_queue())''')
    
#19
def zhtsups():
    print(''' # Опишите класс Animal, заданный видом, возрастом и весом. Включите
# в описание класса методы: вывода информации о животном на экран,
# проверки, является ли животное взрослым (возраст больше 3 лет),
# и свойство, позволяющее установить цвет животного.

class Animal:
    def __init__(self, species, age, weight):
        self.species = species
        self.age = age
        self.weight = weight
        self.color = None

    def display_info(self):
        print("Species:", self.species)
        print("Age:", self.age)
        print("Weight:", self.weight)
        print("Color:", self.color)

    def is_adult(self):
        return self.age > 3

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

# Создание объекта класса Animal
animal = Animal("Lion", 5, 200)

# Вывод информации о животном
animal.display_info()

# Проверка, является ли животное взрослым
print("Is adult:", animal.is_adult())

# Установка цвета животного
animal.color = "Brown"

# Вывод информации о животном с установленным цветом
animal.display_info()''')

def vsapsa():
    print('''# Написать функцию, которая принимает на вход список слов и сортирует
# его по алфавиту с помощью алгоритма сортировки вставками. Функция
# должна возвращать отсортированный список
import copy
def insertion_sort(arr):
    words = arr.copy()
    for i in range(1, len(words)):
        key = words[i]
        j = i - 1
        while j >= 0 and words[j] > key:
            words[j + 1] = words[j]
            j -= 1
        words[j + 1] = key
    return words

word_list = ['v','j','l','a','b','q']
sorted_words = insertion_sort(word_list)

print(f'Initial list: {word_list}, \n Sorted list: {sorted_words}')''')

#20
def kchyaks():
    print('''Используя лямбда-функцию, найдите все числа в заданном списке, которые являются числами Капрекара.
lst = [9, 12, 43, 15, 45, 55, 99, 297, 703, 999]
a = list(filter(lambda x : x in [int(str(x**2)[:i]) + int(str(x**2)[i:]) for i in range(1, len(str(x**2))) if int(str(x**2)[i:]) != 0 and int(str(x**2)[:i]) + int(str(x**2)[i:])], lst))
a''')

def applv():
    print('''Напишите программу для сортировки заданного списка строк в лексикографическом порядке (по алфавиту).
a = ['aa', 'ab', 'aaabbb', 'abc', 'aabbcc', 'aab']
b = ['корова', 'корона', 'король', 'коррида', 'корвалол']

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

insertion_sort(a)

insertion_sort(b)''')

def achyaks():
    print('''Используя лямбда-функцию, найдите все числа в заданном списке, которые являются числами Армстронга.
b = [12, 153, 407, 370, 371, 432]
k = list(filter(lambda x: x == sum([i**len(list(map(int, str(x)))) for i in list(map(int, str(x)))]) , b))
print(k)''')

def sdvek():
    print('''#Реализовать функцию, которая находит количество элементов в двусвязном списке.
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
            new_node.prev = current       

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self):
        if self.head == None:
            return f"Двусвязный список пустой"
        current = self.head
        dllist_str = ""
        while current:
            dllist_str += " ⇄ " + str(current.data)
            current = current.next
        return dllist_str.lstrip(" ⇄ ")

import numpy as np
x = DoublyLinkedList()
for i in range(12):
    x.add_node(np.random.randint(0, 1000, 1)[0])

print(x)

print(len(x))''')

#21
def suknf():
    print('''#Опишите класс Student, заданный фамилией, именем, возрастом
и средним баллом. Включите в описание класса методы: вывода
информации о студенте на экран, проверки, является ли студент
отличником (средний балл больше 4.5), и свойство, позволяющее
установить факультет, на котором учится студент.
class Student:    
    def __init__(self, surname, name, age, mean):
        self.surname = surname
        self.name = name
        self.age = age
        self.mean = mean
        self._faculty = ''
        
    def info(self):
        return self.__dict__        
        
    def excellent(self):
        return self.mean > 4.5 
    
    @property
    def faculty(self):
        return self._faculty
    
    @faculty.setter
    def faculty(self, faculty):
        self._faculty = faculty

a = Student('Головкина', 'Анна', 18, 4.6)
print(a.info())

a.faculty = 'ИТиАБД'

print(a.info())''')

def vsapsu():
    print('''Написать функцию, которая принимает на вход список чисел и сортирует его по убыванию с помощью алгоритма сортировки вставками. Функция должна возвращать отсортированный список.
def insertion_sort(reverse=True):
    arr = []
    while True:
        elem = input()
        if elem != None and elem != '':
            arr.append(int(elem))
        else:
            break
            
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and ((not reverse and arr[j] > key) or (reverse and arr[j] < key)):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

insertion_sort()''')

    
#22
def akvpn():
    print('''Напишите лямбда-функцию, которая умножает заданное число на 7 и вычитает из него 3, переданное в качестве аргумента.
a = [1, 2, 3, 4, 5, 6]
expression = list(map(lambda x: x*7-3, a))

expression''')

def lpschts():
    print('''Найдите сумму всех чисел в заданном списке целых чисел с помощью лямбда-функции.
from functools import reduce
arr = list(np.random.randint(-100, 100, 10))
print(arr, sum(arr))
a = reduce(lambda x, y: x+y, arr)
a''')

def lpschz():
    print('''Извлечь элементы списка, которые больше заданного числа, с помощью лямбда-функции.
arr = list(np.random.randint(-100, 100, 10))
print(arr)
val = int(input())
a = list(filter(lambda x: x > val, arr))
a''')

def chpyake():
    print('''Дан стек. Необходимо найти сумму всех элементов, которые являются простыми числами.
import copy

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def push(self, item):
        new_node = Node(item)
        new_node.next = self.head
        self.head = new_node

    def pop(self):
        if self.is_empty():
            return None
        else:
            popped_item = self.head.data
            self.head = self.head.next
            return popped_item
        
    def find_prime(self):
        
        def is_prime(a):
            if a==1:
                return False
            if a % 2 == 0:
                return a == 2
            d = 3
            while d * d <= a and a % d != 0:
                d += 2
            return d * d > a
        
        a = []
        
        temp_stack = Stack()

        temp_stack = copy.deepcopy(self)

        while not temp_stack.is_empty():
            item = temp_stack.pop()
            if is_prime(item):
                a.append(item)

        return sum(a)
        

    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.head.data

    def __str__(self):
        current = self.head
        stack_str = ""
        while current:
            stack_str += str(current.data) + " → "
            current = current.next
        return stack_str.rstrip(" → ")

stack = Stack()

for i in [x for x in np.random.randint(0, 100, 10)]:
    stack.push(i)
    
print(stack)

stack.find_prime()''')

#23
def igpkd():
    print('''#Создайте класс «Книга» с атрибутами название, автор и год издания.
Напишите методы для вывода информации о книге в виде «Книга
'{название}' автора {автор}, издана в {году}». Используйте магический
метод __eq__ для сравнения двух книг по году издания
class Book:    
    def __init__(self, name, author, year):
        self.name = name
        self.author = author
        self.year = year
        
    def info(self):
        return f'Книга "{self.name}" автора {self.author}, издана в {self.year} году' 
    
    @classmethod
    def __verify_data(cls, other):
        return other.year
    
    def __eq__(self, other):
        sc = self.__verify_data(other)
        return self.year == sc

a = Book('Преступление и наказание', 'Достоевский Ф.М.', 1866)
b = Book('Капитанская дочка', 'Пушкин А.С.', 1836)
c = Book('Война и мир', 'Толстой Л.Н.', 1863)
d = Book('Палата №6', 'Чехов А.П.', 1892)
f = Book('Казаки', 'Толстой Л.Н.', 1863)

a.info(), b.info(), c.info(), d.info(), f.info()

a == b

c == f''')

def vsapss():
    print('''#Написать функцию, которая принимает на вход список строк
и сортирует его по длине строк с помощью алгоритма сортировки
выбором. Функция должна возвращать отсортированный список. 

def selection_sort(arr, reverse=False):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if reverse:
                if len(arr[j]) > len(arr[min_idx]):
                    min_idx = j
            else:
                if len(arr[j]) < len(arr[min_idx]):
                    min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

a = ['1', '12', '123', '1234', '12345', '123456']

selection_sort(a, True)''')

#24    
def sokvv():
    print('''#Опишите класс BankAccount, заданный номером счета, балансом
и владельцем. Включите в описание класса методы: вывода информации
о банковском счете на экран, проверки, достаточно ли денег на счете
для выполнения операции, и свойство, позволяющее установить тип
валюты, в которой открыт счет
class BankAccount:    
    def __init__(self, number, balance, holder):
        self.number = number
        self.balance = balance
        self.holder = holder
        self._currency = ''
        
    def info(self):
        return self.__dict__        
        
    def enough(self, cost):
        return self.balance >= cost 
    
    @property
    def currency(self):
        return self._currency
    
    @currency.setter
    def currency(self, currency):
        self._currency = currency

a = BankAccount(55362036, 201030405020, 'GOLOVKINA ANNA')
print(a.info())

a.currency = 'USD'

print(a.info())''')

def psapsvpe():
    print('''#Написать функцию, которая принимает на вход список дат и сортирует
его по возрастанию с помощью алгоритма сортировки пузырьком.
Функция должна возвращать отсортированный список
def bubble_sort(arr, reverse=True):
    n = len(arr)
    
    for i in range(n):
        for j in range(n - i - 1):
            if not reverse:
                if (arr[j] > arr[j + 1]):
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
            else:
                if (arr[j] < arr[j + 1]):
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

a = ['2004-06-29', '2005-01-17', '2004-02-03', '2004-05-26', '1980-06-18', '1978-02-18', '1953-10-24', '1951-08-31', '2011-01-09']

bubble_sort(a)
''')
    
#25
def fzhups():
    print('''Опишите класс Movie, заданный названием, режиссером, годом выпуска и продолжительностью. Включите в описание класса методы: вывода информации о фильме на экран, проверки, является ли фильм длинным (продолжительность больше 2 часов), и свойство, позволяющее установить жанр фильма.
class Movie:
    def __init__(self, name, director, year, time, genre = None):
        self.name = name
        self.director = director
        self.year = year
        self.time = time
        self.genre = genre

    def set_genre(self, genre):
        self.genre = genre

    def get_data(self):
            print(f'Name of film is : {self.name}, The director is : {self.director}, Year of publication is : {self.year}, Duration is : {self.time} minutes')
        if self.genre:
            print(f'The genre is: {self.genre}')

    def check_time(self):
        if self.time > 120:
            print(f'The film {self.name} lats more 120 minutes')
        else:
            print(f'The film {self.name} lats less 120 minutes')
movie1 = Movie('The Green Mile', 'Ton Khencks', 1999, 189)
movie2 = Movie('Mountain', 'Jo Dain', 2017, 90)

movie1.check_time()
movie1.set_genre('Drama, Thriller')
movie1.get_data()

movie2.check_time()
movie2.set_genre('Drama, Thriller')
movie2.get_data()''')
    
def tyaovkhdon():
    print('''#Реализовать класс хеш-таблицы для хранения объектов класса «Товар». Хеш-функция должна основываться на поле «название #товара». Если два товара имеют одинаковое название, они должны храниться в одной ячейке таблицы.
class Good():
    def __init__(self, name, price):
        self.name = name
        self.price = price

g = [Good('Pork', 100), Good('Pork', 120), Good('Jam', 40), Good('Meat', 300), Good('Lemon', 30), Good('Kale', 25)]
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        slot = self.hash_function(key)
        for pair in self.table[slot]:
            if pair[0] == key:
                pair.append(value)
                return
        self.table[slot].append([key, value])

    def find(self, key):
        slot = self.hash_function(key)
        for pair in self.table[slot]:
            if pair[0] == key:
                return pair[1]
        return None

h = HashTable(3)

for i in g:
    h.insert(i.name, i)
h.table
''')

#26
def pivia():
    print('''Напишите лямбда-функцию, которая принимает два аргумента и возвращает их произведение.
multiplication = lambda x,y: x*y
print(multiplication(7,6))''')

def lichsz():
    print('''Найдите числа, которые являются квадратами целых чисел, из заданного списка чисел, используя лямбда-функцию
numbers = [1,2,4,5,8,9,10,12,14,16,19,25]
result = list(filter(lambda x: int(x**0.5)**2 == x, numbers))
print(result)''')
    
def lpssszvch():
    print('''Напишите программу для подсчёта целых чисел в заданном смешанном списке с помощью лямбда-функции.
numbers = [1, 3.24, 6, 8, 5.45, 10]
result = list(filter(lambda x: isinstance(x, int), numbers))
print(result)''')
    
def sbapsts():
    print('''Написать метод класса «Товар», который сортирует список товаров по цене с помощью алгоритма быстрой сортировки. Метод должен изменять исходный список.
class Product():
    def __init__(self, name, price):
        self.name = name
        self.price = price
     
    def __str__(self):
        return f"Продукты: {self.name}, Цена: {self.price}"
    
    @staticmethod
    def sorting(arr):
        def quick_sort(arr):
            if len(arr) <= 1:
                return arr
            else:
                pivot = arr[0]
                left = []
                right = []
                for i in range(1, len(arr)):
                    if arr[i].price < pivot.price:
                        left.append(arr[i])
                    else:
                        right.append(arr[i])
                return quick_sort(left) + [pivot] + quick_sort(right)
        arr[:] = quick_sort(arr)

products = [Product('Cheese', 77), Product('Apple', 23), Product('Meat', 56), Product('Ice cream', 19)]

Product.sorting(products)

for i in products:
    print(i.name, i.price)''')

#27    
def pppds():
    print('''Создайте класс «Прямоугольник» с атрибутами длины и ширины. Напишите методы для вычисления площади и периметра прямоугольника. Используйте магический метод eq для сравнения двух прямоугольников по площади.
class Rectangle():
  def __init__(self, a, b):
    self.a = a
    self.b = b

  def Perimeter(self):
    return 2*(self.a + self.b)

  def Square(self):
    return self.a*self.b

  def __eq__(self, other):
    if isinstance(other, Rectangle): #проверка принадлежности классу
      return self.Square == other.Square
    False
figure1 = Rectangle(20,16)
figure2 = Rectangle(10,32)

square1 = figure1.Square()
square2 = figure2.Square()

print('Perimetr is: ', figure1.Perimeter())
print('Square is: ', figure1.Square())
print('Perimetr is: ', figure2.Perimeter())
print('Square is: ', figure2.Square())
if  square1 == square2:
  print('square1 and square2 are equal')
else:
  print(False)''')