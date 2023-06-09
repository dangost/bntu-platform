create table roles (
    id serial primary key,
    name text unique
);

insert into roles (name) values ('Admin');
insert into roles (name) values ('Student');
insert into roles (name) values ('Teacher');
insert into roles (name) values ('Worker');

create or replace function get_role_id(role_name text)
returns int as $role_id$
declare
	role_id int;
begin
   select id into role_id from roles where name=role_name;
   return role_id;
end;
$role_id$ language plpgsql;

create table faculties(
    id serial primary key,
    name text not null unique,
    shortcut text not null unique,
    description text,
    avatar text
);

create or replace function get_faculty_by_shortcut(shortname text)
returns int as $factuly_id$
    declare faculty_id int;
    begin
        select id into faculty_id from faculties where shortcut=shortname;
        return faculty_id;
    end;
$factuly_id$ language plpgsql;

create table department(
    id serial primary key,
    faculty_id int references faculties(id),
    name text not null,
    shortcut text not null,
    description text,
    avatar text
);

create or replace function get_dep_by_short(shortname text)
returns int as $dep_id$
declare dep_id int;
begin
    select id into dep_id from department where shortcut = shortname;
    return dep_id;
end;
$dep_id$ language plpgsql;

create table groups(
    id int primary key not null unique,
    faculty_id int not null references faculties(id),
    departament_id int not null references department(id),
    course int not null
);

create table users (
    id serial primary key,
    firstname text not null,
    surname text not null,
    email text not null unique,
    password_hash text not null,
    role_id int references roles(id),
    avatar text,
    phone_number text
);

create table students(
    student_id int not null unique,
    course int not null,
    group_id int not null references groups(id)
) inherits (users);

create table leaders(
    id serial primary key,
    group_id int not null references groups(id),
    leader int not null
);


create table teachers(
    id serial primary key,
    departament_id int not null references department(id),
    schedule json,
    job_title text not null,
    description text,
    phone text
) inherits (users);

create table files(
    id serial primary key,
    filename text not null,
    path text not null unique,
    size_mb text not null,
    file_hash text not null,
    upload_from int references users(id),
    uploaded_time timestamptz default NOW()
);

create table posts(
    id serial primary key,
    user_id int not null,
    datetime timestamptz default NOW(),
    container json not null,
    scope json
);

create table canteens(
    id serial primary key ,
    name text not null,
    description text not null,
    address text not null,
    avatar text not null,
    current_menu text not null,
    admin int not null unique
);


create table retakes(
    id serial primary key,
    subject text not null,
    teacher_id int not null,
    student_id int not null,
    type text not null,
    create_at timestamptz default now(),
    expire_at timestamptz default now() + interval '5 days'
);


insert into faculties (name, shortcut, description) values ('Факультет Информационных Технолоий и Робототехники', 'ФИТР', 'Просто норм, факультет для пацанов');
insert into department (name, shortcut, description, faculty_id)
values('Программное обеспечение информационных систем и технолоий', 'ПОИСиТ', 'Самая пацанская кафедра', get_faculty_by_shortcut('ФИТР'));
insert into groups (id, faculty_id, departament_id, course) values (10702119, get_faculty_by_shortcut('ФИТР'), get_dep_by_short('ПОИСиТ'), 4);
insert into students(role_id, firstname, surname, email, password_hash, student_id, course, group_id) values
(get_role_id('Student'), 'Данила', 'Кислицин', 'fafafa@gmail.com', 'a66b47e6b2fdc5aae2aa914e4718cf2af21f70c7c842ad5ce8b2ac7946840fec', 1070211908, 4, 10702119);
insert into users(firstname, surname, email, password_hash, role_id) values
('Dan', 'Gost', 'dangost16@gmail.com', 'f74b4df676be77106dd1ebecf3bd1657f1b8973858f92878184e41eb488ab9bd', get_role_id('Admin'));



