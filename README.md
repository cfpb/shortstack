# Shortstack

Shortstack will be a web application that does a very simple thing: render [Jinja2](http://jinja.pocoo.org/docs/dev/) templates from an on-disk project
 that resembles a traditional website (so, the URL /foo/ will be served by the template foo/index.html). All by itself, you might find it useful for prototypes and simple websites.


Things get interesting when you start writing extensions for Shortstack: extensions can add information to the template context, provide more complex rules for resolving URL's to 
templates (for example, specifying that URL's like /blog/my_post/ will use the template at \_layouts/articles.html), and return a list of all URL's that the extension adds (for generating static sites).

Shortstack shines when used as a rendering engine for content that may live in your CMS, data files, microservices, or all of the above.


## Open source licensing info
1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)


