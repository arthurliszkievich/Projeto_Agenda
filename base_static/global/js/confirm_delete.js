document.addEventListener('DOMContentLoaded', () => {
    // Encontra o formulário pelo ID
    const deleteForm = document.getElementById('form-delete-contact');

    if (deleteForm) {
        deleteForm.addEventListener('submit', function(event) {
            // Mostra a caixa de diálogo de confirmação padrão do navegador
            const userConfirmed = confirm("Tem certeza que deseja excluir este contato? Esta ação não pode ser desfeita.");

            // Se o usuário clicou em "Cancelar" (userConfirmed é false)
            if (!userConfirmed) {
                // Impede que o formulário seja enviado
                event.preventDefault(); 
                console.log('Exclusão cancelada.');
            }
            // Se o usuário clicou em "OK", o formulário será enviado normalmente.
        });
    }
});