-- Active: 1774607189663@@127.0.0.1@5432@sakila
select first_name,last_name from actor limit 10;


select first_name,last_name as surname from actor limit 10;


select first_name || ' ' || last_name from actor limit 10;
select first_name || '-' || last_name from actor limit 10;

select first_name || ' ' || last_name "Full Name" from actor limit 10;



#PostgreSQL 表别名

select F.film_id,F.title from film F where not exists (select 1 from inventory i where i.film_id = 	F.film_id );

#PostgreSQL IN 运算符用法与实例

select * from actor where last_name in ('ALLEN','DAVIS');
select * from actor where last_name = 'ALLEN' or last_name = 'DAVIS';

select count(*) from film where film_id in (select film_id from inventory);

select count(*) from film f where exists(select 1 from inventory i where i.film_id = f.film_id);


select title,length from film where length between 95 and 98;

select count(*) from film where rental_rate between 3 and 5;



select * from actor where first_name like 'P%';

select * from actor where first_name like '%ES';

select * from actor where first_name like '%AM%';


#PostgreSQL IS NULL 语法

select first_name,last_name,picture from staff where picture is null;

# PostgreSQL EXISTS 语法

select film_id,title from film f where exists (select 1 from inventory i  where i.film_id  = f.film_id );

select film_id,title from film f where not exists(select 1 from inventory i  where i.film_id  = f.film_id );


select first_name,last_name from customer c where exists (select 1 from  payment p where p.customer_id = c.customer_id and p.amount >11)
order  by first_name,last_name;


select 99 > all(select rental_rate from film);


select 66 < all(select rental_rate from film);

select count(*) from film where rental_rate >= all(select rental_rate from film);

#PostgreSQL ANY 运算符的用法与实例


select 5 < any(select rental_rate from film);

select 1 >= any(select rental_rate from film);



#PostgreSQL GROUP BY 用法与实例

select last_name from actor;
select last_name from actor group by last_name;

select last_name,count(*) from actor group by last_name order by count(*) desc;

select customer_id,sum(amount) total from payment group by customer_id order by total desc limit 10;


#PostgreSQL HAVING 用法与实例

select rating,count(*) from film group by rating order by count(*) desc;

select rating,count(*) from film group by rating having count(*) > 200 order by count(*) desc;

select customer_id,sum(amount) total from payment group by customer_id HAVING sum(amount) > 180 order by total desc;


#PostgreSQL GROUPING SETS 用法与实例
select rating,count(*) from film group by rating order by rating;

select rental_rate,count(*) from film group by rental_rate order by rental_rate;


select rating,NULL rental_rate,count(*) from film group by rating union all select null rating,rental_rate,count(*) from film group by rental_rate order by rating,rental_rate;

#PostgreSQL ROLLUP 用法与实例
select rating,rental_rate,count(*) from film group by grouping sets((rating,rental_rate),(rating),()) order by rating,rental_rate;

select rating,rental_rate,count(*) from film group by cube(rating,rental_rate) order by rating,rental_rate;


#PostgreSQL 连接类型

create table student(student_id integer not null,name varchar(45) not null,primary key(student_id));
create table student_score(student_id integer not null,subject varchar(45) NOT NULL,score integer not null);

insert into student (student_id,name) values (1,'TIM'),(2,'Jim'),(3,'Lucy');

insert into student_score (student_id,subject,score) values (1,'English',90),(1,'Math',80),(2,'English',85),(5,'English',92);

SELECT * FROM student;

select student.*,student_score.* from student cross join student_score;

select student.*,student_score.* from student inner join student_score on student.student_id = student_score.student_id;

#在 PostgreSQL EXISTS 运算符中使用子查询
select * from language where exists (select * from film where film.language_id = language.language_id);
select * from film where film.language_id = language.language_id;

select * from language where language_id in (select distinct language_id from film);


