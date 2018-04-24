drop database if exists test;

create database test charset=utf8;

use  test;
grant select, insert, update, delete on test.* to 'root'@'localhost' identified by 'mysql';

create table user (
    `id` varchar(50) not null,
    `name` varchar(50) not null,
    primary key (`id`)
);
