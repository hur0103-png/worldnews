with open("app.js", "r", encoding="utf-8") as f:
    js = f.read()

old_block = """document.addEventListener('DOMContentLoaded', () => {
    const datePicker = document.getElementById('datePicker');
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    datePicker.value = `${yyyy}-${mm}-${dd}`;
    
    fetchNews(datePicker.value);
    
    datePicker.addEventListener('change', (e) => fetchNews(e.target.value));"""

new_block = """document.addEventListener('DOMContentLoaded', async () => {
    const datePicker = document.getElementById('datePicker');
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    const todayStr = `${yyyy}-${mm}-${dd}`;
    
    let availableDates = [];
    try {
        const resp = await fetch('/api/available-dates');
        const data = await resp.json();
        if (data.status === 'success') {
            availableDates = data.data;
        }
    } catch (e) {
        console.error("Failed to fetch available dates", e);
    }

    flatpickr(datePicker, {
        defaultDate: todayStr,
        onChange: function(selectedDates, dateStr, instance) {
            fetchNews(dateStr);
        },
        onDayCreate: function(dObj, dStr, fp, dayElem) {
            const dateObj = dayElem.dateObj;
            const y = dateObj.getFullYear();
            const m = String(dateObj.getMonth() + 1).padStart(2, '0');
            const d = String(dateObj.getDate()).padStart(2, '0');
            const cellDateStr = `${y}-${m}-${d}`;
            
            if (availableDates.includes(cellDateStr)) {
                dayElem.classList.add('has-news');
            }
        }
    });
    
    fetchNews(todayStr);"""

js = js.replace(old_block, new_block)

# Also update the logo click logic to use flatpickr instance
old_logo_block = """        document.getElementById('datePicker').value = todayStr;
        
        window.scrollTo({ top: 0, behavior: 'smooth' });
        fetchNews(todayStr);"""

new_logo_block = """        document.getElementById('datePicker')._flatpickr.setDate(todayStr);
        
        window.scrollTo({ top: 0, behavior: 'smooth' });
        fetchNews(todayStr);"""

js = js.replace(old_logo_block, new_logo_block)

with open("app.js", "w", encoding="utf-8") as f:
    f.write(js)
