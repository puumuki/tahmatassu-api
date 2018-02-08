/* ------------------------ 
 * Footer logic
 * ------------------------ */
"use strict";

var footerTemplate = require("./../templates/footer.hbs");

function footer( $target ) { 
  $('footer').append(footerTemplate());  
}

module.exports = footer;
