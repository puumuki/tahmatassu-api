(function() {

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
			this.save({name:filename, markdown:markdown})
		},

		_onSaveFailure : function() {
			console.log('Failed to save the recipe');
		},

		_onSaveSuccess : function() {
			console.log('Recipe was saved succesfully');
		},

		save : function(data) {
			$.ajax({
				url: '/api/recipe',
				data: JSON.stringify(data),
					  type: "POST",        		
				dataType: "json",
				processData: false,
				contentType: 'application/json',
				context: this,
				failure: this._onSaveFailure,
				success: this._onSaveSuccess,		        
			});
		}
	};


	$(function() {
		Editor.init();
	});

}());