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
    id serial primary key ,
    name text not null unique,
    shortcut text not null unique,
    description text,
    icon_path text
);

create or replace function get_faculty_by_shortcut(shortname text)
returns int as $factuly_id$
    declare faculty_id int;
    begin
        select id into faculty_id from faculties where shortcut=shortname;
        return faculty_id;
    end;
$factuly_id$ language plpgsql;

insert into faculties (name, shortcut, description) values ('Факультет Информационных Технолоий и Робототехники', 'ФИТР', 'Просто норм, факультет для пацанов');

create table groups(
    id int primary key not null unique,
    faculty_id int not null references faculties(id)
);

insert into groups (id, faculty_id) values (10702119, get_faculty_by_shortcut('ФИТР'));


create table users (
    id serial primary key,
    firstname text not null,
    surname text not null,
    email text not null,
    password_hash text not null,
    role_id int references roles(id),
    avatar text
);

create table students(
    student_id int not null,
    course int not null,
    group_id int not null references groups(id)
) inherits (users);

insert into students(role_id, firstname, surname, email, password_hash, student_id, course, group_id) values
(get_role_id('Student'), 'Данила', 'Кислицин', 'dangost16@gmail.cm', 'a66b47e6b2fdc5aae2aa914e4718cf2af21f70c7c842ad5ce8b2ac7946840fec', 1070211908, 4, 10702119);

insert into users(firstname, surname, email, password_hash, role_id) values
('Dan', 'Gost', 'dangost16@gmail.com', 'f74b4df676be77106dd1ebecf3bd1657f1b8973858f92878184e41eb488ab9bd', get_role_id('Admin'))