import Scraper

## passando o dicionário das tags e classes

dict_1 = {
    'user_id': {
        'tag': 'a',
        'class': 'iPqaD _F G- ddFHE eKwUx btBEK fUpii',
        'attr': 'href'
    },
    
    'date': {
        'tag': 'div',
        'class': 'eRduX',
        'attr': 'text'
    }
}


scr_1 = Scraper.main(dict_1)

aaaaa = scr_1.give_me_info()

Scraper.main.quit_()

##damnnnn daniel 
# It works! 