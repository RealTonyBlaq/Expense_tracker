#!/usr/bin/node

const email = 'ife@gmail.co';
const name = 'ifeanyi';

const data = {
    email,
    name,
};

console.log(data);

const check = email.split('.')[1].length >= 2;
console.log(check);
