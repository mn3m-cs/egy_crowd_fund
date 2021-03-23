phone1 = document.querySelector('[name="phone1"]');

(function additions() {
    // ADD MORE PHONES
    more_phones = document.createElement("a"); // without var so we can use it globally
    more_phones.innerText = "+ Add more phones";
    more_phones.classList.add("more");
    // insert after
    phone1.parentNode.insertBefore(more_phones, phone1.nextSibling);
    more_phones.addEventListener("click", addPhone);
})();


function addPhone(event) {
    // get number of lastphone number ex.2 add give the new field 3
    const lastPhoneIndex = event.target.previousSibling.name.slice(-1);
    const lastPhoneField = document.querySelector(`[name=phone${lastPhoneIndex}]`);
    const newPhoneIndex = parseInt(lastPhoneIndex) + 1;
    // create new phone field and give the style of lastPhone element
    let newPhone = document.createElement("input");
    newPhone.type = "text";
    newPhone.name = "phone" + newPhoneIndex;
    // newPhone.style = GFG_Fun(lastPhoneField);
    // newPhone.style.background ='';
    newPhone.classList.add('form-control')
    // label
    const phoneLabel = document.createElement("label");
    phoneLabel.textContent = 'Phone'+newPhoneIndex+':';
    more_phones.parentNode.insertBefore(newPhone, more_phones);
    newPhone.parentNode.insertBefore(phoneLabel, newPhone);
  }
  