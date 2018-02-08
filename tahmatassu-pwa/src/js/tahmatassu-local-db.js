
const VERSION = 1;

class TahmatassuLocalDb {
 
  /**
   * Open connection to IndexedDB
   * @returns {Promise} resolved when connection is opened, rejected on error
   */
  openConnection() {

    var self = this;
    var indexedDB = this.getIndexedDB();

    this.deferred = new Promise((success, failure) => {
      if (indexedDB) {

        self._request = indexedDB.open("Tahmatassu", VERSION);

        self._request.onupgradeneeded = this._onUpgradeNeeded;

        self._request.onsuccess = (event) => {
          self._datastore = event.target.result;
          success(self);
        };

        self._request.onerror = (event) => {
          console.log("Error during creating localdb", event);
          failure(event);
        }

      } else {
        failure("No indexded DB available");
      }
    });

    return this.deferred;
  }

  _onUpgradeNeeded(e) {
    console.info("Creating indexedDB");

    var db = e.target.result;

    // Delete the old datastore.
    if (db.objectStoreNames.contains('receipts')) {
      db.deleteObjectStore('receipts');
    }

    // Create a new datastore.
    var store = db.createObjectStore('receipts', {
      keyPath: 'name'
    });
  }

  getReceipts(receipts) {

    var db = this._datastore;

    return new Promise((success, failure) => {
      var transaction = db.transaction(["receipts"], IDBTransaction.READ_ONLY);
      var objectStore = transaction.objectStore("receipts");

      var keyRange = IDBKeyRange.lowerBound(0);
      var cursorRequest = objectStore.openCursor(keyRange);

      var receipts = [];

      cursorRequest.onsuccess = function (e) {
        var result = e.target.result;

        if (!!result == false) {
          return;
        }

        receipts.push(result.value);

        result.continue();
      };

      transaction.oncomplete = function (e) {
        success(receipts);
      };

      cursorRequest.onerror = failure;
    });
  }

  saveReceipts(receipts) {
    var db = this._datastore;

    var tx = db.transaction(["receipts"], "readwrite");
    var objectStore = tx.objectStore("receipts")

    receipts.forEach((receipt) => {
      objectStore.put(receipt);
    });
  }

  getIndexedDB() {
    // This works on all devices/browsers, and uses IndexedDBShim as a final fallback 
    return window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB || window.shimIndexedDB;
  }

  _onsuccess() {
    console.log("Connection Open to Local DB")
  }

  closeConnection() {
    this._connection.close();
  }
}

module.exports = TahmatassuLocalDb;