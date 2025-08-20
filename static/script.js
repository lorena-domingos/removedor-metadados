const metadata_list = document.getElementById('metadata_list');
const form = document.getElementById('uploadForm');
const remove_metadata = document.getElementById('remove_metadata');
const extensaoPermitida = ["jpg", "jpeg"];

const removeButton = document.createElement('button');
remove_metadata.appendChild(removeButton);
removeButton.innerHTML = 'Remover';
removeButton.disabled = true;

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const fileInput = form.querySelector('input[type="file"]');
    const file = fileInput.files[0];

    if (!file) {
        alert("Nenhum arquivo selecionado!");
        return;
    }

    const nomeDoArquivo = file.name;
    const verificarExtensao = await nomeDoArquivo.split(".").pop().toLowerCase();

    if (!extensaoPermitida.includes(verificarExtensao)) {
        alert("Arquivo com extensão inválida!");
        removeButton.disabled = true;
        return;
    };
    
    const formData = new FormData(form)
    const res1 = await fetch('/upload', { method: 'POST', body: formData });
    const data1 = await res1.json();
    console.log(data1);


    const res2 = await fetch(`/api/metadata?filename=${nomeDoArquivo}`);
    const data2 = await res2.json();

    metadata_list.innerHTML = ''

    if (data2.tags.length === 0) {
        metadata_list.innerHTML = '<li>Nenhuma tag encontrada</li>';
        return;
    };

    data2.tags.forEach(item => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `<strong>${item.tags}</strong>: ${item.values}`;
        metadata_list.append(listItem);
    });

    removeButton.disabled = false;
    removeButton.onclick = async () => {
        const removeFormData = new FormData();
        removeFormData.append('filename', nomeDoArquivo);

        const res3 = await fetch('/remove/metadata', {
            method: 'POST',
            body: removeFormData
        });
        const data3 = await res3.json();

        console.log(data3);

        if (data3.status == 'success') {
            console.log('Metadados removidos');
            metadata_list.innerHTML = 'Metadados removidos!';
            removeButton.disabled = true;
            form.reset();
        } else {
            console.log(`Erro ao remover: ${data3.message}`);
            removeButton.disabled = true;
        }
    };

});