delete from auth_user where  email='me@me.com';
select * from auth_user where email='me@me.com';
delete from repairsapi_employee where user_id = 11;
delete from repairsapi_customer where user_id = 11;
delete from authtoken_token where user_id = 11;
select * from repairsapi_employee;
delete from repairsapi_serviceticket where id = 11;