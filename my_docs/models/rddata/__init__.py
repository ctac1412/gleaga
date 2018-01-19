# -*- coding: utf-8 -*-
import random

ints = u'123456789'
chars = u'qwertyuiopasdfghjklzxcvbnm'.upper() + u'qwertyuiopasdfghjklzxcvbnm'
allsym = ints + chars
names = (u'Ипполит', u'Тит', u'Анатолий', u'Ипатий', u'Онисим',
         u'Лукьян', u'Родион', u'Валерьян', u'Евсей', u'Касьян',
         u'Терентий', u'Вячеслав', u'Адриан', u'Самсон', u'Сергей',
         u'Антип', u'Фадей', u'Богдан', u'Юлий', u'Герасим', u'Никита',
         u'Онуфрий', u'Антон', u'Эммануил', u'Елисей', u'Георгий', u'Демьян',
         u'Мирослав', u'Ким', u'Аристарх', u'Станислав', u'Ульян', u'Евдоким',
         u'Евстигней', u'Пимен', u'Давид', u'Капитон', u'Гавриил', u'Лавр',
         u'Еремей', u'Вадим', u'Глеб', u'Андрей', u'Сократ', u'Валерий',
         u'Гаврила', u'Карл', u'Прокл', u'Михаил', u'Игнат'
         )

surname = (u'Пыхтин', u'Дежнёв', u'Цветков', u'Рябоконь', u'Соломинцев',
           u'Каракозов', u'Янушкевич', u'Якимов', u'Широких', u'Курбанов', u'Сиянов',
           u'Твардовский', u'Стрелков', u'Серебряков', u'Смешной', u'Клюев', u'Боголюбов',
           u'Никифоров', u'Бехтерев', u'Образцов', u'Кутлыев', u'Витаев', u'Актжанов',
           u'Калганов', u'Андреюшкин', u'Мурогов', u'Янборисов', u'Букавицкий', u'Яндиев',
           u'Кочубей', u'Чуканов', u'Лихачев', u'Арцишевский', u'Гориславский', u'Токарев',
           u'Яманов', u'Сиваков', u'Пшеничников', u'Платущихин', u'Буковский', u'Ярилов',
           u'Нежданов', u'Николюк', u'Садыков', u'Осипов', u'Лачков', u'Кадыров', u'Агейкин',
           u'Сухарников', u'Якунчиков'
           )

thirdrname = (u'Демьянович', u'Тимурович', u'Кондратович', u'Андроникович', u'Евграфович', u'Владимирович'
              u'Александрович', u'Адрианович', u'Сократович', u'Левович', u'Панкратиевич',
              u'Чеславович', u'Игнатиевич', u'Проклович', u'Владиславович', u'Филиппович',
              u'Вячеславович', u'Андреевич', u'Ильевич', u'Савелиевич', u'Прокофиевич', u'Ипатиевич',
              u'Семенович', u'Евгениевич', u'Сидорович', u'Эдуардович', u'Леонович', u'Онуфриевич',
              u'Климентович', u'Глебович', u'Леонидович', u'Евстафиевич', u'Сергеевич', u'Дмитриевич',
              u'Елизарович', u'Феликсович', u'Назарович', u'Святославович', u'Фролович', u'Михеевич',
              u'Леонтиевич', u'Федотович', u'Гордеевич', u'Даниилович', u'Иннокентиевич', u'Эмилевич',
              u'Филимонович', u'Федорович', u'Никифорович', u'Модестович'
              )

company = (u'Эслия', u'Пабра', u'Васла', u'Кукла', u'Бюста', u'Мёсте', u'Каста', u'Щясил',
           u'Жащия', u'Укэст', u'Аплия', u'Рещэж', u'Жищех', u'Цоста', u'Гекле', u'Зочка',
           u'Икели', u'Пюбрё', u'Ежега', u'Азест', u'Лерка', u'Елуви', u'Чёчкю', u'Чанка',
           u'Ковиж', u'Шомез', u'Вупла', u'Борса', u'Гэста', u'Авялё', u'Аплэн', u'Лакия',
           u'Ослка', u'Нагия', u'Дасти', u'Хюпло', u'Кущка', u'Ковещ', u'Мафка', u'Хурко',
           u'Абаща', u'Эслка', u'Гютэб', u'Жожка', u'Абава', u'Шошия', u'Ёстик', u'Хэшну',
           u'Личка', u'Ифёрк'
           )

