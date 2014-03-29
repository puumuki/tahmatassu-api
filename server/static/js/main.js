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

		init : function() {
			this.el = '#editor';
			
			var that = this;
			
			$('.save-btn', this.el).click(function(e) {
				that._onClickSaveBtn(e);
			});
		},

		_onClickCancelBtn : function(e) {

		},

		_onClickSaveBtn : function(e) {
			var filename = $('input',this.el).val();
			var markdown = $('textarea',this.el).val();
			this.io({ url: '/api/recipe',
						type: 'POST',
						data:{name:filename, markdown:markdown}})
		},

		_onSaveFailure : function() {
			console.log('Failed to save the recipe');
		},

		_onSaveSuccess : function() {
			console.log('Recipe was saved succesfully');
		},

		io : function(data) {
			$.ajax({
				url: data.url,
				data: JSON.stringify(data.data),
					  type: data.type,        		
				dataType: "json",
				processData: false,
				contentType: 'application/json',
				context: this,
				failure: data.onFailure || this._onSaveFailure,
				success: data.onSuccess || this._onSaveSuccess,		        
			});
		}
	};


	$(function() {
		Editor.init();
	});

}());