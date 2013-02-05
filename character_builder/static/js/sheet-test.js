$(function() {
	window.Character = Backbone.Model.extend({
		idAttribute: "slugname",
		urlRoot:"../api/v1/character"
	});

	window.Characters = Backbone.Collection.extend({
		model:Character,
		url:"../api/v1/character"
	});

	window.CharacterView = Backbone.View.extend({
		render:function (eventName) {
			$(this.el).html(this.model.toJSON());
			return this;
		}
	});

	var AppRouter = Backbone.Router.extend({

		routes: {
			"":"home",
			"character/:id":"character"
		},

		home:function () {
			this.characters = new Characters();
			this.characters.fetch();
			console.log(this.characters);
			console.log('Something');
			console.log($('#app-content').html());
			$('#app-content').html('Do something.');
		},

		character:function (id) {
			console.log(id);
			/*
			this.character = this.characters.get(id);
			this.characterView = new CharacterView({model:this.character});
			console.log('Aw snap');
			$('#app-content').html(this.characterView.render().el);
			*/
		}
	});

	var app = new AppRouter();
	Backbone.history.start({ pushState: true, root: "/DnD/sheettest/"});
});