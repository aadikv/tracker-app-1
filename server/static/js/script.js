// Handle form submission
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    try {
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();
        const messageEl = document.getElementById('message');

        if (response.ok) {
            messageEl.textContent = Expiration date: ${data.expiration_date};
            messageEl.style.color = 'green';
        } else {
            messageEl.textContent = data.error || 'Failed to process the image';
            messageEl.style.color = 'red';
        }
    } catch (error) {
        console.error('Error uploading image:', error);
    }
});

// Load results on results page
document.addEventListener('DOMContentLoaded', async () => {
    if (window.location.pathname === '/results') {
        try {
            const response = await fetch('/api/products');
            const data = await response.json();
            const tableBody = document.getElementById('resultsTable');

            data.products.forEach(product => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${product.name}</td>
                    <td>${product.expiration_date}</td>
                    <td>${product.notify_date}</td>
                `;
                tableBody.appendChild(row);
            });
        } catch (error) {
            console.error('Error fetching results:', error);
        }
    }
});