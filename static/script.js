const metadata_list = document.getElementById('metadata_list');

fetch('/api/metadata')
    .then((res) => res.json())
    .then(data => {
        console.log(data)
        metadata_list.innerHTML = ''

        if (data.tags.length === 0) {
            metadata_list.innerHTML = '<li>Nenhuma tag encontrada</li>';
            return;
        }

        data.tags.forEach(item => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `<strong>${item.tags}</strong>: ${item.values}`;
            metadata_list.append(listItem);
        });
    })
    .catch(error => {
        console.error('Erro ao buscar dados:', error);
        list.innerHTML = '<li>Ocorreu um erro ao carregar os dados.</li>';
    });