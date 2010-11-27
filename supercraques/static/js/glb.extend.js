jQuery.extend({
	/*
	diz o tipo do objeto value passado por parametro.
	*/
	typeOf: function(value){
	    var s = typeof value;
	    if (s === 'object') {
	        if (value) {
	            if (typeof value.length === 'number' &&
	                    !(value.propertyIsEnumerable('length')) &&
	                    typeof value.splice === 'function') {
	                s = 'array';
	            }
	        } else {
	            s = 'null';
	        }
	    }
	    return s;
	},
	/*diz o indice do objeto value em um array.*/
	indexof: function(array,value){
	    for(i=0; i < array.length; i++){
	        if(array[i] == value){
	            return i;
	        }
	    }

	    return -1;
	}
});

