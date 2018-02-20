/**
 * This file containg routing logic. The application user clicks a link in browser and so
 * create an event. The routing is applied to some of the key links, like contact, 
 * "home" and so on. This logic makes this page a "single page application", by always only 
 * replacing <section class="content"> element content. 
 */ 
 "use strict";

var Tahmatassu = require('./tahmatassu');

var indexTemplate = require("./../templates/index.hbs");
var contactTemplate = require("./../templates/contact.hbs");

var loadingTemplate = require("./../templates/loading.hbs");
var receiptTemplate = require("./../templates/receipt.hbs");
var pageNotFoundTemplate = require("./../templates/404.hbs");

var route = require('riot-route');
var tahmatassu = new Tahmatassu();

function replaceContent( element, options ) {
  console.info('Open ', options ? options.text : '' );
  $('header').removeClass('open-menu');  
  $('section.content').empty().append( element );
}

route('/', function() { 
  replaceContent( loadingTemplate(), {text: 'home'} );

  tahmatassu.fetchReceipts().then(function(receipts) {

    var firstletters = receipts.map((r)=>r.title.toUpperCase().substring(0,1));
    var receiptsByTitleFirstLetter = {};

    //Filter out multiple occurances
    var letters = new Set( firstletters );

    //Populate object with empty arrays
    letters.forEach((letter) => {
      receiptsByTitleFirstLetter[ letter ] = [];
    });

    receipts.forEach((receipt) => {
      var letter = receipt.title.toUpperCase().substring(0,1);
      receiptsByTitleFirstLetter[ letter ].push( receipt )
    });
    
    replaceContent( indexTemplate({letters: receiptsByTitleFirstLetter}), {text:'index'} )
  }).catch(function( errors ) {
    console.error( errors );
  });
});

route('/receipt/*', function( name ) {
  tahmatassu.fetchReceiptByName( name ).then((receipt) => {
    replaceContent( receiptTemplate( receipt ), {text: 'Receipt ' + receipt.title + 'found' });   
  }).catch(function( error ) {
    replaceContent( pageNotFoundTemplate( error ), {text: '404 - Page not found'});
  });
});

route('/contact', function() {
  replaceContent( contactTemplate(), {text: 'contact'} );
});


// ServiceWorker is a progressive technology. Ignore unsupported browsers
if ('serviceWorker' in navigator) {
  console.log('CLIENT: service worker registration in progress.');
  navigator.serviceWorker.register('http://127.0.0.1:8080/serviceworker.js').then(function() {
    console.log('CLIENT: service worker registration complete.');
  }, function() {
    console.log('CLIENT: service worker registration failure.');
  });
} else {
  console.log('CLIENT: service worker is not supported.');
}



exports.router = route;