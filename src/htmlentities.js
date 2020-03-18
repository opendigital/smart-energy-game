////
// https://ourcodeworld.com/articles/read/188/encode-and-decode-html-entities-using-pure-javascript
// The previous code creates a global variable (in the window) named htmlentities. This object contains the 2 methods encode and decode.
// To convert a normal string to its html characters use the encode method :
// htmlentities.encode("Hello, this is a test stríng > < with characters that could break html. Therefore we convert it to its html characters.");
// // Output "&#72;&#101;&#108;&#108;&#111;&#44;&#32;&#116;&#...
// To convert an encoded html string to readable characters, use the decode method :
// htmlentities.decode("&#72;&#101;&#108;&#108;&#111 ... &#114;&#115;&#46;");
// // Output
// "Hello, this is a test stríng > < with characters that could break html. Therefore we convert it to its html characters."
///
(function(window){
	window.htmlentities = {
		/**
		 * Converts a string to its html characters completely.
		 *
		 * @param {String} str String with unescaped HTML characters
		 **/
		encode : function(str) {
			var buf = [];

			for (var i=str.length-1;i>=0;i--) {
				buf.unshift(['&#', str[i].charCodeAt(), ';'].join(''));
			}

			return buf.join('');
		},
		/**
		 * Converts an html characterSet into its original character.
		 *
		 * @param {String} str htmlSet entities
		 **/
		decode : function(str) {
			return str.replace(/&#(\d+);/g, function(match, dec) {
				return String.fromCharCode(dec);
			});
		}
	};
})(window);
