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

function mascaraDeTelefone(telefone) {
    const textoAtual = telefone.value;
    const isCelular = textoAtual.length === 11;
    const isFixo = textoAtual.length === 10;
    let textoAjustado;
    if (isCelular) {
        const parte0 = textoAtual.slice(0, 2);
        const parte1 = textoAtual.slice(2, 7);
        const parte2 = textoAtual.slice(7, 11);
        textoAjustado = `${parte0}${parte1}-${parte2}`
        telefone.value = textoAjustado;
    } else if (isFixo) {
        const parte0 = textoAtual.slice(0, 2);
        const parte1 = textoAtual.slice(2, 6);
        const parte2 = textoAtual.slice(6, 10);
        textoAjustado = `${parte0}${parte1}-${parte2}`
        telefone.value = textoAjustado;
    } else {
        telefone.value = 'Número incorreto!';
        //alert(isFixo + ' - Número de telefone deve estar no padrão de Celular: "(99) 9 9999-9999" ou Fixo "(99) 9999-99999"! ')
    }
}

function tiraHifen(telefone) {
    const textoAtual0 = telefone.value.replace('/-/', '');
    const textoAtual1 = textoAtual0.replace('/(/', '');
    const textoAtual2 = textoAtual1.replace('/)/', '');
    const textoAjustado = textoAtual2.replace('/ /', '');
    telefone.value = textoAjustado;
}