$(document).ready(function() {
    // Função para cadastrar usuário
    $('#cadastroForm').submit(function(e) {
        e.preventDefault();

        let cadastroData = {
            login: $('#login').val(),
            senha: $('#senha').val()
        };

        $.post('/usuarios', JSON.stringify(cadastroData), function(data) {
            alert(data.message);
            // Redirecionar para a página de login após cadastro bem-sucedido
            window.location.href = "/";  // Redireciona para a página inicial após cadastro
        }).fail(function(error) {
            alert('Erro ao cadastrar usuário');
        });
    });

    // Função para login de usuário
    $('#loginForm').submit(function(e) {
        e.preventDefault();

        let loginData = {
            login: $('#loginUsername').val(),
            senha: $('#loginSenha').val()
        };

        $.post('/usuarios/login', JSON.stringify(loginData), function(data) {
            alert(data.message);
            if (data.usuario) {
                // Armazenar o ID do usuário na sessão
                sessionStorage.setItem('usuario_id', data.usuario.id);
                // Redirecionar para uma página após o login bem-sucedido, se necessário
                // window.location.href = "/outra_pagina"; 
            }
        }).fail(function(error) {
            alert('Erro ao fazer login');
        });
    });
});
