# Проект "Django-приложение для интернет-библиотеки"

## Описание проекта

Простое Django-приложение для библиотеки, которое позволяет читателям выбрать интересующую книгу из каталога библиотеки, взять её на чтение, а затем вернуть. Приложение предоставляет два уровня доступа: для Библиотекаря и для Читателя, каждый из которых имеет свой функционал и возможности.

## Основные сущности

### Пользователи

Приложение поддерживает две роли пользователей: Библиотекарь и Читатель.

1. **Библиотекарь**:
   - Минимальные обязательные атрибуты:
     - `username` (Имя пользователя)
     - `password` (Пароль)
     - `employee_number` (Табельный номер)
   - Функционал:
     - Управление списком должников;
     - CRUD операции с книгами.
   
2. **Читатель**:
   - Минимальные обязательные атрибуты:
     - `username` (Имя пользователя)
     - `password` (Пароль)
     - `first_name` (Имя)
     - `last_name` (Фамилия)
     - `address` (Адрес проживания)
   - Функционал:
     - Просмотр каталога книг и возможность взять книгу на чтение.
     - Управление своими взятыми книгами.

### Книги

Модель книги в базе данных включает следующие поля:
- `title` (Название книги)
- `author` (Автор)
- `genre` (Жанр)
- `description` (Аннотация)

## Функционал приложения

### Веб-интерфейс

Приложение имеет простой веб-интерфейс на Django-шаблонах (templates) с использованием Bootstrap для стилизации. На всех страницах доступна панель навигации, позволяющая перемещаться между основными разделами сайта. Также на панели есть кнопка для управления сессией аутентификации (вход/выход).

#### Для Читателя

1. **Страница регистрации / входа**:
   - Аутентификация по `username`, `password` (минимальные требования).
   - После аутентификации в консоли в левом верхнем углу отображаются кнопки "Профиль" и "Мои книги" в которых соответственно отображена минимальная информация о читателе и список книг взятых читателем в библиотеке для чтения.
   
2. **Главная страница – Каталог книг**:
   - Отображение всех доступных книг в библиотеке в виде карточек по три штуки по горизонтали и по вертикали в зависимости от количества книг в каталоге.
   - Каждая карточка книги имеет: название книги, обложку, автора книги, жанр и аннотацию, кнопку "Подробнее".
   - Книги отсортированы по названию.
   - Для того чтобы читатель мог взять книгу для чтения необходимо нажать кнопку "Подробнее". После чего читателю открывается детальная информация о книге. После ознакомления с полной информацией о книге читатель может взять её для чтения из библиотеки нажав кнопку "Взять книгу". После этого автоматически открывается страница "Мои книги" где в виде списка отображены все книги взятые читателем для чтения.

3. **Страница "Мои книги"**:
   - Список книг, которые находятся на руках у читателя.
   - Для каждой книги отображается название, дата получения и количество дней, сколько книга на руках.
   - Для того чтобы читатель мог вернуть книгу он может нажать кнопку "Вернуть книгу" в списке "Мои книги".
   - Список книг отсортирован по дате и времени взятия книги для чтения.
   - Ниже кнопки "Вернуть книгу" отображается надпись "Книга взята для чтения", тем самым сообщая читателю о невозможность взять из каталога одну и туже книгу несколько раз. 

#### Для Библиотекаря

1. **Страница регистрации / входа**:
   - Аутентификация по `username`, `password`, `employee_number`.
   - После аутентификации в консоли в левом верхнем углу отображаются кнопки "Профиль" и "Должники книг" в которых соответственно отображена минимальная информация о библиотекаре и список читателей должников книг взятых в библиотеке для чтения и так их не вернувших обратно.

2. **Главная страница – Каталог книг**:
   - Отображение всех доступных книг в библиотеке в виде карточек по три штуки по горизонтали и по вертикали в зависимости от количества книг в каталоге.
   - После аутентификации библиотекарю доступны операции CRUD на главной странице и в карточках книг: создание, чтение, обновление, удаление книг.

3. **Страница – Список должников**:
   - Отображение списка читателей, у которых есть просроченные книги. * Примечание: для проверки работоспособности списка должников книг устанавливается одна минута, после которой читатель считается должником. Для отображения списка должников, которые не вернули книги в течение установленных дней, то необходимо вставить блок кода закомментированный знаком #.
   - Для каждого должника отображаются: `username`, `имя`, `фамилия`, `адрес`, `название книги`, `дата получения` и `количество дней, сколько книга на руках`.

## Установка и запуск проекта

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/Mezentsev-Andrey/django_library_project.git
   
2. Перейдите в директорию проекта:
   ```bash
   cd django_library_project
   
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt

4. Произведите настройку базы данных PostgreSQL в `settings.py`:

    - POSTGRES_DB=`"имя базы данных"`;
    - POSTGRES_USER=`"пользователь базы данных"`;
    - POSTGRES_PASSWORD=`"пароль базы данных"`;
    - POSTGRES_PORT=`"порт базы данных"`;
    - POSTGRES_HOST=`"хост базы данных"`.
   
5. Выполните миграции базы данных:
   ```bash
   python manage.py migrate

6. Создайте суперпользователя:
   ```bash
   python manage.py createsuperuser
   
7. Запуск приложения:
    - Заполнение базы данных произведено в админке. Загруженные данные представлены по адресу: library/fixtures/all_data.json, library/fixtures/library_data.json; users/fixtures/users_data.json. Для их загрузки в базу данных проекта воспользуйтесь командой: `python manage.py loaddatautf8 all_data.json`
    - Для выгрузки данных из базы данных проекта используйте команду: `python manage.py dumpdatautf8 library --output library/fixtures/library_data.json` (в данном примере команды приведена выгрузка всех данных из приложения library.)

8. Запустите сервер разработки:
   ```bash
   python manage.py runserver

9. Откройте браузер и перейдите по адресу http://127.0.0.1:8000/ для доступа к приложению.
