"use strict";

var TahmatassuLocalDB = require('./tahmatassu-local-db');

//const BASE_PATH = 'http://localhost:8080';
const BASE_PATH = 'http://194.168.8.100:8080';

class Tahmatassu {

  constructor() {
    this.localDB = new TahmatassuLocalDB();
  }

  /**
   * Fetch receipts first from indexedDB and if that fails from server.
   * 
   * @return {Promise} resolved when fetching fails
   */
  fetchReceipts() {
    var self = this;

    return new Promise((success, failure) => {
      self.localDB.openConnection().then(function(db) {
  
        db.getReceipts().then(function( receipts ) {
          
          //No receipts available, then try to fetch them from the server   
          if( receipts.length === 0 ) {
      
            self.fetchRecipesFromServer().then( (receipts) => {

              //Extract receipt title from the data
              var receipts = receipts.map(( receipt ) => {
                receipt.title = Tahmatassu.getReceiptTitle( receipt );
                return receipt;
              });

              db.saveReceipts( receipts );  
              
              success(receipts);
            }).catch(function() {
              console.error('No recovery available or try again after when coming back to online');
              failure("/No recovery available or try again after when coming back to online");
            });
      
          } else {
            success( receipts );
          }   

        }).catch(function( error ) {
          console.error(error);
          failure( error );
        });
      });
    });
  }

  fetchReceiptByName(name) {
    var self = this;
    return new Promise((success, failure)=> {
      self.fetchReceipts().then((receipts) => {
        var receipt = receipts.find((receipt) => {
          return receipt.name === name;
        });

        success(receipt);
      }).catch(failure);
    });
  }

  fetchRecipesFromServer() {
    return new Promise((success, failure) => {
      return $.get( BASE_PATH + '/api/v2/recipes' ).done(function( data ) {
        
        try {
          success( JSON.parse( data ) );
        } catch( error ) {
          failure( "Could not parse JSON", error );
        } 

      }).fail(function( error ) {
        failure( error );
      });
    });
  }

  /**
   * Extract receipt title from the markdown content. Takes the first line of the markdown content-
   * @param {object} receipt  
   * @return {string} receipt's title
   */
  static getReceiptTitle( receipt ) {
    var title = '';

    if( receipt && receipt.markdown ) {
      var lines = receipt.markdown.split('\n');

      title =  lines.length > 0 ? lines[0] : '';
    }

    return title;
  }
}

module.exports = Tahmatassu;

