document.addEventListener('DOMContentLoaded', () => {
  // Search
  const searchBtn = document.querySelector('.search-btn');
  const searchInput = document.querySelector('.search-bar input');

  searchBtn.addEventListener('click', () => {
    if (searchInput.value.trim()) {
      alert(`Searching for: ${searchInput.value}`);
    }
  });

  searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') searchBtn.click();
  });

  // Newsletter
  const newsletterForm = document.querySelector('.newsletter-form');
  newsletterForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = newsletterForm.querySelector('input').value;
    if (email && email.includes('@')) {
      alert('Thank you for subscribing!');
      newsletterForm.reset();
    } else {
      alert('Please enter a valid email.');
    }
  });

  // Quote Form
  const quoteForm = document.querySelector('.quote-form');
  quoteForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const item = quoteForm.querySelector('input[placeholder="What item you need?"]').value;
    if (item.trim()) {
      alert('Quote request sent!');
      quoteForm.reset();
    } else {
      alert('Please enter the item you need.');
    }
  });
});
