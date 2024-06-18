async function ativaInformacoes(id) {
    document.getElementById('container-informacoes').style.display = 'flex';
    const response = await fetch(`/api/pokemon/${id}`);
    if (response.ok) {
        const data = await response.json();
        const conteudo = `
            <img src="${data.sprites}" alt="${data.name}" class="img-fluid" width=50%>
            <h3>${data.name}</h3>
            <p><strong>ID:</strong> ${data.id}</p>
            <p><strong>Tipos:</strong> ${data.types.join(', ')}</p>
        `;
        document.getElementById('informacoes-conteudo').innerHTML = conteudo;
    } else {
        document.getElementById('informacoes-conteudo').innerHTML = '<p>Detalhes do Pokémon não disponíveis.</p>';
    }
}

function escondeInformacoes() {
    document.getElementById( 'container-informacoes' ).style.display = 'none';
}