production = (u'Цыпленок охлажденный', u'Макароны', u'Ср.м.посуды', u'Грудка куриная Греча',
              u'Зуб.паста', u'Индейка', u'Панир.сухари', u'Очиститель пос.мойки', u'Фарш', u'Сахар',
              u'Доместос', u'Лимон', u'Фасоль', u'Мешки мусор большие', u'Яблоки', u'Горох',
              u'Мешки мусор маленькие', u'Бананы', u'Овсянка', u'Пленка пищевая', u'Апельсины',
              u'Пшено', u'Рукав для запекания', u'Мандарины', u'Крупа кукурузная', u'Фольга',
              u'Груши', u'Мука ржаная', u'Бумага для выпечки', u'Кабачки', u'Мука пшеничная',
              u'Губки для посуды', u'Капуста белокачанная', u'Шоколад', u'Губки железные', u'Лук', u'Сода', u'Перчатки')


company_type = (u'ООО', u'ОАО', u'ЗАО')
post = (u'менеджер', u'генеральный директор', u'бухгалтер')
city = (u'Москва', u'Санкт-Петербург', u'Казань',
        u'Барнаул', u'Сызрань', u'Абдулино', u'Железногорск')
country = (u'Россия', u'Казань')
street = (u'Лесная', u'Кирпичная', u'Дальняя', u'Земляничная',
          u'Тимирязева', u'Полевая', u'Солнечная')

def rdproduction():
    return random.choice(production)

def rdnums(count=3):
    return ''.join((random.choice(ints) for x in range(count)))


def rdchar(count=3):
    return ''.join((random.choice(chars) for x in range(count)))


def rdalls(count=3):
    return ''.join((random.choice(allsym) for x in range(count)))


def rdcompany():
    return random.choice(company)


def rdcompany_type():
    return random.choice(company_type)


def rdphone():
    return '+9' + '(' + rdnums(3) + ')' + rdnums(7)


def rdemail():
    return ''.join((random.choice(allsym) for x in range(5))) + u'@gmail.ru'


def rdname():
    return random.choice(names)


def rdsurname():
    return random.choice(surname)


def rdthirdrname():
    return random.choice(thirdrname)


def rdfio():
    return rdsurname() + ' ' + rdname() + ' ' + rdthirdrname()


def rdpost():
    return random.choice(post)


def rdcity():
    return random.choice(city)


def rdcountry():
    return random.choice(country)


def rdstreet():
    return random.choice(street)


def rdadress():
    return u'страна ' + random.choice(country) + u' город ' + random.choice(city) + u' улица ' + random.choice(street) + u' дом ' + ''.join((random.choice(ints) for x in range(random.randint(1, 3))))


def rdfast():
    name = rdname()
    surname = rdsurname()
    thirdrname = rdthirdrname()
    company_type = rdcompany_type()
    company = rdcompany()
    full_company = company_type + ' ' + company
    production=rdproduction()
    return {'name': name,
            'surname': surname,
            'thirdrname': thirdrname,
            'fio': name + ' ' + surname + ' ' + thirdrname,
            'email': rdemail(),
            'phone': rdphone(),
            'post': rdpost(),
            'city': rdcity(),
            'country': rdcountry(),
            'street': rdstreet(),
            'adress': rdadress(),
            'company_type': company_type,
            'company': company,
            'full_company': full_company,
            'production' : production
            }


# Есть метод который возвращает объект со всеми рандомными полями, так же можно вызвать каждый метод отдельно
# print (rdfast())
# # {'name': 'Соломон', 'surname': 'Собачкин', 'thirdrname': 'Ерофеевич', 'fio': 'Заславский Богдан Евлампиевич',
# #  'email': 'zFKGr@gmail.ru', 'phone': 'kaJrc@gmail.ru', 'post': 'бухгалтер',
# #  'city': 'Москва', 'country': 'Россия', 'street': 'Полевая', 'adress': 'страна Россия город Москва улица Кирпичная дом 661'}

# Использование  rdfast()('name')
#
# print(rdnums(5))
# # 65771

# print(rdchar(5))
# # ilccC

# print(rdphone())
# # +9(516)1399884

# print(rdemail())
# # yq6PZ@gmail.ru

# print(rdfio())
# # Черепанов Богдан Мартьянович

#  print(rdpost())
# # генеральный директор

# print(rdadress())
# # страна Россия город Казань улица Полевая дом 52
