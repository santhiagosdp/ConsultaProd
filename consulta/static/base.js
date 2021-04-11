// Verificar se esta sendo carregado arquivo XML 
var file = document.getElementById('myfile');

file.onchange = function(e) {
    var ext = this.value.match(/\.([^\.]+)$/)[1];
    switch (ext) {
        case 'xml':
        case '.xml':
            //alert('Aceito');
            break;
        default:
            ///$('.alert').alert('Por Favor, Carregar arquivos no formato .XML')
            alert('Por Favor, Carregar arquivos no formato .XML');
            this.value = '';
    }
};