#!/usr/bin/node

const nodemailer = require('nodemailer');

// Email configuration
const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: '',
    pass: ''
  }
});

// Email content
const mailOptions = {
  from: 'ifeanyi3797@gmail.com',
  to: 'ifeanyiikpenyi@yahoo.com',
  subject: 'Test Email from Node.js',
  text: 'This is a test email sent from Node.js using Yahoo Mail.'
};

// Send email
transporter.sendMail(mailOptions, function(error, info){
  if (error) {
    console.log(error);
  } else {
    console.log('Email sent: ' + info.response);
  }
});