insert into students(role_id, firstname, surname, email, password_hash, student_id, course, group_id) values
(get_role_id('Student'), 'Алексей', 'Сошнев', 'lehanator@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 1070211901, 4, 10702119);

insert into students(role_id, firstname, surname, email, password_hash, student_id, course, group_id) values
(get_role_id('Student'), 'Дмитрий', 'Сударев', 'dima@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 1070211902, 4, 10702119);

insert into students(role_id, firstname, surname, email, password_hash, student_id, course, group_id) values
(get_role_id('Student'), 'Алексей', 'Синкевич', 'sinkevich@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 1070211903, 4, 10702119);

insert into students(role_id, firstname, surname, email, password_hash, student_id, course, group_id) values
(get_role_id('Student'), 'Алина', 'Навоева', 'navoeva@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 1070211904, 4, 10702119);

insert into students(role_id, firstname, surname, email, password_hash, student_id, course, group_id) values
(get_role_id('Student'), 'Анастасия', 'Коледа', 'koleda@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 1070211905, 4, 10702119);

insert into students(role_id, firstname, surname, email, password_hash, student_id, course, group_id) values
(get_role_id('Student'), 'Владислав', 'Кургей', 'kurhey@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 1070211906, 4, 10702119);

insert into students(role_id, firstname, surname, email, password_hash, student_id, course, group_id) values
(get_role_id('Student'), 'Юлианна', 'Костевич', 'kostevich@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 1070211907, 4, 10702119);

insert into students(role_id, firstname, surname, email, password_hash, student_id, course, group_id) values
(get_role_id('Student'), 'Артём', 'Карпук', 'karpuk@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 1070211909, 4, 10702119);

insert into students(role_id, firstname, surname, email, password_hash, student_id, course, group_id) values
(get_role_id('Student'), 'Андрей', 'Кисель', 'kisel@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 1070211910, 4, 10702119);

insert into students(role_id, firstname, surname, email, password_hash, student_id, course, group_id) values
(get_role_id('Student'), 'Дарья', 'Камаева', 'kamaeva@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 1070211911, 4, 10702119);

insert into students(role_id, firstname, surname, email, password_hash, student_id, course, group_id) values
(get_role_id('Student'), 'Никита', 'Шаврук', 'shavruk@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 1070211912, 4, 10702119);

insert into students(role_id, firstname, surname, email, password_hash, student_id, course, group_id) values
(get_role_id('Student'), 'Данил', 'Чернышов', 'chernishow@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 1070211913, 4, 10702119);

insert into students(role_id, firstname, surname, email, password_hash, student_id, course, group_id) values
(get_role_id('Student'), 'Дарья', 'Ярош', 'yarosh@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 1070211914, 4, 10702119);

insert into students(role_id, firstname, surname, email, password_hash, student_id, course, group_id) values
(get_role_id('Student'), 'Екатерина', 'Грицкевич', 'gritskevich@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 1070211915, 4, 10702119);

insert into students(role_id, firstname, surname, email, password_hash, student_id, course, group_id) values
(get_role_id('Student'), 'Борис', 'Микитич', 'mikitich@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 1070211916, 4, 10702119);

insert into students(role_id, firstname, surname, email, password_hash, student_id, course, group_id) values
(get_role_id('Student'), 'Денис', 'Леоненко', 'leonenko@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 1070211917, 4, 10702119);

insert into students(role_id, firstname, surname, email, password_hash, student_id, course, group_id) values
(get_role_id('Student'), 'Данил', 'Фалькович', 'falkovich@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 1070211918, 4, 10702119);

insert into students(role_id, firstname, surname, email, password_hash, student_id, course, group_id) values
(get_role_id('Student'), 'Махмуд', 'Хамади', 'hamadi@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 1070211919, 4, 10702119);

insert into students(role_id, firstname, surname, email, password_hash, student_id, course, group_id) values
(get_role_id('Student'), 'Николай', 'Селивончик', 'selivonchik@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 1070211920, 4, 10702119);

insert into students(role_id, firstname, surname, email, password_hash, student_id, course, group_id) values
(get_role_id('Student'), 'Дмитрий', 'Вонславович', 'vonslavovich@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 1070211921, 4, 10702119);




insert into teachers (id, firstname, surname, email, password_hash, role_id, departament_id, job_title)
values (101, 'Ирина', 'Борисова', 'borisova@bntu.by', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', get_role_id('Teacher'),
        get_dep_by_short('ПОИСиТ'), 'Старший преподаватель');

insert into teachers (id, firstname, surname, email, password_hash, role_id, departament_id, job_title)
values (102, 'Екатерина', 'Стальцова', 'staltsova@bntu.by', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', get_role_id('Teacher'),
        get_dep_by_short('ПОИСиТ'), 'Ассистент');

insert into teachers (id, firstname, surname, email, password_hash, role_id, departament_id, job_title)
values (103, 'Андрей', 'Куприятнов', 'kupriyanov@bntu.by', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', get_role_id('Teacher'),
        get_dep_by_short('ПОИСиТ'), 'Доцент');

insert into teachers (id, firstname, surname, email, password_hash, role_id, departament_id, job_title)
values (104, 'Юрий', 'Полозков', 'kupriyanov@bntu.by', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', get_role_id('Teacher'),
        get_dep_by_short('ПОИСиТ'), 'Заведующий кафедрой');

insert into teachers (id, firstname, surname, email, password_hash, role_id, departament_id, job_title)
values (105, 'Валерий', 'Сидорик', 'sidorik@bntu.by', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', get_role_id('Teacher'),
        get_dep_by_short('ПОИСиТ'), 'Доцент');

insert into teachers (id, firstname, surname, email, password_hash, role_id, departament_id, job_title)
values (106, 'Ирина', 'Тетерюкова', 'teterukova@bntu.by', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', get_role_id('Teacher'),
        get_dep_by_short('ПОИСиТ'), 'Старший преподаватель');

insert into teachers (id, firstname, surname, email, password_hash, role_id, departament_id, job_title)
values (107, 'Виктор', 'Юденков', 'udenkov@bntu.by', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', get_role_id('Teacher'),
        get_dep_by_short('ПОИСиТ'), 'Старший преподаватель');

insert into teachers (id, firstname, surname, email, password_hash, role_id, departament_id, job_title)
values (108, 'Лидия', 'Воронич', 'voronich@bntu.by', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', get_role_id('Teacher'),
        get_dep_by_short('ПОИСиТ'), 'Ассистент');

insert into teachers (id, firstname, surname, email, password_hash, role_id, departament_id, job_title)
values (109, 'Ирина', 'Ковалёва', 'ilkovaleva@bntu.by', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', get_role_id('Teacher'), get_dep_by_short('ПОИСиТ'), 'Доцент');
