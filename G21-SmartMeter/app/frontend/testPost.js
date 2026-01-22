const postBtn = document.getElementById('postBtn');
const cont = document.getElementById('postCont');
const pot = document.getElementById('postPot');

function shakeInput(input) {
  input.classList.remove('input-error');
  void input.offsetWidth;
  input.classList.add('input-error');

  input.addEventListener('animationend', () => {
    input.classList.remove('input-error');
  }, { once: true });
}

postBtn.addEventListener('click', async () => {
  const contVal = parseFloat(cont.value);
  let potVal = parseFloat(pot.value);

  let hasError = false;

  if (isNaN(contVal)) {
    shakeInput(cont);
    hasError = true;
  }

  if (isNaN(potVal)) {
    shakeInput(pot);
    hasError = true;
  }

  if (hasError) return;

  if (potVal > 3) potVal = 3;

  const payload = {
    contatore: contVal,
    potenza: potVal
  };

  try {
    await fetch('sensor/heartbeat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });
  } catch (err) {
    alert('Errore durante la POST');
  } finally{
    cont.value = '';
    pot.value = '';
  }
});
