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

			if(this.ui.filename.length > 0 && this.ui.filename.val().length == 0) {
				this._bindFileNameChange();	
			}

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
			var that = this;
			this.ui.textarea.bind('input propertychange', function() {
				var filename = $(this).val().split('\n')[0];
				that.ui.filename.val(filename);
			});
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
				onFailure:function() {that.ui.saveBtn.button('reset')}
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


	$(function() {
		Editor.init();
		$("textarea#editor").pagedownBootstrap();
		
	});
}());