document.querySelectorAll('input[type="checkbox"]').forEach(cb => {
  cb.addEventListener('change', () => {
    const formData = new FormData();
    formData.append(cb.name, cb.checked ? 'on' : '');

    fetch('/salva_presenze/', {
      method: 'POST',
      body: formData,
      headers: {'X-CSRFToken': '{{ csrf_token }}'}
    }).then(res => res.json())
      .then(data => console.log(data));
  });
});

