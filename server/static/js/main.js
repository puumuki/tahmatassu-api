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
			var that = this;
			var filename = this.ui.filename.val();
			var markdown = this.ui.textarea.val();
			this.io({ url: '/api/recipe',
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
	});

}());