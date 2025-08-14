const metadata_list = document.getElementById('metadata_list');
const form = document.getElementById('uploadForm');

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
});

