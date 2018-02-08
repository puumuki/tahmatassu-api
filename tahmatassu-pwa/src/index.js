global.$ = require('jquery');
var _ = require('underscore');

//Static areas
var header = require('./js/header');
var footer = require('./js/footer');
var router = require('./js/router').router;

//Initialize page static areas
header();
footer();

//Start listening routing actions
router.start(true);

//Addes a loaded class to the body element. This start nonblur css transient effect.
$(function() {
   $('body').addClass('loaded');
});