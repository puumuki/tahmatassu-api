var showdown  = require('showdown'),
    converter = new showdown.Converter();

/**
 * Handlebars markdown helper function
 * @param {*} markdown 
 */
module.exports = function(markdown){
    return converter.makeHtml(markdown);
}