const metadata_list = document.getElementById('metadata_list');
const form = document.getElementById('uploadForm');
const remove_metadata = document.getElementById('remove_metadata');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(form)
    const res1 = await fetch('/upload', { method: 'POST', body: formData });
    const data1 = await res1.json();
    const nomeDoArquivo = data1.filename;

    const res2 = await fetch(`/api/metadata?filename=${nomeDoArquivo}`);
    const data2 = await res2.json();

    metadata_list.innerHTML = ''

    if (data2.tags.length === 0) {
        metadata_list.innerHTML = '<li>Nenhuma tag encontrada</li>';
        return;
    }

    data2.tags.forEach(item => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `<strong>${item.tags}</strong>: ${item.values}`;
        metadata_list.append(listItem);
    });

    const removeButton = document.createElement('button');
    removeButton.innerHTML = 'Remover';
    removeButton.disabled = false;
    removeButton.onclick = async () => {
        const removeFormData = new FormData();
        removeFormData.append('filename', nomeDoArquivo);

        const res3 = await fetch('/remove/metadata', {
            method: 'POST',
            body: removeFormData
        });
        const data3 = await res3.json();

        if (data3.status == 'success') {
            console.log('Metadados removidos');
            metadata_list.innerHTML = 'Metadados removidos!';
            remove_metadata.innerHTML = '';
        } else {
            console.log(`Erro ao remover: ${data3.message}`);
            removeButton.disabled = true;
        }
    };

    remove_metadata.append(removeButton);
});

