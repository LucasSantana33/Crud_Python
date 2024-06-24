$(document).ready(function() {
    // Função para adicionar filme
    $('#filmeForm').submit(function(e) {
        e.preventDefault();

        let filmeData = {
            titulo: $('#titulo').val(),
            diretor: $('#diretor').val(),
            ano: $('#ano').val(),
            genero: $('#genero').val(),
            usuario_id: $('#usuario_id').val()  // Busca o ID do usuário do formulário
        };

        $.post('/filmes', JSON.stringify(filmeData), function(data) {
            alert(data.message);
            $('#titulo').val('');
            $('#diretor').val('');
            $('#ano').val('');
            $('#genero').val('');
            $('#usuario_id').val('');
            listarFilmes();  // Atualiza a lista de filmes após adicionar um novo filme
        }).fail(function(error) {
            alert('Erro ao adicionar filme');
        });
    });

    // Função para listar filmes
    function listarFilmes() {
        $.get('/filmes', function(data) {
            $('#filmesList').empty();
            data.forEach(function(filme) {
                $('#filmesList').append(`<li class="list-group-item">${filme.titulo} - ${filme.diretor} (${filme.ano})</li>`);
            });
        }).fail(function(error) {
            alert('Erro ao carregar lista de filmes');
        });
    }

    // Chamada inicial para listar filmes ao carregar a página
    listarFilmes();
});
