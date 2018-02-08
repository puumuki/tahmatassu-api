/* ------------------------ 
 * Top navigation bar logic 
 * ------------------------ */
"use strict";

var headerTemplate = require("./../templates/header.hbs");

var navigation = {
  items: [
    {href:'#/', text:'Home'},
    {href:'#/contact',    text:'Contact'}
  ]
}

function header() { 

  $('header.navigation').replaceWith( headerTemplate(navigation));  

  $('.icon').click(function() {
    $('header').toggleClass('open-menu');
  });
}

module.exports = header;
