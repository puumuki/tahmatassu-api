(function() {

	$('.recipe-list span.remove').click(function(e) {
		
		var recipename = $(e.currentTarget).data('recipename');

		$('#modal-dialog').modal();
		
		$('#modal-dialog button.delete').click(function() {
			Editor.io({
				url: '/api/recipe/' + recipename,
				type: 'DELETE',
				onSuccess: function() {
					$(e.currentTarget).closest('li').fadeOut('slow');
					$('#modal-dialog').modal('hide');
				} 
			});
		});
	});

	var Editor = {

		fileEnding : '.md',

		ui : {
			filename : $('#editor input[name="filename"]'),
			textarea : $('#editor textarea'),
			saveBtn : $('#editor .save-btn')
		},



		init : function() {
			this.el = '#editor';
			
			var that = this;
			
			$('.save-btn', this.el).click(function(e) {
				that._onClickSaveBtn(e);
			});

			this._fileNameEditable = this.ui.filename.length > 0 && this.ui.filename.val().length == 0;

			this._bindFileNameChange();	
			
			//Bind sortcut keys
			key('ctrl+s', function(){  
				that.save();
				return false;
			});

			key('ctrl+b', function(){  
				that.boldSelection();
				return false;
			});

			//Allow sortcut to work in textareas
			key.filter = function(event){
			  var tagName = (event.target || event.srcElement).tagName;
			  return !(tagName == 'INPUT' || tagName == 'SELECT');
			}
		},

		makeHeader : function() {

		},

		italizeSelection : function() {

		},

		boldSelection : function() {
			var selection = this.ui.textarea.selection();
			this.ui.textarea.selection('replace', {text: '_'+ selection+'_'});
		},

		_bindFileNameChange : function() {
			this.ui.textarea.bind('input propertychange', _.bind(function(event) {
				if(!this._fileNameEditable) {
					return;
				}

				var filename = $(event.currentTarget).val().split('\n')[0];
				this.ui.filename.val(filename);
			}, this));
		},

		_onClickCancelBtn : function(e) {
			//$(this.ui.filename).popover('show');
		},

		_onClickSaveBtn : function(e) {
			this.save();
		},

		save: function() {
			var that = this;
			var filename = this.ui.filename.val();
			var markdown = this.ui.textarea.val();
			this.io({ 
				url: '/api/recipe',
				type: 'POST',
				data:{name:filename+this.fileEnding, 
					  markdown:markdown}, 
				onFailure:function() {
					that.ui.saveBtn.button('reset')
				}, 
				onSuccess: _.bind(function() {
					this._fileNameEditable = false;
				}, this)
			});	
		},

		io : function(data) {
			var that = this;
			that.ui.saveBtn.button('loading');
			$.ajax({
				url: data.url,
				data: JSON.stringify(data.data),
					  type: data.type,        		
				dataType: "json",
				processData: false,
				contentType: 'application/json',
				context: this,
				error: data.onFailure,
				success: data.onSuccess
			}).done(function() {
				that.ui.saveBtn.button('reset');
			});
		}
	};

	function replaceImageDialogBtn() {
		var button = $('#wmd-image-button-0').clone();
		$('#wmd-image-button-0').remove();
		$('#wmd-button-group2-0').append(button);		
		button.click(function() {
			$('#image-dialog').modal({});
		});		
	}

	function imageDialog() {

		var imageDialogEl = $('#image-dialog');

		$('span.image', imageDialogEl).click(function() {
			$(this).toggleClass('text-primary');
			$(this).closest('tr').find('img').toggleClass('image-primary');
		});

		$('.btn-primary').click(function() {

			var images = $('span.image', imageDialogEl ).filter(function(i, el) {
				return $(el).hasClass('text-primary');

			}).map(function(i, el) {
				return '![](' + $(el).data('imageurl') +')';
			});		

			var images = $.makeArray(images).join('\n');		
			var oldText = Editor.ui.textarea.val();
			
			var newText = oldText.substring(0, Editor.ui.textarea.prop('selectionStart'));
			newText += images;
			newText += oldText.substring(Editor.ui.textarea.prop('selectionEnd'), oldText.length-1);

			Editor.ui.textarea.val(newText);
			Editor.ui.textarea.data('markdowneditor').refreshPreview();

			imageDialogEl.modal('hide');
		});

		//Init-tablesorter
		var language = {
		    "emptyTable":     "Kuvia ei ole saatavilla",
		    "info":           "Näytetään _START_ - _END_  / _TOTAL_ kuvasta",
		    "infoEmpty":      "Ei kuvia saatavilla",
		    "infoFiltered":   "(Suodatettiin _MAX_ hakutuloksesta)",
		    "infoPostFix":    "",
		    "thousands":      " ",
		    "lengthMenu":     "Näytä _MENU_ tulosta",
		    "loadingRecords": "Lataa...",
		    "processing":     "Hakee...",
		    "search":         "Haku:",
		    "zeroRecords":    "Hakuehdoilla ei löytynyt kuvia",
		    "paginate": {
		        "first":      "Ensimmäinen",
		        "last":       "Viimeinen",
		        "next":       "Seuraava",
		        "previous":   "Edellinen"
		    },
		    "aria": {
		        "sortAscending":  "Aktivoi järjestääksesi sarake nousevasti",
		        "sortDescending":  "Aktivoi järjestääksesi sarake laskevasti"
		    }
		};

 		$('#image-dialog table').dataTable({
 			"language":language
        });
	}

	$(function() {
		Editor.init();
		$("textarea#editor").pagedownBootstrap();

		replaceImageDialogBtn();
		imageDialog();

		$('input[type=file]').bootstrapFileInput();		
	});
}());